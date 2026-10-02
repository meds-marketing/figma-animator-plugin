#!/usr/bin/env node
// Dependency-free Node 22+ bridge for clients that only launch local MCPs.
const fs = require('node:fs');
const readline = require('node:readline');
const ENDPOINT = 'https://figma.meds-marketing.dev/mcp/tools';
const MAX_RESPONSE_BYTES = 64 * 1024 * 1024;

async function forward(message, { apiKey, protocolVersion, endpoint = ENDPOINT, request = fetch, emit }) {
  const response = await request(endpoint, {
    method: 'POST', redirect: 'error', signal: AbortSignal.timeout(30 * 60 * 1000),
    headers: { authorization: `Bearer ${apiKey}`, 'content-type': 'application/json',
      accept: 'application/json, text/event-stream',
      ...(protocolVersion ? { 'MCP-Protocol-Version': protocolVersion } : {}) }, body: JSON.stringify(message),
  });
  if (!response.ok) {
    await response.body?.cancel();
    throw new Error(`Animator MCP returned HTTP ${response.status}`);
  }
  if (response.status === 202 || response.status === 204) return;
  const sse = response.headers.get('content-type')?.includes('text/event-stream');
  const decoder = new TextDecoder();
  let buffer = '';
  let size = 0;
  const flushEvent = event => {
    const data = event.split(/\r?\n/).filter(line => line.startsWith('data:')).map(line => line.slice(5).replace(/^ /, '')).join('\n');
    if (data) emit(JSON.parse(data));
  };
  for await (const chunk of response.body) {
    size += chunk.byteLength;
    if (size > MAX_RESPONSE_BYTES) throw new Error('Animator MCP response exceeds bridge size limit');
    buffer += decoder.decode(chunk, { stream: true });
    if (sse) {
      let boundary;
      while ((boundary = /\r?\n\r?\n/.exec(buffer))) {
        flushEvent(buffer.slice(0, boundary.index));
        buffer = buffer.slice(boundary.index + boundary[0].length);
      }
    }
  }
  buffer += decoder.decode();
  if (sse) { if (buffer.trim()) flushEvent(buffer); }
  else if (buffer.trim()) emit(JSON.parse(buffer));
}

function main() {
  const apiKey = String(process.env.FIGMA_ANIMATOR_API_KEY ||
    (process.env.FIGMA_ANIMATOR_API_KEY_FILE ? fs.readFileSync(process.env.FIGMA_ANIMATOR_API_KEY_FILE, 'utf8') : '')).trim();
  if (!/^fga_org_[A-Za-z0-9_-]{43}$/.test(apiKey)) throw new Error('Configure FIGMA_ANIMATOR_API_KEY or FIGMA_ANIMATOR_API_KEY_FILE with an organization key');
  const emit = message => process.stdout.write(JSON.stringify(message) + '\n');
  let protocolVersion;
  const input = readline.createInterface({ input: process.stdin, crlfDelay: Infinity });
  input.on('line', async line => {
    if (!line.trim()) return;
    let message;
    try {
      if (Buffer.byteLength(line) > 1024 * 1024) throw new Error('Request size limit');
      message = JSON.parse(line);
      if (message.jsonrpc !== '2.0' || typeof message.method !== 'string') throw new Error('Invalid request');
    } catch {
      emit({ jsonrpc: '2.0', id: null, error: { code: -32700, message: 'Invalid MCP request' } });
      return;
    }
    try { await forward(message, { apiKey, protocolVersion, emit: response => {
      if (message.method === 'initialize' && response.id === message.id &&
          /^\d{4}-\d{2}-\d{2}$/.test(response.result?.protocolVersion || '')) {
        protocolVersion = response.result.protocolVersion;
      }
      emit(response);
    } }); }
    catch {
      // No retries: an interrupted paid submission may already have succeeded.
      if (Object.hasOwn(message, 'id')) emit({ jsonrpc: '2.0', id: message.id,
        error: { code: -32000, message: 'Animator connection failed. Check the key and network; read saved status before retrying a mutation.' } });
      else console.error('Animator notification delivery failed');
    }
  });
}

if (require.main === module) {
  try { main(); } catch { console.error('Animator bridge startup failed. Check Node 22+ and the organization key environment or private key file.'); process.exitCode = 1; }
}
module.exports = { forward };

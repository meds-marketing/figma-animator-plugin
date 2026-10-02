# Organization authorization

Figma Animator supports an administrator-managed credential alongside its existing personal Google OAuth connection. Use a separate organization key per client so one client can be revoked without interrupting the others. Keys never belong in a plugin archive, public repository, URL, screenshot, or prompt.

## Endpoints and identity

| Endpoint | Credentials | Presentation |
| --- | --- | --- |
| `https://figma.meds-marketing.dev/mcp` | Existing personal OAuth, legacy bearer, or organization key | Interactive workspace |
| `https://figma.meds-marketing.dev/mcp/shared` | Organization key only | Interactive workspace |
| `https://figma.meds-marketing.dev/mcp/tools` | Organization key only | Ordinary MCP tools, images and media links; no UI templates or app-private controls |

Send `Authorization: Bearer <organization-key>`. The shared routes return a plain bearer challenge and never start a Google OAuth flow. They reject personal OAuth tokens and the legacy compatibility token. If no organization registry is configured they fail closed with HTTP 503. Browser cookies and query-string credentials do not authenticate them.

The registry binds each credential to an explicit `ownerEmail`. Everyone using that credential shares this owner's saved requests, projects, preferences and generation quota. This is shared service access, not per-user identity or a grant based on membership inferred from a header. Do not assign a personal workspace unless its contents are approved for the organization. Client tool policies and exact-image/prompt approval before paid generation still apply. The server logs the bounded key ID and a hash of its owner, never a usable credential. Removing a member also requires removing their credential access; the key itself does not check the client's membership roster.

## Issue, install, rotate and revoke

From the source repository:

```sh
node scripts/mcp-org-key.js \
  --registry temp/org-auth/registry.json \
  --id codex-bluechew \
  --owner APPROVED_OWNER@bluechew.com \
  --key-file temp/org-auth/codex.key.txt
```

Repeat with distinct IDs/files for Claude, ChatGPT where supported, and Runneth. The command creates a 256-bit random key in a new mode-0600 file; the registry contains only SHA-256 digests and owner metadata. Existing key files cannot be overwritten. Optional `--expires-at 2027-01-01T00:00:00Z` sets an absolute expiry. Without that option the key remains valid until revoked. Run one registry editor at a time.

Inject the registry JSON through `ANIMATOR_MCP_ORG_KEYS`, preferably using Secret Manager. Runtime validation rejects malformed records, duplicate IDs/digests and owners outside `AUTH_ALLOWED_DOMAINS`. Keep the usable key in your organization's credential manager or managed environment, and restrict registry administration to operators who may grant Animator access. Deploy helpers preserve existing references and do not provision secrets or IAM.

For the hosted `.dev` service, an operator can store the registry in the `FIGMA_ANIMATOR_MCP_ORG_KEYS` secret in project `creative-strat`. Grant only the existing Cloud Run runtime identity access to that secret, then attach it as `ANIMATOR_MCP_ORG_KEYS`. Preserve all other secret references and domain mappings. Pin a concrete secret version on the serving revision. Adding a secret version alone does not reload running instances: attach the new version and roll a revision after every registry change.

To revoke:

```sh
node scripts/mcp-org-key.js --registry temp/org-auth/registry.json --revoke codex-bluechew
```

Publish the updated registry and roll the serving revision. Rotation uses a new key ID: install and test the new client credential, disable the old ID, deploy, then verify the old key returns 401. An in-flight operation already authenticated is not cancelled by revocation. There is no paid-request retry in the bridge. Secret Manager version destruction is unnecessary for ordinary credential revocation.

## Codex

Deploy `examples/org-auth/codex.toml` through your managed configuration process and provision `FIGMA_ANIMATOR_API_KEY` in the environment of the process running MCP. Codex sends it as a bearer token; no `codex mcp login` is needed. CLI setup is also supported:

```sh
codex mcp add figma-animator-org \
  --url https://figma.meds-marketing.dev/mcp/shared \
  --bearer-token-env-var FIGMA_ANIMATOR_API_KEY
```

For tools-only operation use `/mcp/tools`. A desktop process launched by Finder does not automatically inherit a terminal's exported variable; provision the environment where the app or remote executor actually starts. Local MCP configuration is separate from a ChatGPT-backed registered-app connection. If both are enabled the client can expose duplicate tool catalogs. Configure the organization connection and skill deliberately rather than requiring the OAuth dependency from a second package.

See [Codex MCP authentication](https://learn.chatgpt.com/docs/extend/mcp?surface=cli) and [managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration). The organization examples provide configuration, not proof that every workstation has received it.

## Claude web, Desktop and Cowork

An organization Owner adds a custom Web connector using `/mcp/shared`, selects **No sign-in**, then adds a required **Authorization** request header whose complete value is `Bearer <organization-key>`. Users may still need to enable/connect the organization connector, but this path requires no individual Google authorization. Use `/mcp/tools` when interactive rendering is unwanted.

**Request-header authentication is a limited beta.** If the organization has no Request headers field, that remote-connector setup is unavailable there; use managed Claude Code configuration or the local stdio bridge for a client supporting local MCP. A local bridge does not add remote connectors to Claude web/Cowork. Changing stored header authentication requires recreating the connector and members reconnecting.

These settings and rollout limits come from [Claude's request-header authentication documentation](https://claude.com/docs/connectors/custom/add-unlisted#authenticate-with-request-headers). This repository does not change Anthropic organization settings.

## Claude Code

Merge `examples/org-auth/claude.mcp.json` into the selected MCP configuration, or distribute it through the organization's supported managed MCP mechanism. Provision `FIGMA_ANIMATOR_API_KEY` on the execution host. The configuration uses Claude Code's documented `${VAR}` expansion in HTTP headers; it contains no actual key. Enable the workflow skill separately if using a direct managed connection.

See [environment substitution](https://code.claude.com/docs/en/mcp#environment-variable-expansion-in-mcp-json) and [managed MCP configuration](https://code.claude.com/docs/en/managed-mcp). Configuration trust and tool approval remain client decisions.

## ChatGPT

Keep the existing registered Figma Animator app identity and its OAuth connection intact. The ChatGPT web ZIP binds an app; it cannot install a bearer credential or change workspace authentication by itself.

OpenAI documents administrator-owned [workspace connections](https://learn.chatgpt.com/docs/enterprise/shared-connections) for eligible Team Tasks and @ChatGPT surfaces. An admin must check that the custom plugin and authentication method are available, authorize the designated account once and grant the intended audience access. This does not establish shared authentication for every ordinary personal chat or Codex app connection.

For a custom-plugin editor offering a protected API-key/header credential, use `/mcp/shared` and the dedicated ChatGPT key. Configure its workspace availability and test with a second member. If that editor lacks fixed credentials or a shared connection for the intended surface, keep OAuth and report this client limitation. Never select anonymous authentication on a private-data endpoint or embed a key in the endpoint URL to hide the authorization step. Published-plugin auth guidance still requires [MCP OAuth](https://developers.openai.com/plugins/build/auth) for authenticated plugin connections.

## Runneth and local-server clients

For a client accepting remote Streamable HTTP, configure `/mcp/tools` and the bearer header. This endpoint has no dependency on rendering extensions. Visibility in a client still depends on that client's supported connection configuration.

For a client accepting only a local command, use `plugins/figma-animator/bridge/mcp-stdio.cjs` with Node 22+. It needs no npm install and reads `FIGMA_ANIMATOR_API_KEY` or `FIGMA_ANIMATOR_API_KEY_FILE` (a private file containing just the key). Configure command `node`, arguments containing the absolute path to the bridge, and the private key file environment. `examples/org-auth/stdio.mcp.json` shows the standard shape; replace its two absolute paths. Hosts differ in how they accept this shape, so import/launch must be tested in the target client.

The bridge posts to the fixed HTTPS `/mcp/tools` endpoint, rejects redirects, preserves JSON-RPC IDs, relays JSON/SSE results and notifications, and writes only protocol messages to stdout. It does not retry failed calls or require a browser sign-in. Missing credentials fail before starting the protocol. Install `skills/animate-frame` through the client's supported skill mechanism; the server also supplies instructions during initialization. Actual comparisons, exact prompts and one explicit chat confirmation provide the animation review in clients without UI.

## Acceptance checks

1. An unauthenticated or revoked key fails; no personal OAuth challenge appears on shared routes.
2. A valid key initializes and lists tools; tools-only discovery has no `ui://` resources, UI tool metadata or app-private approval controls.
3. A read tool acts under the configured owner despite a supplied user-email header. Verify the intended shared workspace using real data before sharing credentials.
4. Validate actual client enablement with a second member. No Google prompt should be required on clients supporting fixed headers.
5. Existing `/mcp` OAuth linking still works. Paid approval and generation receipts remain required.

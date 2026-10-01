# Figma Animator plugin

This desktop package connects to the existing `.dev` MCP and includes the `animate-frame` skill. Sign in with the MCP's Google OAuth flow using an allowed meds.com or bluechew.com account. The browser review must use that same account.

## Package formats

- `plugin.json` + `mcp.json`: Agent Plugins 1.0 portable package. ChatGPT imports with bundled MCP declarations may be marked Desktop only, even when the endpoint is HTTPS.
- `.codex-plugin/plugin.json` + `.mcp.json`: Codex compatibility metadata and remote MCP connection.
- `.claude-plugin/plugin.json` + `.mcp.json`: Claude Code local plugin. Start Claude Code with `claude --plugin-dir /absolute/path/to/figma-animator`, then authenticate the remote MCP with `/mcp`.
- Other MCP clients: connect `https://figma.meds-marketing.dev/mcp` using Streamable HTTP/OAuth, and install or copy `skills/animate-frame/SKILL.md` through that client's supported skill/instruction mechanism. MCP support alone does not imply support for this plugin archive.

## Build archives

Run `python3 scripts/package-plugin.py` from the repository to create `dist/figma-animator-desktop.zip`.

For ChatGPT web, first verify the registered Figma Animator app's technical ID and its MCP endpoint. Run `python3 scripts/package-plugin.py --app-id <current-asdk_app-ID>` to create `dist/figma-animator.zip`. This web archive includes `.app.json` and the skill, excludes both MCP configuration files and Claude compatibility metadata, and points the OpenAI manifest at the registered app. A mapping does not create that app or grant permissions. Do not use an app ID whose detail page returns Plugin not found.

## Approval contract

Preparation returns an authenticated `/mcp/review/<planId>` URL. Open it, inspect the frames, and approve analysis. Return to the agent. After analysis, open the same page to inspect and approve the exact video prompt. The page records approval only; it never makes a Fal request. Typed chat approval and caller-supplied `confirmed:true` cannot create these records.

Receipts identify the signed-in account, stage, timestamp, and digest of the reviewed assets/settings (including the exact prompt for generation). They remain in the owner-scoped GCS plan JSON. The server rejects mismatches, missing approvals, expired plans, and duplicate claims. Browser authentication and CSRF checks restrict the approval route; they do not cryptographically distinguish a human from automation using the same browser session. The skill forbids agents from approving on the user's behalf.

Client automatic reviews still apply. Installing this plugin is not authorization to bypass a rejected export. No provider credentials are included.

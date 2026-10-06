# Figma Animator plugin

Version 0.3.0 adds a Figma library, a saved animation workspace, frame references, preferences and responsive host styling. Sidebar/thread entrypoints and composer mentions depend on the connected host. Local manifest changes do not publish or update the hosted plugin binding. See [workspace contracts](https://github.com/meds-marketing/figma-animator/blob/dev/docs/mcp-workspace.md).
This desktop package connects to the existing `.dev` MCP and includes the `animate-frame` skill. The default package uses Google OAuth. Organization connections can use administrator-provisioned API keys with `/mcp/shared` or `/mcp/tools`, without individual Google authorization. See [organization setup and client limits](ORG-AUTH.md). Previews and approval stay in the inline workspace in ChatGPT, or ordinary chat in tools-only clients.

Version 0.3.10 supports complete chat and interactive app workflows, durable motion revision intents and a preserved-context Animate handoff. It also includes independently revocable organization credentials, a tools-only endpoint, client configuration examples and a dependency-free local bridge that forwards the negotiated MCP protocol version. Build `python3 scripts/package-plugin.py --org-auth` for the skill and bridge without a bundled OAuth dependency. Configure the administrator-managed connection separately before using that package. The ChatGPT web ZIP retains its existing registered app identity; its authentication must be configured in the workspace.

## Package formats

- `plugin.json` + `mcp.json`: Agent Plugins 1.0 portable package. ChatGPT imports with bundled MCP declarations may be marked Desktop only, even when the endpoint is HTTPS.
- `.codex-plugin/plugin.json` + `.mcp.json`: Codex compatibility metadata and remote MCP connection.
- `.claude-plugin/plugin.json` + `.mcp.json`: Claude Code local plugin. Start Claude Code with `claude --plugin-dir /absolute/path/to/figma-animator`, then authenticate the remote MCP with `/mcp`.
- Other MCP clients: connect `https://figma.meds-marketing.dev/mcp` using Streamable HTTP/OAuth, and install or copy `skills/animate-frame/SKILL.md` through that client's supported skill/instruction mechanism. MCP support alone does not imply support for this plugin archive.

## Build archives

Run `python3 scripts/package-plugin.py` from the repository to create `public/plugins/figma-animator-desktop.zip`.

For ChatGPT web, first verify the registered Figma Animator app's technical ID and its MCP endpoint. Run `python3 scripts/package-plugin.py --app-id <current-asdk_app-ID>` to create `public/plugins/figma-animator.zip`. This web archive includes `.app.json` and the skill, excludes both MCP configuration files and Claude compatibility metadata, and points the OpenAI manifest at the registered app. A mapping does not create that app or grant permissions. Do not use an app ID whose detail page returns Plugin not found.

## Approval contract

Preparation returns actual review images. The agent drafts separate `reviewPlan` and `generationPrompt` fields. Review the images, exact H3 prompt, settings and GCS/Fal destinations in the single inline workspace in ChatGPT and other MCP Apps clients. Creating the batch opens this panel automatically. Tools-only clients receive images and prompts in ordinary chat. In every client including ChatGPT, Codex, Claude and Runneth, approve the entire displayed batch once in chat; the agent calls `animator_confirm_generation` with your actual reply and the displayed selection/prompt digests. That records a `chat-confirmation` receipt without a Fal request. The next generation call uses that receipt. Each edit requires renewed approval. App-only approval tools remain reserved for human UI clicks. Client approval policies still apply.

## Animation capabilities

Version 0.2.0 adds explicit layer/background composition, family discovery across actual ratios, one-or-many-item requests, selected-item approval, and one live request panel. The MCP enforces image/prompt revisions and durable execution. See the animate-frame skill for the tool contracts. Client approval policies still apply.

Version 0.2.1 fixes signed-in browser form approval, saves hosted reviews privately across server instances with a 24-hour approval window, and accepts revision 1 for initial batch preparation. Generation approval remains bound to the exact exported images and prompt.

Version 0.2.2 adds ordinary MCP chat confirmation for clients without MCP Apps. No custom UI or browser review page is required.

Version 0.2.3 opens one live inline workspace when a batch is created. Preparation, drafting, edits and generation update it without new panels. External batch pages are read-only views, never input or approval screens. Existing view links remain restricted to the signed-in owner; they do not grant cross-account access.

Version 0.2.4 prepares all requested frames with `animator_prepare_request`, saves all image-specific plans and prompts with `animator_draft_request`, and displays every variant together. Approve the whole batch with one inline button or one explicit chat reply. The agent records the exact displayed batch snapshot in one confirmation call; no per-frame approval is required.

Version 0.3.0 adds Library, Animations history, owner-scoped preferences, stable frame references, native extension entrypoints, request idempotency, responsive batch review and the supplied animation icon. Ordinary MCP tools and explicit chat approval remain available in clients without the native UI.

## Current MCP documentation

See the [documentation index](https://github.com/meds-marketing/figma-animator/blob/dev/docs/INDEX.md), [agent/media workflow](https://github.com/meds-marketing/figma-animator/blob/dev/docs/mcp-agent-workflow.md), [release runbook](https://github.com/meds-marketing/figma-animator/blob/dev/docs/mcp-release.md), and [organization authorization](https://github.com/meds-marketing/figma-animator/blob/dev/docs/mcp-org-auth.md). These distinguish source, package, hosted service and authenticated client verification.

Version 0.3.5 refreshes maintenance documentation alongside the hosted UI recovery and compact history filter release. The server supplies these UI changes; refresh the client package for updated documentation.

Distribution maintainers should also read [distribution maintenance](https://github.com/meds-marketing/figma-animator-plugin/blob/main/docs/maintenance.md).

Version 0.3.6 adds the guided KISS frame editor, image-only Edit with prompt, generated duplicate placement and completed-output acceptance. Server deployment supplies the UI; refresh the package and reconnect the tool catalog for the new KISS capabilities. MCP remains KISS-only.

Version 0.3.7 documents linked ratio edits, preserved-frame video retries, exact H3 source text, and shared internal projects with principal-bound approvals and quotas. MCP remains KISS-only.

Open `skills/animate-frame/SKILL.md` before selecting tools. Image editing (Nano Banana 2 / Ideogram) and H3 video generation run through Figma Animator MCP and its Fal backend; another integration key is not a reason to change providers.

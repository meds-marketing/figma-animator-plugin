# Figma Animator

Public plugin distribution for the hosted Figma Animator MCP. This repository contains client configuration, the animation skill, and packaging tools. It contains no application backend or credentials.

**MCP endpoint:** https://figma.meds-marketing.dev/mcp

## Codex

```sh
codex plugin marketplace add meds-marketing/figma-animator-plugin
codex plugin add figma-animator@figma-animator
```

Sign in through the MCP Google OAuth flow. Previews and approval stay in the inline workspace in ChatGPT, or ordinary chat in tools-only clients.

## Claude Code

```sh
claude plugin marketplace add meds-marketing/figma-animator-plugin
claude plugin install figma-animator@figma-animator
```

Use `/figma-animator:animate-frame` or ask to animate a named frame. Authenticate the remote MCP when prompted.

## Cursor

Merge `examples/cursor-mcp.json` into your Cursor MCP configuration. Copy `plugins/figma-animator/skills/animate-frame` into your project's `.cursor/skills/animate-frame` directory to include the workflow guidance. Authenticate the remote MCP when prompted.

## OpenCode

Merge `examples/opencode.json` into your OpenCode configuration. Copy the `animate-frame` skill directory into `.agents/skills/animate-frame` in your project. Authenticate the remote MCP when prompted.

## ChatGPT web

ChatGPT web uses a registered app binding. The direct MCP package in this repository is for clients that support bundled MCP servers. Importing its marketplace does not create a ChatGPT app or grant access to one.

With the current registered Figma Animator app's technical ID, create the web package:

```sh
python3 scripts/package-plugin.py --app-id asdk_app_YOUR_REGISTERED_APP_ID
```

Use the actual technical ID (32 hexadecimal characters after `asdk_app_`). The resulting `dist/figma-animator.zip` contains an `.app.json` binding and no MCP declarations. Upload it into the account or workspace that has access to that app. No stale app ID is included here.

## Animation workflow

1. Discover actual frames and aspect-ratio variants, resolve version ambiguity, and inspect exportable layers.
2. Organize the selected frames in one request. Call `animator_prepare_request` once to prepare every full-canvas start/end pair with server concurrency two; headline-only is the default composition.
3. `animator_create_request` automatically opens ONE inline workspace in ChatGPT and other MCP Apps hosts. Do not also call `animator_show_animation_review`; it is reserved for explicit reopening. Preparation, drafting, status and `animator_update_request` return data and update that workspace. Inspect all exported comparisons returned together, then call `animator_draft_request` once to save separate `reviewPlan` and clean `generationPrompt` fields for all items with its current revision, image digest, and fixed 15-second / 1080P settings. Review inputs and drafts are cached privately in the Animator account-scoped GCS folder. No image is sent to Fal during preparation or drafting.
4. Show exact images, H3 prompts, selected generation count and GCS/Fal destinations. Obtain ONE approval for the entire displayed batch, with one inline button or one explicit chat reply in any client including ChatGPT. One `animator_confirm_generation` call records the displayed complete-batch snapshot; internal per-item receipts do not require per-frame approval.
5. Execute approved items through `animator_generate_request`. The worker supplies each full-canvas start as the first image and full design as the last, with `minimax/h3-max/image-to-video`, 15 seconds, 1080P and disabled prompt expansion. Durable coordination defaults to two active jobs per request.
6. Present saved MP4s with measured dimensions and verification status. Partial successes remain available. Editing an item invalidates its approval; submitted membership and paid jobs are immutable and uncertain submissions are never automatically repeated.

The skill supplies agent guidance. The hosted service validates approval receipts; client security policies also apply. Installing a plugin cannot override a client's automatic review. Never manufacture approval or automate the approval button for the user.

## Package a ZIP

```sh
python3 scripts/package-plugin.py
```

Produces `dist/figma-animator-desktop.zip`. Packaging uses an explicit file allowlist. Public releases provide the desktop ZIP.

## Reference

- [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins)
- [Claude Code marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Cursor plugins](https://cursor.com/docs/reference/plugins)
- [OpenCode MCP](https://opencode.ai/docs/mcp-servers/)

Client installation and authenticated end-to-end generation must be checked in the target client. Publishing this repository does not install or register the plugin anywhere.

Hosted reviews and drafts survive service restarts and instance changes. They have a 24-hour approval window; assets remain private and no Fal request occurs before exact-prompt approval. Approval expiry is separate from storage retention. External batch pages are read-only views for explicitly requested viewing or sharing. They never accept inputs or approval, and a link does not grant another account access. Older temporary reviews that are missing require fresh preparation and approval. Local development without durable review storage retains a bounded 30-minute in-memory fallback.

## One chat approval in every client

ChatGPT, Codex, Claude, Runneth and other clients can review the actual images and exact prompts in chat. After your explicit approval, the agent records it through `animator_confirm_generation`, then submits the approved generation. The confirmation receipt binds the selected versions, images and exact prompts; edits require fresh approval. This uses ordinary MCP tools and requires no custom UI or review-page visit. The server records the agent reporting your confirmation, while the client retains its own approval policy.

Batch creation opens the inline workspace; the current manifest supplies the package version. Normal workflow results return media links and exact prompts instead of external approval links. No local installation is performed by publishing this package.

### One batch, one approval

Create one request containing all discovered frame identities. `animator_prepare_request` exports all pending frame pairs together, and `animator_draft_request` saves a separate motion plan and exact H3 prompt for every actual layout in one call. All variants appear in the same panel. One explicit chat reply approves the complete displayed batch in ChatGPT, Codex, Claude and tools-only clients; the single inline approval button works too. Any changed image or prompt requires renewed approval.

## Version 0.3.0

Library, Animations history and Preferences now share one responsive workspace. Native MCP extensions advertise global and thread entrypoints, stable frame mentions and settings where the host supports them. The skill explains exact request reopening, actual source identities, request idempotency and composition defaults; ordinary tools and explicit chat approval remain supported. The package includes the supplied animation icon in SVG and PNG.

## Updating an installed plugin

For Codex, refresh this marketplace and reinstall the plugin through its supported commands:

```sh
codex plugin marketplace upgrade figma-animator
codex plugin add figma-animator@figma-animator
```

Start a new chat or reconnect the MCP if the current chat still has the old tool catalog. Keep the same authenticated owner account. A marketplace refresh updates package instructions and icons; the hosted server deploy updates tools and UI independently.

For Claude Code, use `claude plugin marketplace update figma-animator` followed by `claude plugin update figma-animator@figma-animator`, then restart the session if its tool catalog remains stale.

Release maintainers synchronize portable and compatibility manifests, validate and rebuild the ZIP, verify the matching hosted MCP deployment, commit the allowlisted distribution files, and publish a matching version tag and ZIP release asset. Do not include backend source, credentials, app IDs from another account, or private design media.

## Organization authorization (0.3.4)

An administrator can provision a dedicated API key per client. Use `/mcp/shared` for the interactive workspace and `/mcp/tools` for standard tools and media without extensions. Read [organization setup, identity and client limits](plugins/figma-animator/ORG-AUTH.md). Claude header authentication depends on its beta availability; ChatGPT shared connections depend on the target surface and workspace controls.

Build `python3 scripts/package-plugin.py --org-auth` or download `figma-animator-org.zip` for the workflow skill, client examples and local stdio bridge without a bundled OAuth dependency. Configure the managed connection separately. Provision credentials privately; no keys are included in the package or repository. The default desktop package continues to use OAuth.

## Maintainer documentation

Read the [MCP agent and media workflow](docs/mcp-agent-workflow.md) for source selection, frame editing, prompt drafting, batch approval and recovery.

See [distribution maintenance](docs/maintenance.md) for package variants, current first-frame/prompt behavior, backend ownership and release/client verification. Organization setup remains in [ORG-AUTH.md](plugins/figma-animator/ORG-AUTH.md).

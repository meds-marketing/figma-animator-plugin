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
2. Organize the selected frames in one request. Prepare each full-canvas start/end pair with explicit layers and background; headline-only is the default composition.
3. `animator_create_request` automatically opens ONE inline workspace in ChatGPT and other MCP Apps hosts. Do not also call `animator_show_animation_review`; it is reserved for explicit reopening. Preparation, drafting, status and `animator_update_request` return data and update that workspace. Inspect each exported comparison and draft separate `reviewPlan` and clean `generationPrompt` fields with its current revision, image digest, and fixed 15-second / 1080P settings. Review inputs and drafts are cached privately in the Animator account-scoped GCS folder. No image is sent to Fal during preparation or drafting.
4. Show exact images, H3 prompts, selected generation count and GCS/Fal destinations. Wait for user approval inside the inline workspace, or explicit chat confirmation in tools-only clients. Each selected item receives its own bound approval receipt.
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

## Approval in tools-only clients

Runneth and other clients without MCP Apps can review the actual images and exact prompts in chat. After your explicit approval, the agent records it through `animator_confirm_generation`, then submits the approved generation. The confirmation receipt binds the selected versions, images and exact prompts; edits require fresh approval. This uses ordinary MCP tools and requires no custom UI or review-page visit. The server records the agent reporting your confirmation, while the client retains its own approval policy.

Version 0.2.3 opens the inline workspace from batch creation. Normal workflow results return media links and exact prompts instead of external approval links. No local installation is performed by publishing this package.

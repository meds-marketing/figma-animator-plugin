# Figma Animator

Public plugin distribution for the hosted Figma Animator MCP. This repository contains client configuration, the animation skill, and packaging tools. It contains no application backend or credentials.

**MCP endpoint:** https://figma.meds-marketing.dev/mcp

## Codex

```sh
codex plugin marketplace add meds-marketing/figma-animator-plugin
codex plugin add figma-animator@figma-animator
```

Sign in through the MCP Google OAuth flow. Use the same account for the frame and prompt review pages.

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
3. Open `animator_show_animation_review` once for the request. The panel follows all items through drafting, selected approval and generation. Other workflow tools return data only. Inspect each exported comparison and draft separate `reviewPlan` and clean `generationPrompt` fields with its current revision, image digest, and fixed 15-second / 1080P settings. No Fal analysis or upload.
4. Show exact images, H3 prompts, selected generation count and GCS/Fal destinations. Wait for user approval in the panel or signed-in request review page. Each selected item receives its own bound approval receipt.
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

Temporary unapproved reviews expire after 30 minutes and are lost on service restart. A missing review requires fresh preparation and approval. Persisted approved plans retain the service's generation recovery.

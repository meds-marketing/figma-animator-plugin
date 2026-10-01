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

1. Find the exact frame and export headline-only start/full-design end images.
2. Agent inspects the comparison and drafts a concise `reviewPlan` and separate clean `generationPrompt` through `animator_draft_animation`, bound to the exported comparison digest and 15-second / 1080P settings. No Fal analysis or upload.
3. Show actual frames, exact H3 prompt and GCS/Fal destinations. Wait for recorded user approval of upload and paid video generation.
4. Generate with `minimax/h3-max/image-to-video`, headline image first/full frame last, 15 seconds, 1080P, prompt expansion disabled.
5. Save the completed video to GCS and present it. Any draft edit invalidates approval; submitted jobs cannot be edited or automatically resubmitted.

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

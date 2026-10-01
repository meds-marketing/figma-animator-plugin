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

1. Find the named frame, preferring an exact top-level match.
2. Export the full frame and a headline-only start frame; build the comparison with the headline on the left.
3. Return inline review images without uploading review assets to GCS. Present the exact GCS and Fal destinations. Wait for the user to approve storage upload and analysis through the embedded review or signed-in review link.
4. Upload the approved images and plan to the displayed GCS destination, analyze the comparison with Fal, and present the exact animation prompt.
5. Wait for the user's recorded generation approval.
6. Generate with `minimax/h3-max/image-to-video`, duration **15 seconds**, resolution **1080P**, headline image as start and full frame as end.
7. Store the completed video in the configured Google Cloud Storage and present it.

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

# Plugin distribution maintenance

Snapshot: October 2, 2026, base commit `35eb998175b0f219cbc04b8a61adb1e864f2f8f8`. This repo distributes client manifests, instructions, icons, examples and packaging helpers. It does not deploy the Figma Animator service or ship its browser UI. Backend recovery/filter changes are local in the sibling service checkout at this snapshot.

## Source of truth

Backend contracts and runbooks live in [Figma Animator documentation](https://github.com/meds-marketing/figma-animator/tree/dev/docs). In a sibling checkout start at `../figma-animator/docs/INDEX.md`, then `mcp-release.md`, `mcp-agent-workflow.md` and `mcp-ui-development.md`. The hosted MCP resource supplies Library, Animations, Preferences, first/last comparisons and UI lifecycle handling.

Distribution sources are [plugin files](../plugins/figma-animator/README.md), [workflow skill](../plugins/figma-animator/skills/animate-frame/SKILL.md), [organization guide](../plugins/figma-animator/ORG-AUTH.md), [packaging script](../scripts/package-plugin.py), and [.agents marketplace](../.agents/plugins/marketplace.json). Compatibility manifests must keep identity, version, description and presentation synchronized.

## Package matrix

| Command | Output under `dist/` | Connection |
| --- | --- | --- |
| `python3 scripts/package-plugin.py` | `figma-animator-desktop.zip` | portable OAuth MCP plus compatibility overlays |
| `python3 scripts/package-plugin.py --org-auth` | `figma-animator-org.zip` | instructions, examples and stdio bridge; managed credentials supplied separately |
| `python3 scripts/package-plugin.py --app-id <verified-technical-app-id>` | `figma-animator.zip` | private/workspace existing registered-app dependency; no bundled MCP declarations |

Inspect the script's validation and file allowlist; never add secrets/private media/backend files. These ZIPs are not automatically MCPB/DXT bundles. Use a supported remote MCP connection for Claude Desktop or validate a separate local bundle rather than renaming an archive.

## Workflow additions

Batch preparation uses original layout coordinates and actual top-level Figma identities. Generation prompts must describe the actual first-frame pixels, keep existing positions unless movement was requested, complete major motion by five seconds and hold the supplied end layout. The skill is authoritative for the agent sequence.

Semantic keep/hide changes use layer composition. Artwork changes or partial edits within atomic text nodes use separately approved paid `animator_edit_first_frame` with Ideogram 4.5. The revised comparison invalidates prior prompt/video approval. A host custom-frame message is an instruction, not paid approval. Tools-only clients use images, exact prompts and ordinary chat confirmation without requiring a panel.

## Release and installed clients

Verify the matching backend serving revision first. Synchronize released skill/manifests/assets only, build and inspect packages, commit/push the distribution, publish a matching tag with assets, then refresh the intended client's installed package/catalog. Preserve both marketplace files and public repository identity. Do not copy unrelated dirty backend work into a release.

Git-imported workspace plugins update through source sync. Verify the same entry's imported version; Plugin Creator cannot edit an externally managed entry. The main plugin package and native registered MCP app have separate availability states. Importing the Git marketplace does not create/enable a ChatGPT app or grant OAuth access. Never create duplicate plugins to hide an update error.

A marketplace refresh changes instructions/icons; a server deploy changes tools/UI; a session reconnect refreshes the client's catalog. Verify all three separately. Public Git distribution is not OpenAI public-directory submission. No deployment, installed workspace version, authenticated provider execution or all-client compatibility is established by this documentation refresh.

## Version 0.3.7

The plugin instructions follow the deployed KISS-only tools. Frame saves default to linked ratio updates; explicit per-ratio overrides remain available. Video retries preserve saved edited frame pairs and require fresh approval. Source copy and first-frame geometry must remain exact in H3 drafting. Projects and requests are shared internally, while preferences, quotas and approvals remain principal-bound. Animate documents and timelines are application-only.

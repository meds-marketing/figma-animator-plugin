# MCP agent and media workflow

Mirrored from the [backend workflow guide](https://github.com/meds-marketing/figma-animator/blob/dev/docs/mcp-agent-workflow.md). Backend code links point to the service repository; the packaged skill remains local to this public repository.

Source snapshot: October 2, 2026. Canonical contracts: [tool registration](https://github.com/meds-marketing/figma-animator/blob/dev/lib/animator-mcp.js), [animation workflow](https://github.com/meds-marketing/figma-animator/blob/dev/lib/animator-workflow.js), [first-frame edits](https://github.com/meds-marketing/figma-animator/blob/dev/lib/first-frame-edit.js), and [agent skill](../plugins/figma-animator/skills/animate-frame/SKILL.md). Read executable schemas rather than copying argument lists from prose.

## Source selection and review

1. Resolve named frames and duplicate versions through the Figma search tools. Preserve file/page/frame identities. Library displays actual page names and top-level frames, grouped into real sibling aspect ratios; do not invent campaign categories.
2. Create one saved request for selected ratios. Batch preparation produces full-canvas first/last frames. Headline-only defaults to existing headline layers in their original positions; inspect selected text and actual exported pixels.
3. Use semantic layer queries for keep/hide requests. Atomic text nodes cannot be partially removed by selecting a substring. Isolated effects, masks and clipping may require a containing group; do not ignore unsupported-export errors.
4. Inspect every actual comparison. Draft a separate `reviewPlan` and exact provider `generationPrompt` for each layout, bound to the returned revision and image digest.
5. Present the complete batch, exact prompts, count, settings and storage/provider destinations. Obtain one explicit approval, record the returned review snapshot, then submit approved membership. A user request to animate is not approval of a later unseen prompt.

## Motion prompt rules

Describe the actual first-frame pixels. Do not invent centered placement, scaling, new wording, colors or objects. Keep existing headline coordinates fixed unless the user requested movement. Start from the supplied first image and finish at the supplied last image. Complete major entrances and transitions in the first five seconds; hold the complete design during the remaining duration unless the user requested another timing. Keep review commentary out of the clean generation prompt. The fixed video defaults are 15 seconds, 1080P, `minimax/h3-max/image-to-video`, with prompt expansion disabled. Verify actual output dimensions; resolution alone does not establish aspect ratio.

## Custom first frame: two paths

The UI sends the textbox text as the visible host message, with technical request/variant identity in model context. A rejected host message exposes a copyable fallback. The agent resolves the intent; the form does not itself approve a paid action.

Use Figma layer composition when existing nodes can express the change. For rewriting part of a text node or modifying artwork, `animator_edit_first_frame` submits a separately approved paid `ideogram/v4.5/edit` operation. Present the exact edit prompt and private-frame transfer to Fal first. This approval is separate from video approval. The source is the original full exported design, not the comparison image. The operation uses durable storage and a fingerprint of plan, source revision, prompt and model. Poll with the same revision/prompt; a different prompt cannot silently replace an existing operation. Unknown submission must not be repeated automatically.

Returned pixels must match the source aspect ratio. Proportional downscales are normalized to exact source dimensions; changed aspect ratios are rejected. The saved edited start frame increments revision and invalidates old drafts/approvals. Inspect the new comparison, redraft affected prompts, and obtain fresh video approval. This does not mutate the Figma document.

## Tools-only clients

Runneth and other clients without MCP UI can use structured tools, native images and media links, and explicit chat confirmation. UI rendering is optional. Organization `/mcp/tools` deliberately excludes UI advertisement and app-only controls; `/mcp/shared` supports interactive hosts. Client security policies still apply to exports and provider transfers.

## Failure boundaries

A tool can fail inside an HTTP 200 MCP response: inspect `isError`. Saved status takes precedence over a missing response. Prepared exports and drafts do not start video generation. Image edits are independently paid. Never approve unseen frames, manufacture confirmation, bypass an automatic-review rejection, or blindly retry uncertain paid jobs. See [generation jobs](https://github.com/meds-marketing/figma-animator/blob/dev/docs/mcp-generation-jobs.md) and [organization identity](https://github.com/meds-marketing/figma-animator/blob/dev/docs/mcp-org-auth.md).

## Guided KISS frame editing

The application and MCP panel share the guided first/last frame → motion prompt → review/generate → results flow. First-frame defaults use headline-only on black. Ratio changes keep preview heights stable. The breadcrumbs replace the project-title step navigation.

Use `animator_kiss_frame_read` with request/item/current revision to inspect original render layers and separate start/end frame properties. Use `animator_kiss_frame_save` with the returned source digest, every layer identity, the edited frame and a stable intent UUID. Keep position locked by default; explicitly unlock before changing x/y, uniform scale or rotation. Color and opacity changes are deterministic. Saving renders a new actual comparison, retains prior prompt history and invalidates approval. Submitted attempts stay immutable.

Only image layers offer **Edit with prompt**, attached to the canvas selection gizmo. Save property edits first. Present the exact prompt, selected source image, Fal destination, `openai/gpt-image-2.5/flare/edit`, transparent PNG output and supported price (currently unavailable) before requesting separate paid-edit approval. Call `animator_kiss_frame_generate` with confirmed:true and a stable intent UUID only after that approval. `animator_kiss_frame_inspect` recovers the same operation without a new submission. Unknown outcomes never authorize a retry. The server rejects outputs without actual transparent alpha.

Inspect the source/generated comparison and explicitly accept placement using `animator_kiss_frame_place`. It creates “original name — generated” at the source bounds; the original asset is retained and optionally hidden in that frame only. Placement requires the unchanged source revision. Redraft all affected image pairs and obtain fresh batch video approval. `animator_kiss_accept_output` records acceptance of a completed output revision; a retry creates a separate request and requires a fresh reviewed approval.

These are KISS frame operations, not manual Animate project tools. MCP exposes no mode switch, Animate document, timeline or compositor export. The legacy whole-frame Ideogram edit remains available for compatibility and atomic-text edits; it is separate from image-layer duplicates.

## Retrying a video

Use `animator_retry_video` after a known completed, failed, or definitively blocked result. Supply its request/item IDs, current item revision, and a stable UUID `intentId`. Recover a lost response with the same intent. The returned single-item request retains the actual saved frame pair, layer edits, and prompt; it has fresh approval requirements and no queued provider attempt. Review/edit its prompt and obtain approval before generating. The original result remains available. Unknown or active submissions must be reconciled first.

H3 drafting must quote exact important source copy, including headline, supporting copy, CTA, product labels, and legal copy. Prepared plans pin `textContents`; compare visibility with the actual images. Draft saves reinforce literal copy before review, preserving intact glyphs and avoiding flicker, substitutions, morphing, and invented lettering. Do not change already-approved prompts during submission.

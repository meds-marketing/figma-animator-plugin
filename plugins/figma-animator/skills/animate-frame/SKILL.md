---
name: animate-frame
description: Discover Figma variants, compose start frames, draft motion plans, and execute approved H3 animations with one live inline workspace in UI hosts and chat confirmation in tools-only hosts.
---

# Figma animation capabilities

Build a workflow from the user's intent. Headline-only is a default composition, not a mandatory workflow. One animation request can hold one or many independently reviewed variants.

## Discover and inspect

- Use figma_search_frames when a user names a frame. For "all available aspect ratios," supply family:true to match the shared creative name without its ratio suffix. Use actual Figma frames; never crop one source to invent a missing variant. Read dimensions and file/page/parent context. Resolve duplicate names or versions with the user; do not silently choose V4 over V2. Saved Animator projects are unrelated to discovery.
- A search covers configured connected files, or the supplied fileUrl. If no files are indexed, ask only for a design link. Do not demand page or frame IDs from the user.
- Use figma_get_frame to inspect composition.layers before selecting a custom start. It exposes node IDs, bounds, image fills, text descendants, hierarchy, and unsupported dependencies. IMAGE fills can belong to RECTANGLE nodes. A group may include the product and text. Do not infer a product cutout from a flattened photograph.

## Organize and compose

1. Call animator_create_request ONCE with an optional shared brief and explicit frames: [{fileUrl,pageId,frameId}], for a single frame or a whole batch. Record requestId and itemIds. In ChatGPT and other MCP Apps hosts, this call opens the single live inline workspace automatically. Never split a multi-ratio batch into separate requests or panels. To edit membership or brief, use animator_update_request with the current expectedRevision; it updates the existing workspace without opening another.
2. Call animator_prepare_request ONCE with requestId and the current request expectedRevision. It prepares ALL pending frames with server concurrency two and reuses already prepared pairs. Do not require the user to prepare each frame or create a separate request for each ratio. Keep preparationFailures visible and resolve them before calling the entire batch ready; hosted review inputs are cached privately in the Animator account-scoped GCS folder with a 24-hour approval window. Preparation returns expiring read links to private media, never public bucket access or a Fal request. For an intentional individual composition edit, use animator_prepare_frames with requestId/itemId, the current item expectedRevision, and startFrame with explicit includeNodeIds and background. Supported presets are headline_only, image_only and selected_layers; image_only requires explicit selection and rejects text descendants. Background choices are solid with #RRGGBB, supported frame_fill, or selected_layers with nodeIds. The server rejects unsupported masking/blending dependencies. Selecting an enclosing group preserves supported internal rendering. Selected content stays at its source position on the entire source canvas.
3. Inspect EVERY actual comparison image returned together by animator_prepare_request. Each image is labeled with its itemId and digest; preserve that association. LEFT is the selected start; RIGHT is the full end design. Do not invent visual details or continue with unseen/unavailable images.
4. In ChatGPT and other MCP Apps hosts, use the panel opened by animator_create_request for previews, selection, composition edits and approval. Preparation, drafting, generation and status return data and update that panel. DO NOT also call animator_show_animation_review after creation, preparation or drafting. Reopen it only if the user explicitly asks, or for a legacy standalone plan with no panel. Never repeat preparation just to refresh progress. Without panel support, use the media delivery rules below.

## Clients without inline panels

- Share direct media URLs from media.comparison.url, media.startFrame.url, media.endFrame.url, and media.video.url when available. Each prepared request item has its own media links. Include the motion plan, exact H3 prompt and fixed settings as ordinary chat text.
- Never send or construct an /mcp/review/ page link as a fallback, including /mcp/review/request/ links. Do not replace an unavailable media link with a review page.
- These URLs are expiring read links to the existing private Animator media. Refresh them through the ordinary plan/request status tools when needed. Native image content can also show the comparison. Do not invent URLs or claim unavailable media was displayed.
- Viewing or sharing media does not approve a paid render. After explicit user approval of the complete displayed review, use animator_confirm_generation to record a chat receipt. Do not call app-only approval tools or click approval for the user.

## Draft against each actual image pair

Call animator_draft_request ONCE with requestId, the current request expectedRevision, duration:15, resolution:"1080P", and drafts for ALL items. Each draft contains itemId, the current item expectedRevision, imageDigests.comparison as imageDigest, and TWO separate strings:

- reviewPlan: concise user-facing choreography, reveal order, timing, product emphasis and final hold.
- generationPrompt: direct, complete visual instructions for H3, adapted to the actual start/end composition and orientation. Describe the 15-second sequence and readable ending. Preserve the wording, typography, labels and final composition. Do not promise perfect text fidelity. Include no reasoning sections, serialized analysis, tool transcripts, approval instructions or agent commentary.

Reuse a shared creative direction across variants, but adapt reveals, positions and framing to each exported layout. Never submit the comparison as a first/end image. No Fal analysis request is needed.

Present ALL actual frame pairs, their motion plans and EXACT H3 prompts together in ONE batch review, with 15-second / 1080P settings, selected video count and exact GCS/Fal destinations inside the existing inline panel for ChatGPT and other UI hosts, or ordinary chat for tools-only hosts. Never replace inline preview/approval buttons with review links. Ask for ONE approval covering the entire displayed batch. Never require individual frame preparation or individual frame approvals. Keep missing exports and draftFailures visible; do not silently approve only the successful subset. STOP and wait for explicit user approval. The initial request to animate is not approval of a later draft.

## Approve the complete batch once in chat

After the user explicitly approves the displayed review, call the normal, model-visible animator_confirm_generation tool. This works in ALL clients, including ChatGPT, Codex, Claude and Runneth, with or without custom UI. A single explicit “Approved” reply after the complete review covers all displayed items; do not ask the user to click one approval per frame. Call this tool ONCE with confirmed:true, the actual user reply as confirmationText, and the returned review:{requestId, selectionDigest, items:[{itemId,digest}]} snapshot FROM THE COMPLETE REVIEW YOU PRESENTED. Include all displayed items unless the user explicitly approves a subset. Never replace an old reviewed snapshot with silently refreshed digests. For a legacy standalone plan use review:{planId,digest}, with its displayed reviewDigest.

The server records one batch selection with owner-scoped receipts binding every approved image pair, exact prompt and settings. Individual receipts are an internal integrity check, not separate human approval steps. This is the authenticated agent reporting the user reply; the server does not claim to have witnessed a UI click. It stores a hash of the confirmation text, not the raw chat. Confirmation makes no Fal call and submits no generation. Continue with animator_generate_request, or animator_generate_animation for a legacy plan, after the receipt succeeds.

Do not invent confirmation text, refresh stale digests silently, add unapproved items, or use this tool after a client policy rejection as a workaround. If the prompt, composition or selected brief changed, present the new exact review and obtain renewed user approval. If approval/submission may already have succeeded, inspect saved status before continuing. An inline panel and a review web page are optional, never prerequisites for chat approval.

## Execute and recover

- Keep animator_approve_request and animator_approve_review app-only for direct human clicks. Never call these private tools, browser approval endpoints, or click approval for the user. Explicit chat approval uses animator_confirm_generation. Plugin instructions cannot override client approval policies.
- After server-recorded approval, animator_generate_request with requestId and confirmed:true uses the privately cached approved inputs and queues durable work. The panel's approval button performs this directly. Read saved request status before submitting from the agent; do not repeat already queued work.
- Each item sends its prepared full-canvas start as image_url and full end as end_image_url, using minimax/h3-max/image-to-video, 15 seconds, 1080P, and disabled prompt expansion. H3 derives the canvas from the first image. Resolution does not choose orientation or guarantee exact pixel dimensions; report measured output dimensions and verification state.
- The worker defaults to two concurrent generations within a request, finalizes MP4s to GCS, and continues after chat closure. Partial results remain available. Present a video only after the item is completed with result.video.outputUrl.
- The panel refreshes internally. Use animator_get_animation_request once when asked for status, or with includePreviews:true to retrieve all actual comparisons together for planning. Use activeItemId only for intentional individual inspection; imageDigest skips unchanged previews. It creates no new panel. Reopen animator_show_animation_review only when the user explicitly requests another view.
- Revise an individual composition with animator_prepare_frames and the current expectedRevision; revise a single prompt with animator_draft_animation only when the user requests a specific item edit. The default batch uses animator_prepare_request and animator_draft_request. Changes invalidate only the affected item's approval. Changing the request brief invalidates affected drafts. Submitted membership and items are immutable. For an intentional retry or another output, create a new request/item from the source and obtain approval for that new paid attempt. Never automatically retry submission_unknown.
- Hosted reviews and drafts are stored privately and survive server restarts or instance changes. Their approval window is 24 hours; this is an approval expiry, not a storage deletion promise. If an older temporary review is unavailable or a review has expired, prepare fresh inputs, inspect them and obtain new approval. Local development without durable review storage retains a bounded 30-minute in-memory fallback.
- Client denials must be reported with their stated reason. Do not bypass through alternate destinations, indirect execution, or repeated calls. Legacy Fal analysis jobs may be inspected for recovery; never copy raw analysis into generationPrompt.
- Keep the same authenticated owner account. Do not request tokens or put credentials in plugin files. Do not use project-track rendering for this H3 workflow.

## External batch views

Existing /mcp/review/ URLs are read-only views for a viewing or sharing link when the user requests one. They never accept selection, edits or approval. Do not send these links as part of the animation input or approval workflow. Current views require the same signed-in owner account; a link does not grant another account access.

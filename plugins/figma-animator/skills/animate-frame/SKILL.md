---
name: animate-frame
description: Discover Figma variants, compose start frames, draft motion plans, and execute approved H3 animations in one live request panel.
---

# Figma animation capabilities

Build a workflow from the user's intent. Headline-only is a default composition, not a mandatory workflow. One animation request can hold one or many independently reviewed variants.

## Discover and inspect

- Use figma_search_frames when a user names a frame. For "all available aspect ratios," supply family:true to match the shared creative name without its ratio suffix. Use actual Figma frames; never crop one source to invent a missing variant. Read dimensions and file/page/parent context. Resolve duplicate names or versions with the user; do not silently choose V4 over V2. Saved Animator projects are unrelated to discovery.
- A search covers configured connected files, or the supplied fileUrl. If no files are indexed, ask only for a design link. Do not demand page or frame IDs from the user.
- Use figma_get_frame to inspect composition.layers before selecting a custom start. It exposes node IDs, bounds, image fills, text descendants, hierarchy, and unsupported dependencies. IMAGE fills can belong to RECTANGLE nodes. A group may include the product and text. Do not infer a product cutout from a flattened photograph.

## Organize and compose

1. Call animator_create_request with an optional shared brief and explicit frames: [{fileUrl,pageId,frameId}]. Record requestId and itemIds. A single-item request uses the same model. For a simple single frame, animator_prepare_frames with file/page/frame creates its request automatically.
2. Call animator_prepare_frames for each requestId/itemId. Prepare sequentially or in bounded waves; hosted review inputs are cached privately in the Animator account-scoped GCS folder with a 24-hour approval window. No public image URL or Fal request is created during preparation. To change the start, supply startFrame with explicit includeNodeIds and background. Supported presets are headline_only, image_only and selected_layers; image_only requires explicit selection and rejects text descendants. Background choices are solid with #RRGGBB, supported frame_fill, or selected_layers with nodeIds. The server rejects unsupported masking/blending dependencies. Selecting an enclosing group preserves supported internal rendering. Selected content stays at its source position on the entire source canvas.
3. Inspect the returned actual comparison image. LEFT is the selected start; RIGHT is the full end design. Do not invent visual details or continue with unseen/unavailable images.
4. Open animator_show_animation_review ONCE with requestId. This panel follows all items through preparation, drafting, approval, generation and results. All other data operations update it without opening another panel. Never repeat preparation just to refresh progress.

## Draft against each actual image pair

Call animator_draft_animation separately for each prepared planId with its current expectedRevision, imageDigests.comparison as imageDigest, duration:15, resolution:"1080P", and TWO strings:

- reviewPlan: concise user-facing choreography, reveal order, timing, product emphasis and final hold.
- generationPrompt: direct, complete visual instructions for H3, adapted to the actual start/end composition and orientation. Describe the 15-second sequence and readable ending. Preserve the wording, typography, labels and final composition. Do not promise perfect text fidelity. Include no reasoning sections, serialized analysis, tool transcripts, approval instructions or agent commentary.

Reuse a shared creative direction across variants, but adapt reveals, positions and framing to each exported layout. Never submit the comparison as a first/end image. No Fal analysis request is needed.

Present the actual frames, separate motion plans, EXACT H3 prompts, fixed settings, selected video count and exact GCS/Fal destinations. End the response and wait for user approval in the existing panel or its signed-in request review link. Typed confirmation alone does not create a server receipt. The user can review and approve selected variants together.

## Execute and recover

- Never call animator_approve_request or animator_approve_review, browser approval endpoints, or click approval on the user's behalf. The user controls these actions. Plugin instructions cannot override client approval policies.
- After server-recorded approval, animator_generate_request with requestId and confirmed:true uses the privately cached approved inputs and queues durable work. The panel's approval button performs this directly. Read saved request status before submitting from the agent; do not repeat already queued work.
- Each item sends its prepared full-canvas start as image_url and full end as end_image_url, using minimax/h3-max/image-to-video, 15 seconds, 1080P, and disabled prompt expansion. H3 derives the canvas from the first image. Resolution does not choose orientation or guarantee exact pixel dimensions; report measured output dimensions and verification state.
- The worker defaults to two concurrent generations within a request, finalizes MP4s to GCS, and continues after chat closure. Partial results remain available. Present a video only after the item is completed with result.video.outputUrl.
- The panel refreshes internally. Use animator_get_animation_request once when asked for status, or with activeItemId when you need that item's actual comparison; imageDigest skips unchanged previews. It creates no new panel. Reopen animator_show_animation_review only when the user explicitly requests another view.
- Revise composition with animator_prepare_frames and the current expectedRevision; revise the prompt with animator_draft_animation. Changes invalidate only the affected item's approval. Changing the request brief invalidates affected drafts. Submitted membership and items are immutable. For an intentional retry or another output, create a new request/item from the source and obtain approval for that new paid attempt. Never automatically retry submission_unknown.
- Hosted reviews and drafts are stored privately and survive server restarts or instance changes. Their approval window is 24 hours; this is an approval expiry, not a storage deletion promise. Open review links with the same Google account as the MCP connection. If an older temporary review is unavailable or a review has expired, prepare fresh inputs, inspect them and obtain new approval. Local development without durable review storage retains a bounded 30-minute in-memory fallback. A browser approval redirects to saved request progress; inspect that status before making another generation call.
- Client denials must be reported with their stated reason. Do not bypass through alternate destinations, indirect execution, or repeated calls. Legacy Fal analysis jobs may be inspected for recovery; never copy raw analysis into generationPrompt.
- Keep the same authenticated owner account. Do not request tokens or put credentials in plugin files. Do not use project-track rendering for this H3 workflow.

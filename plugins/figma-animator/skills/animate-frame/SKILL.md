---
name: animate-frame
description: Use when the user asks Figma Animator to find, export, review, or animate a named Figma frame, including AD campaign identifiers. Guides frame discovery, inline frame approval, image analysis, exact prompt review, and 15-second 1080P generation.
---

# Animate a Figma frame

Use the authenticated Figma Animator MCP at https://figma.meds-marketing.dev/mcp. Tools may be prefixed by the client; match their leaf names below. Do not substitute another Figma or generation provider.

## Discover and prepare

1. Call `figma_search_frames` with the user's frame name. Prefer an exact top-level match and the requested aspect ratio. Saved Animator projects are not the Figma index. Do not begin by listing saved projects.
2. If more than one plausible match exists, show previews and ask the user to choose. If no connected files were searched, ask for the Figma design URL only; resolve page and frame IDs with tools.
3. Call `animator_prepare_frames` for the chosen fileUrl/pageId/frameId. It exports full and headline-only images and a left/right comparison, retains them temporarily inside the Animator process, and returns inline images. No review asset or plan upload to GCS and no Fal request occurs. Read `animator_get_workflow_details` for the exact configured destination when needed.
4. Show the actual returned comparison: left is headline-only start, right is full end. Never claim an image was displayed if rendering failed. Show `destinations.storage` and the Fal analysis provider/model along with the images. Prefer the embedded chat review; clients without MCP Apps can use the returned signed-in `reviewUrl`.
5. END this response. The user must review the frames and explicitly approve uploading these reviewed assets and plan to the displayed GCS destination and sending the comparison to Fal for analysis, using the review button. An initial animation request, typed approval, successful export, or `confirmed:true` does not create the required approval record.

## Analyze approved frames

6. After the user clicks approval, call `animator_get_animation_plan` with planId. Continue only if `approvals.analysis` exists and the plan is awaiting_frame_review. Do not automate browser clicks, request the approval HTTP endpoint, or approve on behalf of the user.
7. Call `animator_analyze_animation` with planId and confirmed:true. The server validates the owner-scoped approval against the exact image digests and destinations before uploading the reviewed assets and plan to GCS. Only then does analysis run. Analysis uses `fal-ai/bagel/understand` with the left/right comparison.
8. Present the exact returned prompt inside the chat review. END this response. The user must separately approve the prompt and paid video generation using the inline chat button. Frame approval is not video approval.

## Generate approved video

9. Read `animator_get_animation_plan` again. Continue only if approvals.generation exists and the plan is awaiting_confirmation.
10. Call `animator_generate_animation` with planId and confirmed:true. The server validates the approval and submits the stored prompt/start/end images to `minimax/h3-max/image-to-video`, always 15 seconds and 1080P. Never replace the approved prompt, assets, provider, duration, or resolution.
11. Generation returns a saved generating plan immediately. The inline UI polls status; a background Cloud Tasks worker saves the completed video to GCS even when chat is closed. Do not set an agent timer or resubmit. On return or interruption, call animator_get_animation_plan with the same planId to reopen the inline status/video view. Present the MP4 only after status is completed and result.video.outputUrl exists. Do not call an editable project-track renderer for this workflow.

## Errors and status

- Policy rejection: stop the blocked operation, describe the client's stated reason, and read workflow details if needed. Do not retry, change destinations, or use indirect export. The plugin does not override client approval policies.
- Missing approval: ask the user to click the inline approval button and stop. Do not treat confirmed:true as evidence of approval.
- Blank review/image: stop and report it. Do not proceed or open another tab; report the inline rendering failure.
- Temporary review missing after restart or instance routing: prepare a fresh review and obtain new approval; do not upload or analyze using stale approval.
- Expired plan: explain that a fresh review and new approvals are needed before any new provider call.
- Timeout/in-progress/failed generation: inspect animator_get_animation_plan. Never resubmit a paid job automatically. Completed plans return their existing result.
- Cross-account review: use the same Google account as the MCP connection. Do not ask for tokens or copy credentials into plugin files.

---
name: animate-frame
description: Find, review and animate a Figma frame using an agent-authored motion plan and an approved H3 prompt.
---

# Animate a Figma frame

1. Find the frame using figma_search_frames. Prefer an exact name and top-level frame. Saved animation projects are unrelated to frame discovery. Ask the user to choose if multiple plausible matches remain.
2. Call animator_prepare_frames with the chosen fileUrl, pageId and frameId. Inspect the returned actual comparison image: LEFT is the headline-only start, RIGHT the full design end. If the image cannot be inspected or displayed, stop and report that limitation. Do not invent visual details.
3. Reason about the animation yourself. Do not send the images to Fal for analysis. Draft against these exported images and fixed duration 15 seconds / resolution 1080P.
4. Call animator_draft_animation with planId, imageDigest from imageDigests.comparison, duration:15, resolution:"1080P", and TWO separate strings:
   - reviewPlan: concise user-facing choreography, reveal order, timing and final hold. Describe the visible elements and the transition between the actual images.
   - generationPrompt: direct visual instructions for H3. Start from the supplied headline-only image and finish at the supplied full-design image. Include 15-second timing, restrained product motion, sequential supporting-copy reveals, readable final hold, and preservation of composition, typography, wording and labels. No reasoning traces, analysis response, JSON, tool transcripts, approval instructions or agent commentary. Do not promise perfect text fidelity.
5. Show the actual comparison, reviewPlan, EXACT generationPrompt, fixed settings and exact GCS storage/Fal generation destinations. END the response and wait for user approval via the inline review button or authenticated review link. Drafting uploads nothing and makes no Fal request. Generation approval covers the displayed assets, storage upload and paid video request.
6. Never invoke animator_approve_review, browser approval endpoints, or click approval on behalf of the user. confirmed:true alone is not approval. Read animator_get_animation_plan and verify approvals.generation before calling animator_generate_animation with planId and confirmed:true.
7. Generation uses image_url=headline start and end_image_url=full design, minimax/h3-max/image-to-video, 15 seconds and 1080P, with prompt expansion disabled. Never substitute the comparison image or modify the approved prompt.
8. To revise before submission, call animator_draft_animation again. Every edit invalidates existing approval; display and approve the new exact prompt again. Submitted plans cannot be edited or resubmitted.
9. The existing inline panel polls status internally. Do not repeatedly call status tools from the agent or open duplicate panels. Use animator_get_animation_plan once when asked for status; it returns data only. Use animator_show_animation_review only if the user explicitly asks to reopen the review or saved video. The durable worker saves the MP4 to GCS. Present it only after completed with result.video.outputUrl. Do not use project-track rendering or submit another paid request.

## Recovery and client policies

- A client policy denial must be reported with its stated reason; do not bypass it through indirect execution or alternate destinations.
- Blank review: stop; do not claim the images were shown.
- Temporary reviews expire after 30 minutes or restart. Prepare fresh frames if unavailable and obtain new approval.
- Legacy Fal analysis jobs may be inspected for recovery, but new animations use agent-authored planning. Never copy raw analysis into generationPrompt.
- Keep the same authenticated owner account. Do not ask for tokens or embed credentials in plugin files.

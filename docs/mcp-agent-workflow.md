# Figma Animator MCP agent instructions

Canonical operating guidance for chat-led, app-led and mixed workflows. Connected tool schemas remain authoritative.

# Figma animation capabilities

## Read this skill before choosing a generation integration

For a Figma static ad, first open this installed `skills/animate-frame/SKILL.md` and follow it. Discovery, first-frame image editing and video generation all occur through **Figma Animator MCP**. The Animator backend calls Fal using its configured credentials and saves operations, outputs and approvals. The agent calls Animator tools; it does not use raw Fal calls, Higgsfield, integrations-cli or a brain-index search to select a separate animation provider merely because an API key is available. Read current tool schemas to confirm availability. If this skill is unavailable in a client, use the server's matching instructions and schemas and report that limitation.

| Task | Animator tool | Model / provider contract |
| --- | --- | --- |
| Keep/hide existing source content | `animator_prepare_request` / `animator_prepare_frames` | Deterministic Figma composition; no generation model |
| Edit whole design into a first frame | `animator_edit_first_frame` | `model: "fal-ai/nano-banana-2/edit"` for Nano Banana 2 or `model: "ideogram/v4.5/edit"` for Ideogram. Paid, separately approved. |
| Edit isolated image layer | `animator_kiss_frame_generate` → inspect → place | GPT Image 2.5 Flare; actual transparent alpha required. Nano Banana 2 is supported for whole frames, not this alpha-layer path. |
| Animate reviewed first/last pair | `animator_generate_request` after exact review and confirmation | Fal `minimax/h3-max/image-to-video`, 15 seconds, 1080P. |

Nano Banana 2 is an image edit model, not the video model. The backend supplies `image_urls`, `aspect_ratio: "auto"`, `resolution: "2K"`, `output_format: "png"`, `num_images: 1` and disables web search. Agents supply the tool's `model`, exact prompt, real `planId`, current item `expectedRevision` and separately approved `confirmed:true`; do not pass raw provider fields to the MCP tool. Omitting model preserves a saved operation's model, or defaults a new edit to Ideogram. Switching models requires a newly reviewed operation; do not switch during recovery.

Example: inspect the exported AD-4859-C1-V2 artwork, present the exact first-frame prompt and disclosure to Fal Nano Banana 2, obtain approval, then call `animator_edit_first_frame` with its actual plan ID/revision and `model: "fal-ai/nano-banana-2/edit"`. Inspect the returned first/last comparison, draft H3 motion, and request separate video approval.


Build a workflow from the user's intent. Headline-only is a default composition, not a mandatory workflow. One animation request can hold one or many independently reviewed variants.

The MCP surface is KISS-only: Library source browsing, animation requests, motion drafts, exact-input approval, generation history and preferences. Manual layer-animation projects, project edit operations and compositor export belong to the authenticated web application and are unavailable through MCP discovery or invocation. Compatibility tools such as animator_animate_frame operate only on KISS plans.

The client can authenticate with personal OAuth or an administrator-provisioned organization key. Organization keys bind all users to the configured shared owner and quota. Use the client's existing connection; do not ask users for Google authorization when a shared key is configured, and never ask them to paste keys into chat. The `/mcp/tools` endpoint and local stdio bridge have no UI dependency: present images and exact prompts in ordinary chat. Credential setup is documented in `../../ORG-AUTH.md`; authentication does not approve exports or paid generation.

## Runneth and other tools-only clients: bounded operating procedure

Do not narrate credential hunting, speculative tool selection or repeated searches. Start with a short useful status, use the connected Figma Animator tools, then report a saved outcome or one specific blocker. Another provider key is not permission or a reason to change the workflow. No brain-index lookup, generic integrations skill or external ad-library comparison is needed for a named Figma ad. If Animator tools are absent, report that the Animator connection/skill must be enabled in this client; do not invent tools or work around a client policy denial.

### Find the exact creative without a search loop

For `StatiqClub-Batch83-AD-4859-C1-V2`, preserve **StatiqClub / Batch83 / AD-4859 / C1 / V2** as the requested identity. Keep exact frame names and source IDs returned by Figma. Ratio suffixes such as `-9:16`, `-1x1` or `-16X9` identify actual sibling layouts, not versions. Separator differences such as C1-V2 and C1V2 are normalized by family search; do not repeatedly guess punctuation variants.

1. Call `figma_search_frames` with the full supplied name and `family:true`, plus `fileUrl` if the user supplied one. Family search matches the complete family name after stripping a ratio suffix and normalizing separators; it is not a prefix search.
2. If successful but empty, make one query for `AD-4859-C1-V2` with `family:true`. This handles frames stored without the campaign/batch prefix. Retain requested batch context when evaluating matches; names without a batch do not prove membership in Batch83.
3. Only if still empty, make one bounded fallback using `AD-4859` or `Batch83` with `family:false`; inspect its returned matches and filter for the exact C1/V2 and batch context. Do not try unrelated ads such as AD-5. If `truncated:true`, use a discovered file/page/parent scope to narrow the same query before selecting; the visible page is not a complete result inventory.
4. If no verified candidate remains, stop and ask for the Figma design link or specific source-set context. Search only covers configured connected files or the supplied file. Do not enumerate unrelated history, settings or files to guess where the design lives. `animator_list_requests` is for resuming an existing animation, not locating new Figma sources. `animator_read_preferences` is app-only and must not be invoked by the agent.

An empty successful result is not a transient error; change scope as above rather than repeat it. An `isError`, timeout or missing content is not evidence of zero matches. Inspect the actual error. Retry the identical read at most once after a short backoff only for an explicitly transient network/429/5xx failure; honor Retry-After. On repeated failure, state the failed tool, visible error and required next step. Authentication, permission, invalid-input and unavailable-tool errors require resolving that specific condition, not retries or changing providers. Missing images require media recovery, not guessed visual analysis. Never retry a possibly accepted write with a new request/intent ID.

### Resolve duplicate sets once, before creating work

Use returned `families` and `matches` to group by **fileKey + pageId + parentId**, then map each distinct frameId to its ratio/dimensions. Repeated delivery of the same frameId is one source; distinct frame IDs with similar names or identical previews remain separate sources. Do not mix 9:16 from one duplicate parent with 1:1 or 16:9 from another.

If several plausible source sets remain, inspect bounded previews with `figma_list_ad_sets` using the actual fileUrl, pageId and candidate frameIds (maximum 24 per call). Grouped preview output may contain several parents: keep your source-set table from the search identities. Tiny thumbnails are not proof that artwork or disclaimers are identical; use actual inspected exports if detail matters. Do not infer which copy is newer from larger node IDs, parent numbering, search order or visual similarity. A Meta crop is neither source-set identity nor evidence of a missing ratio. Do not silently recommend the "newer" set on that basis.

Present one concise choice with neutral labels, actual parent/page names or IDs, available ratios, source links/previews and only verified differences. Example: "Two distinct C1/V2 source sets remain, both with 9:16, 1:1 and 16:9. Their previews look similar; I cannot establish which is canonical. Use set A [source reference] or set B [source reference]?" Ask once and wait before creating/preparing either set. If the user explicitly approves a documented default or chooses by a source link, record that choice. Unpaid preparation does not justify choosing an ambiguous source on the user's behalf.

### Execute all chosen aspect ratios as one batch

For a request naming one creative without a ratio restriction, include all actual available ratios **from the selected source set**. State the included ratios and any missing variants; do not crop or synthesize a ratio. If a parent holds multiple distinct candidate frames for the same ratio, resolve that ambiguity rather than taking the first. For more than the 24-frame request limit, agree a bounded batch; never silently omit frames.

Maintain a per-item ledger: ratio/dimensions, fileUrl, pageId, frameId, requestId, itemId, planId, item revision, comparison digest, readable motion, exact prompt and status. Request revision and item revision are different fences. Never copy a node ID, planId, image digest or revision from one ratio to another.

| Current state | Next action | Stop / recovery rule |
| --- | --- | --- |
| Source selected, no request | `animator_create_request` once with every selected source frame and one stable idempotencyKey | Recover uncertain creation with identical key/payload; no per-ratio request splitting. |
| Request unprepared | Read once, then `animator_prepare_request` once for all pending items | Let running preparation finish; retain failures and do not call a partial batch ready. |
| Actual pairs ready | Inspect each comparison, record/reuse one motion intent, `animator_draft_request` with each target's own revision/digest | One coherent choreography adapted to each actual layout; no unseen-image drafting. |
| First frame needs generated changes | Present exact image/prompt/model for each affected item, obtain separate paid image-edit approval, call `animator_edit_first_frame` per actual plan | Keep one parent set; recover each paid operation with same plan/revision/prompt/model. Nano Banana 2 edits images; H3 generates video. |
| Entire chosen batch ready | Show all actual pairs, per-item readable/exact prompts, settings, destinations and price availability in chat | Wait for explicit approval; initial "animate this" does not approve paid image edits or videos. |
| Exact video review approved | `animator_confirm_generation` once with the actual reply and displayed complete review, then `animator_generate_request` once | No per-ratio approval loops; stale inputs require refreshed review. |
| Jobs running / partial results | Wait about 60s, then read the existing batch; wait 30–60s between later polls and return actual per-ratio outcomes | No invented ETA, closed-chat monitoring or duplicate submissions. Unknown submission means inspect/reconcile. |

Finish reveals by 5s and hold the actual ending through 15s unless the user requests different choreography. Preserve each ratio's native composition and exact text; matching visual intent does not mean reusing identical geometry or a generic prompt. Keep every included item visible through failures, revision and approval. One failed ratio is not authorization to generate an unstated subset. User-requested frame property saves can link matching layers across ratios; generated image placement remains explicit for each affected ratio.

## Wait and poll for H3 completion

After `animator_generate_request` acknowledges submission, retain the existing requestId and per-item job identities. Read its returned state first: deliver outputs already completed, report definite failures, and treat `submission_unknown` as reconciliation rather than permission to retry. For acknowledged queued/running jobs, tell the user: "The batch is submitted. I'll check its status in about a minute" only when the client can actually wait and continue this run.

1. **Wait about 60 seconds before the first status poll.** This is a polling interval, not an ETA or a promise that H3 finishes in one minute. Use an available client wait/timer tool to resume the active run. Preserve the requestId across the wait. Do not busy-loop, repeatedly call tools while waiting, or open another panel.
2. Call `animator_get_animation_request` **once for the entire batch**. Do not poll each ratio independently. Inspect every included item's state: different ratios can finish at different times.
3. If acknowledged jobs are still queued/running/uploading, wait another **30–60 seconds** before the next batch read. Honor any longer retry-after guidance. Use bounded waits while the client supports continuation; do not invent a maximum generation time or abandon accepted jobs just because the first minute elapsed.
4. Return completed videos through their actual media links/native content as they become available, with concise counts and actionable per-ratio failures. Stay quiet on unchanged intermediate polls. When every included item reaches a known terminal state, deliver the final outcomes and stop polling.
5. Never call `animator_generate_request`, `animator_generate_animation`, create_request or retry tools merely to check progress. A lost/unknown submission must be inspected against the original request and saved job; no fresh paid attempt without reconciliation and a newly reviewed approval.

**Timer capability is a real boundary.** Only say a timer, scheduled check or automatic follow-up is set after an exposed client tool successfully creates it. A text promise or an app's own polling is not an agent wakeup. Do not assume Runneth supports timers. If no wait/continuation tool is available, say "The batch is submitted. This client cannot schedule my next check; the app can continue showing progress, or ask me to check this same request in about a minute." Include the actual saved request identity. Do not require the app for chat-led work or pretend a closed chat is being monitored. Background scheduling/notifications require a supported tool and the user's authorization; this procedure does not create a new automation. App watchers can keep updating locally without extra agent status polls; when the agent is carrying an active chat-led generation to completion, use the batch interval above.

### Deliver media in the initiating chat

**Preview first, download second.** For each ratio, use the client's actually supported inline image/video rendering or media-attachment tool. Preserve `media.*.mimeType` and `media.*.filename` (or the returned result filename): video/mp4 with `.mp4`, image/png with `.png`, image/jpeg with `.jpg`/`.jpeg`. `presentation` describes intended media display, not proof of a host capability. Do not strip extensions, rename media to a generic extensionless artifact, force attachment/download disposition, or re-upload a usable playback URL as an untyped file. Provide the download link separately as an optional secondary action.

Use native MCP image content for images where supported. If the client's documented renderer supports Markdown images, embed the actual returned image URL; Markdown image syntax is not a universal video embed. For video use the host's documented media player/attachment mechanism with the actual playback URL and MIME type. Do not invent `<video>`, a custom widget, or a Runneth tool/API merely because other clients support it. If inline rendering is unavailable or fails, state the observed limitation and supply a labeled browser playback link before a download-only fallback. A file card is not evidence of a playable preview: do not say "watch above" unless the host actually rendered a player. Check available client instructions/capabilities before downgrading; never assert that Runneth lacks previews based solely on generic file cards.

Diagnose a delivery problem using the tool result's media MIME/filename and the client's attachment/renderer metadata if exposed. Figma Animator logs record tool identity/timing/outcome and bounded IDs, not response payloads, signed URLs, or client rendering. Those logs cannot prove an inline player was shown. Avoid logging credentials, private media URLs or full responses to diagnose presentation. Do not make private media public or regenerate a video to fix a display issue.


Use native MCP image content and the returned `media.comparison.url`, start/end or video URLs. Associate each with its actual ratio/item. Workdir paths do not become client artifacts automatically; do not assume an artifacts directory or file-link widget exists in Runneth. Use a host-supported artifact tool only if actually exposed. If native display is unavailable, share the returned read link; if it expired, refresh the same request. If neither is usable, state what cannot be shown and pause visual approval. Do not claim an image was inspected or shown when it was not. No external review page is required.

## Match the initiating modality

Chat, the interactive MCP app and the plugin are complete interfaces to the same request. Do not require app navigation for chat-led work, even when a panel is available. The default journey is select → review → generate → results; carry unpaid preparation, actual-image inspection and agent drafting without asking the user to operate internal stages.

For a request or change in chat, reply in chat with the saved outcome, actual media, motion and per-ratio exceptions. Include every actual frame pair, readable plan, exact saved prompt, selected count, fixed settings, destinations and expiry before paid approval. An app card is optional supporting presentation. Explicit chat approval uses animator_confirm_generation in every host. Do not substitute “open the workspace to continue” for a complete response.

For direct app edits, the app provides saving, saved state and exceptions. Routine selection/status refreshes need no chat messages. An app-origin motion instruction intentionally hands work to the agent; explain the saved result in chat while the same panel updates. Switching surfaces never creates a duplicate request or expands approval scope. Native mentions, fullscreen and host messages are optional capabilities, not prerequisites for the ordinary tool/chat path.

## Open, resume, and configure the workspace

- Open the library with figma_media_browser. Use animator_open_workspace with empty arguments to open Animations and history without creating a request. Both tools have native entrypoints in supporting hosts; ordinary MCP clients can call them directly.
- To resume earlier work, use animator_list_requests with its filter and bounded limit, and follow nextCursor even when a filtered page contains no rows. Open the exact discovered requestId through animator_get_animation_request. Never invent identifiers or create a duplicate request to inspect history.
- Frame resource links are stable figma-frame references to actual file/page/frame identities. Treat them as design references, not image exports or authorization to submit a render. Resolve the referenced identity through the ordinary frame tools before preparing media.
- Use the workspace Preferences view or native settings UI for defaultFileUrl, previewDensity and startPreset. The app uses animator_read_preferences and generation-fenced animator_update_preferences; these are app-only tools, not agent commands. The workspace-open result supplies current preferences for context. Use explicit request inputs over saved defaults; preferences do not constitute paid-generation approval.
- Native mention search and settings tools may be app-only and unavailable to the agent. Use model-visible frame search and explicit user choices when the host does not expose those tools. Do not call private tools through an alternate path.
- For animator_create_request, generate one UUID idempotencyKey for that logical request and retain it with the exact frames and brief. After an uncertain response, retry the same key and unchanged payload. A changed payload needs a new logical request; never replace the key merely because a response timed out.
- For batch preparation, startPreset can choose headline_only or image_only for pending frames. selected_layers requires actual per-item layer choices through animator_prepare_frames; do not reuse a node ID across different frames.

## Discover and inspect

- Use figma_search_frames when a user names a frame. Preserve the full creative/version identity: for AD-4859-C1-V2-9:16 search frameName:"AD-4859-C1-V2", family:true to discover its actual ratio siblings. A broader AD-4859 search is a fallback; filter and resolve the discovered C/V versions before selecting. For "all available aspect ratios," supply family:true to match the shared creative name without its ratio suffix. Use actual Figma frames; never crop one source to invent a missing variant. Read dimensions and file/page/parent context. Resolve duplicate names or versions with the user; do not silently choose V4 over V2. Saved Animator projects are unrelated to discovery.
- A search covers configured connected files, or the supplied fileUrl. If no files are indexed, ask only for a design link. Do not demand page or frame IDs from the user.
- Use figma_get_frame to inspect composition.layers before selecting a custom start. It exposes node IDs, bounds, image fills, text descendants, hierarchy, and unsupported dependencies. IMAGE fills can belong to RECTANGLE nodes. A group may include the product and text. Do not infer a product cutout from a flattened photograph.

## Organize and compose

1. Call animator_create_request ONCE with an optional shared brief and explicit frames: [{fileUrl,pageId,frameId}], for a single frame or a whole batch. Record requestId and itemIds. In ChatGPT and other MCP Apps hosts, this call opens the single live inline workspace automatically. Never split a multi-ratio batch into separate requests or panels. To edit membership or brief, use animator_update_request with the current expectedRevision; it updates the existing workspace without opening another.
2. Read animator_get_animation_request once before preparation. The inline panel automatically prepares headline-only first frames and full-design last frames for a new request. Reuse those prepared pairs; if preparation is running, let it finish. If the request still has unprepared items and no preparation is running, call animator_prepare_request ONCE with requestId, the current request expectedRevision, and startPreset: headline_only unless the user explicitly requested a custom composition. It prepares ALL pending frames with server concurrency two and reuses already prepared pairs. Do not require the user to prepare each frame or create a separate request for each ratio. Keep preparationFailures visible and resolve them before calling the entire batch ready; hosted review inputs are cached privately in the Animator account-scoped GCS folder with a 24-hour approval window. Preparation returns expiring read links to private media, never public bucket access or a Fal request. For an intentional individual composition edit, use animator_prepare_frames with requestId/itemId, the current item expectedRevision, and startFrame with explicit includeNodeIds and background. Supported presets are headline_only, image_only and selected_layers; image_only requires explicit selection and rejects text descendants. Background choices are solid with #RRGGBB, supported frame_fill, or selected_layers with nodeIds. The server rejects unsupported masking/blending dependencies. Selecting an enclosing group preserves supported internal rendering. Selected content stays at its source position on the entire source canvas.
3. Inspect EVERY actual comparison image returned together by animator_prepare_request. Each image is labeled with its itemId and digest; preserve that association. LEFT is the selected start; RIGHT is the full end design. Do not invent visual details or continue with unseen/unavailable images.
4. Use the existing panel for app-led selection, composition edits and approval; for chat-led work present the actual comparisons and review directly in chat, whether or not a panel is available. Preparation, drafting, generation and status return data and update that panel. DO NOT also call animator_show_animation_review after creation, preparation or drafting. Reopen it only if the user explicitly asks, or for a legacy standalone plan with no panel. Never repeat preparation just to refresh progress. Without panel support, use the media delivery rules below.

## Media delivery and complete chat review in every client

- Share direct media URLs from media.comparison.url, media.startFrame.url, media.endFrame.url, and media.video.url when available. Each prepared request item has its own media links. Include the motion plan, exact H3 prompt and fixed settings as ordinary chat text.
- Never send or construct an /mcp/review/ page link as a fallback, including /mcp/review/request/ links. Do not replace an unavailable media link with a review page.
- These URLs are expiring read links to the existing private Animator media. Refresh them through the ordinary plan/request status tools when needed. Native image content can also show the comparison. Do not invent URLs or claim unavailable media was displayed.
- Viewing or sharing media does not approve a paid render. After explicit user approval of the complete displayed review, use animator_confirm_generation to record a chat receipt. Do not call app-only approval tools or click approval for the user.

## Draft against each actual image pair

Read current motionRevisionIntents after preparation. If the app already recorded a matching pending intent, fulfill that exact intent rather than create another. Otherwise call animator_request_motion_revision with the current request expectedRevision, a stable UUID intentId, target itemIds, change and surface:chat. Retain the returned intent identity: concurrent surfaces may deduplicate to an existing pending instruction. This records unpaid work, not a provider request. Inspect every actual target comparison. A failed handoff can be redelivered with the same intent and unchanged baseline; a superseded intent requires reading the changed inputs and creating fresh work.

Call animator_draft_request ONCE with the returned intentId, requestId, the current request expectedRevision, duration:15, resolution:"1080P", and drafts for ALL intent target items. An initial request targets every included item; an intentional revision targets only affected items so other saved drafts remain intact. Partial target completion stays pending until every intended target resolves. Retain the exact payload and intent for recovery after a lost save response. Each draft contains itemId, the current item expectedRevision, imageDigests.comparison as imageDigest, and TWO separate strings:

- reviewPlan: concise user-facing choreography, reveal order, timing, product emphasis and final hold.
- generationPrompt: direct, complete visual instructions for H3, adapted to the actual start/end composition and orientation. Describe the 15-second sequence and readable ending. Preserve the wording, typography, labels and final composition. Do not promise perfect text fidelity. Include no reasoning sections, serialized analysis, tool transcripts, approval instructions or agent commentary.

### First-frame fidelity and default timing

Inspect every actual exported first/last image pair before drafting. Treat the first image as the exact time-zero composition, not a mood reference. Preserve the visible text's position, size, line breaks, typography, background and existing objects. Do not infer a centered or vertically centered headline from the headline-only preset. Removing other layers does not imply moving the remaining headline.

When an element occupies the same position in both images, keep it locked there. Do not add an opening glide, scale change, camera push, reframe or recentering. Describe movement only when the inspected pair supports that change and the user requested or approved the choreography. If the image cannot be inspected, retrieve the actual image before drafting; do not substitute a frame name, generic template or guessed layout.

Unless the user explicitly requests another timeline, finish all major reveals and transitions by **5 seconds** of the fixed 15-second output, then hold the complete end design from **5–15 seconds**. Use this pacing as a starting point, adapting overlap and reveal order to the actual design:

- 0–0.5s: retain the supplied first frame exactly, with the existing headline stationary.
- 0.5–2s: reveal the primary product or artwork in its end-frame position.
- 2–3.5s: reveal supporting copy and secondary imagery.
- 3.5–5s: finish remaining icons, brand marks and call to action.
- 5–15s: hold the complete supplied end frame, stable and legible.

Use image-relative wording such as "Keep the headline exactly where it appears in the supplied first frame; reveal the remaining artwork in its supplied end-frame positions." Do not describe an unverified coordinate or alignment. Keep reviewPlan and generationPrompt consistent about positions, reveal order and timing. Preserve these rules across ratios while inspecting each actual layout separately. A user's explicit timing or movement direction takes precedence over the default.

Reuse a shared creative direction across variants, but adapt reveals, positions and framing to each exported layout. Never submit the comparison as a first/end image. No Fal analysis request is needed.

Present ALL actual frame pairs, their motion plans and EXACT H3 prompts together in ONE batch review, with 15-second / 1080P settings, selected video count and exact GCS/Fal destinations in ordinary chat for chat-led work in every host, or inside the existing panel for app-led review. A panel is never required for detailed review or explicit chat approval. Never replace inline preview/approval buttons with review links. Ask for ONE approval covering the entire displayed batch. Never require individual frame preparation or individual frame approvals. Keep missing exports and draftFailures visible; do not silently approve only the successful subset. STOP and wait for explicit user approval. The initial request to animate is not approval of a later draft.

## Approve the complete batch once in chat

In the internal shared workspace, the current authenticated connection may approve a request created by another teammate. For an organization token, authority belongs to the authenticated credential; the server does not know the identity of the person speaking in chat. The current user’s explicit approval of the complete displayed review is sufficient. Do not require the original requester to return or create a duplicate request to change ownership. Read the returned authorization context; creator/editor attribution does not restrict approval. Client policy denials still apply.

After the user explicitly approves the displayed review, call the normal, model-visible animator_confirm_generation tool. This works in ALL clients, including ChatGPT, Codex, Claude and Runneth, with or without custom UI. A single explicit “Approved” reply after the complete review covers all displayed items; do not ask the user to click one approval per frame. Call this tool ONCE with confirmed:true, the actual user reply as confirmationText, and the returned review:{requestId, selectionDigest, items:[{itemId,digest}]} snapshot FROM THE COMPLETE REVIEW YOU PRESENTED. Include all displayed items unless the user explicitly approves a subset. Never replace an old reviewed snapshot with silently refreshed digests. For a legacy standalone plan use review:{planId,digest}, with its displayed reviewDigest.

The server records one batch selection with authenticated-principal receipts binding every approved image pair, exact prompt and settings. Individual receipts are an internal integrity check, not separate human approval steps. This is the authenticated agent reporting the user reply; the server does not claim to have witnessed a UI click. It stores a hash of the confirmation text, not the raw chat. Confirmation makes no Fal call and submits no generation. Continue with animator_generate_request, or animator_generate_animation for a legacy plan, after the receipt succeeds.

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

## Semantic start-frame selection

For requests such as “only keep the secondary text,” “hide the bottle,” or
“only Modafinil on screen,” inspect real nodes with `figma_query_layers`.
Combine own text (`textMatch: exact` preferred), type, name, image fills,
font-size ranges and relative region. `textRole: secondary` uses relative font
size to find candidates, not a reliable semantic label. Inspect full text,
bounds, ancestors and constraints before selecting. Never invent IDs.

Pass `startFrame.includeNodeIds` to keep specific objects, or
`startFrame.excludeNodeIds` to hide objects (exclusion alone keeps the remaining
top-level content). Both can combine. Pass the query’s sourceDigest as expectedSourceDigest to reject a changed source. Excluding a child splits the selected
group; masks, clipping or blending may prevent safe isolated exports and must
be reported, never silently replaced with another composition. Keep a deliberate
background. Selecting a containing group includes its other descendants.

A text substring match keeps the entire atomic text node. If “Modafinil” shares
a node with other words, do not claim the resulting frame contains only that
word: explain the node boundary and offer the paid Ideogram editing path below
when the user needs a change within that text node. After every composition change inspect the actual comparison,
redraft the motion prompt and obtain fresh generation confirmation.

## Library and panel behavior

Library shows actual document pages, top-level artboard sets, and their available aspect ratios. Use `figma_list_animation_frames` with `topLevelOnly: true` for Library discovery; use bounded `frameIds` with `figma_list_ad_sets` for preview reads. Never invent missing variants. The panel keeps a bounded inline height and scrolls internally. Reuse its existing request and do not open another panel for routine status updates. Custom first-frame requests require actual per-ratio layer inspection, revised comparisons and prompts, and fresh approval.

## First frames that need design changes

Use layer composition when the request only keeps or hides existing objects. If it needs rewriting part of an atomic text node, moving or redrawing artwork, or another change to the exported design, use `animator_edit_first_frame` instead. Inspect the actual exported design and construct a model-specific editing prompt from the user intent. Specify what changes, exact replacement text, what stays fixed, and that the canvas, proportions, typography and unaffected artwork must be preserved. Show the exact prompt and explain that the exported private Figma frame will be sent to Fal's selected `fal-ai/nano-banana-2/edit` or `ideogram/v4.5/edit` model for a paid image edit. Obtain the user's confirmation before setting `confirmed:true`; approval to export or generate a video is not approval for this separate image edit.

Pass the item's `planId`, current plan `expectedRevision`, and approved `prompt`. The tool exports the full original frame and uses high precision, medium quality, one image and `image_size:auto`. Exact pixel dimensions are checked; same-proportion provider downscales are restored to the input size and marked as normalized. A changed aspect ratio is rejected. While pending, repeat the exact same plan, revision and prompt to inspect the existing job. A submitting/unknown result must not be retried with a fresh operation.

After completion, read the existing request and inspect the actual edited first/full last comparison. Draft fresh motion plans and exact H3 prompts, then obtain fresh video-generation approval. The Figma source document remains unchanged.

## Guided KISS frame editing

The application and MCP panel share a single canvas-and-motion workspace followed by exact paid batch review and results. Preparation is automatic. Host-agent drafting is automatic after actual comparisons exist; standalone web model drafting remains an explicitly disclosed paid action, with manual exact-prompt editing available. First-frame defaults use headline-only on black. Ratio changes keep preview heights stable. The breadcrumbs replace the project-title step navigation.

Use `animator_kiss_frame_read` with request/item/current revision to inspect original render layers and separate start/end frame properties. Use `animator_kiss_frame_save` with the returned source digest, every layer identity, the edited frame and a stable intent UUID. Keep position locked by default; explicitly unlock before changing x/y, uniform scale or rotation. Color and opacity changes are deterministic. Saving renders a new actual comparison, retains prior prompt history and invalidates approval. Submitted attempts stay immutable.

Only image layers offer **Edit with prompt**, attached to the canvas selection gizmo. Save property edits first. Present the exact prompt, selected source image, Fal destination, `openai/gpt-image-2.5/flare/edit`, transparent PNG output and supported price (currently unavailable) before requesting separate paid-edit approval. Call `animator_kiss_frame_generate` with confirmed:true and a stable intent UUID only after that approval. `animator_kiss_frame_inspect` recovers the same operation without a new submission. Unknown outcomes never authorize a retry. The server rejects outputs without actual transparent alpha.

Inspect the source/generated comparison and explicitly accept placement using `animator_kiss_frame_place`. It creates “original name — generated” at the source bounds; the original asset is retained and optionally hidden in that frame only. Placement requires the unchanged source revision. Redraft all affected image pairs and obtain fresh batch video approval. `animator_kiss_accept_output` records acceptance of a completed output revision; a retry creates a separate request and requires a fresh reviewed approval.

These are KISS frame operations, not manual Animate project tools. MCP exposes no mode switch, Animate document, timeline or compositor export. The legacy whole-frame Ideogram edit remains available for compatibility and atomic-text edits; it is separate from image-layer duplicates.

## Linked ratio edits and video recovery

Frame saves default to `syncAcrossRatios: true`. Keep that default for changes intended for every included ratio; set it false for a deliberate per-ratio override. Inspect `sync.skipped` for missing or ambiguous matches, and review every affected frame pair before redrafting and approving. Position changes scale with canvas dimensions; generated-image placement remains explicitly reviewed per ratio.

Use `animator_retry_video` only after a known completed, failed, or definitively blocked result, with request/item IDs, current item revision and a stable UUID `intentId`. Recover a lost response with that same intent. The new single-item request retains the saved frame pair, edits and prompt but requires fresh approval. Reconcile active or unknown submissions before retrying.

Quote exact important source copy in H3 drafts, including headline, supporting text, CTA, product labels and legal copy. Compare pinned `textContents` with actual frame visibility. Preserve intact glyphs and avoid substitutions, morphing, flicker or invented lettering. Keep the supplied first-frame geometry exact at time zero; complete major reveals by five seconds and hold the supplied ending layout through fifteen seconds.

Requests and projects are shared within the authenticated internal workspace, with creator/editor attribution. Preferences, quotas and approvals remain principal-bound.

## Continuing in Animate

MCP does not expose manual timeline or compositor operations. When the user wants to continue editing a completed output, offer the signed-in application handoff with the exact request/item identities: https://figma.meds-marketing.dev/#kiss/<requestId>?item=<itemId>&continue=animate. Use actual discovered UUIDs only, with no credentials or signed media URL in the link. The application asks before importing a rendered video asset into an Animate project. Explain that trim, placement and asset motion are editable; generated motion does not become editable source-layer animation. Opening this link does not authorize generation or export. Video approval and “Mark accepted” editorial acceptance remain separate.

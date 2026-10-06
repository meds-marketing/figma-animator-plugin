# Hybrid composition implementation

October 6, 2026. Local implementation and verification; deployment, paid H3 execution and Runneth rendering require separate proof.

New MCP requests on the test deployment resolve to `hybrid`. `ANIMATOR_HYBRID_ENABLED=false` disables new hybrid creation; `true` enables it explicitly. Without an override, the `.com` service retains its existing default. Requests persist their strategy; changing the flag does not rewrite existing records. `whole-frame-generated` explicitly retains KISS, including Nano Banana 2/Ideogram first-frame edits. `deterministic` runs the composition without provider components.

## Actual flow

`animator_composition_capabilities` → discover one source family → `animator_create_request` → `animator_prepare_composition` → `animator_draft_composition` → review exact animatics/input images/recipe → `animator_confirm_generation` → `animator_generate_composition` → wait/poll `animator_get_composition` → inspect candidate videos and `animator_inspect_composition` temporal images → `animator_review_composition_vision` per ratio → `animator_render_composition`.

Text and SVG render units keep original source pixels, with deterministic frame tracks. H3 generates only clean background units. Preparation uses the existing Figma scene extractor and source SVG importer, then independently reconstructs and compares the original. Unsupported separation blocks the item rather than sending text to the generation model. Every chosen ratio remains in the request.

The recipe uses 24/30 fps, integer event frames and explicit source-hold/continuous ending policy. H3 components use 15 seconds at 1080P. Deterministic compositions support up to 120 seconds. Opaque plates replace a contiguous bottom prefix of source units; interleaved foreground requires prepared mattes and is currently blocked. Generated alpha, arbitrary path morphs, animated group compositing and fine-grained native text preparation are not exposed by this recipe. Existing supported Animate features remain available in the editor. The design's advanced fidelity extensions remain staged, rather than silently approximated.

A component can serve several actual source layouts, usually from a 16:9 master. Each target retains its source foreground layout and explicit cover/contain/fill policy with normalized crop anchor. The service automatically renders review candidates and extracts samples at one-second intervals and exact motion/hold boundaries ± one frame. Final release requires a current per-ratio vision receipt bound to recipe, candidate and sample digests. All supplied samples must be inspected, with affirmative subject/crop, focal placement, collision, legal text, ghost text, clipping, matte edge, transition, sharpness and hold checks. This records the agent's actual vision assessment; it is not an independent model certification. Failure never starts a new paid job.

Timing/crop revisions reuse output when exact plate input digest, prompt and model match. They invalidate prior vision approval. `awaiting_export` needs only an explicit render action. Changed paid inputs require fresh actor-bound approval. Immutable generation identities, storage-generation fencing, leases and idempotency keys prevent duplicate submission. An interrupted submission without a saved provider ID becomes `submission_unknown`, requiring reconciliation. Result recovery keeps the same provider ID; dimension/duration mismatches block completion. Render retries operate on saved footage.

Finalization stores the existing schema-2 Animate document and durable source/video assets, preserving overlay tracks. The application route is `/#project/<projectId>/animate`. A manual-edit generation conflict is surfaced rather than overwritten. Existing KISS documents, tools and jobs continue separately.

## Implementation map

- `lib/composition-source.js`: canonical source extraction, pixel reconstruction and text protection.
- `lib/hybrid-composition.js`: durable request, recipe, approval, provider, candidate, vision and export lifecycle.
- `lib/composition-schema.js`: strict typed MCP/API inputs.
- `lib/composition-inspection.js`: actual FFmpeg temporal JPEG extraction.
- `lib/composition-api.js`: authenticated `/api/compositions` routes, matching the same service.
- `lib/animator-mcp.js`: capability discovery, default routing, model-visible recipes and native inspection images.
- `src/mcp-hybrid-ui.js`: source/input images, playable animatics/candidates/finals, exact recipe, explicit approval and existing editor handoff in the current panel.
- Existing motion evaluator, application renderer, project store and generation worker: reused rather than duplicated.

Hosted background work uses existing signed Cloud Tasks; local development schedules continuation at 60-second intervals. Reads also reconcile the saved operation. Chat polling uses a real client timer with an initial 60-second wait. Do not infer a completion ETA or closed-chat monitoring from an agent message.

## Storage, release and verification

No SQL migration is required. Requests are additive `hybrid-composition` application operations; assets and editable projects use existing private storage. Existing schemas remain readable. Rollback disables new hybrid creation while retaining saved records and the explicit legacy strategy.

The source tests cover one master for three ratios, actor/digest approval fences, withheld release before temporal approval, zero provider spend after overlay revision, unknown-submission recovery, deterministic-only output, typed MCP reads and native inspection blocks. Real FFmpeg tests decode event-boundary frames and verify edge crop anchors against browser math. These prove code and renderer behavior, not H3 quality or Runneth's media renderer. The inline app provides video controls; tools-only clients receive actual media URLs/native images, and client-specific display support remains a delivery boundary.

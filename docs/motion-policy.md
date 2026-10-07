# Base motion-policy

Implemented October 6, 2026. A composable agent scene description compiles into existing Animate tracks and ordinary timeline animation clips. There is no choreography inspector, bounce, spring, scale pop or rotation in the base style.

## Contract

Use `recipe.motionPolicy` with `schemaVersion:1`, `style:"base"` and a list of named clips. Every clip supplies actual per-ratio `{itemId,objectIds}` targets and a semantic role: hook, claim, benefit, offer, CTA (`cta`), brand, legal or visual. Join fragments by concatenating their clip lists with unique IDs; `after.clipId` can reference clips from another fragment. Unknown targets, duplicate ownership, missing dependencies and dependency cycles are rejected. Existing custom frame tracks remain available on objects outside policy ownership.

The base defaults preserve a hook from frame zero, bring claims/benefits in with a gentle rise and fade, and use a clean fade for offer/CTA/brand/visual elements. Legal copy remains stationary from frame zero. Effects can be explicitly selected from none/fade/rise/slide/reveal. A none clip stays visible from frame zero; use fade for delayed appearance. The style never randomizes motion or adds bounce.

Each clip may specify startFrame OR an after dependency with event start, settled or end plus gapFrames. `settled` is the last target's entrance completion. `end` includes its stable reading hold. Without an explicit anchor, a non-static clip follows the preceding information clip's end; static legal/brand elements do not become implicit sequencing anchors. Integer durationFrames, holdFrames and staggerFrames override defaults. A group staggers source objects within each ratio, in the supplied order. This is layer-level staggering, not automatic word or character splitting.

All values use the recipe's 24/30 fps timebase. A delay is a start/dependency gap, entrance duration describes movement, and holdFrames describes stable reading time. Hold budgets default to the larger of the role minimum and the longest target's estimated three-words-per-second time. This is an editable heuristic, not a comprehension guarantee. Explicit short holds are preserved with a warning. Translation distance is derived independently from each target's actual bounds.

Example authoring fragment (replace IDs with returned values):

```json
{
  "schemaVersion": 1,
  "style": "base",
  "clips": [
    {"id":"hook","role":"hook","targets":[{"itemId":"<actual ratio UUID>","objectIds":["<headline ID>"]}],"holdFrames":36},
    {"id":"claim","label":"Read the claim","role":"claim","targets":[{"itemId":"<actual ratio UUID>","objectIds":["<claim ID>"]}],"after":{"clipId":"hook","event":"end","gapFrames":6}},
    {"id":"benefits","role":"benefit","targets":[{"itemId":"<actual ratio UUID>","objectIds":["<benefit 1 ID>","<benefit 2 ID>"]}],"after":{"clipId":"claim","event":"end","gapFrames":9},"staggerFrames":4}
  ]
}
```

For a multi-ratio request, bind each clip to each actual ratio's source objects. Missing ratio bindings produce explicit warnings; separate per-ratio clip fragments can express intentional variations. Every recipe still contains every selected ratio. Background components are described separately: a source unit owned by generated footage cannot also carry deterministic source motion that would be discarded by replacement.

## Agent and application behavior

`animator_composition_capabilities.motionPolicy` returns the deployed style, effects, roles, defaults, supported events and limits. `animator_draft_composition` accepts the policy within the existing recipe, compiles it, produces unpaid animatics and returns `motionPolicy.clips` and warnings. Both MCP and authenticated `/api/compositions/:id/draft` invoke this same service. No new paid API or separate planner tool is required.

The saved public recipe retains authored policy and custom tracks separately. The execution recipe contains the resolved frame tracks, and the compilation digest participates in approval. Temporal candidate inspection includes compiled policy event boundaries. Timing/hold changes invalidate the prior review and reuse saved background output when its actual input/prompt/model remain unchanged. Existing provider ambiguity, actor approval and per-ratio vision gates still apply.

In the primary app, entrances appear as ordinary animation clips labelled with the clip name and treatment. Stable holds are the gaps between entrances. Move/trim and existing timing controls edit the actual tracks, snap policy clips to output frames and mark them customized. Undo restores both tracks and policy metadata. Authored intent is provenance; manual edits do not silently regenerate dependencies. Project-generation conflicts continue to protect newer manual edits from an older MCP request export.

No new inspector or editor mode was added. Existing advanced controls and native word/grapheme preparation remain available in Animate. The base policy compiles whole source layers, preserving source typography; it does not silently substitute fonts or pretend to expose native unit preparation through MCP.

## Diagnostics and compatibility

The report preserves explicit timing and names conflicts: short_reading_hold, reading_hold_exceeds_duration, competing_entrances, reading_window_overlap, entrance_interrupted_by_source_hold, unbound_ratio and legal_motion_override. It rejects impossible entrances rather than silently shortening them. Review the actual animatic to assess information order and readability; numerical schedules do not prove visible comprehension or lack of occlusion.

Only policy-origin clip metadata and versioned policy provenance are additive to existing schema-2 documents. Old recipes and projects continue to work. The compiler/defaults version and compiled digest are stored; existing projects play their baked tracks rather than recomputing against changed defaults. No database migration or new dependency is required.

Tests cover sequencing, longer reading holds, explicit delay pins, stagger, ratio-local movement, no-bounce schema validation, dependency/ownership failures, source-hold warnings, zero extra provider submissions after policy edits and actual primary-app retime/save/undo behavior. Existing FFmpeg/evaluator tests remain the export foundation. Live creative tuning, the deployed revision and installed chat-client delivery are separate verification gates.

# Travel Planning and Combing Migration Notes

Date: 2026-02-13  
Checklist ID: `T229`

## Legacy Baseline

- `slicer_v2` travel stage previously emitted only a simple travel move count heuristic.
- Combing, retract, and Z-hop decisions were not represented in travel-stage outputs.

## Current Baseline

- `App/slicer_v2/travel_planning.py` introduces deterministic per-layer travel planning.
- `App/slicer_v2/travel.py` now consumes per-layer feature counts and island graph data.
- Travel stage now emits combed/fallback move splits, travel length totals, retract counts, and Z-hop counts.

## Migration Impact

- Existing `travel_move_count` remains available for compatibility.
- New fields are additive (`travel_length_mm_total`, combing/retract/z-hop totals, layer-level travel arrays, report payload).
- Fallback behavior remains for flows that do not provide island graph artifacts.

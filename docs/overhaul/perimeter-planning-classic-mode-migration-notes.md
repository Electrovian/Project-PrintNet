# Perimeter Planning Classic Mode Migration Notes

Date: 2026-02-13  
Checklist ID: `T179`

## Legacy Baseline

- `slicer_v2` perimeters stage previously used a simple `region_count * perimeter_count` estimate.
- No shell-level perimeter loop planning existed in `slicer_v2`.

## Current Baseline

- `App/slicer_v2/perimeter_classic.py` now generates deterministic classic shell loops and metrics.
- `App/slicer_v2/perimeters.py` consumes `islands.layer_graphs` and emits classic report metadata.
- Fallback behavior remains for scenarios where island graph data is unavailable.

## Migration Impact

- Perimeter stage artifacts now include richer fields (`perimeter_length_mm_total`, `layer_perimeter_counts`, `report`).
- Downstream travel/G-code workstreams can consume shell-level planning signals instead of pure path-count heuristics.
- Existing pipelines remain executable with additive artifact fields.


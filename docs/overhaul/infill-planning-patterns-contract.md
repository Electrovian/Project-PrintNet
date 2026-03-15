# Infill Planning Patterns Contract

Date: 2026-02-13  
Checklist ID: `T192`

## Core Module

- `App/slicer_v2/infill_patterns.py`

Primary types:

- `InfillPathPlan`
- `LayerInfillPlan`
- `InfillPatternsReport`

Primary API:

- `build_infill_patterns(layer_graphs, infill_pattern, infill_percent, extrusion_width_mm, angle_start_deg=45.0, angle_step_deg=90.0) -> (list[LayerInfillPlan], InfillPatternsReport)`

## Stage Integration Contract

- `App/slicer_v2/infill.py`
  - consumes `islands.layer_graphs`.
  - emits:
    - `infill_path_count`
    - `infill_path_length_mm_total`
    - `layer_infill_counts`
    - `layer_infill_angles_deg`
    - `report`
  - retains fallback behavior if island graphs are unavailable.

## Settings Contract

- `App/slicer_v2/settings.py` adds/normalizes:
  - `infill_angle_start`
  - `infill_angle_step`
  - aliases for common infill angle keys.

## Script Contract

- `scripts/run-slicer-v2-infill-patterns-smoke.ps1`
- `scripts/test-slicer-v2-infill-patterns-unit.ps1`
- `scripts/test-slicer-v2-infill-patterns-integration.ps1`

Outputs:

- `docs/_slicer_v2_infill_patterns_report*.json`
- `docs/_slicer_v2_infill_patterns_summary*.txt`


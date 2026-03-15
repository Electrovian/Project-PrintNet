# Perimeter Planning Classic Mode Contract

Date: 2026-02-13  
Checklist ID: `T172`

## Core Module

- `App/slicer_v2/perimeter_classic.py`

Primary types:

- `PerimeterLoopPlan`
- `LayerPerimeterPlan`
- `PerimeterClassicReport`

Primary API:

- `build_classic_perimeters(layer_graphs, perimeter_count, line_width_mm, wall_sequence="outer_to_inner", first_layer_single_wall=False) -> (list[LayerPerimeterPlan], PerimeterClassicReport)`

## Stage Integration Contract

- `App/slicer_v2/perimeters.py`
  - consumes `islands.layer_graphs` when available.
  - emits classic perimeter mode metadata:
    - `perimeter_mode`
    - `perimeter_path_count`
    - `layer_perimeter_counts`
    - `perimeter_length_mm_total`
    - `report`

- fallback path remains available if island graph data is unavailable.

## Script Contract

- `scripts/run-slicer-v2-perimeter-classic-smoke.ps1`
- `scripts/test-slicer-v2-perimeter-classic-unit.ps1`
- `scripts/test-slicer-v2-perimeter-classic-integration.ps1`

Outputs:

- `docs/_slicer_v2_perimeter_classic_report*.json`
- `docs/_slicer_v2_perimeter_classic_summary*.txt`


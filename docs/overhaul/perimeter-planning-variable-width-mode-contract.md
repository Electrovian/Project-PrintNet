# Perimeter Planning Variable-Width Mode Contract

Date: 2026-02-13  
Checklist ID: `T182`

## Core Module

- `App/slicer_v2/perimeter_variable.py`

Primary types:

- `VariableWidthLoopPlan`
- `LayerVariableWidthPlan`
- `PerimeterVariableWidthReport`

Primary API:

- `build_variable_width_perimeters(layer_graphs, perimeter_count, base_line_width_mm, min_line_width_mm, max_line_width_mm, wall_sequence="outer_to_inner", first_layer_single_wall=False) -> (list[LayerVariableWidthPlan], PerimeterVariableWidthReport)`

## Stage Integration Contract

- `App/slicer_v2/perimeters.py`
  - uses `resolved_settings.perimeter_mode`.
  - routes to variable-width planner when `perimeter_mode == "variable_width"`.
  - emits variable-width fields:
    - `line_width_min_mm`
    - `line_width_max_mm`
    - `layer_min_widths_mm`
    - `layer_max_widths_mm`

## Settings Contract

- `App/slicer_v2/settings.py` adds:
  - `perimeter_mode`
  - `wall_sequence`
  - `first_layer_single_wall`
  - `variable_line_width_min`
  - `variable_line_width_max`

## Script Contract

- `scripts/run-slicer-v2-perimeter-variable-smoke.ps1`
- `scripts/test-slicer-v2-perimeter-variable-unit.ps1`
- `scripts/test-slicer-v2-perimeter-variable-integration.ps1`

Outputs:

- `docs/_slicer_v2_perimeter_variable_report*.json`
- `docs/_slicer_v2_perimeter_variable_summary*.txt`


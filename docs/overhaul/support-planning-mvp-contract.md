# Support Planning MVP Contract

Date: 2026-02-13  
Checklist ID: `T212`

## Core Module

- `App/slicer_v2/support_planning.py`

Primary types:

- `SupportRegionPlan`
- `LayerSupportPlan`
- `SupportPlanningReport`

Primary API:

- `build_support_plan(layer_graphs, vertical_edges=(), support_enabled, support_type, support_density_percent, support_spacing_mm, support_xy_gap_mm, support_z_gap_mm, support_interface_layers, extrusion_width_mm) -> (list[LayerSupportPlan], SupportPlanningReport)`

## Stage Integration Contract

- `App/slicer_v2/supports.py`
  - consumes:
    - `islands.layer_graphs`
    - `islands.vertical_edges`
  - emits:
    - `support_region_count`
    - `support_path_count`
    - `support_path_length_mm_total`
    - `support_interface_path_count_total`
    - `unsupported_island_count_total`
    - `layer_support_counts`
    - `layer_support_path_counts`
    - `layer_support_interface_path_counts`
    - `report`
  - retains fallback behavior when island graph data is unavailable.

## Settings Contract

- `App/slicer_v2/settings.py` normalizes:
  - `support_enabled`
  - `support_type`
  - `support_density_percent`
  - `support_spacing_mm`
  - `support_xy_gap_mm`
  - `support_z_gap_mm`
  - `support_interface_layers`
  - common aliases (`support_density`, `support_spacing`, `support_xy_gap`, `support_z_gap`, `support_interface_layer_count`).

## Script Contract

- `scripts/run-slicer-v2-support-planning-smoke.ps1`
- `scripts/test-slicer-v2-support-planning-unit.ps1`
- `scripts/test-slicer-v2-support-planning-integration.ps1`

Outputs:

- `docs/_slicer_v2_support_planning_report*.json`
- `docs/_slicer_v2_support_planning_summary*.txt`

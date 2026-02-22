# Extrusion Volume and Flow Model Contract

Date: 2026-02-13  
Checklist ID: `T232`

## Core Module

- `App/slicer_v2/extrusion_flow.py`

Primary types:

- `FeatureExtrusionPlan`
- `LayerExtrusionFlowPlan`
- `ExtrusionFlowReport`

Primary API:

- `build_extrusion_flow_model(layer_heights_mm, layer_z_values_mm, perimeter_lengths_mm, infill_lengths_mm, support_lengths_mm, solid_lengths_mm, bridge_lengths_mm, line_width_mm, nozzle_diameter_mm, filament_diameter_mm, ...) -> (list[LayerExtrusionFlowPlan], ExtrusionFlowReport)`

## Stage Integration Contract

- `App/slicer_v2/gcode.py`
  - consumes:
    - `slice_grid.layer_heights_mm`
    - `slice_grid.layer_z_values_mm`
    - `perimeters.layer_plans`
    - `infill.layer_plans`
    - `supports.layer_plans`
    - `bridges.layer_plans`
  - emits:
    - `extrusion_path_length_mm_total`
    - `extrusion_volume_mm3_total`
    - `estimated_filament_mm`
    - `estimated_mass_g`
    - `estimated_cost_usd`
    - `layer_extrusion_volumes_mm3`
    - `layer_filament_lengths_mm`
    - `extrusion_flow`
  - retains existing top-level G-code artifact fields.

## Settings Contract

- `App/slicer_v2/settings.py` normalizes:
  - `flow_multiplier`
  - `perimeter_flow_ratio`
  - `infill_flow_ratio`
  - `support_flow_ratio`
  - `solid_flow_ratio`
  - `bridge_flow_ratio`
  - `filament_density_g_cm3`
  - `filament_cost_usd_per_kg`
  - `small_feature_threshold_mm`
  - `small_feature_flow_boost_ratio`
  - common aliases (`flow`, `wall_flow`, `infill_flow`, `support_flow`, `solid_flow`, `filament_density`, `filament_cost_per_kg`).

## Script Contract

- `scripts/run-slicer-v2-extrusion-flow-smoke.ps1`
- `scripts/test-slicer-v2-extrusion-flow-unit.ps1`
- `scripts/test-slicer-v2-extrusion-flow-integration.ps1`

Outputs:

- `docs/_slicer_v2_extrusion_flow_report*.json`
- `docs/_slicer_v2_extrusion_flow_summary*.txt`

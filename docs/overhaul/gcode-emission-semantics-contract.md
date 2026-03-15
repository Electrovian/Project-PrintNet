# G-code Emission Semantics Contract

Date: 2026-02-13  
Checklist ID: `T242`

## Core Module

- `App/slicer_v2/gcode_emission.py`

Primary types:

- `GCodeCommandPlan`
- `LayerGCodePlan`
- `GCodeEmissionReport`

Primary API:

- `emit_gcode_semantics(layer_heights_mm, layer_z_values_mm, layer_path_lengths_mm, layer_filament_lengths_mm, layer_travel_move_counts, layer_travel_lengths_mm, ..., absolute_extrusion, firmware_flavor, startup_macro, end_macro) -> (list[LayerGCodePlan], list[str], GCodeEmissionReport)`

## Stage Integration Contract

- `App/slicer_v2/gcode.py`
  - consumes:
    - extrusion flow layer estimates from `build_extrusion_flow_model(...)`
    - travel layer counts/lengths/retract/zhop arrays
    - normalized G-code semantic settings
  - emits:
    - `lines`
    - `line_count`
    - `gcode_emission`
    - `layer_gcode_plans`
    - compatibility and summary fields (`estimated_time_seconds`, `estimated_filament_mm`, `estimated_mass_g`, `estimated_cost_usd`)

## Settings Contract

- `App/slicer_v2/settings.py` normalizes:
  - `gcode_absolute_extrusion`
  - `gcode_firmware_flavor`
  - `gcode_startup_macro`
  - `gcode_end_macro`
  - `gcode_retract_length_mm`
  - `gcode_emit_layer_comments`
  - aliases:
    - `absolute_extrusion`
    - `gcode_firmware`
    - `start_gcode`
    - `end_gcode`
    - `gcode_retract_length`
    - `gcode_layer_comments`

## Script Contract

- `scripts/run-slicer-v2-gcode-emission-smoke.ps1`
- `scripts/test-slicer-v2-gcode-emission-unit.ps1`
- `scripts/test-slicer-v2-gcode-emission-integration.ps1`

Outputs:

- `docs/_slicer_v2_gcode_emission_report*.json`
- `docs/_slicer_v2_gcode_emission_summary*.txt`

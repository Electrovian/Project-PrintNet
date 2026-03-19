# G-code Validation and Sanity Checks Contract

Date: 2026-02-13  
Checklist ID: `T252`

## Core Module

- `App/slicer_v2/gcode_validation.py`

Primary types:

- `GCodeValidationIssue`
- `GCodeValidationReport`

Primary API:

- `validate_gcode_semantics(lines, *, absolute_extrusion, strict, bed_x_mm, bed_y_mm, bed_z_mm, require_monotonic_z, require_monotonic_e, allow_absolute_retract, allow_negative_xy, line_length_limit, max_line_count, tolerance_mm) -> GCodeValidationReport`

## Stage Integration Contract

- `App/slicer_v2/gcode.py`
  - consumes:
    - emitted semantic `lines`
    - normalized validation settings
  - emits:
    - `gcode_validation_enabled`
    - `gcode_validation_ok`
    - `gcode_validation_error_count`
    - `gcode_validation_warning_count`
    - `gcode_validation` (full report payload)

## Settings Contract

- `App/slicer_v2/settings.py` normalizes:
  - `gcode_validation_enabled`
  - `gcode_validation_strict`
  - `gcode_validation_bed_x_mm`
  - `gcode_validation_bed_y_mm`
  - `gcode_validation_bed_z_mm`
  - `gcode_validation_require_monotonic_z`
  - `gcode_validation_require_monotonic_e`
  - `gcode_validation_allow_absolute_retract`
  - `gcode_validation_allow_negative_xy`
  - `gcode_validation_line_length_limit`
  - `gcode_validation_max_line_count`
  - `gcode_validation_tolerance_mm`

Aliases include:

- `gcode_validate_enabled`
- `gcode_validate_strict`
- `bed_x`, `bed_y`, `bed_z`
- `build_volume_x`, `build_volume_y`, `build_volume_z`
- `validation_require_monotonic_z`, `validation_require_monotonic_e`
- `validation_allow_absolute_retract`, `validation_allow_negative_xy`
- `gcode_validation_line_limit`, `gcode_validation_max_lines`
- `gcode_validation_line_length`, `gcode_validation_tolerance`

## Script Contract

- `scripts/run-slicer-v2-gcode-validation-smoke.ps1`
- `scripts/test-slicer-v2-gcode-validation-unit.ps1`
- `scripts/test-slicer-v2-gcode-validation-integration.ps1`

Outputs:

- `docs/_slicer_v2_gcode_validation_report*.json`
- `docs/_slicer_v2_gcode_validation_summary*.txt`

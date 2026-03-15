# G-code Validation and Sanity Checks Migration Notes

Date: 2026-02-13  
Checklist ID: `T259`

## Legacy Baseline

- `slicer_v2` emitted G-code semantics without a dedicated post-emission bounds/sequence validator.
- Consumers had no structured stage-level report for G-code sanity failures.

## Current Baseline

- `App/slicer_v2/gcode_validation.py` validates emitted G-code lines for parse integrity, bounds, and monotonicity constraints.
- `App/slicer_v2/gcode.py` publishes validation summary fields and full structured report payload.
- Strict mode can fail the `gcode` stage when validation errors are present.

## Migration Impact

- Existing G-code output fields remain available.
- New validation fields are additive:
  - `gcode_validation_enabled`
  - `gcode_validation_ok`
  - `gcode_validation_error_count`
  - `gcode_validation_warning_count`
  - `gcode_validation`
- Bounds defaults come from validator settings; deployments with non-220/220/250 beds should set machine-specific overrides.

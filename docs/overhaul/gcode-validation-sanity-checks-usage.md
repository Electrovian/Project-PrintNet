# G-code Validation and Sanity Checks Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T258`

## Run G-code Validation Smoke

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-slicer-v2-gcode-validation-smoke.ps1
```

## Run Unit and Integration Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-gcode-validation-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-gcode-validation-integration.ps1
```

## Defaults

- Validation enabled: `true` (`gcode_validation_enabled`)
- Strict mode: `false` (`gcode_validation_strict`)
- Bed bounds: `220 x 220 x 250` mm (`gcode_validation_bed_x_mm`, `gcode_validation_bed_y_mm`, `gcode_validation_bed_z_mm`)
- Require monotonic Z: `true` (`gcode_validation_require_monotonic_z`)
- Require monotonic E: `true` (`gcode_validation_require_monotonic_e`)
- Allow absolute retract: `true` (`gcode_validation_allow_absolute_retract`)
- Allow negative XY: `false` (`gcode_validation_allow_negative_xy`)
- Line length limit: `512` (`gcode_validation_line_length_limit`)
- Max line count: `250000` (`gcode_validation_max_line_count`)
- Numeric tolerance: `0.0001` mm (`gcode_validation_tolerance_mm`)
- Smoke report path: `docs/_slicer_v2_gcode_validation_report.json`
- Smoke summary path: `docs/_slicer_v2_gcode_validation_summary.txt`

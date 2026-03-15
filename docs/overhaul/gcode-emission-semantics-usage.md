# G-code Emission Semantics Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T248`

## Run G-code Emission Smoke

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-slicer-v2-gcode-emission-smoke.ps1
```

## Run Unit and Integration Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-gcode-emission-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-gcode-emission-integration.ps1
```

## Defaults

- Absolute extrusion mode: `true` (`gcode_absolute_extrusion`)
- Firmware flavor: `marlin` (`gcode_firmware_flavor`)
- Startup macro: empty (`gcode_startup_macro`)
- End macro: empty (`gcode_end_macro`)
- Retract length: `0.8` (`gcode_retract_length_mm`)
- Emit layer comments: `true` (`gcode_emit_layer_comments`)
- Smoke report path: `docs/_slicer_v2_gcode_emission_report.json`
- Smoke summary path: `docs/_slicer_v2_gcode_emission_summary.txt`

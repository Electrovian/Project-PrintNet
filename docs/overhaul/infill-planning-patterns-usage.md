# Infill Planning Patterns Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T198`

## Run Infill Patterns Smoke

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-slicer-v2-infill-patterns-smoke.ps1
```

## Run Unit and Integration Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-infill-patterns-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-infill-patterns-integration.ps1
```

## Defaults

- Infill percent: `15.0` (`infill_percent`)
- Infill pattern: `rectilinear` (`infill_pattern`)
- Infill angle start: `45.0` (`infill_angle_start`)
- Infill angle step: `90.0` (`infill_angle_step`)
- Base extrusion width: `0.4` (`extrusion_width`)
- Smoke report path: `docs/_slicer_v2_infill_patterns_report.json`
- Smoke summary path: `docs/_slicer_v2_infill_patterns_summary.txt`


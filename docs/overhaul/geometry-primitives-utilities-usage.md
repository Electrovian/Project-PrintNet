# Geometry Primitives and Utilities Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T128`

## Run Geometry Smoke

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-slicer-v2-geometry-smoke.ps1
```

## Run Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-geometry-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-geometry-integration.ps1
```

## Defaults

- Coordinate epsilon: `1e-9`
- Smoke report path: `docs/_slicer_v2_geometry_report.json`
- Smoke summary path: `docs/_slicer_v2_geometry_summary.txt`
- Test performance budget: `20 seconds`

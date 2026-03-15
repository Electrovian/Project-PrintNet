# Polygon Offset and Cleanup Pipeline Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T138`

## Run Polygon Smoke

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-slicer-v2-polygon-offset-smoke.ps1
```

## Run Unit and Integration Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-polygon-offset-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-polygon-offset-integration.ps1
```

## Defaults

- Offset distance: `0.6 mm`
- Minimum area filter: `0.01` in smoke fixture pipeline
- Smoke report path: `docs/_slicer_v2_polygon_offset_report.json`
- Smoke summary path: `docs/_slicer_v2_polygon_offset_summary.txt`
- Test performance budget: `20 seconds`

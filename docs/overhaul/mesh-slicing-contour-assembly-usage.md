# Mesh Slicing and Contour Assembly Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T148`

## Run Mesh Slicing Smoke

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-slicer-v2-mesh-slicing-smoke.ps1
```

## Run Unit and Integration Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-mesh-slicing-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-mesh-slicing-integration.ps1
```

## Defaults

- Layer height: `0.2 mm`
- Segment dedupe tolerance: `1e-6` (module default)
- Contour join tolerance: `1e-4` (module default)
- Min contour area: `1e-6` (module default)
- Smoke report path: `docs/_slicer_v2_mesh_slicing_report.json`
- Smoke summary path: `docs/_slicer_v2_mesh_slicing_summary.txt`

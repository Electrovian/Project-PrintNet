# slicer_v2 Package Scaffolding Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T108`

## Run Smoke Pipeline

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-slicer-v2-scaffold-smoke.ps1
```

## Run via CLI Module

```powershell
python -m App.slicer_v2.cli --mesh-path path/to/model.stl --layer-height 0.2
```

## Run Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-scaffolding-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-scaffolding-integration.ps1
```

## Defaults

- Stage order:
  - `mesh`
  - `slice_grid`
  - `regions`
  - `perimeters`
  - `infill`
  - `supports`
  - `bridges`
  - `travel`
  - `gcode`
- Default layer height: `0.2 mm`
- Default model height hint: `20.0 mm`
- Default support: `disabled`
- Smoke report path: `docs/_slicer_v2_scaffolding_report.json`
- Smoke summary path: `docs/_slicer_v2_scaffolding_summary.txt`

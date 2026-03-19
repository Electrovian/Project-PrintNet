# Perimeter Planning Classic Mode Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T178`

## Run Perimeter Classic Smoke

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-slicer-v2-perimeter-classic-smoke.ps1
```

## Run Unit and Integration Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-perimeter-classic-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-perimeter-classic-integration.ps1
```

## Defaults

- Perimeter count: `2` (`perimeter_count`)
- Line width: `0.4 mm` (`extrusion_width`)
- Wall sequence: `outer_to_inner` (`wall_sequence`)
- First layer single wall: `False` (`first_layer_single_wall`)
- Smoke report path: `docs/_slicer_v2_perimeter_classic_report.json`
- Smoke summary path: `docs/_slicer_v2_perimeter_classic_summary.txt`


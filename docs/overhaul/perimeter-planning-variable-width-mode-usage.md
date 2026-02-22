# Perimeter Planning Variable-Width Mode Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T188`

## Run Perimeter Variable-Width Smoke

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-slicer-v2-perimeter-variable-smoke.ps1
```

## Run Unit and Integration Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-perimeter-variable-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-perimeter-variable-integration.ps1
```

## Defaults

- Perimeter mode: `classic` (`perimeter_mode`)
- Wall sequence: `outer_to_inner` (`wall_sequence`)
- First-layer single wall: `False` (`first_layer_single_wall`)
- Base line width: `0.4 mm` (`extrusion_width`)
- Variable minimum line width: `0.3 mm` (`variable_line_width_min`)
- Variable maximum line width: `0.5 mm` (`variable_line_width_max`)
- Smoke report path: `docs/_slicer_v2_perimeter_variable_report.json`
- Smoke summary path: `docs/_slicer_v2_perimeter_variable_summary.txt`


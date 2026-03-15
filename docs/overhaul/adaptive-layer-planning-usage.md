# Adaptive Layer Planning Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T158`

## Run Adaptive Layer Smoke

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-slicer-v2-adaptive-layer-smoke.ps1
```

## Run Unit and Integration Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-adaptive-layer-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-adaptive-layer-integration.ps1
```

## Defaults

- Base layer height: `0.2 mm` (`layer_height`)
- Adaptive enabled: `False` (`adaptive_layering_enabled`)
- Adaptive minimum height: `0.08 mm` (`adaptive_layer_min`)
- Adaptive maximum height: `0.32 mm` (`adaptive_layer_max`)
- Top/bottom refinement zone: `0.0 mm` (`adaptive_top_bottom_refine_mm`)
- Manual adaptive ranges: empty (`adaptive_layer_ranges`)
- Smoke report path: `docs/_slicer_v2_adaptive_layer_report.json`
- Smoke summary path: `docs/_slicer_v2_adaptive_layer_summary.txt`


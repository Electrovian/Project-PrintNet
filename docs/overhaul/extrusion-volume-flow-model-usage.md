# Extrusion Volume and Flow Model Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T238`

## Run Extrusion Flow Smoke

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-slicer-v2-extrusion-flow-smoke.ps1
```

## Run Unit and Integration Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-extrusion-flow-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-extrusion-flow-integration.ps1
```

## Defaults

- Global flow multiplier: `1.0` (`flow_multiplier`)
- Perimeter flow ratio: `1.0` (`perimeter_flow_ratio`)
- Infill flow ratio: `1.0` (`infill_flow_ratio`)
- Support flow ratio: `1.0` (`support_flow_ratio`)
- Solid flow ratio: `1.0` (`solid_flow_ratio`)
- Bridge flow ratio: `1.0` (`bridge_flow_ratio`)
- Filament density: `1.24` (`filament_density_g_cm3`)
- Filament cost per kg: `0.0` (`filament_cost_usd_per_kg`)
- Small-feature threshold: `4.0` (`small_feature_threshold_mm`)
- Small-feature flow boost: `1.05` (`small_feature_flow_boost_ratio`)
- Smoke report path: `docs/_slicer_v2_extrusion_flow_report.json`
- Smoke summary path: `docs/_slicer_v2_extrusion_flow_summary.txt`

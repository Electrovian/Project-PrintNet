# Solid Layers and Bridge Planning Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T208`

## Run Solid/Bridge Smoke

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-slicer-v2-solid-bridges-smoke.ps1
```

## Run Unit and Integration Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-solid-bridges-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-solid-bridges-integration.ps1
```

## Defaults

- Top solid layers: `3` (`top_layers`)
- Bottom solid layers: `3` (`bottom_layers`)
- Bridge enabled: `true` (`bridge_enabled`)
- Bridge flow ratio: `1.0` (`bridge_flow_ratio`)
- Bridge speed ratio: `0.8` (`bridge_speed_ratio`)
- Extrusion width: `0.4` (`extrusion_width`)
- Smoke report path: `docs/_slicer_v2_solid_bridges_report.json`
- Smoke summary path: `docs/_slicer_v2_solid_bridges_summary.txt`

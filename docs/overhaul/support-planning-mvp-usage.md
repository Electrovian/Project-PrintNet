# Support Planning MVP Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T218`

## Run Support Planning Smoke

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-slicer-v2-support-planning-smoke.ps1
```

## Run Unit and Integration Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-support-planning-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-support-planning-integration.ps1
```

## Defaults

- Support enabled: `false` (`support_enabled`)
- Support type: `normal` (`support_type`)
- Support density: `15.0` (`support_density_percent`)
- Support spacing: `2.5` (`support_spacing_mm`)
- Support XY gap: `0.25` (`support_xy_gap_mm`)
- Support Z gap: `0.2` (`support_z_gap_mm`)
- Support interface layers: `2` (`support_interface_layers`)
- Extrusion width: `0.4` (`extrusion_width`)
- Smoke report path: `docs/_slicer_v2_support_planning_report.json`
- Smoke summary path: `docs/_slicer_v2_support_planning_summary.txt`

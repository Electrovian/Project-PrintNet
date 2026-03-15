# Travel Planning and Combing Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T228`

## Run Travel Planning Smoke

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-slicer-v2-travel-planning-smoke.ps1
```

## Run Unit and Integration Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-travel-planning-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-travel-planning-integration.ps1
```

## Defaults

- Travel speed: `150.0` (`travel_speed`)
- Combing enabled: `true` (`travel_combing_enabled`)
- Combing max detour ratio: `1.5` (`travel_combing_max_detour_ratio`)
- Retract enabled: `true` (`travel_retract_enabled`)
- Retract minimum travel: `2.0` (`travel_retract_min_travel_mm`)
- Z-hop enabled: `false` (`travel_z_hop_enabled`)
- Z-hop height: `0.2` (`travel_z_hop_mm`)
- Smoke report path: `docs/_slicer_v2_travel_planning_report.json`
- Smoke summary path: `docs/_slicer_v2_travel_planning_summary.txt`

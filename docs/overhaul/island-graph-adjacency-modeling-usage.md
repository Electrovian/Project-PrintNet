# Island Graph and Adjacency Modeling Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T168`

## Run Island Graph Smoke

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-slicer-v2-island-graph-smoke.ps1
```

## Run Unit and Integration Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-island-graph-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-island-graph-integration.ps1
```

## Defaults

- Minimum contour area: `1e-6`
- Maximum nesting depth: `128`
- Vertical adjacency layer gap: `1`
- Smoke report path: `docs/_slicer_v2_island_graph_report.json`
- Smoke summary path: `docs/_slicer_v2_island_graph_summary.txt`


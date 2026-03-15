# Polygon Offset and Cleanup Pipeline Contract

Date: 2026-02-13  
Checklist ID: `T132`

## Core Module

- `App/slicer_v2/polygon_pipeline.py`

Primary APIs:

- `cleanup_polygon(polygon, remove_collinear=True, min_area=1e-6) -> Polygon | None`
- `cleanup_polygons(polygons, remove_collinear=True, min_area=1e-6) -> list[Polygon]`
- `offset_polygon(polygon, distance, min_area=1e-6) -> Polygon | None`
- `offset_polygons(polygons, distance, min_area=1e-6) -> list[Polygon]`
- `cleanup_and_offset_polygons(polygons, offset_distance, min_area=1e-6, strict=False) -> (list[Polygon], PolygonOffsetCleanupReport)`

Core types:

- `PolygonOffsetCleanupReport`
- `SlicerV2PolygonPipelineError`

## Contract Semantics

- Cleanup stage:
  - removes collinear vertices
  - drops polygons below `min_area`
- Offset stage:
  - applies deterministic edge-normal offset
  - drops invalid/degenerate results
- Batch stage report contains:
  - counts (`input`, `cleaned`, `output`, `dropped`)
  - applied offset distance
  - warning list and warning count

## Script Contract

- `scripts/run-slicer-v2-polygon-offset-smoke.ps1`
- `scripts/test-slicer-v2-polygon-offset-unit.ps1`
- `scripts/test-slicer-v2-polygon-offset-integration.ps1`

Outputs:

- `docs/_slicer_v2_polygon_offset_report*.json`
- `docs/_slicer_v2_polygon_offset_summary*.txt`

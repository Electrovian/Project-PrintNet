# Geometry Primitives and Utilities Contract

Date: 2026-02-13  
Checklist ID: `T122`

## Core Module

- `App/slicer_v2/geometry.py`

Primary types:

- `Point2`
- `AABB`
- `Polygon`
- `Island`

Primary helpers:

- `polygon_from_tuples(...)`
- `island_from_tuples(...)`
- `polyline_length(...)`
- `bounds_for_polygons(...)`

## Contract Semantics

- `Point2` coordinates must be finite.
- `AABB` bounds must satisfy `max >= min` per axis.
- `Polygon` requires at least 3 unique points and non-zero signed area.
- `Island` normalizes winding:
  - outer polygon => counter-clockwise
  - hole polygons => clockwise
- Containment API:
  - `Polygon.contains_point(...)`
  - `Island.contains_point(...)` (outer included, holes excluded)

## Script Contract

- `scripts/run-slicer-v2-geometry-smoke.ps1`
- `scripts/test-slicer-v2-geometry-unit.ps1`
- `scripts/test-slicer-v2-geometry-integration.ps1`

Outputs:

- `docs/_slicer_v2_geometry_report*.json`
- `docs/_slicer_v2_geometry_summary*.txt`

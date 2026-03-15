# Geometry Primitives and Utilities Migration Notes

Date: 2026-02-13  
Checklist ID: `T129`

## Legacy Baseline

- Geometry utilities were concentrated in `App/slicer/geometry.py` with broad legacy scope.
- `slicer_v2` did not yet expose a dedicated primitives layer for new stage modules.

## Current Baseline

- `App/slicer_v2/geometry.py` now provides canonical primitives/utilities for v2 development.
- Winding and containment semantics are explicit and validated by unit/integration tests.
- Public `slicer_v2` exports now include geometry types and helper APIs.

## Migration Impact

- New `slicer_v2` geometry features should build on these primitives rather than importing legacy geometry directly.
- Existing stage placeholders can incrementally adopt `Polygon`/`Island`/`AABB` contracts in upcoming blocks.
- Legacy and v2 geometry stacks remain separated to reduce regression risk during migration.

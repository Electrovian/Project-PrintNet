# Island Graph and Adjacency Modeling Migration Notes

Date: 2026-02-13  
Checklist ID: `T169`

## Legacy Baseline

- `slicer_v2` previously moved from `regions` directly to `perimeters`.
- No explicit island graph stage existed for nesting and adjacency metadata.

## Current Baseline

- `App/slicer_v2/island_graph.py` now computes contour-to-island topology, hole grouping, and adjacency edges.
- New `App/slicer_v2/islands.py` stage is inserted between `regions` and `perimeters`.
- `perimeters` now consumes island totals when available for path cardinality decisions.

## Migration Impact

- Downstream geometry planning can use `islands.layer_graphs` and `islands.vertical_edges`.
- Existing stage contracts remain intact; additional metadata is additive.
- Scaffolding stage count increases by one due to the new `islands` stage.


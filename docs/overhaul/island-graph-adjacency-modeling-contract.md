# Island Graph and Adjacency Modeling Contract

Date: 2026-02-13  
Checklist ID: `T162`

## Core Module

- `App/slicer_v2/island_graph.py`

Primary types:

- `LayerAdjacencyEdge`
- `VerticalAdjacencyEdge`
- `LayerIslandGraph`
- `IslandGraphReport`

Primary APIs:

- `build_layer_island_graph(contours, layer_index, z_height_mm, min_area=1e-6, max_nesting_depth=128) -> LayerIslandGraph`
- `build_vertical_adjacency(layer_graphs, max_layer_gap=1) -> tuple[VerticalAdjacencyEdge, ...]`
- `build_island_graph_report(layer_graphs, vertical_edges) -> IslandGraphReport`

## Stage Integration Contract

- `App/slicer_v2/islands.py`
  - consumes `regions.layer_contours` and `slice_grid.layer_z_values_mm`.
  - emits layer island counts, hole counts, adjacency counts, and report metadata.

- `App/slicer_v2/pipeline.py`
  - adds `islands` stage between `regions` and `perimeters`.

- `App/slicer_v2/perimeters.py`
  - uses `islands.island_count_total` as preferred region cardinality when available.

## Script Contract

- `scripts/run-slicer-v2-island-graph-smoke.ps1`
- `scripts/test-slicer-v2-island-graph-unit.ps1`
- `scripts/test-slicer-v2-island-graph-integration.ps1`

Outputs:

- `docs/_slicer_v2_island_graph_report*.json`
- `docs/_slicer_v2_island_graph_summary*.txt`


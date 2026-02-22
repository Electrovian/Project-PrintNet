# Island Graph and Adjacency Modeling Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T164`

## Error Classes

- `ISLAND_GRAPH_MAX_DEPTH_INVALID`
  - Trigger: `max_nesting_depth < 1`.
  - Behavior: raises `SlicerV2IslandGraphError`.

- `ISLAND_GRAPH_MIN_AREA_INVALID`
  - Trigger: negative `min_area`.
  - Behavior: raises `SlicerV2IslandGraphError`.

- `ISLAND_GRAPH_CONTOUR_NOT_POLYGON`
  - Trigger: layer contour payload contains non-`Polygon` item.
  - Behavior: raises `SlicerV2IslandGraphError`.

- `ISLAND_GRAPH_PARENT_CYCLE_DETECTED`
  - Trigger: invalid parent chain cycle while computing nesting depth.
  - Behavior: raises `SlicerV2IslandGraphError`.

- `ISLAND_GRAPH_MAX_DEPTH_EXCEEDED`
  - Trigger: contour nesting exceeds configured limit.
  - Behavior: raises `SlicerV2IslandGraphError`.

- `ISLAND_GRAPH_LAYER_GAP_INVALID`
  - Trigger: `max_layer_gap < 1` for vertical adjacency.
  - Behavior: raises `SlicerV2IslandGraphError`.

- `SLICER_V2_ISLAND_GRAPH_SMOKE_COMMAND_FAILED`
  - Trigger: smoke script command exits non-zero.
  - Behavior: PowerShell wrapper failure with exit code.

## Warning Classes (report-level)

- `layer_<idx>:polygons_without_islands:<count>`


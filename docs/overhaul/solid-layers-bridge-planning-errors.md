# Solid Layers and Bridge Planning Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T204`

## Error Classes

- `SOLID_BRIDGE_LAYER_GRAPH_INVALID`
  - Trigger: planner receives non-`LayerIslandGraph` input.
  - Behavior: raises `SlicerV2SolidBridgeError`.

- `SOLID_BRIDGE_VERTICAL_EDGE_INVALID`
  - Trigger: planner receives non-`VerticalAdjacencyEdge` input.
  - Behavior: raises `SlicerV2SolidBridgeError`.

- `SOLID_BRIDGE_LAYER_COUNT_NEGATIVE`
  - Trigger: `top_layers` or `bottom_layers` is negative.
  - Behavior: raises `SlicerV2SolidBridgeError`.

- `SOLID_BRIDGE_LAYER_COUNT_EXCESSIVE`
  - Trigger: `top_layers` or `bottom_layers` exceeds hard safety cap.
  - Behavior: raises `SlicerV2SolidBridgeError`.

- `SOLID_BRIDGE_EXTRUSION_WIDTH_INVALID`
  - Trigger: extrusion width is non-positive.
  - Behavior: raises `SlicerV2SolidBridgeError`.

- `SOLID_BRIDGE_FLOW_RATIO_INVALID`
  - Trigger: bridge flow ratio is outside `0.2..3.0`.
  - Behavior: raises `SlicerV2SolidBridgeError`.

- `SOLID_BRIDGE_SPEED_RATIO_INVALID`
  - Trigger: bridge speed ratio is outside `0.1..3.0`.
  - Behavior: raises `SlicerV2SolidBridgeError`.

- `SLICER_V2_SOLID_BRIDGES_SMOKE_COMMAND_FAILED`
  - Trigger: smoke command exits non-zero.
  - Behavior: PowerShell wrapper failure with exit code.

## Warning Classes (report-level)

- `solid_bridges:no_layers`
- `solid_bridges:top_bottom_overlap`
- `layer_<idx>:island_<idx>:degenerate_bounds`
- `layer_<idx>:island_<idx>:bridge_skipped_disabled`
- `solid_bridges:fallback_without_islands`

# Support Planning MVP Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T214`

## Error Classes

- `SUPPORT_LAYER_GRAPH_INVALID`
  - Trigger: planner receives non-`LayerIslandGraph` input.
  - Behavior: raises `SlicerV2SupportPlanningError`.

- `SUPPORT_VERTICAL_EDGE_INVALID`
  - Trigger: planner receives non-`VerticalAdjacencyEdge` input.
  - Behavior: raises `SlicerV2SupportPlanningError`.

- `SUPPORT_TYPE_UNSUPPORTED`
  - Trigger: support mode is not in allowed MVP types.
  - Behavior: raises `SlicerV2SupportPlanningError`.

- `SUPPORT_DENSITY_PERCENT_INVALID`
  - Trigger: support density is outside `0..100`.
  - Behavior: raises `SlicerV2SupportPlanningError`.

- `SUPPORT_SPACING_INVALID`
  - Trigger: support spacing is non-positive.
  - Behavior: raises `SlicerV2SupportPlanningError`.

- `SUPPORT_XY_GAP_INVALID`
  - Trigger: support XY gap is negative.
  - Behavior: raises `SlicerV2SupportPlanningError`.

- `SUPPORT_Z_GAP_INVALID`
  - Trigger: support Z gap is negative.
  - Behavior: raises `SlicerV2SupportPlanningError`.

- `SUPPORT_INTERFACE_LAYER_COUNT_INVALID`
  - Trigger: support interface layer count is negative.
  - Behavior: raises `SlicerV2SupportPlanningError`.

- `SUPPORT_INTERFACE_LAYER_COUNT_EXCESSIVE`
  - Trigger: support interface layer count exceeds safety cap.
  - Behavior: raises `SlicerV2SupportPlanningError`.

- `SUPPORT_EXTRUSION_WIDTH_INVALID`
  - Trigger: extrusion width is non-positive.
  - Behavior: raises `SlicerV2SupportPlanningError`.

- `SLICER_V2_SUPPORT_PLANNING_SMOKE_COMMAND_FAILED`
  - Trigger: smoke command exits non-zero.
  - Behavior: PowerShell wrapper failure with exit code.

## Warning Classes (report-level)

- `support_planning:no_layers`
- `support_planning:tree_mode_mvp_estimate`
- `support_planning:density_zero`
- `layer_<idx>:island_<idx>:degenerate_bounds`
- `layer_<idx>:unsupported_islands_without_density:<count>`
- `support_planning:fallback_without_islands`

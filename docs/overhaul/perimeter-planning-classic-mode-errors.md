# Perimeter Planning Classic Mode Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T174`

## Error Classes

- `PERIMETER_CLASSIC_COUNT_INVALID`
  - Trigger: requested perimeter count `< 1`.
  - Behavior: raises `SlicerV2PerimeterClassicError`.

- `PERIMETER_CLASSIC_COUNT_EXCESSIVE`
  - Trigger: requested perimeter count exceeds safety cap (`> 20`).
  - Behavior: raises `SlicerV2PerimeterClassicError`.

- `PERIMETER_CLASSIC_LINE_WIDTH_INVALID`
  - Trigger: non-positive line width.
  - Behavior: raises `SlicerV2PerimeterClassicError`.

- `PERIMETER_CLASSIC_WALL_SEQUENCE_INVALID`
  - Trigger: unsupported wall sequence string.
  - Behavior: raises `SlicerV2PerimeterClassicError`.

- `PERIMETER_CLASSIC_LAYER_GRAPH_INVALID`
  - Trigger: non-`LayerIslandGraph` object passed into planner.
  - Behavior: raises `SlicerV2PerimeterClassicError`.

- `PERIMETER_CLASSIC_ROLE_INVALID`
  - Trigger: unsupported perimeter role value.
  - Behavior: raises `SlicerV2PerimeterClassicError`.

- `SLICER_V2_PERIMETER_CLASSIC_SMOKE_COMMAND_FAILED`
  - Trigger: perimeter classic smoke script exits non-zero.
  - Behavior: PowerShell wrapper failure with exit code.

## Warning Classes (report-level)

- `layer_<idx>:island_<idx>:<role>:shell_<idx>:offset_failed`
- `perimeter_classic:fallback_without_islands`


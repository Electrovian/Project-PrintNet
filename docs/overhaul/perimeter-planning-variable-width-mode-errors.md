# Perimeter Planning Variable-Width Mode Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T184`

## Error Classes

- `PERIMETER_VARIABLE_COUNT_INVALID`
  - Trigger: requested perimeter count `< 1`.
  - Behavior: raises `SlicerV2PerimeterVariableError`.

- `PERIMETER_VARIABLE_COUNT_EXCESSIVE`
  - Trigger: requested perimeter count exceeds safety cap (`> 20`).
  - Behavior: raises `SlicerV2PerimeterVariableError`.

- `PERIMETER_VARIABLE_MIN_WIDTH_INVALID`
  - Trigger: invalid minimum width (`<= 0`).
  - Behavior: raises `SlicerV2PerimeterVariableError`.

- `PERIMETER_VARIABLE_MAX_WIDTH_INVALID`
  - Trigger: invalid maximum width (`<= 0`).
  - Behavior: raises `SlicerV2PerimeterVariableError`.

- `PERIMETER_VARIABLE_WIDTH_RANGE_INVALID`
  - Trigger: `max_width < min_width`.
  - Behavior: raises `SlicerV2PerimeterVariableError`.

- `PERIMETER_VARIABLE_BASE_WIDTH_INVALID`
  - Trigger: invalid base width (`<= 0`).
  - Behavior: raises `SlicerV2PerimeterVariableError`.

- `PERIMETER_VARIABLE_WALL_SEQUENCE_INVALID`
  - Trigger: unsupported wall sequence value.
  - Behavior: raises `SlicerV2PerimeterVariableError`.

- `PERIMETER_VARIABLE_ROLE_INVALID`
  - Trigger: unsupported loop role value.
  - Behavior: raises `SlicerV2PerimeterVariableError`.

- `PERIMETER_VARIABLE_LAYER_GRAPH_INVALID`
  - Trigger: non-`LayerIslandGraph` input object.
  - Behavior: raises `SlicerV2PerimeterVariableError`.

- `SLICER_V2_PERIMETER_VARIABLE_SMOKE_COMMAND_FAILED`
  - Trigger: variable-width smoke command exits non-zero.
  - Behavior: PowerShell wrapper failure with exit code.

## Warning Classes (report-level)

- `layer_<idx>:island_<idx>:<role>:shell_<idx>:offset_failed`
- `perimeter_variable:fallback_without_islands`


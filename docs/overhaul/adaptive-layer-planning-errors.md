# Adaptive Layer Planning Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T154`

## Error Classes

- `ADAPTIVE_LAYER_SETTINGS_NOT_DICT`
  - Trigger: planner input settings are not a dictionary.
  - Behavior: raises `SlicerV2AdaptiveLayerError`.

- `ADAPTIVE_LAYER_MAX_COUNT_INVALID`
  - Trigger: invalid `max_layer_count` argument (`< 1`).
  - Behavior: raises `SlicerV2AdaptiveLayerError`.

- `ADAPTIVE_LAYER_BASE_HEIGHT_INVALID`
  - Trigger: `layer_height` is non-positive after normalization.
  - Behavior: raises `SlicerV2AdaptiveLayerError`.

- `ADAPTIVE_LAYER_INVALID_Z_BOUNDS`
  - Trigger: invalid layer bounds where end Z cannot be resolved above start Z.
  - Behavior: raises `SlicerV2AdaptiveLayerError`.

- `ADAPTIVE_LAYER_MIN_MAX_NON_POSITIVE`
  - Trigger: adaptive min/max layer heights are non-positive.
  - Behavior: raises `SlicerV2AdaptiveLayerError`.

- `ADAPTIVE_LAYER_MIN_GREATER_THAN_MAX`
  - Trigger: adaptive min height exceeds adaptive max height.
  - Behavior: raises `SlicerV2AdaptiveLayerError`.

- `ADAPTIVE_LAYER_TARGET_NON_POSITIVE`
  - Trigger: derived target layer height becomes non-positive during planning.
  - Behavior: raises `SlicerV2AdaptiveLayerError`.

- `ADAPTIVE_LAYER_MAX_COUNT_EXCEEDED`
  - Trigger: planner reaches `max_layer_count` before covering model height.
  - Behavior: raises `SlicerV2AdaptiveLayerError`.

- `ADAPTIVE_LAYER_CLOSURE_INVALID`
  - Trigger: final closure correction would create invalid final layer height.
  - Behavior: raises `SlicerV2AdaptiveLayerError`.

- `SLICER_V2_ADAPTIVE_LAYER_SMOKE_COMMAND_FAILED`
  - Trigger: adaptive smoke wrapper returns non-zero.
  - Behavior: PowerShell wrapper failure with exit code.

## Warning Classes (report-level)

- `adaptive_layer_ranges:invalid_json`
- `adaptive_layer_ranges:not_list`
- `adaptive_layer_ranges[<idx>]:invalid_item`
- `adaptive_layer_ranges[<idx>]:invalid_z_window`
- `adaptive_layer_ranges[<idx>]:invalid_layer_height`


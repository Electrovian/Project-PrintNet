# Infill Planning Patterns Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T194`

## Error Classes

- `INFILL_PATTERN_UNSUPPORTED`
  - Trigger: infill pattern is not supported by the planner.
  - Behavior: raises `SlicerV2InfillPatternError`.

- `INFILL_PERCENT_NEGATIVE`
  - Trigger: infill percent is below `0`.
  - Behavior: raises `SlicerV2InfillPatternError`.

- `INFILL_PERCENT_EXCESSIVE`
  - Trigger: infill percent exceeds `100`.
  - Behavior: raises `SlicerV2InfillPatternError`.

- `INFILL_EXTRUSION_WIDTH_INVALID`
  - Trigger: non-positive extrusion width.
  - Behavior: raises `SlicerV2InfillPatternError`.

- `INFILL_LAYER_GRAPH_INVALID`
  - Trigger: invalid non-`LayerIslandGraph` input object.
  - Behavior: raises `SlicerV2InfillPatternError`.

- `SLICER_V2_INFILL_PATTERNS_SMOKE_COMMAND_FAILED`
  - Trigger: infill smoke command exits non-zero.
  - Behavior: PowerShell wrapper failure with exit code.

## Warning Classes (report-level)

- `infill_pattern:triangle_delegated_to_grid`
- `layer_<idx>:island_<idx>:degenerate_bounds`
- `infill_patterns:fallback_without_islands`


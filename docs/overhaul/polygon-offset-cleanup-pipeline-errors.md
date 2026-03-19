# Polygon Offset and Cleanup Pipeline Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T134`

## Error Classes

- `MIN_AREA_NEGATIVE`
  - Trigger: `min_area` less than zero.
  - Behavior: raises `SlicerV2PolygonPipelineError`.

- `EDGE_LENGTH_ZERO`
  - Trigger: offset stage encounters zero-length edge.
  - Behavior: raises `SlicerV2PolygonPipelineError`.

- `STRICT_POLYGON_PIPELINE_WARNING_FAILURE`
  - Trigger: strict mode enabled and warnings exist.
  - Behavior: raises `SlicerV2PolygonPipelineError`.

- `SLICER_V2_POLYGON_OFFSET_SMOKE_COMMAND_FAILED`
  - Trigger: smoke wrapper returns non-zero.
  - Behavior: PowerShell wrapper failure with exit code.

## Warning Classes (non-strict mode)

- `dropped_in_cleanup:<count>`
- `dropped_in_offset:<count>`

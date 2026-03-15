# Mesh Slicing and Contour Assembly Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T144`

## Error Classes

- `MESH_PATH_MISSING`
  - Trigger: mesh file path not found.
  - Behavior: raises `SlicerV2MeshSlicingError`.

- `MESH_PATH_NOT_FILE`
  - Trigger: mesh path exists but is not a file.
  - Behavior: raises `SlicerV2MeshSlicingError`.

- `MESH_FILE_EMPTY`
  - Trigger: mesh file has zero bytes.
  - Behavior: raises `SlicerV2MeshSlicingError`.

- `TRIANGLE_COUNT_TOO_LARGE`
  - Trigger: binary STL triangle count exceeds safety threshold.
  - Behavior: raises `SlicerV2MeshSlicingError`.

- `BINARY_STL_TRUNCATED`
  - Trigger: binary STL byte stream shorter than declared triangle payload.
  - Behavior: raises `SlicerV2MeshSlicingError`.

- `MESH_TRIANGLES_NOT_FOUND`
  - Trigger: no valid triangles parsed from ASCII or binary reader.
  - Behavior: raises `SlicerV2MeshSlicingError`.

- `MESH_Z_BOUNDS_INVALID`
  - Trigger: invalid z bound ordering after parse.
  - Behavior: raises `SlicerV2MeshSlicingError`.

- `SLICER_V2_MESH_SLICING_SMOKE_COMMAND_FAILED`
  - Trigger: smoke wrapper returns non-zero.
  - Behavior: PowerShell wrapper failure with exit code.

## Warning Classes (report-level)

- `layer_<idx>:segments_without_contours:<count>`

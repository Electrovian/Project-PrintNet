# Mesh Slicing and Contour Assembly Contract

Date: 2026-02-13  
Checklist ID: `T142`

## Core Module

- `App/slicer_v2/mesh_slicing.py`

Primary types:

- `Point3`
- `MeshData`
- `LayerContourSet`
- `MeshSlicingReport`

Primary APIs:

- `load_mesh_file(mesh_path) -> MeshData`
- `slice_triangle_at_z(triangle, z_height, tolerance=1e-6) -> Segment2 | None`
- `slice_mesh_at_z(mesh, z_height, tolerance=1e-6) -> list[Segment2]`
- `assemble_contours_from_segments(segments, join_tolerance=1e-4, min_area=1e-6) -> list[Polygon]`
- `slice_mesh_to_contours(mesh, layer_z_values, join_tolerance=1e-4, min_area=1e-6) -> (list[LayerContourSet], MeshSlicingReport)`

## Stage Integration Contract

- `App/slicer_v2/mesh.py`
  - loads mesh and stores `mesh_data`, triangle count, and z-bounds.
- `App/slicer_v2/slice_grid.py`
  - derives layer z values from mesh z-range when available.
- `App/slicer_v2/regions.py`
  - slices mesh across layer z values and emits contour/segment counts.

## Script Contract

- `scripts/run-slicer-v2-mesh-slicing-smoke.ps1`
- `scripts/test-slicer-v2-mesh-slicing-unit.ps1`
- `scripts/test-slicer-v2-mesh-slicing-integration.ps1`

Outputs:

- `docs/_slicer_v2_mesh_slicing_report*.json`
- `docs/_slicer_v2_mesh_slicing_summary*.txt`

# geometry.py

Geometric helper utilities.

For now this is intentionally tiny. As you extend the slicer, this is
where you can put plane/triangle intersections, polygon offset
operations, etc.

## Functions

### `_points_close(a, b, tol=...)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_geometry_helpers.py`

### `_dedupe_points(points)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_geometry_helpers.py`

### `_normalize_polygon(polygon)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_geometry_helpers.py`

### `_close_polygon(points)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_geometry_helpers.py`

### `_polygon_area(points)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_geometry_clip.py`
- `App\Tests\test_geometry_helpers.py`
- `App\slicer\slicer.py`

### `_require_pyclipper()`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `_polygon_perimeter(points)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_geometry_helpers.py`

### `_polygon_centroid(points)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_geometry_helpers.py`
- `App\gui\widgets\view_cube_overlay.py`

### `_is_circular_polygon(points, circularity_threshold, radius_variation)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_geometry_helpers.py`

### `_is_clockwise(points)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_geometry_helpers.py`

### `lowest_planar_face(vertices, faces, up_axis=..., normal_threshold=...)`
Return (normal, centroid) for the lowest mostly-planar face.

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_geometry.py`
- `App\gui\viewer_3d.py`

### `arrange_rectangles(sizes, spacing, align_y=...)`
Arrange rectangles (id, width, depth) with spacing and center the layout.

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_geometry.py`
- `App\gui\viewer_3d.py`

### `_clean_loop(points)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `_simplify_polygon(polygon, tolerance)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `clean_polygons(polygons, tolerance=...)`
Clean and simplify polygons, splitting self-intersections when possible.

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_geometry.py`

### `ensure_winding(polygon, clockwise)`
Return a closed polygon with a consistent winding direction.

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_geometry.py`
- `App\slicer\slicer.py`

### `_to_clip_path(points)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `_from_clip_path(path)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `slice_mesh(mesh, z_height, tolerance=...)`
Slice a mesh at a Z plane and return closed 2D loops in XY.

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\slicer\mesh.py`

### `polygons_with_holes(polygons)`
Group loops into islands with holes using nesting.

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_bridge.py`
- `App\Tests\test_geometry.py`
- `App\Tests\test_geometry_clip.py`
- `App\Tests\test_infill.py`
- `App\Tests\test_infill_extra.py`
- `App\Tests\test_path_planner.py`
- `App\Tests\test_support_extra.py`
- `App\slicer\mesh.py`
- `App\slicer\support.py`

### `islands_difference(subject, clip)`
Return subject islands with clip islands removed.

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\slicer\path_planner.py`

### `_islands_to_paths(islands)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `_polytree_to_islands(tree)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `offset_islands(islands, distance)`
Offset island polygons (outer + holes) by a signed distance.

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_geometry.py`
- `App\slicer\slicer.py`
- `App\slicer\support.py`

### `offset_polygon(polygon, distance)`
Offset a polygon by a signed distance, returning zero or more polygons.

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_geometry_clip.py`

### `clip_lines_to_polygon(lines, polygon)`
Clip line segments to a polygon boundary.

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_geometry_clip.py`

### `clip_lines_to_island(lines, outer, holes)`
Clip line segments to an island (outer polygon with holes).

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\slicer\infill.py`

### `_clip_lines_to_paths(lines, paths)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `point_in_polygon(point, polygon)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_geometry_clip.py`
- `App\slicer\support.py`

### `point_in_island(point, island)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_geometry_clip.py`
- `App\Tests\test_path_planner.py`
- `App\slicer\path_planner.py`
- `App\slicer\slicer.py`

### `line_inside_island(segment, island, samples=...)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_geometry_clip.py`
- `App\slicer\path_planner.py`

### `path_inside_island(points, island, samples=...)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\slicer\path_planner.py`

### `_loops_to_lines(loops)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `thin_wall_lines(islands, extrusion_width)`
Approximate thin walls as centerline paths.

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_geometry.py`
- `App\slicer\slicer.py`

### `gap_fill_lines(islands, extrusion_width, perimeter_spacing)`
Detect narrow gaps between perimeters and return fill lines.

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_geometry.py`
- `App\slicer\slicer.py`

### `_best_offset_loops(polygon, distance)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `compensate_holes(islands, compensation_mm, circularity_threshold=..., radius_variation=...)`
Expand circular holes to compensate for shrinkage.

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_geometry.py`
- `App\slicer\slicer.py`

### `compute_bounding_square(bounds)`
Return a simple XY square that covers the mesh bounds.

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_geometry_helpers.py`

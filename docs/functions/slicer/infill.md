# infill.py

Infill pattern generation.

## Functions

### `_rotate_point(point, angle_rad)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `_rotate_points(points, angle_rad)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `_rotate_lines(lines, angle_rad)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `_bounds(points)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `_line_spacing(density, extrusion_width, directions)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_infill_extra.py`

### `_generate_parallel_lines(polygon, spacing, angle_deg)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `rectilinear_infill(islands, density, angle_deg, layer_index, extrusion_width, alternate=...)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\slicer\path_planner.py`
- `App\slicer\slicer.py`
- `App\slicer\support.py`

### `grid_infill(islands, density, angle_deg, layer_index, extrusion_width, alternate=...)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_infill_extra.py`

### `triangle_infill(islands, density, angle_deg, layer_index, extrusion_width, alternate=...)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `generate_infill(islands, density, angle_deg, layer_index, extrusion_width, pattern=..., alternate=...)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_infill.py`
- `App\Tests\test_infill_extra.py`
- `App\slicer\slicer.py`

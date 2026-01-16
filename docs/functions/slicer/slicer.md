# slicer.py

## Classes

### IslandPerimeters

_No public methods documented._

### PerimeterShell

_No public methods documented._

### LayerPerimeters

_No public methods documented._

### LayerInfill

_No public methods documented._

### IroningPass

_No public methods documented._

### BridgeInfill

_No public methods documented._

### BrimPlan

_No public methods documented._

### SkirtPlan

_No public methods documented._

### RaftLayer

_No public methods documented._

### LayerPlan

_No public methods documented._

### PrintPlan

_No public methods documented._

## Functions

### `_wrap_islands(islands)`

Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:

- `App\Tests\test_slicer_helpers.py`

### `_polygon_area(points)`

Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:

- `App\Tests\test_geometry_clip.py`
- `App\Tests\test_geometry_helpers.py`
- `App\slicer\geometry.py`

### `_island_area(island)`

Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `_holes_as_islands(islands)`

Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `_close_gap_islands(islands, radius)`

Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `_wall_spacing(settings, layer_index)`

Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `_thin_wall_width(settings, layer_index)`

Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `_filter_thin_walls(lines, settings)`

Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `_offset_holes(islands, delta)`

Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `_polyhole_for_polygon(polygon, nozzle)`

Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `_convert_holes_to_polyholes(islands, nozzle)`

Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `_normalize_height_ranges(ranges)`

Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:

- `App\Tests\test_slicer_helpers.py`

### `build_z_heights(mesh, settings)`

Generate variable Z heights using manual ranges and overhang data.

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:

- `App\Tests\test_slicer.py`
- `App\Tests\test_slicer_helpers.py`

### `generate_layer_perimeters(mesh, z_heights, settings=..., perimeter_count=..., perimeter_spacing=...)`

Return per-layer perimeter shells with islands and holes grouped.

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:

- `App\Tests\test_slicer.py`

### `_shells_to_islands(shell)`

Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `generate_layer_plans(mesh, z_heights=..., settings=..., perimeter_count=..., perimeter_spacing=...)`

Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:

- `App\Tests\test_slicer.py`

### `_emit_gcode(plan, output_gcode_path, settings)`

Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `slice_mesh_model(mesh, output_gcode_path=..., settings=..., source_path=...)`

Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `slice_trimesh(mesh, output_gcode_path=..., settings=..., source_path=...)`

Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:

- `App\gui\Windows\controller\print.py`

### `slice_file(stl_path, output_gcode_path=..., settings=...)`

Slice an STL into multi-layer toolpaths and emit G-code.

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:

- `App\integrations\printer_manager.py`

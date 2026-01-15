# path_planner.py

Path planning helpers.

## Classes

### Toolpath
#### Methods

- `start(self)`
- `end(self)`

### BridgeRegion
_No public methods documented._

### ArcFit
_No public methods documented._

## Functions

### `_circle_from_points(p1, p2, p3)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_path_planner_extra.py`

### `fit_arc(points, tolerance=..., require_closed=...)`
Detect circular paths and return an arc fit if points are near a circle.

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_path_planner_extra.py`
- `App\slicer\gcode.py`

### `apply_seam_placement(loop, mode, anchor=..., rear_angle=..., rng=...)`
Return a closed loop reordered to match the requested seam placement.

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_path_planner.py`
- `App\Tests\test_path_planner_extra.py`
- `App\slicer\slicer.py`

### `comb_travel(start, end, island)`
Route travel inside an island when possible.

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_path_planner.py`

### `plan_travel(start, end, retracted, z_hop_height, comb_island=..., z_hop_only_outside=...)`
Return travel points with optional combing and Z-hop.

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_path_planner.py`
- `App\slicer\slicer.py`

### `order_islands_nearest(islands, start)`
Order islands by nearest neighbor using centroids.

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_path_planner.py`

### `order_toolpaths(toolpaths, start=...)`
Order toolpaths by nearest neighbor, keeping perimeters before infill.

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_path_planner.py`

### `plan_sequential_print(object_bounds, nozzle_clearance, max_height=...)`
Plan by-object printing order and warn if clearance is unsafe.

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `_bounds_overlap_xy(bounds_a, bounds_b)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `detect_bridge_islands(current, below)`
Return regions on the current layer lacking support below.

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_bridge.py`
- `App\slicer\slicer.py`

### `bridge_direction(island)`
Compute a bridge direction aligned with the shortest span.

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\Tests\test_bridge.py`

### `generate_bridge_infill(islands, layer_index, extrusion_width, density=...)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by:
- `App\slicer\slicer.py`

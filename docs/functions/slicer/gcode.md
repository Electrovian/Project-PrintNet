# gcode.py

## Classes

### FirmwareProfile
_No public methods documented._

### SliceSettings
_No public methods documented._

### GCodeWriter
#### Methods

- `add(self, line)`
- `write_header(self)`
- `write_footer(self)`
- `move_travel(self, x, y, z, f)`
- `move_wipe(self, x, y, z, speed)`
- `move_extrude(self, x, y, z, speed, extrusion)`
- `move_arc_extrude(self, x, y, z, speed, extrusion, center_xy, clockwise)`
- `retract(self)`
- `unretract(self)`
- `extrusion_for_length(self, length, width=..., multiplier=...)`
- `perimeter_loop(self, points, z, speed, width=..., multiplier=..., seam_gap=..., wipe_distance=..., wipe_speed=...)`
- `extrude_lines(self, lines, z, speed, width=..., multiplier=...)`
- `get_gcode(self)`

### PreviewSegment
_No public methods documented._

### PreviewFeatureGroup
_No public methods documented._

### PreviewLayer
_No public methods documented._

### GCodePreview
_No public methods documented._

## Functions

### `_normalize_gcode_lines(value)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `get_firmware_profile(name)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `_arc_center_from_radius(start, end, radius, clockwise)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `_arc_delta(start, end, center, clockwise)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `_arc_points(start, end, center, clockwise, segments)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `parse_gcode_preview(lines, settings=...)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `parse_gcode_preview_file(path, settings=...)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `_format_duration(seconds)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `estimate_gcode_stats(lines, settings)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `estimate_gcode_file(path, settings)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `_tower_square(size, center=...)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `generate_temperature_tower(settings, start_temp, end_temp, step, block_height=..., tower_size=...)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `generate_retraction_tower(settings, start_distance, end_distance, step, block_height=..., tower_size=...)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `generate_pressure_advance_pattern(settings, start_value, end_value, step, line_length=..., line_count=..., spacing=...)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

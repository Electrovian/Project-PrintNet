# mesh.py

## Classes

### MeshModel
Simple wrapper around a trimesh mesh.

#### Methods

- `from_file(cls, path)`
- `from_trimesh(cls, mesh, path=...)`
- `bounds(self)`
- `overhang_face_indices(self, overhang_angle)`
- `overhang_triangles(self, overhang_angle)`
- `slice_layer(self, z_height, tolerance=...)`
- `slice_layers(self, z_heights, tolerance=...)`
- `set_slice_cache_limit(self, max_mb)`
- `clear_slice_cache(self)`

## Functions

### `_estimate_islands_bytes(islands)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

### `_apply_default_cache_limit(model)`
Summary: TODO

Inputs: TODO

Outputs: TODO

Processing: TODO

Used by: TODO

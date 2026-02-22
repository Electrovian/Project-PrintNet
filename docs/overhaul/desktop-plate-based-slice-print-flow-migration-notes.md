# Desktop Plate-Based Slice/Print Flow Migration Notes

Date: 2026-02-13  
Checklist ID: `T269`

## Legacy Baseline

- `print_current_model()` and `export_gcode()` were selected-model oriented.
- Device send reused `_last_gcode_path` based only on file existence.

## Current Baseline

- Plate-first APIs are now explicit: `slice_current_plate()` and `print_current_plate()`.
- Legacy methods are compatibility wrappers to plate APIs.
- `export_gcode()` now slices plate meshes via `slice_trimesh_auto(...)`.
- Device send reuses cache only when signature + file checks pass.

## Migration Impact

- Existing UI triggers continue to work through compatibility wrappers.
- Cached G-code reuse is stricter; stale signatures now force re-slice path.
- Export filenames are more deterministic for multi-model plates.

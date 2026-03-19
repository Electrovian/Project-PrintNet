# Desktop Plate-Based Slice/Print Flow Contract

Date: 2026-02-13  
Checklist ID: `T262`

## Core Modules

- `App/gui/Windows/controller/print.py`
  - `slice_current_plate()`
  - `print_current_plate(printer=None)`
  - compatibility wrappers:
    - `slice_current_model() -> slice_current_plate()`
    - `print_current_model(printer=None) -> print_current_plate(printer)`
  - cache/signature helpers:
    - `_resolve_reusable_gcode_path(settings) -> str | None`
    - `_default_plate_gcode_basename()`
    - `_default_plate_gcode_path()`

## UI Trigger Contract

- `App/gui/Windows/prepare.py`
- `App/gui/Windows/preview.py`
- `App/gui/Windows/shared_view.py`

Each trigger resolves `slice_current_plate` first, with fallback to `slice_current_model` for compatibility.

## Device Send Contract

- `_on_device_send_requested(printer)` must:
  - try reusable path from `_resolve_reusable_gcode_path(settings)`
  - call `_send_existing_gcode(printer, path)` when valid
  - otherwise call `print_current_plate(printer=printer)`

## Export Contract

- `export_gcode()` slices the full plate using `slice_trimesh_auto(...)`.
- Suggested filename uses deterministic plate basename with `_plate` suffix for multi-model plates.

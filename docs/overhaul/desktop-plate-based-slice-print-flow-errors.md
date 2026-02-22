# Desktop Plate-Based Slice/Print Flow Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T264`

## Guard/Error Cases

- `NO_PLATE_MODELS`
  - Trigger: no models loaded on plate for slice/print/export.
  - Handling: show "No model" warning with `Load model(s) first.`

- `PLATE_DATA_UNAVAILABLE`
  - Trigger: model IDs exist but mesh data could not be assembled.
  - Handling: show "No model" warning with `Model data unavailable for slicing.`

- `REUSABLE_GCODE_CACHE_MISS`
  - Trigger: `_last_gcode_path` missing, file does not exist, or signature mismatch.
  - Handling: do not send cached file; fall back to `print_current_plate(...)`.

- `REUSABLE_GCODE_PATH_INVALID`
  - Trigger: `_send_existing_gcode` receives missing/nonexistent file.
  - Handling: show warning and abort send action.

- `SLICE_OR_PRINT_WORKER_FAILURE`
  - Trigger: worker error from `slice_trimesh_auto` or printer upload/send call.
  - Handling: close dialog, update status, show critical message box.

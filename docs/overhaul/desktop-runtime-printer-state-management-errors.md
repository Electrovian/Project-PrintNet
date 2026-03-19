# Desktop Runtime Printer State Management Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T274`

## Guard/Error Cases

- `RUNTIME_STATE_MISSING`
  - Trigger: runtime state is unavailable when bed limits are requested.
  - Handling: reconstruct from `DEFAULTS["printer"]`.

- `PRINTER_PROFILE_MISSING`
  - Trigger: printer profile selection callback receives `None`.
  - Handling: ignore update, retain current runtime state.

- `PRINTER_DIMENSION_INVALID`
  - Trigger: `bed_x`, `bed_y`, or `bed_z` is non-numeric, non-finite, or out of minimum bounds.
  - Handling: fall back to previous runtime dimension.

- `PRINTER_DIMENSION_EXCESSIVE`
  - Trigger: provided dimension exceeds maximum accepted bound.
  - Handling: clamp to bounded maximum.

- `VIEWER_BED_LIMIT_APPLY_FAILED`
  - Trigger: viewer object missing or does not expose `set_bed_limits`.
  - Handling: skip viewer update without crashing; keep runtime state updated.

# Desktop Plate-Based Slice/Print Flow Requirements

Date: 2026-02-13  
Checklist ID: `T261`

## Objective

Make desktop slicing/export/print operations plate-first, so all operations use current plate content (not selected-model-only paths).

## Required Outcomes

- Introduce explicit plate APIs: `slice_current_plate()` and `print_current_plate()`.
- Keep compatibility wrappers for existing call sites (`slice_current_model`, `print_current_model`).
- Reuse cached G-code only when file exists and plate/settings signature matches.
- Device send flow must share the same plate validation and fallback pipeline.
- Export path naming should be deterministic for multi-model plates.

## Acceptance Criteria

- Slice/print/export on desktop operate on full plate geometry.
- Device send uses cached plate G-code only when valid.
- Stale/missing cache falls back to re-slice print path.
- Unit/integration/performance checks pass within runtime budget.
- Usage/defaults, migration notes, and completion gate docs are published.

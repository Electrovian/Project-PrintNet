# Desktop Runtime Printer State Management Migration Notes

Date: 2026-02-13  
Checklist ID: `T279`

## Legacy Baseline

- Printer profile changes mutated global `DEFAULTS["printer"]`.
- Bed warnings and viewer limits depended directly on global defaults.
- Default printer selection in UI views came from global defaults only.

## Current Baseline

- Runtime state is initialized once and updated per active printer selection.
- `_apply_printer_profile(...)` updates runtime state and viewer bed limits without global default mutation.
- Bed warning logic and printer pickers resolve from runtime state first.

## Migration Impact

- Lower cross-view side effects from printer switches.
- Printer selection state is session-local and safer for multi-view workflows.
- Existing defaults remain as fallback baseline for startup and guard paths.

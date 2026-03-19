# Desktop Runtime Printer State Management Contract

Date: 2026-02-13  
Checklist ID: `T272`

## Core Modules

- `App/config/runtime_printer_state.py`
  - `RuntimePrinterState`
  - `runtime_printer_state_from_defaults(printer_defaults)`
  - `runtime_printer_state_from_profile(printer, fallback_state, source)`
- `App/gui/Windows/controller/core.py`
  - initializes `self.runtime_printer_state`
  - applies runtime bed limits at startup
- `App/gui/Windows/controller/ui.py`
  - `_effective_bed_limits()`
  - `_apply_printer_profile(printer, source)`
  - `_sync_printer_selection(printer, source)`

## Runtime State Contract

- `RuntimePrinterState.name`: active printer display name.
- `RuntimePrinterState.bed_x`, `bed_y`, `bed_z`: active build volume in mm.
- `RuntimePrinterState.source`: source tag (`defaults`, `device`, `control`, `settings`, `preview`, `initialize`).
- `RuntimePrinterState.updated_at_utc`: ISO-8601 UTC timestamp of last update.

## UI Resolution Contract

- Bed checks and viewer limits resolve from `runtime_printer_state` first.
- If runtime state is unavailable, fall back to `DEFAULTS["printer"]`.
- Printer list defaults in Device/Control/Settings/Preview prefer `runtime_printer_state.name`.

## Mutation Contract

- Applying a runtime printer profile must not mutate `DEFAULTS["printer"]`.
- Runtime updates are local to app session unless persisted by explicit settings save flow.

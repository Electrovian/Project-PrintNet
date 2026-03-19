# Desktop Runtime Printer State Management Requirements

Date: 2026-02-13  
Checklist ID: `T271`

## Objective

Replace desktop global printer-default mutation with runtime printer state so active printer limits are scoped, deterministic, and reversible.

## Required Outcomes

- Introduce runtime state model for active printer name and bed limits.
- Initialize runtime state from defaults on controller startup.
- Apply selected printer profiles into runtime state instead of mutating `DEFAULTS["printer"]`.
- Ensure bed warnings and viewer bed limits resolve from runtime state first.
- Ensure device/control/settings/preview printer selectors use runtime state as default selection.

## Acceptance Criteria

- Runtime state exists and is used by desktop controller and UI flow.
- Applying a printer profile leaves `DEFAULTS["printer"]` unchanged.
- Bed limits update visually when active printer changes.
- Unit/integration/performance checks pass within runtime budget.
- Usage/defaults, migration notes, and completion gate docs are published.

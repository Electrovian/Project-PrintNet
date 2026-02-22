# Desktop Runtime Printer State Management Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T278`

## Run Smoke

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-desktop-runtime-printer-state-smoke.ps1
```

## Run Unit and Integration Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-desktop-runtime-printer-state-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-desktop-runtime-printer-state-integration.ps1
```

## Defaults

- Runtime source bootstrap: `runtime_printer_state_from_defaults(DEFAULTS["printer"])`.
- Bed limit precedence: runtime state first, then `DEFAULTS["printer"]` fallback.
- Numeric bounds:
  - minimum dimension: `1.0 mm`
  - maximum dimension: `10000.0 mm`
- Runtime printer source tags: `defaults`, `initialize`, `device`, `control`, `settings`, `preview`.

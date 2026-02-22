# Moonraker Connector Operations Migration Notes

Date: 2026-02-13  
Checklist ID: `T309`

## Legacy Baseline

- No dedicated Moonraker connector implementation existed.
- Printer dispatch paths were effectively OctoPrint-focused.

## Current Baseline

- `MoonrakerConnector` now provides typed connector methods for connect/upload/start/control/status.
- Default registry resolves Moonraker metadata to connector type `moonraker`.
- Printer manager remains protocol-neutral and dispatches by registry resolution.

## Migration Impact

- Printers with `moonraker_url` can be routed without changing desktop print manager call sites.
- Existing OctoPrint and local connector flows remain intact.
- Connector-specific operations can now evolve independently in future workstreams.

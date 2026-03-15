# PrusaLink Connector Operations Migration Notes

Date: 2026-02-13  
Checklist ID: `T319`

## Legacy Baseline

- No dedicated PrusaLink connector implementation existed.
- Printer dispatch paths were centered on local and OctoPrint-oriented connectors.

## Current Baseline

- `PrusaLinkConnector` now provides typed connector methods for connect/upload/start/control/status.
- Default registry resolves PrusaLink metadata to connector type `prusalink`.
- Printer manager remains protocol-neutral and dispatches by registry resolution.

## Migration Impact

- Printers with `prusalink_url` and `prusalink_api_key` route through PrusaLink connector without call-site changes.
- Existing local, OctoPrint, and Moonraker flows remain intact.
- Future PrusaLink feature growth is isolated to connector module without manager rewrites.

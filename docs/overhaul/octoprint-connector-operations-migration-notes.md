# OctoPrint Connector Operations Migration Notes

Date: 2026-02-13  
Checklist ID: `T299`

## Legacy Baseline

- OctoPrint print dispatch was handled by a single helper call (`upload_and_print`) with no explicit connector operation contract.
- Pause/resume/cancel/status were not available through connector abstraction.

## Current Baseline

- `OctoPrintConnector` now provides typed connector methods for connect/upload/start/control/status.
- Default registry resolves OctoPrint metadata to connector type `octoprint`.
- Printer manager validates connector readiness before upload and start operations.

## Migration Impact

- Existing printers with OctoPrint metadata route through `octoprint` by default.
- `octoprint_legacy` connector remains available for explicit compatibility pinning.
- Desktop print flow now has clearer separation between connector readiness and execution failures.

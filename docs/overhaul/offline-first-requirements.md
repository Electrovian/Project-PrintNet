# Offline-First Runtime Requirements

## Hard Requirement
After installation, core desktop slicing and local printer workflows must work without internet access.

## Must Work Offline
- Load STL/3MF and manage project files.
- Slice models and generate G-code locally.
- Import/use local printer profile catalog.
- Connect to local-network printers (OctoPrint/Moonraker/PrusaLink) by IP/hostname.
- Queue and send print jobs on LAN.

## Must Not Be Required for Core Flow
- Cloud auth checks.
- Remote telemetry dependency.
- Remote configuration fetches.

## Packaging Requirements
- Bundle all runtime dependencies required for local execution.
- Ship default local config templates in installer/package.
- Ship fallback local mode for backend/web stack when internet is unavailable.

## Validation Gate
- Run a no-internet smoke test before release:
  1. Disable network egress.
  2. Launch app.
  3. Slice a sample model.
  4. Send to a local printer endpoint simulator.
  5. Confirm completion and status updates.

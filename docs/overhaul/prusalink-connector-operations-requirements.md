# PrusaLink Connector Operations Requirements

Date: 2026-02-13  
Checklist ID: `T311`

## Objective

Implement a first-class PrusaLink connector that supports health checks and runtime print control operations through PrusaLink HTTP API endpoints.

## Required Outcomes

- Add `PrusaLinkConnector` with typed operations:
  - `connect`
  - `upload`
  - `start_print`
  - `pause`
  - `resume`
  - `cancel`
  - `status`
- Register the connector in default connector registry and infer it from PrusaLink metadata.
- Keep desktop print manager protocol-neutral by dispatching through connector registry.

## Acceptance Criteria

- PrusaLink connector exists as a concrete `PrinterConnector` implementation.
- Connector registry includes `prusalink` in default set and resolves PrusaLink printers correctly.
- Unit and integration checks pass within runtime budget.
- Usage/defaults, migration notes, and completion gate docs are published.

# Moonraker Connector Operations Requirements

Date: 2026-02-13  
Checklist ID: `T301`

## Objective

Implement a first-class Moonraker connector that supports health checks and runtime print control operations through Moonraker HTTP API endpoints.

## Required Outcomes

- Add `MoonrakerConnector` with typed operations:
  - `connect`
  - `upload`
  - `start_print`
  - `pause`
  - `resume`
  - `cancel`
  - `status`
- Register the connector in default connector registry and infer it from Moonraker metadata.
- Keep desktop print manager protocol-neutral by dispatching through the connector registry.

## Acceptance Criteria

- Moonraker connector exists as a concrete `PrinterConnector` implementation.
- Connector registry includes `moonraker` in default set and resolves Moonraker printers correctly.
- Unit and integration checks pass within runtime budget.
- Usage/defaults, migration notes, and completion gate docs are published.

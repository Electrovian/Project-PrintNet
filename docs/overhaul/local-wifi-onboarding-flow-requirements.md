# Local Wi-Fi Onboarding Flow Requirements

Date: 2026-02-13  
Checklist ID: `T321`

## Objective

Provide a local-network onboarding path that discovers supported printers on Wi-Fi/LAN and generates protocol-specific printer config candidates for desktop runtime use.

## Required Outcomes

- Implement deterministic local target discovery with bounded scan size.
- Detect supported protocol endpoints:
  - OctoPrint
  - Moonraker
  - PrusaLink
- Produce onboarding-ready printer candidate records with connector-specific URL/auth keys.
- Merge discovered candidates into runtime printer list without duplicate entries.

## Acceptance Criteria

- `LocalWifiOnboarding` exists and supports host-based and CIDR-based discovery.
- Discovery execution is bounded by `max_targets` and timeout controls.
- `PrinterManager` can execute onboarding and merge discovered printers in-memory.
- Unit and integration checks pass under a defined runtime budget.

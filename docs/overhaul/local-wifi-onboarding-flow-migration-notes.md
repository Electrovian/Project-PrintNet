# Local Wi-Fi Onboarding Flow Migration Notes

Date: 2026-02-13  
Checklist ID: `T329`

## Legacy Baseline

- Printer setup depended on manual entry/import of endpoint metadata.
- No bounded, protocol-aware local discovery path existed in desktop runtime.

## Current Baseline

- `LocalWifiOnboarding` provides bounded local discovery for OctoPrint, Moonraker, and PrusaLink.
- Discovery outputs protocol-specific printer candidate configs.
- `PrinterManager` can trigger host/CIDR onboarding and merge candidates into active runtime list.

## Migration Impact

- Existing manually-configured printers remain valid and are preserved during merge.
- Newly discovered printers are appended only when identity is not already present.
- Callers can move from ad-hoc network setup to repeatable, testable onboarding APIs.

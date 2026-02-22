# Printer Profile File Discovery Requirements

Date: 2026-02-13  
Checklist ID: `T051`

## Objective

Discover vendor/profile file layout from a local printer-profile source tree so later import/resolve phases can consume deterministic inputs.

## Required Outcomes

- Source-root validation and deterministic discovery ordering.
- Vendor-level file inventory for `machine`, `process`, and `filament`.
- Warning model for missing index/vendor/category paths.
- JSON and text report artifacts for diagnostics.

## Acceptance Criteria

- Discovery fails fast on invalid source paths.
- Discovery report includes counts and per-vendor records.
- Unit and integration tests pass.
- Discovery on local mirror completes within runtime budget.

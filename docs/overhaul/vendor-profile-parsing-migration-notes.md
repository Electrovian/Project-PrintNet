# Vendor Profile Parsing Migration Notes

Date: 2026-02-13  
Checklist ID: `T069`

## Legacy Baseline

- Vendor/profile JSON inspection was manual and non-deterministic.
- Type mismatches were not centrally counted.

## Current Baseline

- Parsing is centralized in `App/profiles_import/parsing.py`.
- Discovery + parsing flow is scriptable and report-driven.
- Warning and mismatch counts are explicit in outputs.

## Migration Impact

- Inheritance/merge tasks should consume parser reports rather than manual directory scans.
- Type-mismatch and missing-field warnings now provide measurable quality signals before import.

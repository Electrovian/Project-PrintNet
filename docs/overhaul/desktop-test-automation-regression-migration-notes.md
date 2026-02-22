# Desktop Test Automation and Regression Migration Notes

Date: 2026-02-13  
Checklist ID: `T339`

## Legacy Baseline

- Desktop regression checks were run ad-hoc with individual test commands.
- No single typed runner contract existed for core desktop regression case sequencing.
- Report artifacts were inconsistent across manual invocations.

## Current Baseline

- `App/testing/desktop_regression.py` defines typed regression contracts and a deterministic case runner.
- A stable default case set covers core desktop flows:
  - plate flow
  - runtime printer state
  - connector registry
  - local Wi-Fi onboarding
- Smoke run emits standardized JSON and summary artifacts.

## Migration Impact

- Existing per-module tests remain unchanged and reusable.
- Teams can run one command for a consistent regression snapshot.
- Gate decisions can consume uniform report fields (`ok`, counts, failed ids, durations).

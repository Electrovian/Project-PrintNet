# Desktop Test Automation and Regression Contract

Date: 2026-02-13  
Checklist ID: `T332`

## Core Modules

- `App/testing/desktop_regression.py`
  - `RegressionCase`
  - `RegressionRunConfig`
  - `CommandExecutionResult`
  - `RegressionCaseResult`
  - `DesktopRegressionReport`
  - `default_desktop_regression_cases()`
  - `run_regression_cases(...)`
  - `report_to_dict(...)`
  - `summarize_failures(...)`
  - `report_metadata(...)`
- `App/testing/__init__.py`
  - exports regression interfaces

## Default Case Contract

`default_desktop_regression_cases()` returns sequential regression cases:

- `desktop_plate_flow` -> `App.Tests.test_desktop_plate_flow`
- `desktop_runtime_printer_state` -> `App.Tests.test_runtime_printer_state`
- `connector_registry` -> `App.Tests.test_connector_registry`
- `local_wifi_onboarding` -> `App.Tests.test_local_wifi_onboarding`

## Execution Contract

- Each case runs with command format:
  - `python -m unittest <module...>`
- Case execution tracks:
  - `ok`
  - `exit_code`
  - `duration_s`
  - `timed_out`
  - `module_count`
  - `command`
- Report aggregates:
  - `case_count`
  - `passed_case_count`
  - `failed_case_count`
  - `total_duration_s`
  - `failed_case_ids`
  - per-case `results`

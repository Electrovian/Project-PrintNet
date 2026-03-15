# Desktop Test Automation and Regression Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T334`

## Guard/Error Cases

- `DESKTOP_REGRESSION_PYTHON_REQUIRED`
  - Trigger: `python_executable` missing/empty.
  - Handling: raise `DesktopRegressionError`.

- `DESKTOP_REGRESSION_DEFAULT_TIMEOUT_INVALID`
  - Trigger: `default_max_seconds <= 0`.
  - Handling: raise `DesktopRegressionError`.

- `DESKTOP_REGRESSION_WORKDIR_INVALID`
  - Trigger: configured working directory does not exist.
  - Handling: raise `DesktopRegressionError`.

- `DESKTOP_REGRESSION_CASES_REQUIRED`
  - Trigger: no regression cases supplied.
  - Handling: raise `DesktopRegressionError`.

- `DESKTOP_REGRESSION_CASE_ID_REQUIRED`
  - Trigger: case id missing/empty.
  - Handling: raise `DesktopRegressionError`.

- `DESKTOP_REGRESSION_DUPLICATE_CASE_ID`
  - Trigger: duplicate case id in supplied case set.
  - Handling: raise `DesktopRegressionError`.

- `DESKTOP_REGRESSION_MODULES_REQUIRED`
  - Trigger: case has no valid unittest modules.
  - Handling: raise `DesktopRegressionError`.

- `DESKTOP_REGRESSION_TIMEOUT_INVALID`
  - Trigger: case timeout resolves to non-positive.
  - Handling: raise `DesktopRegressionError`.

- Runtime timeout state
  - Trigger: subprocess execution exceeds case timeout.
  - Handling: case result marked `timed_out=true`, `exit_code=124`, and case marked failed.

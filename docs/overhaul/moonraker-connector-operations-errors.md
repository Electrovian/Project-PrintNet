# Moonraker Connector Operations Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T304`

## Guard/Error Cases

- `MOONRAKER_URL_REQUIRED`
  - Trigger: printer missing `moonraker_url` (or `klipper_url` fallback).
  - Handling: `connect(...)` returns `ok=false`; operation calls raise `InvalidPrinterConfigError`.

- `MOONRAKER_REQUEST_FAILED`
  - Trigger: request transport failure or timeout.
  - Handling: raise `ConnectorOperationError`.

- `MOONRAKER_HTTP_<status>`
  - Trigger: endpoint returns HTTP status >= 400.
  - Handling: raise `ConnectorOperationError` with response snippet.

- `GCODE_NOT_FOUND`
  - Trigger: upload path does not exist.
  - Handling: raise `ConnectorOperationError`.

- `GCODE_PATH_REQUIRED`
  - Trigger: `start_print(...)` called without `remote_path` and without `gcode_path`.
  - Handling: raise `ConnectorOperationError`.

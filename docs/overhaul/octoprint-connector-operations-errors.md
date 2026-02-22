# OctoPrint Connector Operations Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T294`

## Guard/Error Cases

- `OCTOPRINT_URL_REQUIRED`
  - Trigger: printer missing `octoprint_url`.
  - Handling: `connect(...)` returns `ok=false`; operation calls raise `InvalidPrinterConfigError`.

- `OCTOPRINT_API_KEY_REQUIRED`
  - Trigger: printer missing `octoprint_api_key`.
  - Handling: `connect(...)` returns `ok=false`; operation calls raise `InvalidPrinterConfigError`.

- `OCTOPRINT_REQUEST_FAILED`
  - Trigger: request transport failure or timeout.
  - Handling: raise `ConnectorOperationError`.

- `OCTOPRINT_HTTP_<status>`
  - Trigger: endpoint returns HTTP status >= 400.
  - Handling: raise `ConnectorOperationError` with response snippet.

- `GCODE_NOT_FOUND`
  - Trigger: upload path does not exist.
  - Handling: raise `ConnectorOperationError`.

- `GCODE_PATH_REQUIRED`
  - Trigger: `start_print(...)` called without `remote_path` and without `gcode_path`.
  - Handling: raise `ConnectorOperationError`.

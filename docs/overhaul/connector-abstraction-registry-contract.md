# Connector Abstraction and Registry Contract

Date: 2026-02-13  
Checklist ID: `T282`

## Core Modules

- `App/connectors/base.py`
  - `ConnectorCapabilities`
  - `PrinterConnector`
- `App/connectors/errors.py`
  - `ConnectorError`
  - `InvalidPrinterConfigError`
  - `UnsupportedConnectorError`
  - `ConnectorOperationError`
- `App/connectors/registry.py`
  - `ConnectorRegistry`
  - `build_default_connector_registry()`
- `App/connectors/local_file.py`
  - `LocalFileConnector`
- `App/connectors/legacy_octoprint.py`
  - `LegacyOctoPrintConnector`

## Resolution Contract

- Explicit printer fields checked first: `connector_type`, `connector`, `protocol`.
- If explicit connector field is absent:
  - resolve to `octoprint` when OctoPrint metadata is present.
  - otherwise resolve to `local_file`.

## Integration Contract

- `App/integrations/printer_manager.py` resolves connector via registry for `print_gcode(...)`.
- Print dispatch sequence:
  1. `registry.resolve(printer)`
  2. `connector.upload(printer, gcode_path)`
  3. `connector.start_print(printer, remote_path=..., gcode_path=...)`

## Compatibility Contract

- Legacy OctoPrint missing-credentials path remains non-crashing and returns a safe message.
- No internet dependency is introduced for local/offline connector flow.

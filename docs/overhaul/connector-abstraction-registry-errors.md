# Connector Abstraction and Registry Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T284`

## Guard/Error Cases

- `CONNECTOR_TYPE_INVALID`
  - Trigger: connector registration with empty connector type.
  - Handling: raise `InvalidPrinterConfigError`.

- `CONNECTOR_UNSUPPORTED`
  - Trigger: connector lookup for unknown type.
  - Handling: raise `UnsupportedConnectorError` with supported type list.

- `PRINTER_CONFIG_INVALID`
  - Trigger: connector resolution/operation called with non-mapping printer config.
  - Handling: raise `InvalidPrinterConfigError`.

- `PRINTER_NAME_REQUIRED`
  - Trigger: legacy connector printer config missing `name`.
  - Handling: raise `InvalidPrinterConfigError`.

- `GCODE_NOT_FOUND`
  - Trigger: connector upload path does not exist.
  - Handling: raise `ConnectorOperationError`.

- `GCODE_PATH_REQUIRED`
  - Trigger: connector start operation called without uploaded or explicit path.
  - Handling: raise `ConnectorOperationError`.

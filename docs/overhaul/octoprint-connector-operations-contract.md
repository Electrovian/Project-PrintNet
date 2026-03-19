# OctoPrint Connector Operations Contract

Date: 2026-02-13  
Checklist ID: `T292`

## Core Modules

- `App/connectors/octoprint.py`
  - `OctoPrintConnector`
- `App/connectors/registry.py`
  - default registry includes `OctoPrintConnector`
  - OctoPrint metadata inference resolves `octoprint`
- `App/integrations/printer_manager.py`
  - performs connector readiness check via `connect(...)`
  - dispatches upload/start print through resolved connector

## Endpoint Contract

- `GET /api/version` for connector health/readiness.
- `POST /api/files/local` for G-code upload.
- `POST /api/files/local/{path}` with `{"command":"select","print":true}` for start-print.
- `POST /api/job` for pause/resume/cancel commands.
- `GET /api/job` for print status/progress.

## Printer Metadata Contract

- Required:
  - `name`
  - `octoprint_url`
  - `octoprint_api_key`
- Optional:
  - `connector_type` (`octoprint`) for explicit protocol pinning.

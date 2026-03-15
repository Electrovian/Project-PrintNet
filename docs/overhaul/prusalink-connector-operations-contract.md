# PrusaLink Connector Operations Contract

Date: 2026-02-13  
Checklist ID: `T312`

## Core Modules

- `App/connectors/prusalink.py`
  - `PrusaLinkConnector`
- `App/connectors/registry.py`
  - default registry includes `PrusaLinkConnector`
  - PrusaLink metadata inference resolves `prusalink`
- `App/integrations/printer_manager.py`
  - connector readiness check via `connect(...)`
  - upload/start print dispatch via resolved connector

## Endpoint Contract

- `GET /api/version` for connector health/readiness.
- `POST /api/files/local` for G-code upload.
- `POST /api/files/local/{path}` with `{"command":"select","print":true}` for start-print.
- `POST /api/job` for pause/resume/cancel.
- `GET /api/job` for print status/progress.

## Printer Metadata Contract

- Required:
  - `name`
  - `prusalink_url`
  - `prusalink_api_key`
- Optional:
  - alias fields: `prusa_url`, `prusa_api_key`
  - `connector_type` (`prusalink`) for explicit protocol pinning.

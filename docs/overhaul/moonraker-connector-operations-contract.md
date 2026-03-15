# Moonraker Connector Operations Contract

Date: 2026-02-13  
Checklist ID: `T302`

## Core Modules

- `App/connectors/moonraker.py`
  - `MoonrakerConnector`
- `App/connectors/registry.py`
  - default registry includes `MoonrakerConnector`
  - Moonraker metadata inference resolves `moonraker`
- `App/integrations/printer_manager.py`
  - connector readiness check via `connect(...)`
  - upload/start print dispatch via resolved connector

## Endpoint Contract

- `GET /server/info` for connector health/readiness.
- `POST /server/files/upload` for G-code upload.
- `POST /printer/print/start?filename=<path>` for start-print.
- `POST /printer/print/pause` for pause.
- `POST /printer/print/resume` for resume.
- `POST /printer/print/cancel` for cancel.
- `GET /printer/objects/query?print_stats&virtual_sdcard` for print status/progress.

## Printer Metadata Contract

- Required:
  - `name`
  - `moonraker_url`
- Optional:
  - `moonraker_token` or `moonraker_api_key` (sent as `Authorization: Bearer ...`)
  - `connector_type` (`moonraker`) for explicit protocol pinning.

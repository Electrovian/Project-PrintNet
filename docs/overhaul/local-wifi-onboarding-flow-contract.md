# Local Wi-Fi Onboarding Flow Contract

Date: 2026-02-13  
Checklist ID: `T322`

## Core Modules

- `App/connectors/local_wifi.py`
  - `LocalWifiProbeTarget`
  - `LocalWifiOnboarding`
    - `discover(...)`
    - `discover_from_cidr(...)`
    - `merge_printers(...)`
- `App/integrations/printer_manager.py`
  - `discover_local_wifi_printers(...)`
  - `discover_local_wifi_printers_from_cidr(...)`

## Discovery Contract

- Input:
  - `hosts`: required host list for direct discovery.
  - `ports`: optional scan ports, defaults to known ports.
  - `timeout_s`: optional request timeout override.
  - `max_targets`: optional global scan target bound.
- Output:
  - `ok`
  - `scanned_target_count`
  - `online_target_count`
  - `printer_count`
  - `printers`
  - `warnings`
  - `config`

## CIDR Contract

- Input:
  - `cidr`: network in CIDR notation.
  - `host_limit`: maximum number of hosts generated from CIDR.
- Output extends discovery result with:
  - `cidr`
  - `cidr_host_limit`
  - `cidr_host_count`

## Printer Candidate Contract

- Common fields:
  - `name`
  - `connector_type`
  - `host`
  - `port`
  - `discovered_via` (`local_wifi_scan`)
  - `network_transport` (`wifi_local`)
- Protocol-specific fields:
  - OctoPrint: `octoprint_url`, `octoprint_api_key`
  - Moonraker: `moonraker_url`, `moonraker_token`
  - PrusaLink: `prusalink_url`, `prusalink_api_key`

# Printer Profile File Discovery Contract

Date: 2026-02-13  
Checklist ID: `T052`

## Core Module

- `App/profiles_import/discovery.py`

Exports:

- `discover_printer_profile_files(source_path: str, strict: bool = False) -> PrinterProfileDiscoveryReport`
- `ProfileDiscoveryError`
- `VendorProfileDiscovery`
- `PrinterProfileDiscoveryReport`

## Discovery Report Schema

- `source_path`
- `discovered_at_utc`
- `vendor_count`
- `total_index_files`
- `total_machine_files`
- `total_process_files`
- `total_filament_files`
- `warnings[]`
- `vendors[]`

Vendor record schema:

- `vendor`
- `index_file`
- `vendor_dir`
- `machine_files[]`
- `process_files[]`
- `filament_files[]`
- `warnings[]`

## Script Contract

- `scripts/discover-printer-profiles.ps1`

Outputs:

- `docs/_printer_profile_file_discovery_report*.json`
- `docs/_printer_profile_file_discovery_summary*.txt`

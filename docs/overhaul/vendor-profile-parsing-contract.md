# Vendor/Machine/Process/Filament Parsing Contract

Date: 2026-02-13  
Checklist ID: `T062`

## Core Module

- `App/profiles_import/parsing.py`

Public functions:

- `parse_vendor_index_file(source_path, index_relative_path)`
- `parse_vendor_profile_files(source_path, discovery_report, strict=False)`
- `discover_and_parse_vendor_profiles(source_path, discovery_strict=False, parse_strict=False)`

Core classes:

- `ProfileParsingError`
- `VendorIndexEntry`
- `VendorIndexParseResult`
- `VendorProfileParseResult`
- `VendorProfileParseReport`

## Script Contract

- `scripts/parse-vendor-profiles.ps1`

Outputs:

- `docs/_vendor_profile_parsing_report*.json`
- `docs/_vendor_profile_parsing_summary*.txt`

Key parameters:

- `-VendorLimit` (`0` means full vendor set; positive values bound vendor count for targeted runs/tests)

## Parsing Rules

- Expected `type` by category:
  - machine -> `machine_model`
  - process -> `process`
  - filament -> `filament`
- Type mismatches are warnings (strict mode can elevate to failure).

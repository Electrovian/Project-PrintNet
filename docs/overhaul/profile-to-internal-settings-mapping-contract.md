# Profile-to-Internal Settings Mapping Contract

Date: 2026-02-13  
Checklist ID: `T082`

## Core Module

- `App/profiles_import/mapping.py`

Primary APIs:

- `map_resolved_profiles_to_settings(source_path, inheritance_report, strict=False)`
- `discover_resolve_and_map_profiles(source_path, discovery_strict=False, inheritance_strict=False, mapping_strict=False, vendor_limit=None, max_chain_depth=64)`

Core classes:

- `ProfileMappingError`
- `MappedProfileSettings`
- `ProfileSettingsMappingReport`

## Mapping Contract

- Input is resolved inheritance output (`ResolvedProfileDocument`) from the inheritance stage.
- Category mappers:
  - `machine` -> bed/nozzle/firmware/start-end G-code fields.
  - `process` -> layer/infill/perimeter/speed/support fields.
  - `filament` -> filament identity/color/density/flow fields.
- Unknown source keys are retained as metadata (`unknown_keys`) per mapped profile.
- Warnings are aggregated in report-level and profile-level structures.

## Script Contract

- `scripts/map-profile-settings.ps1`

Outputs:

- `docs/_profile_settings_mapping_report*.json`
- `docs/_profile_settings_mapping_summary*.txt`

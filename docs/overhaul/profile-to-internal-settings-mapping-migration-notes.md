# Profile-to-Internal Settings Mapping Migration Notes

Date: 2026-02-13  
Checklist ID: `T089`

## Legacy Baseline

- Profile values were consumed directly by mixed UI/runtime paths.
- Coercion and defaulting logic were spread across multiple call-sites.
- Unknown profile keys were not tracked in a central artifact.

## Current Baseline

- Mapping is centralized in `App/profiles_import/mapping.py`.
- Category-specific mapping produces deterministic internal settings payloads.
- Unknown keys and coercion warnings are explicit in mapping reports.

## Migration Impact

- Import workflows should use resolved mapping reports before building runtime slicer settings.
- Existing ad hoc profile-to-setting transforms should be replaced by mapping outputs.
- Unknown-key reports now provide a concrete backlog for future field coverage.

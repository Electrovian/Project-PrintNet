# Slicer Settings Normalization Contract

Date: 2026-02-13  
Checklist ID: `T112`

## Core Module

- `App/slicer_v2/settings.py`

Primary APIs:

- `normalize_settings(raw_settings, strict=False, keep_unknown_keys=True) -> dict`
- `normalize_settings_with_report(raw_settings, strict=False, keep_unknown_keys=True) -> (dict, SettingsNormalizationReport)`

Core types:

- `SettingsNormalizationReport`
- `SlicerV2SettingsNormalizationError`

## Contract Rules

- Baseline output starts from `DEFAULT_SETTINGS`.
- Aliases in `KEY_ALIASES` map legacy/profile keys into canonical keys.
- Known canonical keys are normalized by type/range/enum handlers.
- Unknown keys are reported and optionally retained (`keep_unknown_keys=True` default).
- Strict mode fails on warning presence.

## Script Contract

- `scripts/normalize-slicer-v2-settings.ps1`
- `scripts/test-slicer-v2-settings-normalization-unit.ps1`
- `scripts/test-slicer-v2-settings-normalization-integration.ps1`

Outputs:

- `docs/_slicer_v2_settings_normalization_report*.json`
- `docs/_slicer_v2_settings_normalization_summary*.txt`

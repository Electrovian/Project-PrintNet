# Profile Inheritance and Merge Engine Contract

Date: 2026-02-13  
Checklist ID: `T072`

## Core Module

- `App/profiles_import/inheritance.py`

Primary APIs:

- `resolve_profile_inheritance(source_path, discovery_report, vendor_limit=None, max_chain_depth=64, strict=False)`
- `discover_and_resolve_profile_inheritance(source_path, discovery_strict=False, inheritance_strict=False, vendor_limit=None, max_chain_depth=64)`

Core classes:

- `ProfileInheritanceError`
- `ProfileDocument`
- `ResolvedProfileDocument`
- `ProfileInheritanceReport`

## Merge Rules

- Parent chain resolved by profile `name` within same vendor/category first, then category-global fallback.
- Child values override parent values.
- Reserved key `inherits` is excluded from merged payload.
- Resolved payload includes:
  - `inherits_chain`
  - `inherits_chain_files`

## Script Contract

- `scripts/resolve-profile-inheritance.ps1`

Outputs:

- `docs/_profile_inheritance_report*.json`
- `docs/_profile_inheritance_summary*.txt`

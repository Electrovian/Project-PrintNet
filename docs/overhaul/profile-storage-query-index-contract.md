# Profile Storage and Query Index Contract

Date: 2026-02-13  
Checklist ID: `T092`

## Core Module

- `App/profiles_import/storage.py`

Primary APIs:

- `build_profile_storage_index(source_path, mapping_report, strict=False)`
- `persist_profile_storage_index(index, output_path)`
- `load_profile_storage_index(index_path)`
- `query_profile_storage_index(index, vendor=None, category=None, name_contains=None, mapped_key=None, limit=200)`
- `discover_resolve_map_build_and_persist_profile_storage_index(source_path, output_index_path, ...)`

Core classes:

- `ProfileStorageError`
- `ProfileStorageRecord`
- `ProfileStorageIndex`

## Data Contract

- Record key is deterministic:
  - `profile_id = vendor|category|name|relative_path` (normalized)
- Stored index payload contains:
  - record list
  - by-vendor index
  - by-category index
  - by-vendor-category index
  - aggregate counts and warning metadata

## Script Contract

- `scripts/store-profile-index.ps1`

Outputs:

- `docs/_profile_storage_index*.json`
- `docs/_profile_storage_index_report*.json`
- `docs/_profile_storage_index_summary*.txt`

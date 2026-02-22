# Profile Storage and Query Index Migration Notes

Date: 2026-02-13  
Checklist ID: `T099`

## Legacy Baseline

- Profile discovery/parsing/mapping outputs were ephemeral and pipeline-only.
- No persisted, queryable local catalog existed for fast lookups.
- Repeated scans/rebuilds were required for filtered profile browsing.

## Current Baseline

- Storage/indexing is centralized in `App/profiles_import/storage.py`.
- Persisted JSON index can be loaded and queried without rerunning upstream stages.
- Vendor/category indexes support deterministic filtered retrieval.

## Migration Impact

- Consumers that previously queried in-memory mapping outputs should switch to persisted index APIs.
- Profile catalog UI/backend adapters can reuse query filters from `query_profile_storage_index(...)`.
- Future storage backends (Mongo/Redis) can bridge from the same deterministic record schema.

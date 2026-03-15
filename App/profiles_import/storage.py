from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from .mapping import (
    ProfileSettingsMappingReport,
    discover_resolve_and_map_profiles,
)
from .json_catalog import (
    JSON_BUCKET_VENDOR_FILAMENT,
    JSON_BUCKET_VENDOR_MACHINE,
    JSON_BUCKET_VENDOR_PROCESS,
    discover_json_config_catalog,
)
from .source_resolver import resolve_profile_source_root


class ProfileStorageError(ValueError):
    """Raised when profile storage/index workflows fail."""


@dataclass
class ProfileStorageRecord:
    profile_id: str
    vendor: str
    category: str
    name: str
    relative_path: str
    mapped_settings: dict
    unknown_keys: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class ProfileStorageIndex:
    source_path: str
    built_at_utc: str
    record_count: int
    vendor_count: int
    category_counts: dict[str, int]
    duplicate_id_count: int
    warning_count: int
    warnings: list[str] = field(default_factory=list)
    records: list[ProfileStorageRecord] = field(default_factory=list)
    by_vendor: dict[str, list[str]] = field(default_factory=dict)
    by_category: dict[str, list[str]] = field(default_factory=dict)
    by_vendor_category: dict[str, list[str]] = field(default_factory=dict)
    total_json_file_count: int = 0
    json_file_count_by_bucket: dict[str, int] = field(default_factory=dict)
    json_files: list[str] = field(default_factory=list)
    unmapped_profile_json_files: list[str] = field(default_factory=list)
    invalid_json_file_count: int = 0

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "ProfileStorageIndex":
        if not isinstance(data, dict):
            raise ProfileStorageError("PROFILE_STORAGE_INDEX_INVALID_PAYLOAD")
        raw_records = data.get("records", [])
        records: list[ProfileStorageRecord] = []
        if not isinstance(raw_records, list):
            raise ProfileStorageError("PROFILE_STORAGE_INDEX_RECORDS_NOT_LIST")
        for raw in raw_records:
            if not isinstance(raw, dict):
                raise ProfileStorageError("PROFILE_STORAGE_INDEX_RECORD_NOT_OBJECT")
            records.append(
                ProfileStorageRecord(
                    profile_id=str(raw.get("profile_id", "")).strip(),
                    vendor=str(raw.get("vendor", "")).strip(),
                    category=str(raw.get("category", "")).strip(),
                    name=str(raw.get("name", "")).strip(),
                    relative_path=str(raw.get("relative_path", "")).strip(),
                    mapped_settings=dict(raw.get("mapped_settings", {})),
                    unknown_keys=[str(item) for item in raw.get("unknown_keys", [])],
                    warnings=[str(item) for item in raw.get("warnings", [])],
                )
            )

        return ProfileStorageIndex(
            source_path=str(data.get("source_path", "")).strip(),
            built_at_utc=str(data.get("built_at_utc", "")).strip(),
            record_count=int(data.get("record_count", len(records))),
            vendor_count=int(data.get("vendor_count", 0)),
            category_counts=dict(data.get("category_counts", {})),
            duplicate_id_count=int(data.get("duplicate_id_count", 0)),
            warning_count=int(data.get("warning_count", 0)),
            warnings=[str(item) for item in data.get("warnings", [])],
            records=records,
            by_vendor={str(k): [str(v) for v in values] for k, values in dict(data.get("by_vendor", {})).items()},
            by_category={
                str(k): [str(v) for v in values]
                for k, values in dict(data.get("by_category", {})).items()
            },
            by_vendor_category={
                str(k): [str(v) for v in values]
                for k, values in dict(data.get("by_vendor_category", {})).items()
            },
            total_json_file_count=int(data.get("total_json_file_count", 0)),
            json_file_count_by_bucket={
                str(k): int(v) for k, v in dict(data.get("json_file_count_by_bucket", {})).items()
            },
            json_files=[str(item) for item in data.get("json_files", [])],
            unmapped_profile_json_files=[str(item) for item in data.get("unmapped_profile_json_files", [])],
            invalid_json_file_count=int(data.get("invalid_json_file_count", 0)),
        )


def _key(text: str) -> str:
    return str(text).casefold().strip()


def _vendor_category_key(vendor: str, category: str) -> str:
    return f"{_key(vendor)}|{_key(category)}"


def _profile_id(vendor: str, category: str, name: str, relative_path: str) -> str:
    return f"{_key(vendor)}|{_key(category)}|{_key(name)}|{_key(relative_path)}"


def _vendor_key_from_relative_path(relative_path: str) -> str:
    parts = Path(str(relative_path).replace("\\", "/")).parts
    if not parts:
        return ""
    return _key(parts[0])


def build_profile_storage_index(
    source_path: str,
    mapping_report: ProfileSettingsMappingReport,
    *,
    strict: bool = False,
) -> ProfileStorageIndex:
    source_root = resolve_profile_source_root(
        source_path,
        error_factory=ProfileStorageError,
    )

    records: list[ProfileStorageRecord] = []
    warnings: list[str] = []
    duplicate_id_count = 0
    category_counts: dict[str, int] = {}
    by_vendor: dict[str, list[str]] = {}
    by_category: dict[str, list[str]] = {}
    by_vendor_category: dict[str, list[str]] = {}

    warning_from_mapping = int(mapping_report.warning_count)
    if warning_from_mapping > 0:
        warnings.append(f"mapping_warning_count:{warning_from_mapping}")
    if int(mapping_report.unknown_key_count) > 0:
        warnings.append(f"mapping_unknown_key_count:{int(mapping_report.unknown_key_count)}")

    seen_profile_ids: set[str] = set()
    sorted_profiles = sorted(
        mapping_report.profiles,
        key=lambda item: (item.vendor.casefold(), item.category.casefold(), item.name.casefold(), item.relative_path),
    )

    empty_mapping_count = 0

    for mapped in sorted_profiles:
        identifier = _profile_id(mapped.vendor, mapped.category, mapped.name, mapped.relative_path)
        if identifier in seen_profile_ids:
            duplicate_id_count += 1
            warnings.append(f"duplicate_profile_id:{identifier}")
            continue
        seen_profile_ids.add(identifier)

        if not mapped.mapped_settings:
            empty_mapping_count += 1

        record = ProfileStorageRecord(
            profile_id=identifier,
            vendor=mapped.vendor,
            category=mapped.category,
            name=mapped.name,
            relative_path=mapped.relative_path,
            mapped_settings=dict(mapped.mapped_settings),
            unknown_keys=list(mapped.unknown_keys),
            warnings=list(mapped.warnings),
        )
        records.append(record)

        vendor_key = _key(record.vendor)
        category_key = _key(record.category)
        vendor_category_key = _vendor_category_key(record.vendor, record.category)

        if vendor_key not in by_vendor:
            by_vendor[vendor_key] = []
        by_vendor[vendor_key].append(record.profile_id)

        if category_key not in by_category:
            by_category[category_key] = []
        by_category[category_key].append(record.profile_id)

        if vendor_category_key not in by_vendor_category:
            by_vendor_category[vendor_category_key] = []
        by_vendor_category[vendor_category_key].append(record.profile_id)

        category_counts[category_key] = category_counts.get(category_key, 0) + 1

    if empty_mapping_count > 0:
        warnings.append(f"empty_mapped_settings_count:{empty_mapping_count}")

    json_catalog = discover_json_config_catalog(str(source_root), validate_json=False)
    covered_vendor_keys = {_key(mapped.vendor) for mapped in sorted_profiles if str(mapped.vendor).strip()}
    mapped_relative_paths = {str(mapped.relative_path).replace("\\", "/") for mapped in sorted_profiles}

    profile_json_files: list[str] = []
    for bucket in (
        JSON_BUCKET_VENDOR_MACHINE,
        JSON_BUCKET_VENDOR_PROCESS,
        JSON_BUCKET_VENDOR_FILAMENT,
    ):
        for relative_path in json_catalog.files_by_bucket.get(bucket, []):
            if covered_vendor_keys:
                if _vendor_key_from_relative_path(relative_path) not in covered_vendor_keys:
                    continue
            else:
                continue
            profile_json_files.append(relative_path)

    unmapped_profile_json_files = sorted(set(profile_json_files) - mapped_relative_paths)
    if unmapped_profile_json_files:
        warnings.append(f"unmapped_profile_json_count:{len(unmapped_profile_json_files)}")

    index = ProfileStorageIndex(
        source_path=str(source_root.resolve()),
        built_at_utc=datetime.now(timezone.utc).isoformat(),
        record_count=len(records),
        vendor_count=len(by_vendor),
        category_counts=category_counts,
        duplicate_id_count=duplicate_id_count,
        warning_count=len(warnings),
        warnings=warnings,
        records=records,
        by_vendor=by_vendor,
        by_category=by_category,
        by_vendor_category=by_vendor_category,
        total_json_file_count=int(json_catalog.total_json_files),
        json_file_count_by_bucket=dict(json_catalog.bucket_counts),
        json_files=list(json_catalog.all_json_files),
        unmapped_profile_json_files=unmapped_profile_json_files,
        invalid_json_file_count=int(json_catalog.invalid_json_count),
    )

    if strict and index.warning_count > 0:
        raise ProfileStorageError(f"STRICT_PROFILE_STORAGE_WARNING_FAILURE: {index.warning_count} warning(s)")

    return index


def persist_profile_storage_index(index: ProfileStorageIndex, output_path: str) -> str:
    output_file = Path(output_path).expanduser()
    if output_file.exists() and output_file.is_dir():
        raise ProfileStorageError(f"OUTPUT_PATH_IS_DIRECTORY: {output_file}")
    if not output_file.parent.exists():
        output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(index.to_dict(), indent=2), encoding="utf-8")
    return str(output_file.resolve())


def load_profile_storage_index(index_path: str) -> ProfileStorageIndex:
    path = Path(index_path).expanduser()
    if not path.exists():
        raise ProfileStorageError(f"INDEX_PATH_MISSING: {path}")
    if not path.is_file():
        raise ProfileStorageError(f"INDEX_PATH_NOT_FILE: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ProfileStorageError(f"INDEX_JSON_PARSE_ERROR: {path}: {exc}") from exc
    return ProfileStorageIndex.from_dict(payload)


def query_profile_storage_index(
    index: ProfileStorageIndex,
    *,
    vendor: str | None = None,
    category: str | None = None,
    name_contains: str | None = None,
    mapped_key: str | None = None,
    limit: int = 200,
) -> list[ProfileStorageRecord]:
    if limit <= 0:
        raise ProfileStorageError("QUERY_LIMIT_INVALID")

    by_id = {record.profile_id: record for record in index.records}

    candidate_ids: set[str] = set(by_id.keys())
    if vendor and category:
        vc_key = _vendor_category_key(vendor, category)
        candidate_ids &= set(index.by_vendor_category.get(vc_key, []))
    else:
        if vendor:
            candidate_ids &= set(index.by_vendor.get(_key(vendor), []))
        if category:
            candidate_ids &= set(index.by_category.get(_key(category), []))

    filtered: list[ProfileStorageRecord] = []
    contains_key = str(name_contains).casefold().strip() if name_contains else ""
    mapped_key_norm = str(mapped_key).strip() if mapped_key else ""

    for record in index.records:
        if record.profile_id not in candidate_ids:
            continue
        if contains_key and contains_key not in record.name.casefold():
            continue
        if mapped_key_norm and mapped_key_norm not in record.mapped_settings:
            continue
        filtered.append(record)
        if len(filtered) >= limit:
            break

    return filtered


def discover_resolve_map_build_and_persist_profile_storage_index(
    source_path: str,
    output_index_path: str,
    *,
    discovery_strict: bool = False,
    inheritance_strict: bool = False,
    mapping_strict: bool = False,
    storage_strict: bool = False,
    vendor_limit: int | None = None,
    max_chain_depth: int = 64,
) -> ProfileStorageIndex:
    mapping_report = discover_resolve_and_map_profiles(
        source_path,
        discovery_strict=discovery_strict,
        inheritance_strict=inheritance_strict,
        mapping_strict=mapping_strict,
        vendor_limit=vendor_limit,
        max_chain_depth=max_chain_depth,
    )
    index = build_profile_storage_index(
        source_path,
        mapping_report,
        strict=storage_strict,
    )
    persist_profile_storage_index(index, output_index_path)
    return index

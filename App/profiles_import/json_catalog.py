from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .discovery import IGNORED_ROOT_INDEX_NAMES
from .source_resolver import resolve_profile_source_root


JSON_BUCKET_VENDOR_INDEX = "vendor_index"
JSON_BUCKET_VENDOR_MACHINE = "vendor_machine"
JSON_BUCKET_VENDOR_PROCESS = "vendor_process"
JSON_BUCKET_VENDOR_FILAMENT = "vendor_filament"
JSON_BUCKET_ROOT_AUX = "root_aux"
JSON_BUCKET_MISC = "misc"


class JsonConfigCatalogError(ValueError):
    """Raised when JSON config catalog discovery fails validation."""


@dataclass
class JsonConfigCatalogReport:
    source_path: str
    cataloged_at_utc: str
    total_json_files: int
    bucket_counts: dict[str, int]
    invalid_json_count: int
    warning_count: int
    warnings: list[str] = field(default_factory=list)
    all_json_files: list[str] = field(default_factory=list)
    files_by_bucket: dict[str, list[str]] = field(default_factory=dict)
    invalid_json_files: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def _key(text: str) -> str:
    return str(text).casefold().strip()


def _normalized_relative_path(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def _classify_bucket(relative_path: str, *, ignored_root_index_names: set[str]) -> str:
    rel = Path(relative_path)
    parts = rel.parts
    if not parts:
        return JSON_BUCKET_MISC

    if len(parts) == 1:
        if _key(rel.stem) in ignored_root_index_names:
            return JSON_BUCKET_ROOT_AUX
        return JSON_BUCKET_VENDOR_INDEX

    if len(parts) >= 3:
        category = _key(parts[1])
        if category == "machine":
            return JSON_BUCKET_VENDOR_MACHINE
        if category == "process":
            return JSON_BUCKET_VENDOR_PROCESS
        if category == "filament":
            return JSON_BUCKET_VENDOR_FILAMENT

    return JSON_BUCKET_MISC


def discover_json_config_catalog(
    source_path: str,
    *,
    ignored_root_index_names: Iterable[str] = IGNORED_ROOT_INDEX_NAMES,
    validate_json: bool = False,
    strict: bool = False,
) -> JsonConfigCatalogReport:
    source_root = resolve_profile_source_root(
        source_path,
        error_factory=JsonConfigCatalogError,
    )

    ignore_keys = {_key(name) for name in ignored_root_index_names}
    discovered_files = sorted(path for path in source_root.rglob("*.json") if path.is_file())

    all_json_files: list[str] = []
    files_by_bucket: dict[str, list[str]] = {
        JSON_BUCKET_VENDOR_INDEX: [],
        JSON_BUCKET_VENDOR_MACHINE: [],
        JSON_BUCKET_VENDOR_PROCESS: [],
        JSON_BUCKET_VENDOR_FILAMENT: [],
        JSON_BUCKET_ROOT_AUX: [],
        JSON_BUCKET_MISC: [],
    }
    warnings: list[str] = []
    invalid_json_files: list[str] = []

    for path in discovered_files:
        relative_path = _normalized_relative_path(path, source_root)
        all_json_files.append(relative_path)
        bucket = _classify_bucket(relative_path, ignored_root_index_names=ignore_keys)
        files_by_bucket.setdefault(bucket, []).append(relative_path)
        if not validate_json:
            continue
        try:
            raw = path.read_text(encoding="utf-8")
            json.loads(raw)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            invalid_json_files.append(relative_path)
            warnings.append(f"invalid_json:{relative_path}:{exc}")

    bucket_counts = {bucket: len(paths) for bucket, paths in files_by_bucket.items()}
    report = JsonConfigCatalogReport(
        source_path=str(source_root.resolve()),
        cataloged_at_utc=datetime.now(timezone.utc).isoformat(),
        total_json_files=len(all_json_files),
        bucket_counts=bucket_counts,
        invalid_json_count=len(invalid_json_files),
        warning_count=len(warnings),
        warnings=warnings,
        all_json_files=all_json_files,
        files_by_bucket=files_by_bucket,
        invalid_json_files=invalid_json_files,
    )
    if strict and report.warning_count > 0:
        raise JsonConfigCatalogError(f"STRICT_JSON_CATALOG_WARNING_FAILURE: {report.warning_count} warning(s)")
    return report

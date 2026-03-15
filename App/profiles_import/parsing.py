from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from .discovery import PrinterProfileDiscoveryReport, discover_printer_profile_files
from .source_resolver import resolve_profile_source_root


EXPECTED_TYPE_BY_CATEGORY = {
    "machine": "machine_model",
    "process": "process",
    "filament": "filament",
}


class ProfileParsingError(ValueError):
    """Raised when vendor/profile parsing fails."""


@dataclass
class VendorIndexEntry:
    name: str
    sub_path: str


@dataclass
class VendorIndexParseResult:
    vendor: str
    index_file: str
    machine_entries: list[VendorIndexEntry] = field(default_factory=list)
    process_entries: list[VendorIndexEntry] = field(default_factory=list)
    filament_entries: list[VendorIndexEntry] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class VendorProfileParseResult:
    vendor: str
    index_file: str | None
    machine_files_parsed: int
    process_files_parsed: int
    filament_files_parsed: int
    machine_type_mismatches: int
    process_type_mismatches: int
    filament_type_mismatches: int
    warnings: list[str] = field(default_factory=list)


@dataclass
class VendorProfileParseReport:
    source_path: str
    parsed_at_utc: str
    vendor_count: int
    total_machine_files_parsed: int
    total_process_files_parsed: int
    total_filament_files_parsed: int
    total_type_mismatches: int
    total_warnings: int
    warnings: list[str] = field(default_factory=list)
    vendors: list[VendorProfileParseResult] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def _absolute_path(source_root: Path, relative_path: str) -> Path:
    return source_root.resolve() / Path(relative_path)


def _load_json_dict(path: Path) -> dict:
    if not path.exists():
        raise ProfileParsingError(f"PROFILE_FILE_MISSING: {path}")
    if not path.is_file():
        raise ProfileParsingError(f"PROFILE_PATH_NOT_FILE: {path}")
    try:
        raw = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ProfileParsingError(f"PROFILE_FILE_DECODE_ERROR: {path}: {exc}") from exc
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ProfileParsingError(f"PROFILE_JSON_PARSE_ERROR: {path}: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ProfileParsingError(f"PROFILE_JSON_NOT_OBJECT: {path}")
    return parsed


def _extract_index_entries(
    *,
    data: dict,
    key: str,
    expected_prefix: str,
    warnings: list[str],
    vendor: str,
) -> list[VendorIndexEntry]:
    raw = data.get(key)
    if raw is None:
        warnings.append(f"{vendor}: index_missing_key:{key}")
        return []
    if not isinstance(raw, list):
        warnings.append(f"{vendor}: index_key_not_list:{key}")
        return []

    entries: list[VendorIndexEntry] = []
    for idx, item in enumerate(raw):
        if not isinstance(item, dict):
            warnings.append(f"{vendor}: index_item_not_object:{key}:{idx}")
            continue
        name = str(item.get("name", "")).strip()
        sub_path = str(item.get("sub_path", "")).strip()
        if not name:
            warnings.append(f"{vendor}: index_item_missing_name:{key}:{idx}")
            continue
        if not sub_path:
            warnings.append(f"{vendor}: index_item_missing_sub_path:{key}:{idx}")
            continue
        if not sub_path.replace("\\", "/").startswith(f"{expected_prefix}/"):
            warnings.append(f"{vendor}: index_item_path_category_mismatch:{key}:{sub_path}")
        entries.append(VendorIndexEntry(name=name, sub_path=sub_path.replace("\\", "/")))
    return entries


def parse_vendor_index_file(source_path: str, index_relative_path: str) -> VendorIndexParseResult:
    source_root = resolve_profile_source_root(
        source_path,
        error_factory=ProfileParsingError,
    )

    index_abs = _absolute_path(source_root, index_relative_path)
    data = _load_json_dict(index_abs)

    vendor = str(data.get("name", "")).strip() or Path(index_relative_path).stem
    warnings: list[str] = []

    machine_entries = _extract_index_entries(
        data=data,
        key="machine_model_list",
        expected_prefix="machine",
        warnings=warnings,
        vendor=vendor,
    )
    process_entries = _extract_index_entries(
        data=data,
        key="process_list",
        expected_prefix="process",
        warnings=warnings,
        vendor=vendor,
    )
    filament_entries = _extract_index_entries(
        data=data,
        key="filament_list",
        expected_prefix="filament",
        warnings=warnings,
        vendor=vendor,
    )

    return VendorIndexParseResult(
        vendor=vendor,
        index_file=index_relative_path.replace("\\", "/"),
        machine_entries=machine_entries,
        process_entries=process_entries,
        filament_entries=filament_entries,
        warnings=warnings,
    )


def _parse_profile_category_files(
    *,
    source_root: Path,
    vendor: str,
    category: str,
    relative_paths: list[str],
) -> tuple[int, int, list[str]]:
    expected_type = EXPECTED_TYPE_BY_CATEGORY[category]
    parsed_count = 0
    type_mismatch_count = 0
    warnings: list[str] = []

    for rel_path in relative_paths:
        rel_norm = rel_path.replace("\\", "/")
        data = _load_json_dict(_absolute_path(source_root, rel_norm))
        parsed_count += 1
        actual_type = str(data.get("type", "")).strip()
        if actual_type != expected_type:
            type_mismatch_count += 1
            warnings.append(
                f"{vendor}: {category}_type_mismatch:{rel_norm}:expected={expected_type}:actual={actual_type or 'missing'}"
            )
        if not str(data.get("name", "")).strip():
            warnings.append(f"{vendor}: {category}_name_missing:{rel_norm}")

    return parsed_count, type_mismatch_count, warnings


def parse_vendor_profile_files(
    source_path: str,
    discovery_report: PrinterProfileDiscoveryReport,
    *,
    strict: bool = False,
    vendor_limit: int | None = None,
) -> VendorProfileParseReport:
    source_root = resolve_profile_source_root(
        source_path,
        error_factory=ProfileParsingError,
    )

    report_warnings: list[str] = []
    vendor_results: list[VendorProfileParseResult] = []

    total_machine = 0
    total_process = 0
    total_filament = 0
    total_mismatches = 0

    for idx, vendor in enumerate(discovery_report.vendors):
        if vendor_limit is not None and vendor_limit > 0 and idx >= vendor_limit:
            break
        vendor_warnings = list(vendor.warnings)
        index_file = vendor.index_file

        if index_file:
            index_result = parse_vendor_index_file(str(source_root), index_file)
            vendor_warnings.extend(index_result.warnings)
        else:
            vendor_warnings.append(f"{vendor.vendor}: index_file_missing")

        machine_count, machine_mismatches, machine_warnings = _parse_profile_category_files(
            source_root=source_root,
            vendor=vendor.vendor,
            category="machine",
            relative_paths=vendor.machine_files,
        )
        process_count, process_mismatches, process_warnings = _parse_profile_category_files(
            source_root=source_root,
            vendor=vendor.vendor,
            category="process",
            relative_paths=vendor.process_files,
        )
        filament_count, filament_mismatches, filament_warnings = _parse_profile_category_files(
            source_root=source_root,
            vendor=vendor.vendor,
            category="filament",
            relative_paths=vendor.filament_files,
        )

        vendor_warnings.extend(machine_warnings)
        vendor_warnings.extend(process_warnings)
        vendor_warnings.extend(filament_warnings)

        total_machine += machine_count
        total_process += process_count
        total_filament += filament_count
        total_mismatches += machine_mismatches + process_mismatches + filament_mismatches
        report_warnings.extend(vendor_warnings)

        vendor_results.append(
            VendorProfileParseResult(
                vendor=vendor.vendor,
                index_file=index_file,
                machine_files_parsed=machine_count,
                process_files_parsed=process_count,
                filament_files_parsed=filament_count,
                machine_type_mismatches=machine_mismatches,
                process_type_mismatches=process_mismatches,
                filament_type_mismatches=filament_mismatches,
                warnings=vendor_warnings,
            )
        )

    parse_report = VendorProfileParseReport(
        source_path=str(source_root.resolve()),
        parsed_at_utc=datetime.now(timezone.utc).isoformat(),
        vendor_count=len(vendor_results),
        total_machine_files_parsed=total_machine,
        total_process_files_parsed=total_process,
        total_filament_files_parsed=total_filament,
        total_type_mismatches=total_mismatches,
        total_warnings=len(report_warnings),
        warnings=report_warnings,
        vendors=vendor_results,
    )

    if strict and parse_report.total_warnings > 0:
        raise ProfileParsingError(f"STRICT_PARSING_WARNING_FAILURE: {parse_report.total_warnings} warning(s)")

    return parse_report


def discover_and_parse_vendor_profiles(
    source_path: str,
    *,
    discovery_strict: bool = False,
    parse_strict: bool = False,
    vendor_limit: int | None = None,
) -> VendorProfileParseReport:
    discovery_report = discover_printer_profile_files(source_path, strict=discovery_strict)
    return parse_vendor_profile_files(
        source_path,
        discovery_report,
        strict=parse_strict,
        vendor_limit=vendor_limit,
    )

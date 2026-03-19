from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .source_resolver import resolve_profile_source_root


PROFILE_CATEGORY_DIRS = ("machine", "process", "filament")
IGNORED_ROOT_INDEX_NAMES = ("blacklist",)


class ProfileDiscoveryError(ValueError):
    """Raised when profile source discovery fails validation."""


@dataclass
class VendorProfileDiscovery:
    vendor: str
    index_file: str | None
    vendor_dir: str | None
    machine_files: list[str] = field(default_factory=list)
    process_files: list[str] = field(default_factory=list)
    filament_files: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class PrinterProfileDiscoveryReport:
    source_path: str
    discovered_at_utc: str
    vendor_count: int
    total_index_files: int
    total_machine_files: int
    total_process_files: int
    total_filament_files: int
    warnings: list[str] = field(default_factory=list)
    vendors: list[VendorProfileDiscovery] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def _normalized_relative_path(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def _collect_json_files(root: Path, source_root: Path) -> list[str]:
    if not root.exists() or not root.is_dir():
        return []
    files = sorted(path for path in root.rglob("*.json") if path.is_file())
    return [_normalized_relative_path(path, source_root) for path in files]


def _key(name: str) -> str:
    return name.casefold().strip()


def discover_printer_profile_files(
    source_path: str,
    *,
    ignored_root_index_names: Iterable[str] = IGNORED_ROOT_INDEX_NAMES,
    strict: bool = False,
) -> PrinterProfileDiscoveryReport:
    source_root = resolve_profile_source_root(
        source_path,
        error_factory=ProfileDiscoveryError,
    )

    ignore_keys = {_key(name) for name in ignored_root_index_names}

    index_by_key: dict[str, Path] = {}
    dir_by_key: dict[str, Path] = {}

    for child in source_root.iterdir():
        if child.is_file() and child.suffix.casefold() == ".json":
            index_key = _key(child.stem)
            if index_key in ignore_keys:
                continue
            index_by_key[index_key] = child
        elif child.is_dir():
            dir_by_key[_key(child.name)] = child

    vendor_keys = sorted(set(index_by_key.keys()) | set(dir_by_key.keys()))
    all_warnings: list[str] = []
    vendors: list[VendorProfileDiscovery] = []

    for vendor_key in vendor_keys:
        index_file = index_by_key.get(vendor_key)
        vendor_dir = dir_by_key.get(vendor_key)

        if vendor_dir is not None:
            vendor_name = vendor_dir.name
        elif index_file is not None:
            vendor_name = index_file.stem
        else:
            vendor_name = vendor_key
        vendor_warnings: list[str] = []

        if index_file is None:
            vendor_warnings.append("index_file_missing")
        if vendor_dir is None:
            vendor_warnings.append("vendor_directory_missing")

        machine_files: list[str] = []
        process_files: list[str] = []
        filament_files: list[str] = []

        if vendor_dir is not None:
            machine_files = _collect_json_files(vendor_dir / PROFILE_CATEGORY_DIRS[0], source_root)
            process_files = _collect_json_files(vendor_dir / PROFILE_CATEGORY_DIRS[1], source_root)
            filament_files = _collect_json_files(vendor_dir / PROFILE_CATEGORY_DIRS[2], source_root)

            if not machine_files:
                vendor_warnings.append("machine_profiles_missing")
            if not process_files:
                vendor_warnings.append("process_profiles_missing")
            if not filament_files:
                vendor_warnings.append("filament_profiles_missing")

        for warn in vendor_warnings:
            all_warnings.append(f"{vendor_name}: {warn}")

        vendors.append(
            VendorProfileDiscovery(
                vendor=vendor_name,
                index_file=_normalized_relative_path(index_file, source_root) if index_file is not None else None,
                vendor_dir=_normalized_relative_path(vendor_dir, source_root) if vendor_dir is not None else None,
                machine_files=machine_files,
                process_files=process_files,
                filament_files=filament_files,
                warnings=vendor_warnings,
            )
        )

    report = PrinterProfileDiscoveryReport(
        source_path=str(source_root.resolve()),
        discovered_at_utc=datetime.now(timezone.utc).isoformat(),
        vendor_count=len(vendors),
        total_index_files=len(index_by_key),
        total_machine_files=sum(len(v.machine_files) for v in vendors),
        total_process_files=sum(len(v.process_files) for v in vendors),
        total_filament_files=sum(len(v.filament_files) for v in vendors),
        warnings=all_warnings,
        vendors=vendors,
    )

    if strict and report.warnings:
        raise ProfileDiscoveryError(f"STRICT_DISCOVERY_WARNING_FAILURE: {len(report.warnings)} warning(s)")

    return report

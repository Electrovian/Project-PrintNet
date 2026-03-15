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

RESERVED_KEYS = {"inherits"}


class ProfileInheritanceError(ValueError):
    """Raised when profile inheritance/merge processing fails."""


@dataclass
class ProfileDocument:
    vendor: str
    category: str
    name: str
    relative_path: str
    profile_type: str
    inherits: str | None
    data: dict


@dataclass
class ResolvedProfileDocument:
    vendor: str
    category: str
    name: str
    relative_path: str
    chain_paths: list[str]
    chain_names: list[str]
    resolved_data: dict
    warnings: list[str] = field(default_factory=list)


@dataclass
class ProfileInheritanceReport:
    source_path: str
    resolved_at_utc: str
    vendor_count: int
    profile_count: int
    resolved_profile_count: int
    duplicate_name_count: int
    missing_parent_count: int
    cycle_count: int
    max_depth_exceeded_count: int
    type_mismatch_count: int
    warning_count: int
    warnings: list[str] = field(default_factory=list)
    resolved_profiles: list[ResolvedProfileDocument] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def _absolute_path(source_root: Path, relative_path: str) -> Path:
    return source_root.resolve() / Path(relative_path)


def _load_profile_json(path: Path) -> dict:
    if not path.exists():
        raise ProfileInheritanceError(f"PROFILE_FILE_MISSING: {path}")
    if not path.is_file():
        raise ProfileInheritanceError(f"PROFILE_PATH_NOT_FILE: {path}")
    try:
        raw = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ProfileInheritanceError(f"PROFILE_FILE_DECODE_ERROR: {path}: {exc}") from exc
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ProfileInheritanceError(f"PROFILE_JSON_PARSE_ERROR: {path}: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ProfileInheritanceError(f"PROFILE_JSON_NOT_OBJECT: {path}")
    return parsed


def _safe_name(data: dict, fallback: str) -> str:
    name = str(data.get("name", "")).strip()
    if name:
        return name
    return fallback


def _key(text: str) -> str:
    return text.casefold().strip()


def _collect_profile_documents(
    source_root: Path,
    discovery_report: PrinterProfileDiscoveryReport,
    *,
    vendor_limit: int | None,
) -> tuple[list[ProfileDocument], int, int, list[str]]:
    documents: list[ProfileDocument] = []
    warnings: list[str] = []
    duplicate_name_count = 0
    type_mismatch_count = 0

    key_counts: dict[tuple[str, str, str], int] = {}

    for vendor_index, vendor in enumerate(discovery_report.vendors):
        if vendor_limit is not None and vendor_limit > 0 and vendor_index >= vendor_limit:
            break

        category_paths = {
            "machine": vendor.machine_files,
            "process": vendor.process_files,
            "filament": vendor.filament_files,
        }

        for category, rel_paths in category_paths.items():
            expected_type = EXPECTED_TYPE_BY_CATEGORY[category]
            for rel_path in rel_paths:
                rel_norm = rel_path.replace("\\", "/")
                data = _load_profile_json(_absolute_path(source_root, rel_norm))
                name = _safe_name(data, Path(rel_norm).stem)
                profile_type = str(data.get("type", "")).strip()
                inherits = str(data.get("inherits", "")).strip() or None

                if profile_type != expected_type:
                    type_mismatch_count += 1
                    warnings.append(
                        f"{vendor.vendor}: type_mismatch:{rel_norm}:expected={expected_type}:actual={profile_type or 'missing'}"
                    )

                key = (_key(vendor.vendor), category, _key(name))
                seen_count = key_counts.get(key, 0)
                key_counts[key] = seen_count + 1
                if seen_count > 0:
                    duplicate_name_count += 1
                    warnings.append(f"{vendor.vendor}: duplicate_profile_name:{category}:{name}")

                documents.append(
                    ProfileDocument(
                        vendor=vendor.vendor,
                        category=category,
                        name=name,
                        relative_path=rel_norm,
                        profile_type=profile_type,
                        inherits=inherits,
                        data=data,
                    )
                )

    return documents, duplicate_name_count, type_mismatch_count, warnings


def _build_lookup_indexes(
    documents: list[ProfileDocument],
) -> tuple[
    dict[tuple[str, str, str], list[ProfileDocument]],
    dict[tuple[str, str], list[ProfileDocument]],
]:
    same_vendor: dict[tuple[str, str, str], list[ProfileDocument]] = {}
    global_index: dict[tuple[str, str], list[ProfileDocument]] = {}

    for doc in documents:
        vendor_key = _key(doc.vendor)
        name_key = _key(doc.name)

        sv_key = (vendor_key, doc.category, name_key)
        if sv_key not in same_vendor:
            same_vendor[sv_key] = []
        same_vendor[sv_key].append(doc)

        g_key = (doc.category, name_key)
        if g_key not in global_index:
            global_index[g_key] = []
        global_index[g_key].append(doc)

    return same_vendor, global_index


def _select_parent_candidate(
    *,
    vendor: str,
    category: str,
    parent_name: str,
    same_vendor_index: dict[tuple[str, str, str], list[ProfileDocument]],
    global_index: dict[tuple[str, str], list[ProfileDocument]],
) -> tuple[ProfileDocument | None, str | None]:
    vendor_key = _key(vendor)
    parent_key = _key(parent_name)

    candidates = same_vendor_index.get((vendor_key, category, parent_key), [])
    if not candidates:
        candidates = global_index.get((category, parent_key), [])
    if not candidates:
        return None, "parent_missing"

    sorted_candidates = sorted(candidates, key=lambda x: x.relative_path)
    selected = sorted_candidates[0]
    if len(sorted_candidates) > 1:
        return selected, "parent_ambiguous"
    return selected, None


def resolve_profile_inheritance(
    source_path: str,
    discovery_report: PrinterProfileDiscoveryReport,
    *,
    vendor_limit: int | None = None,
    max_chain_depth: int = 64,
    strict: bool = False,
) -> ProfileInheritanceReport:
    if max_chain_depth <= 0:
        raise ProfileInheritanceError("INVALID_MAX_CHAIN_DEPTH")

    source_root = resolve_profile_source_root(
        source_path,
        error_factory=ProfileInheritanceError,
    )

    docs, duplicate_count, type_mismatch_count, warnings = _collect_profile_documents(
        source_root,
        discovery_report,
        vendor_limit=vendor_limit,
    )

    same_vendor_index, global_index = _build_lookup_indexes(docs)

    missing_parent_count = 0
    cycle_count = 0
    depth_exceeded_count = 0
    resolved_docs: list[ResolvedProfileDocument] = []

    for doc in docs:
        chain: list[ProfileDocument] = [doc]
        seen_paths = {doc.relative_path}
        local_warnings: list[str] = []

        parent_name = doc.inherits
        depth = 0

        while parent_name:
            if depth >= max_chain_depth:
                depth_exceeded_count += 1
                local_warnings.append(
                    f"{doc.vendor}: max_chain_depth_exceeded:{doc.category}:{doc.name}:{max_chain_depth}"
                )
                break

            parent, parent_warn = _select_parent_candidate(
                vendor=doc.vendor,
                category=doc.category,
                parent_name=parent_name,
                same_vendor_index=same_vendor_index,
                global_index=global_index,
            )

            if parent is None:
                missing_parent_count += 1
                local_warnings.append(
                    f"{doc.vendor}: missing_parent:{doc.category}:{doc.name}:{parent_name}"
                )
                break

            if parent_warn == "parent_ambiguous":
                local_warnings.append(
                    f"{doc.vendor}: ambiguous_parent:{doc.category}:{doc.name}:{parent_name}:{parent.relative_path}"
                )

            if parent.relative_path in seen_paths:
                cycle_count += 1
                local_warnings.append(
                    f"{doc.vendor}: inheritance_cycle:{doc.category}:{doc.name}:{parent.relative_path}"
                )
                break

            chain.append(parent)
            seen_paths.add(parent.relative_path)
            parent_name = parent.inherits
            depth += 1

        resolved: dict = {}
        ordered_chain = list(reversed(chain))
        for chain_doc in ordered_chain:
            for key, value in chain_doc.data.items():
                if key in RESERVED_KEYS:
                    continue
                resolved[key] = value
        resolved["name"] = doc.name
        resolved["type"] = doc.profile_type
        resolved["inherits_chain"] = [item.name for item in ordered_chain]
        resolved["inherits_chain_files"] = [item.relative_path for item in ordered_chain]

        resolved_docs.append(
            ResolvedProfileDocument(
                vendor=doc.vendor,
                category=doc.category,
                name=doc.name,
                relative_path=doc.relative_path,
                chain_paths=[item.relative_path for item in ordered_chain],
                chain_names=[item.name for item in ordered_chain],
                resolved_data=resolved,
                warnings=local_warnings,
            )
        )
        warnings.extend(local_warnings)

    report = ProfileInheritanceReport(
        source_path=str(source_root.resolve()),
        resolved_at_utc=datetime.now(timezone.utc).isoformat(),
        vendor_count=len({doc.vendor for doc in docs}),
        profile_count=len(docs),
        resolved_profile_count=len(resolved_docs),
        duplicate_name_count=duplicate_count,
        missing_parent_count=missing_parent_count,
        cycle_count=cycle_count,
        max_depth_exceeded_count=depth_exceeded_count,
        type_mismatch_count=type_mismatch_count,
        warning_count=len(warnings),
        warnings=warnings,
        resolved_profiles=resolved_docs,
    )

    if strict and report.warning_count > 0:
        raise ProfileInheritanceError(f"STRICT_INHERITANCE_WARNING_FAILURE: {report.warning_count} warning(s)")

    return report


def discover_and_resolve_profile_inheritance(
    source_path: str,
    *,
    discovery_strict: bool = False,
    inheritance_strict: bool = False,
    vendor_limit: int | None = None,
    max_chain_depth: int = 64,
) -> ProfileInheritanceReport:
    discovery_report = discover_printer_profile_files(source_path, strict=discovery_strict)
    return resolve_profile_inheritance(
        source_path,
        discovery_report,
        vendor_limit=vendor_limit,
        max_chain_depth=max_chain_depth,
        strict=inheritance_strict,
    )

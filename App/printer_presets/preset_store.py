from __future__ import annotations

import copy
import json
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterator

from . import preset_table


@dataclass(frozen=True)
class PresetDocument:
    id: str
    bucket: str
    relative_path: str
    storage_path: str
    vendor: str
    category: str
    name: str
    source_relative_path: str
    payload: dict[str, Any]


_CACHE_DOCS: list[PresetDocument] | None = None
_CACHE_ID: dict[str, PresetDocument] | None = None
_CACHE_ALIAS_TO_ID: dict[str, str] | None = None
_CACHE_CLI_CONFIG_IDS: list[str] | None = None
_MATERIALIZED_ROOT: Path | None = None
_PRINTERS_DATA: dict[str, dict[str, Any]] | None = None


def _normalize_slashes(value: str) -> str:
    return str(PurePosixPath(value.replace("\\", "/")))


def _normalize_alias(value: str) -> str:
    text = str(value).strip().replace("\\", "/")
    while "//" in text:
        text = text.replace("//", "/")
    return text.casefold().strip("/")


def _normalize_module_name(vendor_name: str) -> str:
    import re

    text = re.sub(r"[^A-Za-z0-9]+", "_", str(vendor_name)).strip("_")
    if not text:
        text = "vendor"
    if text[0].isdigit():
        text = f"v_{text}"
    return text.lower()


def _strip_known_prefixes(text: str) -> str:
    raw = text.replace("\\", "/").strip()
    lowered = raw.casefold()
    prefixes = (
        "app/printer_presets/seed_resources/",
        "printer_presets/seed_resources/",
        "seed_resources/",
    )
    for prefix in prefixes:
        index = lowered.find(prefix)
        if index >= 0:
            return raw[index + len(prefix) :].strip("/")
    return raw.strip("/")


def _load_printers_data() -> dict[str, dict[str, Any]]:
    global _PRINTERS_DATA
    if _PRINTERS_DATA is not None:
        return _PRINTERS_DATA
    try:
        from App.printer_presets.seed_resources.printers.printers_data import PRINTERS_DATA
    except Exception:
        _PRINTERS_DATA = {}
        return _PRINTERS_DATA
    if isinstance(PRINTERS_DATA, dict):
        _PRINTERS_DATA = {str(key): dict(value) for key, value in PRINTERS_DATA.items() if isinstance(value, dict)}
    else:
        _PRINTERS_DATA = {}
    return _PRINTERS_DATA


def _try_fast_embedded_payload(identifier: str) -> tuple[str, dict[str, Any]] | None:
    raw = str(identifier).strip()
    if not raw:
        return None
    relative = _strip_known_prefixes(raw)
    lowered = relative.casefold()

    # Printer JSONs from printers_data.py
    if lowered.startswith("printers/") and lowered.endswith(".json"):
        key = relative.split("/", 1)[1]
        data = _load_printers_data()
        payload = data.get(key)
        if payload is not None:
            return f"embedded:printers/{key}", copy.deepcopy(payload)

    # Vendor profile JSONs from python_vendors/*.py
    if not lowered.startswith("profiles/"):
        return None

    profile_rel = relative.split("/", 1)[1]
    parts = profile_rel.split("/")
    if not parts:
        return None

    vendor = parts[0]
    try:
        from App.printer_presets.seed_resources.profiles import python_vendors

        module_name = _normalize_module_name(vendor)
        module = python_vendors.load_vendor_module(module_name)
    except Exception:
        # Fallback to brute-force module search only if direct normalization misses.
        try:
            from App.printer_presets.seed_resources.profiles import python_vendors
        except Exception:
            return None

        module = None
        for candidate in getattr(python_vendors, "VENDOR_MODULES", []):
            try:
                loaded = python_vendors.load_vendor_module(candidate)
            except Exception:
                continue
            candidate_vendor = str(getattr(loaded, "VENDOR", "")).strip().casefold()
            if candidate_vendor == vendor.casefold():
                module = loaded
                break
        if module is None:
            return None

    # vendor index file: profiles/<Vendor>.json
    if len(parts) == 1 and parts[0]:
        index_payload = getattr(module, "INDEX", None)
        if isinstance(index_payload, dict) and index_payload:
            return f"embedded:profiles/{parts[0]}.json", copy.deepcopy(index_payload)
        if parts[0].casefold() == "blacklist":
            try:
                from App.printer_presets.seed_resources.profiles.python_vendors.global_profiles_data import (
                    GLOBAL_PROFILE_DATA,
                )
            except Exception:
                return None
            payload = GLOBAL_PROFILE_DATA.get("blacklist.json") if isinstance(GLOBAL_PROFILE_DATA, dict) else None
            if isinstance(payload, dict):
                return "embedded:profiles/blacklist.json", copy.deepcopy(payload)
        return None

    section = parts[1].casefold()
    key = "/".join(parts[1:])
    if section == "machine":
        dataset = getattr(module, "MACHINE", None)
    elif section == "process":
        dataset = getattr(module, "PROCESS", None)
    elif section == "filament":
        dataset = getattr(module, "FILAMENT", None)
    else:
        dataset = getattr(module, "MISC", None)
    if isinstance(dataset, dict):
        payload = dataset.get(key)
        if isinstance(payload, dict):
            return f"embedded:profiles/{profile_rel}", copy.deepcopy(payload)
    return None


def _load_caches() -> None:
    global _CACHE_DOCS, _CACHE_ID, _CACHE_ALIAS_TO_ID, _CACHE_CLI_CONFIG_IDS
    if _CACHE_DOCS is not None:
        return

    payload = preset_table.get_payload()
    raw_docs = payload.get("documents", [])
    raw_indexes = payload.get("indexes", {})
    if not isinstance(raw_docs, list):
        raise ValueError("PRESET_TABLE_DOCUMENTS_INVALID")
    if not isinstance(raw_indexes, dict):
        raise ValueError("PRESET_TABLE_INDEXES_INVALID")

    documents: list[PresetDocument] = []
    id_map: dict[str, PresetDocument] = {}
    for entry in raw_docs:
        if not isinstance(entry, dict):
            continue
        doc = PresetDocument(
            id=str(entry.get("id", "")),
            bucket=str(entry.get("bucket", "")),
            relative_path=str(entry.get("relative_path", "")),
            storage_path=str(entry.get("storage_path", "")),
            vendor=str(entry.get("vendor", "")),
            category=str(entry.get("category", "")),
            name=str(entry.get("name", "")),
            source_relative_path=str(entry.get("source_relative_path", "")),
            payload=dict(entry.get("payload", {})),
        )
        if not doc.id:
            continue
        documents.append(doc)
        id_map[doc.id] = doc

    alias_to_id_raw = raw_indexes.get("alias_to_id", {})
    if isinstance(alias_to_id_raw, dict):
        alias_to_id = {str(key): str(value) for key, value in alias_to_id_raw.items() if str(value) in id_map}
    else:
        alias_to_id = {}

    cli_config_ids_raw = raw_indexes.get("cli_config_ids", [])
    if isinstance(cli_config_ids_raw, list):
        cli_config_ids = [str(item) for item in cli_config_ids_raw if str(item) in id_map]
    else:
        cli_config_ids = []

    _CACHE_DOCS = documents
    _CACHE_ID = id_map
    _CACHE_ALIAS_TO_ID = alias_to_id
    _CACHE_CLI_CONFIG_IDS = cli_config_ids


def get_meta() -> dict[str, Any]:
    meta = preset_table.get_meta()
    return dict(meta)


def iter_documents(bucket: str | None = None) -> Iterator[PresetDocument]:
    _load_caches()
    assert _CACHE_DOCS is not None
    bucket_key = str(bucket).strip().casefold() if bucket else ""
    for doc in _CACHE_DOCS:
        if bucket_key and doc.bucket.casefold() != bucket_key:
            continue
        yield doc


def _resolve_document_id(identifier: str) -> str | None:
    _load_caches()
    assert _CACHE_ID is not None
    assert _CACHE_ALIAS_TO_ID is not None

    direct = str(identifier).strip()
    if not direct:
        return None
    if direct in _CACHE_ID:
        return direct

    candidates: list[str] = []
    raw = direct.replace("\\", "/")
    candidates.append(raw)
    candidates.append(raw.strip("/"))

    lower = raw.casefold()
    seeds = (
        "app/printer_presets/seed_resources/",
        "printer_presets/seed_resources/",
        "seed_resources/",
    )
    for prefix in seeds:
        idx = lower.find(prefix)
        if idx >= 0:
            trimmed = raw[idx + len(prefix) :]
            candidates.append(trimmed)

    normalized_candidates = [_normalize_alias(item) for item in candidates if str(item).strip()]

    for candidate in normalized_candidates:
        resolved = _CACHE_ALIAS_TO_ID.get(candidate)
        if resolved:
            return resolved

    # Fallback: suffix lookup for legacy absolute paths.
    for candidate in normalized_candidates:
        matches = [doc_id for alias, doc_id in _CACHE_ALIAS_TO_ID.items() if alias.endswith(candidate)]
        if len(matches) == 1:
            return matches[0]

    return None


def get_document(identifier: str) -> PresetDocument | None:
    _load_caches()
    assert _CACHE_ID is not None
    resolved_id = _resolve_document_id(identifier)
    if not resolved_id:
        return None
    return _CACHE_ID.get(resolved_id)


def get_payload(identifier: str) -> tuple[str, dict[str, Any]] | None:
    fast = _try_fast_embedded_payload(identifier)
    if fast is not None:
        return fast
    doc = get_document(identifier)
    if doc is None:
        return None
    return f"embedded:{doc.storage_path}", copy.deepcopy(doc.payload)


def get_cli_config_payload(preferred_identifier: str | None = None) -> dict[str, Any] | None:
    _load_caches()
    assert _CACHE_ID is not None
    assert _CACHE_CLI_CONFIG_IDS is not None

    if preferred_identifier:
        preferred = get_document(preferred_identifier)
        if preferred and preferred.payload:
            return copy.deepcopy(preferred.payload)

    for cli_config_id in _CACHE_CLI_CONFIG_IDS:
        doc = _CACHE_ID.get(cli_config_id)
        if doc and doc.payload:
            return copy.deepcopy(doc.payload)
    return None


def materialize_seed_resources() -> Path:
    global _MATERIALIZED_ROOT
    if _MATERIALIZED_ROOT is not None and _MATERIALIZED_ROOT.exists():
        return _MATERIALIZED_ROOT

    root = Path(tempfile.mkdtemp(prefix="eon_preset_seed_"))
    for doc in iter_documents():
        output = root / _normalize_slashes(doc.storage_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(doc.payload, indent=2, ensure_ascii=False), encoding="utf-8", newline="\n")
    _MATERIALIZED_ROOT = root
    return root

from __future__ import annotations

from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any, Iterable

from slicer_v2.legacy_gcode_writer import SliceSettings


@dataclass(frozen=True)
class ProcessPreset:
    preset_id: str
    name: str
    vendor: str
    relative_path: str
    mapped_settings: dict[str, Any]


_SLICE_SETTING_KEYS = {field.name for field in fields(SliceSettings)}


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _candidate_index_paths() -> tuple[Path, ...]:
    root = _repo_root()
    return (
        root / "docs" / "_profile_storage_index.json",
        root / "App" / "docs" / "_profile_storage_index.json",
    )


def _normalize_settings(payload: object) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    normalized: dict[str, Any] = {}
    for key, value in payload.items():
        text = str(key).strip()
        if not text or text not in _SLICE_SETTING_KEYS:
            continue
        normalized[text] = value
    return normalized


def _load_from_storage_index(index_path: Path) -> list[ProcessPreset]:
    from profiles_import.storage import load_profile_storage_index

    index = load_profile_storage_index(str(index_path))
    presets: list[ProcessPreset] = []
    for record in index.records:
        if str(record.category).strip().casefold() != "process":
            continue
        name = str(record.name).strip()
        if not name:
            continue
        presets.append(
            ProcessPreset(
                preset_id=str(record.profile_id).strip(),
                name=name,
                vendor=str(record.vendor).strip(),
                relative_path=str(record.relative_path).strip(),
                mapped_settings=_normalize_settings(record.mapped_settings),
            )
        )
    presets.sort(key=lambda item: (item.name.casefold(), item.vendor.casefold(), item.preset_id.casefold()))
    return presets


def _load_from_embedded_presets() -> list[ProcessPreset]:
    from printer_presets import preset_store

    presets: list[ProcessPreset] = []
    for doc in preset_store.iter_documents("profiles"):
        if str(doc.category).strip().casefold() != "process":
            continue
        name = str(doc.name).strip()
        if not name:
            continue
        preset_id = str(doc.id).strip() or str(doc.storage_path).strip()
        presets.append(
            ProcessPreset(
                preset_id=preset_id,
                name=name,
                vendor=str(doc.vendor).strip(),
                relative_path=str(doc.relative_path).strip(),
                mapped_settings=_normalize_settings(doc.payload),
            )
        )
    presets.sort(key=lambda item: (item.name.casefold(), item.vendor.casefold(), item.preset_id.casefold()))
    return presets


def load_process_presets() -> list[ProcessPreset]:
    for path in _candidate_index_paths():
        if not path.exists():
            continue
        try:
            presets = _load_from_storage_index(path)
        except Exception:
            continue
        if presets:
            return presets
    return _load_from_embedded_presets()


def coerce_process_presets(items: Iterable[ProcessPreset | dict[str, Any]]) -> list[ProcessPreset]:
    presets: list[ProcessPreset] = []
    for item in items:
        if isinstance(item, ProcessPreset):
            presets.append(item)
            continue
        if not isinstance(item, dict):
            continue
        preset_id = str(item.get("preset_id") or item.get("id") or item.get("profile_id") or "").strip()
        name = str(item.get("name") or "").strip()
        if not preset_id or not name:
            continue
        presets.append(
            ProcessPreset(
                preset_id=preset_id,
                name=name,
                vendor=str(item.get("vendor") or "").strip(),
                relative_path=str(item.get("relative_path") or "").strip(),
                mapped_settings=_normalize_settings(item.get("mapped_settings", {})),
            )
        )
    presets.sort(key=lambda entry: (entry.name.casefold(), entry.vendor.casefold(), entry.preset_id.casefold()))
    return presets


def order_process_presets(presets: Iterable[ProcessPreset], printer: dict[str, Any] | None) -> list[ProcessPreset]:
    process_presets = list(presets)
    if not process_presets:
        return []
    printer = printer if isinstance(printer, dict) else {}

    printer_name = str(printer.get("name") or "").strip().casefold()
    printer_model = str(printer.get("model") or "").strip().casefold()
    printer_brand = str(printer.get("brand") or "").strip().casefold()
    default_profile = str(printer.get("default_print_profile") or "").strip().casefold()

    def score(entry: ProcessPreset) -> tuple[int, str, str]:
        text = entry.name.casefold()
        score_value = 0
        if default_profile:
            if text == default_profile:
                score_value += 1200
            elif default_profile in text:
                score_value += 500
        if printer_name:
            if f"@{printer_name}" in text:
                score_value += 300
            elif printer_name in text:
                score_value += 240
        if printer_model and printer_model in text:
            score_value += 180
        if printer_brand and printer_brand and printer_brand in entry.vendor.casefold():
            score_value += 80
        return (
            -score_value,
            entry.name.casefold(),
            entry.vendor.casefold(),
        )

    return sorted(process_presets, key=score)


def display_label_for_preset(entry: ProcessPreset, duplicate_name_count: int) -> str:
    if duplicate_name_count > 1 and entry.vendor:
        return f"{entry.name} [{entry.vendor}]"
    return entry.name


def find_preset_id_by_name(presets: Iterable[ProcessPreset], name: str) -> str | None:
    target = str(name or "").strip().casefold()
    if not target:
        return None
    for entry in presets:
        if entry.name.casefold() == target:
            return entry.preset_id
    return None


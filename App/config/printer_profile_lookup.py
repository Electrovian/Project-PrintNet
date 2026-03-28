from __future__ import annotations

import ast
import math
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping


@dataclass(frozen=True)
class MachinePresetRecord:
    path: Path
    name: str
    kind: str
    payload: dict[str, Any]


_ROOT = Path(__file__).resolve().parents[1]
_PROFILE_ROOT = _ROOT / "printer_presets" / "seed_resources" / "profiles"
_NOZZLE_SUFFIX_RE = re.compile(r"\s+\d+(?:\.\d+)?\s*nozzle\s*$", re.IGNORECASE)
_PAIR_RE = re.compile(r"(-?\d+(?:\.\d+)?)\s*[x,]\s*(-?\d+(?:\.\d+)?)", re.IGNORECASE)


def _normalize_name(value: object) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _strip_nozzle_suffix(value: object) -> str:
    text = str(value or "").strip()
    return _NOZZLE_SUFFIX_RE.sub("", text).strip()


def _as_float(value: object) -> float | None:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed) or parsed <= 0.0:
        return None
    return float(parsed)


def _as_number(value: object) -> float | None:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return float(parsed)


def _parse_data_dict(path: Path) -> dict[str, Any] | None:
    try:
        source = path.read_text(encoding="utf-8")
    except Exception:
        return None
    try:
        tree = ast.parse(source, filename=str(path))
    except Exception:
        return None
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "DATA":
                try:
                    payload = ast.literal_eval(node.value)
                except Exception:
                    return None
                if isinstance(payload, dict):
                    return dict(payload)
                return None
    return None


@lru_cache(maxsize=1)
def _index_machine_presets() -> tuple[dict[str, list[MachinePresetRecord]], dict[str, list[MachinePresetRecord]]]:
    by_name: dict[str, list[MachinePresetRecord]] = {}
    by_model: dict[str, list[MachinePresetRecord]] = {}
    for path in _PROFILE_ROOT.glob("*/machine/*.py"):
        payload = _parse_data_dict(path)
        if not payload:
            continue
        name = str(payload.get("name") or path.stem).strip() or path.stem
        kind = str(payload.get("type", "")).strip().lower()
        record = MachinePresetRecord(path=path, name=name, kind=kind, payload=payload)

        name_keys = {
            _normalize_name(name),
            _normalize_name(path.stem),
            _normalize_name(_strip_nozzle_suffix(name)),
            _normalize_name(_strip_nozzle_suffix(path.stem)),
        }
        for key in name_keys:
            if not key:
                continue
            by_name.setdefault(key, []).append(record)

        model_keys = {
            _normalize_name(payload.get("printer_model")),
            _normalize_name(payload.get("model_id")),
        }
        for key in model_keys:
            if not key:
                continue
            by_model.setdefault(key, []).append(record)
    return by_name, by_model


def _pick_record(candidates: list[MachinePresetRecord], preferred_kind: str | None = None) -> MachinePresetRecord | None:
    if not candidates:
        return None
    if preferred_kind:
        candidates = [record for record in candidates if record.kind == preferred_kind]
        if not candidates:
            return None
    # Prefer explicit nozzle presets for dimensions.
    return sorted(
        candidates,
        key=lambda record: (
            0 if "nozzle" in record.name.lower() else 1,
            len(record.name),
            str(record.path),
        ),
    )[0]


def _find_by_name(name: object, preferred_kind: str | None = None) -> MachinePresetRecord | None:
    key = _normalize_name(name)
    if not key:
        return None
    by_name, _by_model = _index_machine_presets()
    exact = list(by_name.get(key, []))
    picked = _pick_record(exact, preferred_kind=preferred_kind)
    if picked is not None:
        return picked

    fallback_key = _normalize_name(_strip_nozzle_suffix(name))
    if not fallback_key or fallback_key == key:
        return None
    return _pick_record(list(by_name.get(fallback_key, [])), preferred_kind=preferred_kind)


def _find_by_model_name(name: object, preferred_kind: str | None = None) -> MachinePresetRecord | None:
    key = _normalize_name(name)
    if not key:
        return None
    _by_name, by_model = _index_machine_presets()
    return _pick_record(list(by_model.get(key, [])), preferred_kind=preferred_kind)


def _parse_pair(value: object) -> tuple[float, float] | None:
    if isinstance(value, (list, tuple)):
        if len(value) < 2:
            return None
        x = _as_number(value[0])
        y = _as_number(value[1])
        if x is None or y is None:
            return None
        return (x, y)
    if isinstance(value, str):
        match = _PAIR_RE.search(value)
        if match is None:
            return None
        x = _as_number(match.group(1))
        y = _as_number(match.group(2))
        if x is None or y is None:
            return None
        return (x, y)
    return None


def _parse_printable_area(value: object) -> tuple[float, float] | None:
    points: list[tuple[float, float]] = []
    if isinstance(value, (list, tuple)):
        for item in value:
            pair = _parse_pair(item)
            if pair is not None:
                points.append(pair)
    elif isinstance(value, str):
        for group in _PAIR_RE.findall(value):
            x = _as_number(group[0])
            y = _as_number(group[1])
            if x is None or y is None:
                continue
            points.append((x, y))
    if len(points) < 2:
        return None
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    width = max(xs) - min(xs)
    depth = max(ys) - min(ys)
    if width <= 0.0 or depth <= 0.0:
        return None
    return (float(width), float(depth))


def _extract_geometry(payload: Mapping[str, Any]) -> tuple[float | None, float | None, float | None]:
    bed_x = _as_float(payload.get("bed_x"))
    bed_y = _as_float(payload.get("bed_y"))
    bed_z = _as_float(payload.get("bed_z"))

    if bed_x is None or bed_y is None:
        pair = _parse_pair(payload.get("bed_size"))
        if pair is not None:
            bed_x = bed_x if bed_x is not None else pair[0]
            bed_y = bed_y if bed_y is not None else pair[1]

    if bed_x is None or bed_y is None:
        area = _parse_printable_area(payload.get("printable_area"))
        if area is None:
            area = _parse_printable_area(payload.get("bed_shape"))
        if area is not None:
            bed_x = bed_x if bed_x is not None else area[0]
            bed_y = bed_y if bed_y is not None else area[1]

    if bed_x is None or bed_y is None:
        width = _as_float(payload.get("machine_width"))
        depth = _as_float(payload.get("machine_depth"))
        if width is not None and bed_x is None:
            bed_x = width
        if depth is not None and bed_y is None:
            bed_y = depth

    if bed_z is None:
        for key in ("max_height", "printable_height", "machine_height"):
            bed_z = _as_float(payload.get(key))
            if bed_z is not None:
                break

    return bed_x, bed_y, bed_z


def _resolve_asset_path(asset: object, source_path: Path | None) -> str:
    text = str(asset or "").strip()
    if not text:
        return ""

    candidate = Path(text)
    if candidate.is_file():
        try:
            return str(candidate.resolve())
        except Exception:
            return str(candidate)

    paths: list[Path] = []
    if source_path is not None:
        paths.append(source_path.parent / text)
        paths.append(source_path.parent.parent / text)
    paths.append(_PROFILE_ROOT / text)

    for path in paths:
        if path.is_file():
            try:
                return str(path.resolve())
            except Exception:
                return str(path)
    return ""


def _non_empty(payload: Mapping[str, Any], *keys: str) -> str:
    for key in keys:
        value = str(payload.get(key, "")).strip()
        if value:
            return value
    return ""


def resolve_printer_plate_config(printer: Mapping[str, Any] | None) -> dict[str, Any]:
    if not isinstance(printer, Mapping):
        return {
            "bed_x": None,
            "bed_y": None,
            "bed_z": None,
            "bed_texture_path": "",
            "bed_model_path": "",
            "machine_profile_path": "",
            "machine_model_path": "",
        }

    printer_geom = _extract_geometry(printer)
    machine = _find_by_name(printer.get("name"), preferred_kind="machine")
    model = _find_by_name(printer.get("name"), preferred_kind="machine_model")

    if machine is None:
        machine = _find_by_model_name(printer.get("printer_model"), preferred_kind="machine")
    if model is None:
        model = _find_by_model_name(printer.get("printer_model"), preferred_kind="machine_model")

    if machine is not None:
        model_name = _non_empty(machine.payload, "printer_model", "model_id")
        if model_name:
            linked_model = _find_by_model_name(model_name, preferred_kind="machine_model")
            if linked_model is not None:
                model = linked_model

    machine_geom = _extract_geometry(machine.payload) if machine is not None else (None, None, None)
    model_geom = _extract_geometry(model.payload) if model is not None else (None, None, None)

    bed_x = printer_geom[0] or machine_geom[0] or model_geom[0]
    bed_y = printer_geom[1] or machine_geom[1] or model_geom[1]
    bed_z = printer_geom[2] or machine_geom[2] or model_geom[2]

    texture_ref = _non_empty(printer, "bed_custom_texture", "bed_texture")
    texture_source = None
    if not texture_ref and machine is not None:
        texture_ref = _non_empty(machine.payload, "bed_custom_texture", "bed_texture")
        texture_source = machine.path
    if not texture_ref and model is not None:
        texture_ref = _non_empty(model.payload, "bed_custom_texture", "bed_texture")
        texture_source = model.path
    if texture_source is None:
        texture_source = machine.path if machine is not None else (model.path if model is not None else None)
    texture_path = _resolve_asset_path(texture_ref, texture_source)

    model_ref = _non_empty(printer, "bed_custom_model", "bed_model")
    model_source = None
    if not model_ref and machine is not None:
        model_ref = _non_empty(machine.payload, "bed_custom_model", "bed_model")
        model_source = machine.path
    if not model_ref and model is not None:
        model_ref = _non_empty(model.payload, "bed_custom_model", "bed_model")
        model_source = model.path
    if model_source is None:
        model_source = machine.path if machine is not None else (model.path if model is not None else None)
    model_path = _resolve_asset_path(model_ref, model_source)

    return {
        "bed_x": bed_x,
        "bed_y": bed_y,
        "bed_z": bed_z,
        "bed_texture_path": texture_path,
        "bed_model_path": model_path,
        "machine_profile_path": str(machine.path) if machine is not None else "",
        "machine_model_path": str(model.path) if model is not None else "",
    }

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
import math
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


_DEFAULT_BED_X_MM = 220.0
_DEFAULT_BED_Y_MM = 220.0
_DEFAULT_BED_Z_MM = 250.0
_ALLOWED_FIRMWARES = {"marlin", "klipper", "prusalink", "generic"}
_END_MACRO_OWNERSHIP = {"END_PRINT", "PRINT_END"}


def _as_payload(value: object | None) -> dict[str, object]:
    if value is None:
        return {}
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, Mapping):
        return {str(key): item for key, item in value.items()}
    if hasattr(value, "__dict__"):
        return {
            str(key): item
            for key, item in vars(value).items()
            if not str(key).startswith("_")
        }
    return {}


def _parse_float(value: object, *, minimum: float | None = None) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (list, tuple)):
        for item in value:
            parsed = _parse_float(item, minimum=minimum)
            if parsed is not None:
                return parsed
        return None
    try:
        parsed = float(value)
    except (TypeError, ValueError, OverflowError):
        text = str(value or "").strip()
        if not text:
            return None
        try:
            parsed = float(text)
        except (TypeError, ValueError, OverflowError):
            return None
    if not math.isfinite(parsed):
        return None
    if minimum is not None and parsed < minimum:
        return None
    return float(parsed)


def _normalize_macro_lines(value: Sequence[str] | str | None) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        items = value.splitlines()
    elif isinstance(value, (list, tuple)):
        items = value
    else:
        return []
    lines: list[str] = []
    for item in items:
        text = str(item or "").rstrip()
        if text.strip():
            lines.append(text)
    return lines


def _first_macro_lines(*candidates: object) -> list[str]:
    for candidate in candidates:
        lines = _normalize_macro_lines(candidate)
        if lines:
            return lines
    return []


def _first_float(*candidates: object, minimum: float | None = None, fallback: float | None = None) -> float | None:
    for candidate in candidates:
        parsed = _parse_float(candidate, minimum=minimum)
        if parsed is not None:
            return parsed
    return fallback


def _first_bool(*candidates: object) -> bool | None:
    for candidate in candidates:
        if isinstance(candidate, bool):
            return candidate
        text = str(candidate or "").strip().lower()
        if text in {"true", "1", "yes", "on"}:
            return True
        if text in {"false", "0", "no", "off"}:
            return False
    return None


def _normalize_firmware(value: object | None, *, fallback: str = "marlin") -> str:
    text = str(value or "").strip().lower()
    if text in _ALLOWED_FIRMWARES:
        return text
    aliases = {
        "reprap": "marlin",
        "prusa": "prusalink",
        "prusa_link": "prusalink",
        "moonraker": "klipper",
    }
    if text in aliases:
        return aliases[text]
    return fallback


def _infer_firmware_from_printer(printer: Mapping[str, object] | None) -> str | None:
    if not isinstance(printer, Mapping):
        return None
    for key in ("gcode_firmware_flavor", "firmware_flavor", "gcode_flavor", "firmware_type"):
        value = printer.get(key)
        if value is None:
            continue
        normalized = _normalize_firmware(value, fallback="")
        if normalized:
            return normalized
    connector_type = str(printer.get("connector_type", "")).strip().lower()
    if "moonraker" in connector_type or "klipper" in connector_type:
        return "klipper"
    if "prusalink" in connector_type:
        return "prusalink"
    return None


def _resolve_printer_plate_config(printer: Mapping[str, object] | None) -> dict[str, object]:
    if not isinstance(printer, Mapping):
        return {}
    try:
        from config.printer_profile_lookup import resolve_printer_plate_config

        return dict(resolve_printer_plate_config(printer) or {})
    except Exception:
        return {}


def _settings_value(payload: Mapping[str, object], *keys: str) -> object | None:
    for key in keys:
        if key in payload:
            return payload.get(key)
    return None


def _printer_value(printer: Mapping[str, object] | None, *keys: str) -> object | None:
    if not isinstance(printer, Mapping):
        return None
    for key in keys:
        if key in printer:
            return printer.get(key)
    return None


def _runtime_value(runtime_printer_state: object | None, key: str) -> object | None:
    if runtime_printer_state is None:
        return None
    if isinstance(runtime_printer_state, Mapping):
        return runtime_printer_state.get(key)
    return getattr(runtime_printer_state, key, None)


def _format_number(value: float, digits: int = 3) -> str:
    text = f"{float(value):.{digits}f}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    if text in {"-0", "-0.0"}:
        return "0"
    return text


def resolve_absolute_extrusion(firmware_flavor: object | None, explicit_value: object | None) -> bool:
    explicit = _first_bool(explicit_value)
    if explicit is not None:
        return explicit
    firmware = _normalize_firmware(firmware_flavor)
    return firmware != "klipper"


@dataclass(frozen=True)
class GCodeOutputContract:
    bed_x_mm: float
    bed_y_mm: float
    firmware_flavor: str
    absolute_extrusion: bool
    startup_macro_lines: tuple[str, ...]
    end_macro_lines: tuple[str, ...]
    nozzle_temperature_c: float | None = None
    bed_temperature_c: float | None = None


def build_output_contract(
    *,
    bed_x_mm: object = _DEFAULT_BED_X_MM,
    bed_y_mm: object = _DEFAULT_BED_Y_MM,
    firmware_flavor: object = "marlin",
    absolute_extrusion: object | None = None,
    startup_macro: Sequence[str] | str | None = (),
    end_macro: Sequence[str] | str | None = (),
    nozzle_temperature_c: object | None = None,
    bed_temperature_c: object | None = None,
) -> GCodeOutputContract:
    firmware = _normalize_firmware(firmware_flavor)
    resolved_absolute_extrusion = resolve_absolute_extrusion(firmware, absolute_extrusion)
    normalized_startup = tuple(_normalize_macro_lines(startup_macro))
    normalized_end = tuple(_normalize_macro_lines(end_macro))
    nozzle_temp = _parse_float(nozzle_temperature_c, minimum=0.0)
    bed_temp = _parse_float(bed_temperature_c, minimum=0.0)
    if not normalized_startup and firmware == "klipper" and nozzle_temp is not None and bed_temp is not None:
        normalized_startup = (
            f"M190 S{_format_number(bed_temp, 2)}",
            f"M109 S{_format_number(nozzle_temp, 2)}",
            f"PRINT_START EXTRUDER={_format_number(nozzle_temp, 2)} BED={_format_number(bed_temp, 2)}",
        )
    bed_x = _first_float(bed_x_mm, minimum=1.0, fallback=_DEFAULT_BED_X_MM)
    bed_y = _first_float(bed_y_mm, minimum=1.0, fallback=_DEFAULT_BED_Y_MM)
    return GCodeOutputContract(
        bed_x_mm=float(bed_x or _DEFAULT_BED_X_MM),
        bed_y_mm=float(bed_y or _DEFAULT_BED_Y_MM),
        firmware_flavor=firmware,
        absolute_extrusion=bool(resolved_absolute_extrusion),
        startup_macro_lines=normalized_startup,
        end_macro_lines=normalized_end,
        nozzle_temperature_c=nozzle_temp,
        bed_temperature_c=bed_temp,
    )


def build_setup_lines(contract: GCodeOutputContract, *, header_comment: str) -> list[str]:
    lines = [
        f"; {header_comment}",
        f"; firmware={contract.firmware_flavor}",
        "G21 ; mm units",
        "G90 ; absolute XYZ mode",
    ]
    lines.extend(contract.startup_macro_lines)
    lines.append("M82 ; absolute extrusion" if contract.absolute_extrusion else "M83 ; relative extrusion")
    lines.append("G92 E0")
    return lines


def _macro_first_token(line: str) -> str:
    text = str(line or "").strip()
    if not text or text.startswith(";"):
        return ""
    command = text.split(";", 1)[0].strip()
    if not command:
        return ""
    return command.split()[0].strip().upper()


def _macro_contains(line: str, needle: str) -> bool:
    return needle.upper() in str(line or "").upper()


def build_teardown_lines(contract: GCodeOutputContract) -> list[str]:
    lines = list(contract.end_macro_lines)
    tokens = {_macro_first_token(line) for line in contract.end_macro_lines}
    owns_all_shutdown = bool(tokens & _END_MACRO_OWNERSHIP)
    owns_hotend = owns_all_shutdown or "M104" in tokens or "TURN_OFF_HEATERS" in tokens
    owns_bed = owns_all_shutdown or "M140" in tokens or "TURN_OFF_HEATERS" in tokens
    owns_motors = owns_all_shutdown or "M84" in tokens or "M18" in tokens
    owns_reset_e = owns_all_shutdown or any(_macro_contains(line, "G92 E") for line in contract.end_macro_lines)
    if not owns_hotend:
        lines.append("M104 S0")
    if not owns_bed:
        lines.append("M140 S0")
    if not owns_reset_e:
        lines.append("G92 E0")
    if not owns_motors:
        lines.append("M84")
    return lines


def translate_xy_to_bed(x: float, y: float, bed_x_mm: float, bed_y_mm: float) -> tuple[float, float]:
    return (float(x) + (float(bed_x_mm) * 0.5), float(y) + (float(bed_y_mm) * 0.5))


def resolve_output_settings_payload(
    settings: object | None,
    *,
    runtime_printer_state: object | None = None,
    printer: Mapping[str, object] | None = None,
) -> dict[str, object]:
    payload = _as_payload(settings)
    printer_payload = dict(printer) if isinstance(printer, Mapping) else {}
    plate_payload = _resolve_printer_plate_config(printer_payload)

    firmware = _normalize_firmware(
        _infer_firmware_from_printer(printer_payload)
        or _settings_value(payload, "gcode_firmware_flavor", "firmware_flavor")
        or "marlin"
    )
    absolute_extrusion = resolve_absolute_extrusion(
        firmware,
        _settings_value(payload, "gcode_absolute_extrusion", "absolute_extrusion"),
    )
    start_gcode = _first_macro_lines(
        _settings_value(payload, "gcode_startup_macro", "start_gcode"),
        _printer_value(printer_payload, "gcode_startup_macro", "start_gcode", "machine_start_gcode"),
    )
    end_gcode = _first_macro_lines(
        _settings_value(payload, "gcode_end_macro", "end_gcode"),
        _printer_value(printer_payload, "gcode_end_macro", "end_gcode", "machine_end_gcode"),
    )

    bed_x = _first_float(
        _runtime_value(runtime_printer_state, "bed_x"),
        _printer_value(printer_payload, "bed_x"),
        plate_payload.get("bed_x"),
        _settings_value(payload, "bed_x", "gcode_validation_bed_x_mm"),
        minimum=1.0,
        fallback=_DEFAULT_BED_X_MM,
    )
    bed_y = _first_float(
        _runtime_value(runtime_printer_state, "bed_y"),
        _printer_value(printer_payload, "bed_y"),
        plate_payload.get("bed_y"),
        _settings_value(payload, "bed_y", "gcode_validation_bed_y_mm"),
        minimum=1.0,
        fallback=_DEFAULT_BED_Y_MM,
    )
    bed_z = _first_float(
        _runtime_value(runtime_printer_state, "bed_z"),
        _printer_value(printer_payload, "bed_z"),
        plate_payload.get("bed_z"),
        _settings_value(payload, "bed_z", "gcode_validation_bed_z_mm"),
        minimum=1.0,
        fallback=_DEFAULT_BED_Z_MM,
    )
    nozzle_temp = _first_float(
        _settings_value(payload, "nozzle_temperature_c", "nozzle_temperature", "nozzle_temperature_initial_layer"),
        _printer_value(
            printer_payload,
            "nozzle_temperature_c",
            "nozzle_temperature",
            "nozzle_temperature_initial_layer",
        ),
        minimum=0.0,
    )
    bed_temp = _first_float(
        _settings_value(payload, "bed_temperature_c", "bed_temperature", "bed_temperature_initial_layer"),
        _printer_value(
            printer_payload,
            "bed_temperature_c",
            "bed_temperature",
            "bed_temperature_initial_layer",
            "bed_temperature_initial_layer_single",
        ),
        minimum=0.0,
    )

    payload["firmware_flavor"] = firmware
    payload["gcode_firmware_flavor"] = firmware
    payload["gcode_absolute_extrusion"] = bool(absolute_extrusion)
    payload["absolute_extrusion"] = bool(absolute_extrusion)
    payload["start_gcode"] = start_gcode
    payload["gcode_startup_macro"] = list(start_gcode)
    payload["end_gcode"] = end_gcode
    payload["gcode_end_macro"] = list(end_gcode)
    payload["bed_x"] = float(bed_x or _DEFAULT_BED_X_MM)
    payload["bed_y"] = float(bed_y or _DEFAULT_BED_Y_MM)
    payload["gcode_validation_bed_x_mm"] = float(bed_x or _DEFAULT_BED_X_MM)
    payload["gcode_validation_bed_y_mm"] = float(bed_y or _DEFAULT_BED_Y_MM)
    payload["gcode_validation_bed_z_mm"] = float(bed_z or _DEFAULT_BED_Z_MM)
    payload["gcode_validation_allow_negative_xy"] = False
    payload["nozzle_temperature_c"] = nozzle_temp
    payload["bed_temperature_c"] = bed_temp
    return payload

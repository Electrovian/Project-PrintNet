from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .inheritance import (
    ProfileInheritanceReport,
    ResolvedProfileDocument,
    discover_and_resolve_profile_inheritance,
)
from .source_resolver import resolve_profile_source_root


RESERVED_RESOLVED_KEYS = {
    "name",
    "type",
    "inherits_chain",
    "inherits_chain_files",
}

TRUTHY_VALUES = {"1", "true", "yes", "on", "enabled"}
FALSY_VALUES = {"0", "false", "no", "off", "disabled"}

SEAM_POSITION_VALUES = {
    "nearest": "nearest",
    "aligned": "aligned",
    "rear": "rear",
    "back": "rear",
    "random": "random",
}

INFILL_PATTERN_VALUES = {
    "rectilinear": "rectilinear",
    "grid": "grid",
    "gyroid": "gyroid",
    "triangles": "triangle",
    "triangle": "triangle",
}

SUPPORT_PATTERN_VALUES = {
    "rectilinear": "rectilinear",
    "grid": "grid",
    "triangle": "triangle",
}

FIRMWARE_VALUES = {
    "marlin": "marlin",
    "reprap": "marlin",
    "prusa": "marlin",
    "prusalink": "marlin",
    "klipper": "klipper",
}


class ProfileMappingError(ValueError):
    """Raised when resolved profile mapping fails."""


@dataclass
class MappedProfileSettings:
    vendor: str
    category: str
    name: str
    relative_path: str
    mapped_settings: dict
    mapped_key_count: int
    unknown_keys: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class ProfileSettingsMappingReport:
    source_path: str
    mapped_at_utc: str
    profile_count: int
    mapped_profile_count: int
    machine_mapped_count: int
    process_mapped_count: int
    filament_mapped_count: int
    unknown_key_count: int
    warning_count: int
    warnings: list[str] = field(default_factory=list)
    profiles: list[MappedProfileSettings] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def _first_key(data: dict, keys: Iterable[str]) -> tuple[str | None, object | None]:
    for key in keys:
        if key in data:
            return key, data.get(key)
    return None, None


def _parse_float_value(value: object) -> float:
    if isinstance(value, (int, float, str, bytes, bytearray)):
        return float(value)
    return float(str(value).strip())


def _to_float(
    value: object,
    *,
    warning_context: str,
    warnings: list[str],
    minimum: float | None = None,
    maximum: float | None = None,
) -> float | None:
    if value is None:
        return None
    try:
        result = _parse_float_value(value)
    except (TypeError, ValueError, OverflowError):
        warnings.append(f"{warning_context}:invalid_float:{value}")
        return None
    if minimum is not None and result < minimum:
        result = minimum
    if maximum is not None and result > maximum:
        result = maximum
    return result


def _to_int(
    value: object,
    *,
    warning_context: str,
    warnings: list[str],
    minimum: int | None = None,
    maximum: int | None = None,
) -> int | None:
    if value is None:
        return None
    try:
        result = int(_parse_float_value(value))
    except (TypeError, ValueError, OverflowError):
        warnings.append(f"{warning_context}:invalid_int:{value}")
        return None
    if minimum is not None and result < minimum:
        result = minimum
    if maximum is not None and result > maximum:
        result = maximum
    return result


def _to_bool(value: object, *, warning_context: str, warnings: list[str]) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in TRUTHY_VALUES:
        return True
    if text in FALSY_VALUES:
        return False
    warnings.append(f"{warning_context}:invalid_bool:{value}")
    return None


def _to_percent(
    value: object,
    *,
    warning_context: str,
    warnings: list[str],
) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    has_percent = text.endswith("%")
    if has_percent:
        text = text[:-1].strip()
    try:
        numeric = float(text)
    except (TypeError, ValueError):
        warnings.append(f"{warning_context}:invalid_percent:{value}")
        return None
    if not has_percent and 0.0 <= numeric <= 1.0:
        numeric *= 100.0
    if numeric < 0.0:
        numeric = 0.0
    if numeric > 100.0:
        numeric = 100.0
    return numeric


def _to_ratio(
    value: object,
    *,
    warning_context: str,
    warnings: list[str],
) -> float | None:
    if value is None:
        return None
    try:
        numeric = _parse_float_value(value)
    except (TypeError, ValueError, OverflowError):
        warnings.append(f"{warning_context}:invalid_ratio:{value}")
        return None
    if numeric > 10.0:
        numeric /= 100.0
    if numeric < 0.0:
        numeric = 0.0
    return numeric


def _normalize_gcode_lines(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [line.rstrip() for line in value.splitlines() if line.strip()]
    if isinstance(value, (list, tuple)):
        lines: list[str] = []
        for item in value:
            if item is None:
                continue
            line = str(item).rstrip()
            if line.strip():
                lines.append(line)
        return lines
    return []


def _normalize_firmware(value: object) -> str | None:
    if value is None:
        return None
    normalized = str(value).strip().lower()
    if not normalized:
        return None
    return FIRMWARE_VALUES.get(normalized, "marlin")


def _parse_bed_shape(
    value: object,
    *,
    warning_context: str,
    warnings: list[str],
) -> tuple[float, float] | None:
    if value is None:
        return None

    points: list[tuple[float, float]] = []
    if isinstance(value, str):
        tokens = re.findall(r"(-?\d+(?:\.\d+)?)x(-?\d+(?:\.\d+)?)", value)
        for token in tokens:
            points.append((float(token[0]), float(token[1])))
    elif isinstance(value, (list, tuple)):
        for item in value:
            if not isinstance(item, (list, tuple)) or len(item) < 2:
                continue
            try:
                points.append((float(item[0]), float(item[1])))
            except (TypeError, ValueError):
                continue
    else:
        warnings.append(f"{warning_context}:invalid_bed_shape:{value}")
        return None

    if len(points) < 2:
        warnings.append(f"{warning_context}:insufficient_bed_shape_points")
        return None

    min_x = min(point[0] for point in points)
    max_x = max(point[0] for point in points)
    min_y = min(point[1] for point in points)
    max_y = max(point[1] for point in points)
    size_x = max(0.0, max_x - min_x)
    size_y = max(0.0, max_y - min_y)
    return size_x, size_y


def _normalize_seam_position(value: object) -> str | None:
    if value is None:
        return None
    normalized = str(value).strip().lower()
    if not normalized:
        return None
    return SEAM_POSITION_VALUES.get(normalized, "aligned")


def _normalize_pattern(
    value: object,
    *,
    allowed_values: dict[str, str],
) -> str | None:
    if value is None:
        return None
    normalized = str(value).strip().lower()
    if not normalized:
        return None
    return allowed_values.get(normalized, next(iter(allowed_values.values())))


def _map_machine_profile(
    profile: ResolvedProfileDocument,
) -> tuple[dict, set[str], list[str]]:
    data = profile.resolved_data
    mapped: dict = {}
    mapped_source_keys: set[str] = set()
    warnings = [f"{profile.vendor}: {warn}" for warn in profile.warnings]
    context_prefix = f"{profile.vendor}:machine:{profile.name}"

    key, value = _first_key(data, ("nozzle_diameter", "default_nozzle_diameter", "nozzle_size"))
    if key:
        mapped_source_keys.add(key)
        numeric = _to_float(value, warning_context=f"{context_prefix}:{key}", warnings=warnings, minimum=0.1)
        if numeric is not None:
            mapped["nozzle_diameter"] = numeric

    key, value = _first_key(data, ("filament_diameter", "filament_size"))
    if key:
        mapped_source_keys.add(key)
        numeric = _to_float(value, warning_context=f"{context_prefix}:{key}", warnings=warnings, minimum=1.0)
        if numeric is not None:
            mapped["filament_diameter"] = numeric

    key, value = _first_key(data, ("gcode_flavor", "firmware_type"))
    if key:
        mapped_source_keys.add(key)
        normalized = _normalize_firmware(value)
        if normalized:
            mapped["firmware_flavor"] = normalized

    key, value = _first_key(data, ("machine_start_gcode", "start_gcode"))
    if key:
        mapped_source_keys.add(key)
        lines = _normalize_gcode_lines(value)
        if lines:
            mapped["start_gcode"] = lines

    key, value = _first_key(data, ("machine_end_gcode", "end_gcode"))
    if key:
        mapped_source_keys.add(key)
        lines = _normalize_gcode_lines(value)
        if lines:
            mapped["end_gcode"] = lines

    key, value = _first_key(data, ("bed_shape", "printable_area"))
    if key:
        mapped_source_keys.add(key)
        bed_size = _parse_bed_shape(value, warning_context=f"{context_prefix}:{key}", warnings=warnings)
        if bed_size:
            mapped["bed_x"] = bed_size[0]
            mapped["bed_y"] = bed_size[1]

    key, value = _first_key(data, ("bed_x", "machine_width", "printable_width"))
    if key:
        mapped_source_keys.add(key)
        numeric = _to_float(value, warning_context=f"{context_prefix}:{key}", warnings=warnings, minimum=1.0)
        if numeric is not None:
            mapped["bed_x"] = numeric

    key, value = _first_key(data, ("bed_y", "machine_depth", "printable_depth"))
    if key:
        mapped_source_keys.add(key)
        numeric = _to_float(value, warning_context=f"{context_prefix}:{key}", warnings=warnings, minimum=1.0)
        if numeric is not None:
            mapped["bed_y"] = numeric

    key, value = _first_key(data, ("bed_z", "machine_height", "printable_height", "max_print_height"))
    if key:
        mapped_source_keys.add(key)
        numeric = _to_float(value, warning_context=f"{context_prefix}:{key}", warnings=warnings, minimum=1.0)
        if numeric is not None:
            mapped["bed_z"] = numeric

    return mapped, mapped_source_keys, warnings


def _map_process_profile(
    profile: ResolvedProfileDocument,
) -> tuple[dict, set[str], list[str]]:
    data = profile.resolved_data
    mapped: dict = {}
    mapped_source_keys: set[str] = set()
    warnings = [f"{profile.vendor}: {warn}" for warn in profile.warnings]
    context_prefix = f"{profile.vendor}:process:{profile.name}"

    key, value = _first_key(data, ("layer_height",))
    if key:
        mapped_source_keys.add(key)
        numeric = _to_float(
            value,
            warning_context=f"{context_prefix}:{key}",
            warnings=warnings,
            minimum=0.01,
            maximum=1.0,
        )
        if numeric is not None:
            mapped["layer_height"] = numeric

    key, value = _first_key(data, ("first_layer_height",))
    if key:
        mapped_source_keys.add(key)
        numeric = _to_float(
            value,
            warning_context=f"{context_prefix}:{key}",
            warnings=warnings,
            minimum=0.01,
            maximum=1.0,
        )
        if numeric is not None:
            mapped["first_layer_height"] = numeric

    key, value = _first_key(data, ("line_width", "default_line_width"))
    if key:
        mapped_source_keys.add(key)
        numeric = _to_float(
            value,
            warning_context=f"{context_prefix}:{key}",
            warnings=warnings,
            minimum=0.1,
            maximum=2.0,
        )
        if numeric is not None:
            mapped["extrusion_width"] = numeric

    key, value = _first_key(data, ("wall_loops", "perimeters", "wall_line_count"))
    if key:
        mapped_source_keys.add(key)
        numeric = _to_int(
            value,
            warning_context=f"{context_prefix}:{key}",
            warnings=warnings,
            minimum=1,
            maximum=20,
        )
        if numeric is not None:
            mapped["perimeter_count"] = numeric

    key, value = _first_key(data, ("top_shell_layers", "top_layers"))
    if key:
        mapped_source_keys.add(key)
        numeric = _to_int(
            value,
            warning_context=f"{context_prefix}:{key}",
            warnings=warnings,
            minimum=0,
            maximum=50,
        )
        if numeric is not None:
            mapped["top_layers"] = numeric

    key, value = _first_key(data, ("bottom_shell_layers", "bottom_layers"))
    if key:
        mapped_source_keys.add(key)
        numeric = _to_int(
            value,
            warning_context=f"{context_prefix}:{key}",
            warnings=warnings,
            minimum=0,
            maximum=50,
        )
        if numeric is not None:
            mapped["bottom_layers"] = numeric

    key, value = _first_key(data, ("sparse_infill_density", "infill_density", "infill_percent", "fill_density"))
    if key:
        mapped_source_keys.add(key)
        percent = _to_percent(value, warning_context=f"{context_prefix}:{key}", warnings=warnings)
        if percent is not None:
            mapped["infill_percent"] = percent

    key, value = _first_key(data, ("sparse_infill_pattern", "infill_pattern"))
    if key:
        mapped_source_keys.add(key)
        pattern = _normalize_pattern(value, allowed_values=INFILL_PATTERN_VALUES)
        if pattern:
            mapped["infill_pattern"] = pattern

    key, value = _first_key(data, ("outer_wall_speed", "default_speed", "print_speed"))
    if key:
        mapped_source_keys.add(key)
        numeric = _to_float(
            value,
            warning_context=f"{context_prefix}:{key}",
            warnings=warnings,
            minimum=1.0,
            maximum=600.0,
        )
        if numeric is not None:
            mapped["print_speed"] = numeric

    key, value = _first_key(data, ("travel_speed",))
    if key:
        mapped_source_keys.add(key)
        numeric = _to_float(
            value,
            warning_context=f"{context_prefix}:{key}",
            warnings=warnings,
            minimum=1.0,
            maximum=1000.0,
        )
        if numeric is not None:
            mapped["travel_speed"] = numeric

    key, value = _first_key(data, ("seam_position",))
    if key:
        mapped_source_keys.add(key)
        seam = _normalize_seam_position(value)
        if seam:
            mapped["seam_position"] = seam

    key, value = _first_key(data, ("enable_support", "support_enable", "support"))
    if key:
        mapped_source_keys.add(key)
        enabled = _to_bool(value, warning_context=f"{context_prefix}:{key}", warnings=warnings)
        if enabled is not None:
            mapped["support_enabled"] = enabled

    key, value = _first_key(data, ("support_type",))
    if key:
        mapped_source_keys.add(key)
        normalized = str(value).strip().lower()
        if normalized:
            mapped["support_type"] = "tree" if "tree" in normalized else "normal"

    key, value = _first_key(data, ("support_top_z_distance", "support_z_distance"))
    if key:
        mapped_source_keys.add(key)
        numeric = _to_float(
            value,
            warning_context=f"{context_prefix}:{key}",
            warnings=warnings,
            minimum=0.0,
            maximum=5.0,
        )
        if numeric is not None:
            mapped["support_z_gap"] = numeric

    key, value = _first_key(data, ("support_object_xy_distance", "support_xy_distance"))
    if key:
        mapped_source_keys.add(key)
        numeric = _to_float(
            value,
            warning_context=f"{context_prefix}:{key}",
            warnings=warnings,
            minimum=0.0,
            maximum=10.0,
        )
        if numeric is not None:
            mapped["support_xy_gap"] = numeric

    key, value = _first_key(data, ("support_base_pattern", "support_pattern"))
    if key:
        mapped_source_keys.add(key)
        pattern = _normalize_pattern(value, allowed_values=SUPPORT_PATTERN_VALUES)
        if pattern:
            mapped["support_pattern"] = pattern

    key, value = _first_key(data, ("support_interface_pattern",))
    if key:
        mapped_source_keys.add(key)
        pattern = _normalize_pattern(value, allowed_values=SUPPORT_PATTERN_VALUES)
        if pattern:
            mapped["support_interface_pattern"] = pattern

    key, value = _first_key(data, ("brim_width",))
    if key:
        mapped_source_keys.add(key)
        numeric = _to_float(
            value,
            warning_context=f"{context_prefix}:{key}",
            warnings=warnings,
            minimum=0.0,
            maximum=20.0,
        )
        if numeric is not None:
            mapped["brim_width"] = numeric

    key, value = _first_key(data, ("ironing_type",))
    if key:
        mapped_source_keys.add(key)
        normalized = str(value).strip().lower()
        if normalized:
            mapped["ironing_type"] = normalized

    return mapped, mapped_source_keys, warnings


def _map_filament_profile(
    profile: ResolvedProfileDocument,
) -> tuple[dict, set[str], list[str]]:
    data = profile.resolved_data
    mapped: dict = {}
    mapped_source_keys: set[str] = set()
    warnings = [f"{profile.vendor}: {warn}" for warn in profile.warnings]
    context_prefix = f"{profile.vendor}:filament:{profile.name}"

    key, value = _first_key(data, ("filament_type", "name"))
    if key:
        mapped_source_keys.add(key)
        text = str(value).strip()
        if text:
            mapped["filament_name"] = text

    key, value = _first_key(data, ("filament_colour", "filament_color", "filament_colour_hex"))
    if key:
        mapped_source_keys.add(key)
        text = str(value).strip()
        if text:
            mapped["filament_color"] = text

    key, value = _first_key(data, ("filament_density",))
    if key:
        mapped_source_keys.add(key)
        numeric = _to_float(
            value,
            warning_context=f"{context_prefix}:{key}",
            warnings=warnings,
            minimum=0.1,
            maximum=10.0,
        )
        if numeric is not None:
            mapped["filament_density"] = numeric

    key, value = _first_key(data, ("filament_diameter",))
    if key:
        mapped_source_keys.add(key)
        numeric = _to_float(
            value,
            warning_context=f"{context_prefix}:{key}",
            warnings=warnings,
            minimum=1.0,
            maximum=5.0,
        )
        if numeric is not None:
            mapped["filament_diameter"] = numeric

    key, value = _first_key(data, ("filament_flow_ratio", "flow_ratio", "extrusion_multiplier"))
    if key:
        mapped_source_keys.add(key)
        ratio = _to_ratio(value, warning_context=f"{context_prefix}:{key}", warnings=warnings)
        if ratio is not None:
            mapped["extrusion_multiplier"] = ratio

    return mapped, mapped_source_keys, warnings


def _map_single_profile(profile: ResolvedProfileDocument) -> MappedProfileSettings:
    if profile.category == "machine":
        mapped_settings, mapped_source_keys, warnings = _map_machine_profile(profile)
    elif profile.category == "process":
        mapped_settings, mapped_source_keys, warnings = _map_process_profile(profile)
    elif profile.category == "filament":
        mapped_settings, mapped_source_keys, warnings = _map_filament_profile(profile)
    else:
        mapped_settings = {}
        mapped_source_keys = set()
        warnings = [f"{profile.vendor}:unknown_category:{profile.category}:{profile.relative_path}"]

    unknown_keys = sorted(
        key
        for key in profile.resolved_data.keys()
        if key not in mapped_source_keys and key not in RESERVED_RESOLVED_KEYS
    )

    return MappedProfileSettings(
        vendor=profile.vendor,
        category=profile.category,
        name=profile.name,
        relative_path=profile.relative_path,
        mapped_settings=mapped_settings,
        mapped_key_count=len(mapped_settings),
        unknown_keys=unknown_keys,
        warnings=warnings,
    )


def map_resolved_profiles_to_settings(
    source_path: str,
    inheritance_report: ProfileInheritanceReport,
    *,
    strict: bool = False,
) -> ProfileSettingsMappingReport:
    source_root = resolve_profile_source_root(
        source_path,
        error_factory=ProfileMappingError,
    )

    mapped_profiles: list[MappedProfileSettings] = []
    warnings: list[str] = []

    machine_count = 0
    process_count = 0
    filament_count = 0
    unknown_key_count = 0

    for profile in inheritance_report.resolved_profiles:
        mapped = _map_single_profile(profile)
        mapped_profiles.append(mapped)
        warnings.extend(mapped.warnings)
        unknown_key_count += len(mapped.unknown_keys)
        if mapped.mapped_key_count > 0:
            if mapped.category == "machine":
                machine_count += 1
            elif mapped.category == "process":
                process_count += 1
            elif mapped.category == "filament":
                filament_count += 1

    report = ProfileSettingsMappingReport(
        source_path=str(source_root.resolve()),
        mapped_at_utc=datetime.now(timezone.utc).isoformat(),
        profile_count=len(inheritance_report.resolved_profiles),
        mapped_profile_count=sum(1 for profile in mapped_profiles if profile.mapped_key_count > 0),
        machine_mapped_count=machine_count,
        process_mapped_count=process_count,
        filament_mapped_count=filament_count,
        unknown_key_count=unknown_key_count,
        warning_count=len(warnings),
        warnings=warnings,
        profiles=mapped_profiles,
    )

    if strict and report.warning_count > 0:
        raise ProfileMappingError(f"STRICT_MAPPING_WARNING_FAILURE: {report.warning_count} warning(s)")

    return report


def discover_resolve_and_map_profiles(
    source_path: str,
    *,
    discovery_strict: bool = False,
    inheritance_strict: bool = False,
    mapping_strict: bool = False,
    vendor_limit: int | None = None,
    max_chain_depth: int = 64,
) -> ProfileSettingsMappingReport:
    inheritance_report = discover_and_resolve_profile_inheritance(
        source_path,
        discovery_strict=discovery_strict,
        inheritance_strict=inheritance_strict,
        vendor_limit=vendor_limit,
        max_chain_depth=max_chain_depth,
    )
    return map_resolved_profiles_to_settings(
        source_path,
        inheritance_report,
        strict=mapping_strict,
    )

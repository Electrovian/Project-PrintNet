from __future__ import annotations

import copy
import json
from dataclasses import dataclass, field
from pathlib import Path

from printer_presets.preset_store import get_cli_config_payload, get_document, get_payload

from .settings import normalize_settings


PROFILE_METADATA_KEYS = {
    "name",
    "type",
    "inherits",
    "inherits_chain",
    "inherits_chain_files",
    "from",
    "model_id",
    "filament_id",
}

SETTING_PROFILE_TYPES = {"machine", "machine_model", "process"}
FILAMENT_PROFILE_TYPES = {"filament"}
DEFAULT_CLI_CONFIG_IDENTIFIER = "profiles/BBL/cli_config.json"


def _normalize_reference(value: str) -> str:
    text = str(value).strip().replace("\\", "/")
    while "//" in text:
        text = text.replace("//", "/")
    return text.strip()


def _resolve_embedded_cli_config_identifier(value: str) -> str | None:
    normalized = _normalize_reference(value)
    if not normalized:
        return None

    lowered = normalized.casefold()
    if lowered == DEFAULT_CLI_CONFIG_IDENTIFIER.casefold():
        return DEFAULT_CLI_CONFIG_IDENTIFIER

    if lowered.startswith("embedded:"):
        lowered = lowered.removeprefix("embedded:")
        if lowered == DEFAULT_CLI_CONFIG_IDENTIFIER.casefold():
            return DEFAULT_CLI_CONFIG_IDENTIFIER

    prefixes = (
        "app/printer_presets/seed_resources/",
        "printer_presets/seed_resources/",
        "seed_resources/",
    )
    for prefix in prefixes:
        index = lowered.find(prefix)
        if index >= 0:
            trimmed = normalized[index + len(prefix) :].strip("/")
            if trimmed.casefold() == DEFAULT_CLI_CONFIG_IDENTIFIER.casefold():
                return DEFAULT_CLI_CONFIG_IDENTIFIER

    return None


class ProfileCompatError(ValueError):
    pass


class ProfileCompatFileNotFoundError(ProfileCompatError):
    pass


class ProfileCompatConfigError(ProfileCompatError):
    pass


@dataclass
class ProfileMergeReport:
    normalized_settings: dict[str, object]
    loaded_setting_paths: list[str] = field(default_factory=list)
    loaded_filament_paths: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class CompatibilityLookupResult:
    downward_compatible_machine: list[str] = field(default_factory=list)
    config_source: str = ""
    warnings: list[str] = field(default_factory=list)


def _load_json_object(path_value: str) -> tuple[str, dict[str, object]]:
    text = str(path_value).strip()
    if not text:
        raise ProfileCompatFileNotFoundError("MISSING_PROFILE_FILE:")

    path = Path(text).expanduser()
    if path.exists() and path.is_file():
        path_display = str(path.resolve())
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ProfileCompatConfigError(f"PROFILE_JSON_PARSE_ERROR:{path_display}:{exc}") from exc
        if not isinstance(payload, dict):
            raise ProfileCompatConfigError(f"PROFILE_JSON_NOT_OBJECT:{path_display}")
        normalized_payload = {str(key): value for key, value in payload.items()}
        return path_display, normalized_payload

    embedded_payload = get_payload(text)
    if embedded_payload is None:
        raise ProfileCompatFileNotFoundError(f"MISSING_PROFILE_FILE:{path}")

    path_display, payload = embedded_payload
    if not isinstance(payload, dict):
        raise ProfileCompatConfigError(f"PROFILE_JSON_NOT_OBJECT:{path_display}")
    normalized_payload = {str(key): value for key, value in payload.items()}
    return path_display, normalized_payload


def _load_cli_config_object(path_value: str) -> tuple[str, dict[str, object]]:
    text = str(path_value or "").strip()
    if not text:
        payload = get_cli_config_payload(DEFAULT_CLI_CONFIG_IDENTIFIER)
        if payload is None:
            raise ProfileCompatConfigError(
                f"CLI_CONFIG_DEFAULT_UNAVAILABLE:{DEFAULT_CLI_CONFIG_IDENTIFIER}"
            )
        return f"embedded:{DEFAULT_CLI_CONFIG_IDENTIFIER}", {str(key): value for key, value in payload.items()}

    path = Path(text).expanduser()
    if path.exists() and path.is_file():
        path_display = str(path.resolve())
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ProfileCompatConfigError(f"CLI_CONFIG_JSON_PARSE_ERROR:{path_display}:{exc}") from exc
        if not isinstance(payload, dict):
            raise ProfileCompatConfigError(f"CLI_CONFIG_JSON_NOT_OBJECT:{path_display}")
        normalized_payload = {str(key): value for key, value in payload.items()}
        return path_display, normalized_payload

    embedded_identifier = _resolve_embedded_cli_config_identifier(text)
    if embedded_identifier is not None:
        payload = get_cli_config_payload(embedded_identifier)
        if payload is None:
            raise ProfileCompatConfigError(
                f"CLI_CONFIG_EMBEDDED_UNAVAILABLE:{embedded_identifier}"
            )
        return f"embedded:{embedded_identifier}", {str(key): value for key, value in payload.items()}

    raise ProfileCompatFileNotFoundError(f"MISSING_CLI_CONFIG_FILE:{text}")


def _validate_profile_type(path: str, payload: dict[str, object], allowed_types: set[str]) -> str:
    raw_type = str(payload.get("type", "")).strip().casefold()
    if not raw_type:
        raise ProfileCompatConfigError(f"PROFILE_TYPE_MISSING:{path}")
    if raw_type not in allowed_types:
        raise ProfileCompatConfigError(f"PROFILE_TYPE_INVALID:{path}:{raw_type}")
    return raw_type


def _flatten_paths(values: list[str] | tuple[str, ...] | None) -> list[str]:
    if not values:
        return []
    flattened: list[str] = []
    for value in values:
        text = str(value).strip()
        if text:
            flattened.append(text)
    return flattened


def _filtered_settings_payload(payload: dict[str, object]) -> dict[str, object]:
    merged: dict[str, object] = {}
    for key, value in payload.items():
        if key in PROFILE_METADATA_KEYS:
            continue
        merged[key] = value
    return merged


def load_and_merge_profiles(
    load_settings: list[str] | tuple[str, ...] | None,
    load_filaments: list[str] | tuple[str, ...] | None,
) -> ProfileMergeReport:
    setting_paths = _flatten_paths(load_settings)
    filament_paths = _flatten_paths(load_filaments)

    merged_raw_settings: dict[str, object] = {}
    warnings: list[str] = []
    resolved_setting_paths: list[str] = []
    resolved_filament_paths: list[str] = []

    for setting_path in setting_paths:
        path_display, payload = _load_json_object(setting_path)
        _validate_profile_type(path_display, payload, SETTING_PROFILE_TYPES)
        filtered = _filtered_settings_payload(payload)
        if not filtered:
            warnings.append(f"empty_setting_payload:{path_display}")
        merged_raw_settings.update(filtered)
        resolved_setting_paths.append(path_display)

    for filament_path in filament_paths:
        path_display, payload = _load_json_object(filament_path)
        _validate_profile_type(path_display, payload, FILAMENT_PROFILE_TYPES)
        filtered = _filtered_settings_payload(payload)
        if not filtered:
            warnings.append(f"empty_filament_payload:{path_display}")
        merged_raw_settings.update(filtered)
        resolved_filament_paths.append(path_display)

    normalized_settings = normalize_settings(merged_raw_settings, keep_unknown_keys=True)
    return ProfileMergeReport(
        normalized_settings=normalized_settings,
        loaded_setting_paths=resolved_setting_paths,
        loaded_filament_paths=resolved_filament_paths,
        warnings=warnings,
    )


def apply_cli_setting_overrides(
    base_settings: dict[str, object],
    *,
    layer_height: float | None = None,
    model_height_mm: float | None = None,
    infill_percent: float | None = None,
    support_enabled: bool | None = None,
) -> dict[str, object]:
    overrides: dict[str, object] = {}
    if layer_height is not None:
        overrides["layer_height"] = float(layer_height)
    if model_height_mm is not None:
        overrides["model_height_mm"] = float(model_height_mm)
    if infill_percent is not None:
        overrides["infill_percent"] = float(infill_percent)
    if support_enabled is not None:
        overrides["support_enabled"] = bool(support_enabled)

    merged = dict(base_settings)
    merged.update(overrides)
    return normalize_settings(merged, keep_unknown_keys=True)


def resolve_downward_compatible_machines(
    *,
    cli_config_path: str,
    printer_model: str,
    printer_name: str,
) -> CompatibilityLookupResult:
    config_path, payload = _load_cli_config_object(cli_config_path)
    warnings: list[str] = []

    printer_node = payload.get("printer")
    if not isinstance(printer_node, dict):
        raise ProfileCompatConfigError(f"CLI_CONFIG_PRINTER_NODE_INVALID:{config_path}")

    model_key = str(printer_model).strip()
    name_key = str(printer_name).strip()
    if not model_key:
        raise ProfileCompatConfigError("PRINTER_MODEL_EMPTY")
    if not name_key:
        raise ProfileCompatConfigError("PRINTER_NAME_EMPTY")

    model_payload = printer_node.get(model_key)
    if not isinstance(model_payload, dict):
        warnings.append(f"model_not_found:{model_key}")
        return CompatibilityLookupResult(config_source=config_path, warnings=warnings)

    downward_payload = model_payload.get("downward_check")
    if not isinstance(downward_payload, dict):
        warnings.append(f"downward_check_not_found:{model_key}")
        return CompatibilityLookupResult(config_source=config_path, warnings=warnings)

    machines = downward_payload.get(name_key)
    if machines is None:
        warnings.append(f"printer_name_not_found:{model_key}:{name_key}")
        return CompatibilityLookupResult(config_source=config_path, warnings=warnings)
    if not isinstance(machines, list):
        warnings.append(f"downward_check_not_list:{model_key}:{name_key}")
        return CompatibilityLookupResult(config_source=config_path, warnings=warnings)

    normalized = [str(item).strip() for item in machines if str(item).strip()]
    return CompatibilityLookupResult(
        downward_compatible_machine=normalized,
        config_source=config_path,
        warnings=warnings,
    )

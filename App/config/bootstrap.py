from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
from typing import Any, Mapping

_HOST_PATH = type(Path())


def bootstrap_defaults() -> dict[str, Any]:
    return {
        "ui_language": "en",
        "region_code": "",
        "setup_completed_at_utc": "",
        "connectivity_preferences": {
            "wifi_enabled": True,
            "bluetooth_enabled": True,
        },
    }


def _host_path(value: str) -> Path:
    return _HOST_PATH(value)


def _host_home() -> Path:
    return _HOST_PATH.home()


def user_config_dir() -> Path:
    if os.name == "nt":
        root = os.environ.get("APPDATA") or os.environ.get("LOCALAPPDATA") or str(_host_home())
        return _host_path(root).joinpath("EON-OpenSlicer")
    xdg = str(os.environ.get("XDG_CONFIG_HOME", "")).strip()
    if xdg:
        return Path(xdg).joinpath("eon-openslicer")
    return Path.home().joinpath(".config", "eon-openslicer")


def user_cache_dir() -> Path:
    if os.name == "nt":
        root = os.environ.get("LOCALAPPDATA") or str(_host_home())
        return _host_path(root).joinpath("EON-OpenSlicer", "cache")
    xdg = str(os.environ.get("XDG_CACHE_HOME", "")).strip()
    if xdg:
        return Path(xdg).joinpath("eon-openslicer")
    return Path.home().joinpath(".cache", "eon-openslicer")


def bootstrap_config_path() -> Path:
    return user_config_dir().joinpath("bootstrap.json")


def _as_bool(value: object, default: bool) -> bool:
    if isinstance(value, bool):
        return bool(value)
    text = str(value or "").strip().lower()
    if text in ("1", "true", "yes", "on"):
        return True
    if text in ("0", "false", "no", "off"):
        return False
    return bool(default)


def _normalize_language(value: object) -> str:
    text = str(value or "").strip().lower()
    if not text:
        return "en"
    if "-" in text:
        text = text.split("-", 1)[0].strip()
    if "_" in text:
        text = text.split("_", 1)[0].strip()
    if text in ("en", "es"):
        return text
    return "en"


def _normalize_region(value: object) -> str:
    text = str(value or "").strip().upper()
    if not text:
        return ""
    if len(text) > 8:
        text = text[:8]
    return text


def normalize_bootstrap_config(payload: Mapping[str, Any] | None) -> dict[str, Any]:
    defaults = bootstrap_defaults()
    source = dict(payload or {})
    preferences = source.get("connectivity_preferences", {})
    if not isinstance(preferences, Mapping):
        preferences = {}
    return {
        "ui_language": _normalize_language(source.get("ui_language", defaults["ui_language"])),
        "region_code": _normalize_region(source.get("region_code", defaults["region_code"])),
        "setup_completed_at_utc": str(source.get("setup_completed_at_utc", "")).strip(),
        "connectivity_preferences": {
            "wifi_enabled": _as_bool(preferences.get("wifi_enabled", True), True),
            "bluetooth_enabled": _as_bool(preferences.get("bluetooth_enabled", True), True),
        },
    }


def load_bootstrap_config() -> dict[str, Any]:
    path = bootstrap_config_path()
    if not path.exists():
        return bootstrap_defaults()
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return bootstrap_defaults()
    if not isinstance(payload, Mapping):
        return bootstrap_defaults()
    return normalize_bootstrap_config(payload)


def save_bootstrap_config(payload: Mapping[str, Any]) -> Path:
    normalized = normalize_bootstrap_config(payload)
    path = bootstrap_config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(normalized, indent=2, sort_keys=True), encoding="utf-8")
    return path


def mark_setup_completed(payload: Mapping[str, Any]) -> dict[str, Any]:
    normalized = normalize_bootstrap_config(payload)
    normalized["setup_completed_at_utc"] = datetime.now(timezone.utc).isoformat()
    return normalized


def setup_completed(payload: Mapping[str, Any] | None) -> bool:
    source = dict(payload or {})
    stamp = str(source.get("setup_completed_at_utc", "")).strip()
    if not stamp:
        return False
    return True

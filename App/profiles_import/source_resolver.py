from __future__ import annotations

from pathlib import Path
from typing import Callable, TypeVar

from printer_presets.preset_store import materialize_seed_resources


ErrorType = TypeVar("ErrorType", bound=Exception)

LEGACY_PROFILE_PATH_SUFFIXES: tuple[str, ...] = (
    "app/printer_presets/seed_resources/profiles",
)


def _normalize(path_value: str) -> str:
    return str(path_value).replace("\\", "/").strip().casefold().strip("/")


def _is_legacy_profile_path(path_value: str) -> bool:
    normalized = _normalize(path_value)
    if not normalized:
        return False
    if normalized in {"embedded://profiles", "__embedded_profiles__"}:
        return True
    return any(normalized.endswith(suffix) for suffix in LEGACY_PROFILE_PATH_SUFFIXES)


def resolve_profile_source_root(
    source_path: str,
    *,
    error_factory: Callable[[str], ErrorType],
) -> Path:
    text = str(source_path).strip()
    if not text:
        raise error_factory("SOURCE_PATH_EMPTY")

    source_root = Path(text).expanduser()
    if source_root.exists():
        if not source_root.is_dir():
            raise error_factory(f"SOURCE_PATH_NOT_DIRECTORY: {source_root}")
        has_json = any(source_root.rglob("*.json"))
        if has_json:
            return source_root.resolve()
        if _is_legacy_profile_path(text):
            embedded_seed_root = materialize_seed_resources()
            embedded_profiles = embedded_seed_root / "profiles"
            if embedded_profiles.exists() and embedded_profiles.is_dir():
                return embedded_profiles.resolve()
        return source_root.resolve()

    if _is_legacy_profile_path(text):
        embedded_seed_root = materialize_seed_resources()
        embedded_profiles = embedded_seed_root / "profiles"
        if embedded_profiles.exists() and embedded_profiles.is_dir():
            return embedded_profiles.resolve()

    raise error_factory(f"SOURCE_PATH_MISSING: {source_root}")

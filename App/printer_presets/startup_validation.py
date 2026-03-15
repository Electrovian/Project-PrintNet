from __future__ import annotations

import ast
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from . import preset_store


@dataclass(frozen=True)
class PresetValidationFailure:
    path: str
    reason: str


@dataclass(frozen=True)
class PresetValidationReport:
    checked_count: int
    failed_count: int
    total_files: int
    failures: tuple[PresetValidationFailure, ...]


class PresetValidationError(RuntimeError):
    def __init__(self, message: str, failures: tuple[PresetValidationFailure, ...]) -> None:
        super().__init__(message)
        self.failures = failures


ProgressCallback = Callable[[int, int, str], None]


_CACHE_VERSION = 1
_CACHE_SCAN_BYTES = 8192
_DICT_PREFIXES = ("{", "dict(", "OrderedDict(", "collections.OrderedDict(")


@dataclass(frozen=True)
class _ValidationRule:
    symbol: str | None
    missing_reason: str | None
    not_dict_reason: str | None
    dict_required: bool = False


_PROFILE_RULE = _ValidationRule(
    symbol="DATA",
    missing_reason="DATA_PAYLOAD_MISSING",
    not_dict_reason="DATA_PAYLOAD_NOT_DICT",
    dict_required=True,
)
_PRINTERS_RULE = _ValidationRule(
    symbol="PRINTERS_DATA",
    missing_reason="PRINTERS_DATA_MISSING",
    not_dict_reason="PRINTERS_DATA_NOT_DICT",
    dict_required=True,
)
_VENDOR_INIT_RULE = _ValidationRule(
    symbol="VENDOR_MODULES",
    missing_reason="VENDOR_MODULES_MISSING",
    not_dict_reason=None,
    dict_required=False,
)
_VENDOR_ALL_RULE = _ValidationRule(
    symbol="ALL",
    missing_reason="ALL_PAYLOAD_MISSING",
    not_dict_reason=None,
    dict_required=False,
)
_VENDOR_SKIP_RULE = _ValidationRule(symbol=None, missing_reason=None, not_dict_reason=None, dict_required=False)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _validation_cache_path() -> Path:
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data) / "EON-OpenSlicer" / "cache" / "preset_validation_cache.json"
    return Path.home() / ".cache" / "eon-openslicer" / "preset_validation_cache.json"


def _rule_cache_tag(rule: _ValidationRule) -> str:
    return f"{rule.symbol or '_'}:{1 if rule.dict_required else 0}"


def _load_validation_cache() -> dict[str, dict[str, str]]:
    path = _validation_cache_path()
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    if not isinstance(payload, dict):
        return {}
    if payload.get("version") != _CACHE_VERSION:
        return {}

    raw_files = payload.get("files")
    if not isinstance(raw_files, dict):
        return {}

    cache: dict[str, dict[str, str]] = {}
    for key, value in raw_files.items():
        if not isinstance(key, str) or not isinstance(value, dict):
            continue
        sig = value.get("sig")
        tag = value.get("tag")
        if isinstance(sig, str) and isinstance(tag, str):
            cache[key] = {"sig": sig, "tag": tag}
    return cache


def _save_validation_cache(cache: dict[str, dict[str, str]]) -> None:
    path = _validation_cache_path()
    payload = {"version": _CACHE_VERSION, "files": cache}
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = path.with_suffix(path.suffix + ".tmp")
        temp_path.write_text(json.dumps(payload, separators=(",", ":"), ensure_ascii=False), encoding="utf-8")
        temp_path.replace(path)
    except Exception:
        # Cache writes are best-effort; validation outcome should not depend on them.
        return


def _file_signature(path: Path) -> str:
    stat = path.stat()
    return f"{stat.st_size}:{stat.st_mtime_ns}"


def _profile_py_path_from_storage(storage_path: str, profiles_dir: Path) -> Path:
    normalized = str(storage_path).replace("\\", "/")
    if not normalized.startswith("profiles/"):
        raise RuntimeError(f"PROFILE_STORAGE_PATH_INVALID:{storage_path}")
    relative = normalized[len("profiles/") :]
    file_path = profiles_dir / relative
    if file_path.suffix.casefold() == ".json":
        return file_path.with_suffix(".py")
    return file_path.with_name(f"{file_path.name}.py")


def _rule_for_path(path: Path, printers_module_path: Path) -> _ValidationRule:
    if path == printers_module_path:
        return _PRINTERS_RULE

    as_posix = path.as_posix()
    if "/python_vendors/" in as_posix:
        if path.name == "__init__.py":
            return _VENDOR_INIT_RULE
        if path.name in {"global_profiles_data.py", "blacklist.py"}:
            return _VENDOR_SKIP_RULE
        return _VENDOR_ALL_RULE
    return _PROFILE_RULE


def _read_prefix(path: Path, max_bytes: int = _CACHE_SCAN_BYTES) -> tuple[str, bool]:
    with path.open("rb") as handle:
        raw = handle.read(max_bytes + 1)
    truncated = len(raw) > max_bytes
    if truncated:
        raw = raw[:max_bytes]
    return raw.decode("utf-8", errors="ignore"), truncated


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")


def _find_assignment(source: str, symbol: str):
    pattern = re.compile(rf"(?m)^\s*{re.escape(symbol)}\s*=")
    return pattern.search(source)


def _is_dict_like_probe(probe: str) -> bool:
    text = probe.lstrip()
    while text.startswith("("):
        text = text[1:].lstrip()
    return text.startswith(_DICT_PREFIXES)


def _assignment_value_is_dict_via_ast(source: str, symbol: str) -> bool | None:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return False

    def _target_matches(node: ast.AST) -> bool:
        return isinstance(node, ast.Name) and node.id == symbol

    def _is_dict_expr(node: ast.AST | None) -> bool:
        if node is None:
            return False
        if isinstance(node, ast.Dict):
            return True
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == "dict":
                return True
            if isinstance(node.func, ast.Attribute) and node.func.attr == "dict":
                return True
        return False

    found = False
    for stmt in tree.body:
        if isinstance(stmt, ast.Assign):
            if not any(_target_matches(target) for target in stmt.targets):
                continue
            found = True
            return _is_dict_expr(stmt.value)
        if isinstance(stmt, ast.AnnAssign):
            if not _target_matches(stmt.target):
                continue
            found = True
            return _is_dict_expr(stmt.value)
    if found:
        return False
    return None


def _validate_source_against_rule(source: str, rule: _ValidationRule) -> None:
    symbol = rule.symbol
    if symbol is None:
        return

    match = _find_assignment(source, symbol)
    if match is None:
        raise RuntimeError(rule.missing_reason or f"{symbol}_MISSING")
    if not rule.dict_required:
        return

    probe = source[match.end() : match.end() + 256]
    if _is_dict_like_probe(probe):
        return

    ast_result = _assignment_value_is_dict_via_ast(source, symbol)
    if ast_result is True:
        return
    raise RuntimeError(rule.not_dict_reason or f"{symbol}_NOT_DICT")


def _validate_file(path: Path, rule: _ValidationRule) -> None:
    if rule.symbol is None:
        return

    prefix, truncated = _read_prefix(path)
    try:
        _validate_source_against_rule(prefix, rule)
        return
    except RuntimeError:
        if not truncated:
            raise

    source = _read_text(path)
    _validate_source_against_rule(source, rule)


def validate_preset_python_files(
    *,
    profiles_root: Path | None = None,
    printers_data_path: Path | None = None,
    on_progress: ProgressCallback | None = None,
) -> PresetValidationReport:
    root = _repo_root()
    profiles_dir = (profiles_root or (root / "App" / "printer_presets" / "seed_resources" / "profiles")).resolve()
    printers_module_path = (
        printers_data_path
        or (root / "App" / "printer_presets" / "seed_resources" / "printers" / "printers_data.py")
    ).resolve()

    if not profiles_dir.exists() or not profiles_dir.is_dir():
        raise PresetValidationError(
            f"PRESET_PROFILES_ROOT_NOT_FOUND:{profiles_dir}",
            (PresetValidationFailure(path=str(profiles_dir), reason="MISSING_PROFILES_ROOT"),),
        )
    if not printers_module_path.exists() or not printers_module_path.is_file():
        raise PresetValidationError(
            f"PRESET_PRINTERS_DATA_NOT_FOUND:{printers_module_path}",
            (PresetValidationFailure(path=str(printers_module_path), reason="MISSING_PRINTERS_DATA"),),
        )

    profile_paths_expected: set[Path] = set()
    for document in preset_store.iter_documents("profiles"):
        profile_paths_expected.add(_profile_py_path_from_storage(document.storage_path, profiles_dir).resolve())
    python_vendors_dir = profiles_dir / "python_vendors"
    if python_vendors_dir.exists() and python_vendors_dir.is_dir():
        for vendor_file in python_vendors_dir.glob("*.py"):
            if vendor_file.is_file():
                profile_paths_expected.add(vendor_file.resolve())

    failures: list[PresetValidationFailure] = []
    profile_files: list[Path] = []
    for expected_path in sorted(profile_paths_expected):
        if expected_path.exists() and expected_path.is_file():
            profile_files.append(expected_path)
        else:
            failures.append(PresetValidationFailure(path=str(expected_path), reason="MISSING_PROFILE_PY_FILE"))

    candidates = profile_files + [printers_module_path]
    total = len(candidates)
    checked = 0

    cached_results = _load_validation_cache()
    next_cache = dict(cached_results)

    for idx, file_path in enumerate(candidates, start=1):
        if on_progress is not None:
            on_progress(idx, total, str(file_path))

        key = str(file_path)
        rule = _rule_for_path(file_path, printers_module_path)
        tag = _rule_cache_tag(rule)

        try:
            signature = _file_signature(file_path)
            cached = cached_results.get(key)
            if cached and cached.get("sig") == signature and cached.get("tag") == tag:
                checked += 1
                continue

            _validate_file(file_path, rule)
            checked += 1
            next_cache[key] = {"sig": signature, "tag": tag}
        except Exception as exc:  # pragma: no cover - startup guard
            failures.append(PresetValidationFailure(path=key, reason=f"{type(exc).__name__}:{exc}"))
            next_cache.pop(key, None)

    _save_validation_cache(next_cache)

    report = PresetValidationReport(
        checked_count=checked,
        failed_count=len(failures),
        total_files=total,
        failures=tuple(failures),
    )
    if failures:
        preview = "; ".join(f"{item.path} -> {item.reason}" for item in failures[:10])
        if len(failures) > 10:
            preview += f"; ... ({len(failures) - 10} more)"
        raise PresetValidationError(f"PRESET_STARTUP_VALIDATION_FAILED:{preview}", report.failures)
    return report

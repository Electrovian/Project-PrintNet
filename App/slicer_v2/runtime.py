from __future__ import annotations

from collections.abc import Mapping


def _to_int(value: object, default: int) -> int:
    if isinstance(value, bool):
        return default
    if isinstance(value, int):
        return int(value)
    if isinstance(value, float):
        return int(value)
    text = str(value).strip()
    if not text:
        return default
    try:
        return int(float(text))
    except (TypeError, ValueError, OverflowError):
        return default


def resolve_cpu_threads(runtime_settings: Mapping[str, object] | None, default: int = 1) -> int:
    if runtime_settings is None:
        return max(1, int(default))
    value = runtime_settings.get("cpu_threads", default)
    parsed = _to_int(value, default)
    return max(1, parsed)


def resolve_worker_count(
    runtime_settings: Mapping[str, object] | None,
    item_count: int,
    default: int = 1,
) -> int:
    if item_count <= 1:
        return 1
    cpu_threads = resolve_cpu_threads(runtime_settings, default=default)
    return max(1, min(item_count, cpu_threads))


def resolve_gpu_mode(runtime_settings: Mapping[str, object] | None, default: str = "auto") -> str:
    if runtime_settings is None:
        return default
    value = str(runtime_settings.get("gpu_mode", default)).strip().lower()
    if value in {"off", "none", "false", "0"}:
        return "off"
    if value in {"cuda", "opencl", "metal", "vulkan"}:
        return value
    return "auto"

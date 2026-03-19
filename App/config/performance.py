from __future__ import annotations

import os
import sys
from typing import Dict, Optional


_CACHED_LIMITS: Optional[Dict[str, int]] = None
_CACHED_TOTAL_MB: Optional[int] = None


def _env_int(name: str) -> Optional[int]:
    raw = os.environ.get(name)
    if raw is None:
        return None
    text = str(raw).strip()
    if not text:
        return None
    try:
        return int(text)
    except (TypeError, ValueError):
        return None


def detect_total_memory_mb() -> Optional[int]:
    global _CACHED_TOTAL_MB
    if _CACHED_TOTAL_MB is not None:
        return _CACHED_TOTAL_MB

    total = None
    if os.name == "nt":
        try:
            import ctypes

            class _MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]

            status = _MEMORYSTATUSEX()
            status.dwLength = ctypes.sizeof(_MEMORYSTATUSEX)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
                total = int(status.ullTotalPhys / (1024 * 1024))
        except Exception:
            total = None
    elif sys.platform.startswith("linux"):
        try:
            with open("/proc/meminfo", "r", encoding="utf-8") as handle:
                for line in handle:
                    if line.startswith("MemTotal:"):
                        parts = line.split()
                        if len(parts) >= 2:
                            total = int(int(parts[1]) / 1024)
                        break
        except Exception:
            total = None
    elif sys.platform == "darwin":
        try:
            import subprocess

            out = subprocess.check_output(["sysctl", "-n", "hw.memsize"]).strip()
            total = int(int(out) / (1024 * 1024))
        except Exception:
            total = None

    _CACHED_TOTAL_MB = total
    return total


def _recommend_cache_mb(total_mb: Optional[int]) -> int:
    if total_mb is None:
        return 128
    if total_mb < 4096:
        return 32
    if total_mb < 8192:
        return 64
    if total_mb < 16384:
        return 128
    return 256


def _recommend_threads(total_mb: Optional[int], cpu_count: int) -> int:
    if cpu_count <= 1:
        return 1
    if total_mb is None:
        return max(1, cpu_count - 1)
    if total_mb < 4096:
        return 1
    if total_mb < 8192:
        return min(2, max(1, cpu_count - 1))
    if total_mb < 16384:
        return min(4, max(1, cpu_count - 1))
    return max(1, cpu_count - 1)


def resolve_performance_limits(overrides: Optional[dict] = None) -> Dict[str, int]:
    global _CACHED_LIMITS
    if _CACHED_LIMITS is not None:
        return dict(_CACHED_LIMITS)

    overrides = overrides or {}
    total_mb = detect_total_memory_mb()
    cpu_count = os.cpu_count() or 2

    max_threads = overrides.get("max_threads")
    env_max_threads = _env_int("EON_MAX_THREADS")
    if max_threads is None and env_max_threads is not None:
        max_threads = env_max_threads
    if max_threads is None:
        max_threads = _recommend_threads(total_mb, cpu_count)
    max_threads = max(1, int(max_threads))
    if cpu_count > 2 and max_threads != 1:
        max_threads = max(2, max_threads)
        max_threads = min(max_threads, cpu_count)

    cache_mb = overrides.get("max_slice_cache_mb")
    env_cache_mb = _env_int("EON_MAX_SLICE_CACHE_MB")
    if cache_mb is None and env_cache_mb is not None:
        cache_mb = env_cache_mb
    if cache_mb is None:
        cache_mb = _recommend_cache_mb(total_mb)
    cache_mb = max(16, int(cache_mb))

    limits = {"max_threads": max_threads, "max_slice_cache_mb": cache_mb}
    _CACHED_LIMITS = dict(limits)
    return limits

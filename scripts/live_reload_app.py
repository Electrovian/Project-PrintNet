from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_WATCH_PATHS = (
    ROOT / "App" / "gui",
    ROOT / "App" / "config",
    ROOT / "App" / "integrations",
    ROOT / "App" / "slicer_v2",
    ROOT / "App" / "main.py",
    ROOT / "App" / "__main__.py",
)

DEFAULT_EXTENSIONS = (".py", ".qss", ".json", ".yaml", ".yml", ".ui")


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run desktop app and restart it automatically when watched files change.",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=0.75,
        help="Polling interval in seconds (default: 0.75).",
    )
    parser.add_argument(
        "--watch",
        action="append",
        default=[],
        help="Additional file or folder to watch. Can be used multiple times.",
    )
    parser.add_argument(
        "--ext",
        action="append",
        default=[],
        help="Additional file extension to watch (example: --ext .css).",
    )
    parser.add_argument(
        "--cmd",
        nargs=argparse.REMAINDER,
        help="Command to run. Defaults to: python -m App",
    )
    return parser.parse_args(argv)


def _normalize_extensions(custom: Sequence[str]) -> tuple[str, ...]:
    values = set(DEFAULT_EXTENSIONS)
    for item in custom:
        text = str(item or "").strip()
        if not text:
            continue
        if not text.startswith("."):
            text = "." + text
        values.add(text.lower())
    return tuple(sorted(values))


def _resolve_watch_paths(custom: Sequence[str]) -> list[Path]:
    paths: list[Path] = []
    seen: set[Path] = set()
    for raw in list(DEFAULT_WATCH_PATHS) + [Path(item) for item in custom]:
        candidate = raw if raw.is_absolute() else (ROOT / raw)
        path = candidate.resolve()
        if path in seen:
            continue
        seen.add(path)
        paths.append(path)
    return paths


def _iter_watched_files(paths: Sequence[Path], extensions: tuple[str, ...]) -> Iterable[Path]:
    for path in paths:
        if path.is_file():
            if path.suffix.lower() in extensions:
                yield path
            continue
        if not path.exists():
            continue
        for item in path.rglob("*"):
            if not item.is_file():
                continue
            if item.suffix.lower() not in extensions:
                continue
            yield item


def _build_snapshot(paths: Sequence[Path], extensions: tuple[str, ...]) -> dict[str, int]:
    snapshot: dict[str, int] = {}
    for file_path in _iter_watched_files(paths, extensions):
        try:
            stat = file_path.stat()
        except OSError:
            continue
        snapshot[str(file_path)] = int(stat.st_mtime_ns)
    return snapshot


def _detect_changes(prev: dict[str, int], current: dict[str, int]) -> list[str]:
    changed: list[str] = []
    for path, mtime in current.items():
        if path not in prev:
            changed.append(path)
            continue
        if int(prev[path]) != int(mtime):
            changed.append(path)
    for path in prev:
        if path not in current:
            changed.append(path)
    changed.sort()
    return changed


def _start_process(command: Sequence[str]) -> subprocess.Popen[bytes]:
    env = os.environ.copy()
    existing = str(env.get("PYTHONPATH", "")).strip()
    app_path = str(ROOT / "App")
    env["PYTHONPATH"] = app_path if not existing else f"{app_path}{os.pathsep}{existing}"
    return subprocess.Popen(
        list(command),
        cwd=str(ROOT),
        env=env,
    )


def _stop_process(proc: subprocess.Popen[bytes], timeout: float = 5.0) -> None:
    if proc.poll() is not None:
        return
    try:
        proc.terminate()
        proc.wait(timeout=timeout)
        return
    except Exception:
        pass
    try:
        proc.kill()
        proc.wait(timeout=timeout)
    except Exception:
        pass


def _default_command() -> list[str]:
    return [sys.executable, "-m", "App"]


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(list(argv or []))
    interval = max(0.15, float(args.interval))
    extensions = _normalize_extensions(args.ext)
    watch_paths = _resolve_watch_paths(args.watch)
    command = list(args.cmd or [])
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        command = _default_command()

    print("[live-reload] Root:", ROOT)
    print("[live-reload] Command:", " ".join(command))
    print("[live-reload] Watching:")
    for path in watch_paths:
        print("  -", path)
    print("[live-reload] Extensions:", ", ".join(extensions))

    process = _start_process(command)
    previous = _build_snapshot(watch_paths, extensions)
    restart_count = 0

    try:
        while True:
            time.sleep(interval)
            current = _build_snapshot(watch_paths, extensions)
            changed = _detect_changes(previous, current)
            previous = current
            if not changed:
                continue

            restart_count += 1
            preview = changed[:6]
            suffix = "" if len(changed) <= 6 else f" (+{len(changed) - 6} more)"
            print(f"[live-reload] Change detected ({len(changed)} file(s)){suffix}")
            for path in preview:
                print("  *", path)
            print(f"[live-reload] Restarting app instance #{restart_count}...")

            _stop_process(process)
            process = _start_process(command)
    except KeyboardInterrupt:
        print("\n[live-reload] Stopping...")
    finally:
        _stop_process(process)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

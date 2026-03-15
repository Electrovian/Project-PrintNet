from __future__ import annotations

import argparse
import json
import os
import time
from datetime import datetime
from pathlib import Path


PATTERNS = ("activity_*.log", "fault_*.log", "crash_*.log")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Tail desktop usage logs and write a consolidated session transcript."
    )
    parser.add_argument(
        "--logs-dir",
        default="logs",
        help="Directory containing activity/fault/crash logs.",
    )
    parser.add_argument(
        "--out",
        required=True,
        help="Output transcript path.",
    )
    parser.add_argument(
        "--poll-seconds",
        type=float,
        default=0.5,
        help="Polling interval in seconds.",
    )
    parser.add_argument(
        "--max-seconds",
        type=float,
        default=0.0,
        help="Optional max runtime; 0 means run until interrupted.",
    )
    parser.add_argument(
        "--include-existing",
        action="store_true",
        help="Also stream existing historical content already present in log files.",
    )
    return parser.parse_args()


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def iter_log_paths(logs_dir: Path) -> list[Path]:
    paths: list[Path] = []
    for pattern in PATTERNS:
        paths.extend(logs_dir.glob(pattern))
    return sorted(set(paths), key=lambda p: (p.stat().st_mtime, p.name))


def summarize_line(path: Path, line: str) -> str:
    raw = str(line or "").strip()
    if not raw:
        return ""
    if path.name.startswith("activity_"):
        try:
            payload = json.loads(raw)
        except Exception:
            return f"{now_iso()} [{path.name}] {raw}"
        event = str(payload.get("event", ""))
        if event == "action":
            action = str(payload.get("action", ""))
            return f"{now_iso()} [{path.name}] action={action} payload={json.dumps(payload, ensure_ascii=False)}"
        return f"{now_iso()} [{path.name}] event={event} payload={json.dumps(payload, ensure_ascii=False)}"
    return f"{now_iso()} [{path.name}] {raw}"


def main() -> int:
    args = parse_args()
    logs_dir = Path(args.logs_dir).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()
    poll_seconds = max(0.1, float(args.poll_seconds))
    max_seconds = max(0.0, float(args.max_seconds))

    if not logs_dir.exists() or not logs_dir.is_dir():
        raise SystemExit(f"Logs directory not found: {logs_dir}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    offsets: dict[Path, int] = {}
    start = time.monotonic()

    if not bool(args.include_existing):
        for existing in iter_log_paths(logs_dir):
            try:
                offsets[existing] = existing.stat().st_size
            except OSError:
                offsets[existing] = 0

    with out_path.open("a", encoding="utf-8") as out:
        out.write(f"{now_iso()} [monitor] start logs_dir={logs_dir}\n")
        out.flush()
        print(f"monitor started -> {out_path}")

        try:
            while True:
                if max_seconds > 0.0 and (time.monotonic() - start) >= max_seconds:
                    out.write(f"{now_iso()} [monitor] max-seconds reached ({max_seconds})\n")
                    out.flush()
                    print("monitor stopped: max-seconds reached")
                    return 0

                for path in iter_log_paths(logs_dir):
                    if not path.exists():
                        continue

                    file_size = path.stat().st_size
                    previous = offsets.get(path, 0)
                    if file_size < previous:
                        previous = 0
                    if file_size == previous:
                        continue

                    with path.open("rb") as handle:
                        handle.seek(previous)
                        chunk = handle.read(file_size - previous)
                    offsets[path] = file_size
                    text = chunk.decode("utf-8", errors="ignore")
                    for raw_line in text.splitlines():
                        rendered = summarize_line(path, raw_line)
                        if not rendered:
                            continue
                        out.write(rendered + "\n")
                        print(rendered)

                    out.flush()

                time.sleep(poll_seconds)
        except KeyboardInterrupt:
            out.write(f"{now_iso()} [monitor] interrupted\n")
            out.flush()
            print("monitor interrupted")
            return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import sys
from pathlib import Path


def _ensure_app_on_path() -> None:
    app_dir = Path(__file__).resolve().parent
    app_path = str(app_dir)
    if app_path not in sys.path:
        sys.path.insert(0, app_path)


def main():
    _ensure_app_on_path()
    from main import main as desktop_main

    return desktop_main()


if __name__ == "__main__":
    raise SystemExit(main() or 0)


from __future__ import annotations

import os
import platform
import sys
from pathlib import Path


def _ensure_project_paths() -> None:
    mobile_dir = Path(__file__).resolve().parent
    repo_root = mobile_dir.parent
    app_dir = repo_root / "App"
    for path in (str(mobile_dir), str(app_dir), str(repo_root)):
        if path not in sys.path:
            sys.path.insert(0, path)


def _is_android() -> bool:
    if hasattr(sys, "getandroidapilevel"):
        return True
    env = os.environ
    if env.get("ANDROID_ROOT") or env.get("ANDROID_DATA"):
        return True
    prefix = sys.prefix.lower()
    return "android" in prefix


def _is_ios() -> bool:
    if sys.platform == "ios":
        return True
    system = platform.system().strip().lower()
    if system != "darwin":
        return False
    plat = platform.platform().lower()
    if "iphone" in plat or "ipad" in plat or "ios" in plat:
        return True
    machine = platform.machine().lower()
    return "iphone" in machine or "ipad" in machine


def is_mobile_platform() -> bool:
    return _is_android() or _is_ios()


def main():
    _ensure_project_paths()
    if is_mobile_platform():
        print("Starting EON-OpenSlicer in mobile mode...")
        try:
            from Mobile.app_mobile import main as mobile_main
        except ImportError as exc:
            print(f"Error: Mobile dependencies not installed: {exc}")
            print("Please install: pip install -r Mobile/requirements-mobile.txt")
            return 1
        app = mobile_main()
        return app.main_loop()

    print("Starting EON-OpenSlicer in desktop mode...")
    try:
        from App.main import main as desktop_main
    except ImportError as exc:
        print(f"Error: Desktop dependencies not installed: {exc}")
        print("Please install: pip install -r App/requirements.txt")
        return 1
    return desktop_main()


if __name__ == "__main__":
    sys.exit(main() or 0)

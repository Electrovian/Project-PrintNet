from __future__ import annotations

import os
import platform
import sys
from pathlib import Path


def _ensure_app_on_path() -> None:
    app_dir = Path(__file__).resolve().parent
    if str(app_dir) not in sys.path:
        sys.path.insert(0, str(app_dir))


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
    _ensure_app_on_path()
    if is_mobile_platform():
        print("Starting EON-OpenSlicer in mobile mode...")
        try:
            from app_mobile import main as mobile_main
        except ImportError as exc:
            print(f"Error: Mobile dependencies not installed: {exc}")
            print("Please install: pip install -r Mobile/requirements-mobile.txt")
            return 1
        app = mobile_main()
        return app.main_loop()

    print("Starting EON-OpenSlicer in desktop mode...")
    try:
        from main import main as desktop_main
    except ImportError as exc:
        print(f"Error: Desktop dependencies not installed: {exc}")
        print("Please install: pip install -r App/requirements.txt")
        return 1
    return desktop_main()


if __name__ == "__main__":
    sys.exit(main() or 0)

import os
import sys


def _base_dir() -> str:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return getattr(sys, "_MEIPASS")
    return os.path.dirname(os.path.dirname(__file__))


def assets_dir() -> str:
    return os.path.join(_base_dir(), "assets")

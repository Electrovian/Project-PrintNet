import argparse
import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

def _build_suite(scope: str) -> unittest.TestSuite:
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    scope = (scope or "full").strip().lower()
    if scope == "gui":
        return loader.discover(start_dir, pattern="test_gui_*.py")
    if scope == "smoke":
        patterns = [
            "test_preview_utils.py",
            "test_arrange_utils.py",
            "test_selection_utils.py",
            "test_geometry_helpers.py",
            "test_gcode_extra.py",
            "test_slicer_helpers.py",
        ]
        suite = unittest.TestSuite()
        for pattern in patterns:
            suite.addTests(loader.discover(start_dir, pattern=pattern))
        return suite
    return loader.discover(start_dir, pattern="test_*.py")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scope",
        choices=("smoke", "full", "gui"),
        default=os.environ.get("TEST_SCOPE", "full"),
        help="Test scope: smoke, full, or gui",
    )
    args = parser.parse_args()

    suite = _build_suite(args.scope)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    raise SystemExit(main())

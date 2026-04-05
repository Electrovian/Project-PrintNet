import argparse
import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


SMOKE_TESTS = [
    "test_desktop_startup_smoke.py",
    "test_slicer_v2_scaffolding.py",
    "test_slicer_v2_cli_contract.py",
    "test_slicer_v2_fff_corpus.py",
    "test_gcode_output_contract_plumbing.py",
    "test_slice_plate_behavior.py",
    "test_slice_plate_scene_defaults.py",
    "test_desktop_plate_flow.py",
    "test_runtime_printer_state.py",
    "test_startup_validation.py",
    "test_device_view.py",
    "test_files_view_persistence.py",
    "test_activity_view.py",
    "test_printer_manager_demo.py",
    "test_gui_main_window.py",
    "test_gui_prepare_view.py",
    "test_gui_control_view.py",
]


def _build_suite(scope: str) -> unittest.TestSuite:
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    scope = (scope or "full").strip().lower()
    if scope == "gui":
        return loader.discover(start_dir, pattern="test_gui_*.py")
    if scope == "smoke":
        suite = unittest.TestSuite()
        for pattern in SMOKE_TESTS:
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
    verbosity = int(os.environ.get("TEST_VERBOSITY", "1") or "1")
    runner = unittest.TextTestRunner(verbosity=verbosity, buffer=True)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    raise SystemExit(main())

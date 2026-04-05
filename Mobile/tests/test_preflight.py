from __future__ import annotations

import io
import os
import sys
import types
import unittest
from contextlib import redirect_stdout
from unittest import mock

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from Mobile import preflight  # noqa: E402


class MobilePreflightTests(unittest.TestCase):
    def test_evaluate_preflight_tracks_required_and_optional_modules(self):
        def fake_find_spec(name: str):
            return object() if name == "requests" else None

        with mock.patch("importlib.util.find_spec", side_effect=fake_find_spec):
            result = preflight.evaluate_preflight(require_briefcase=False, import_app=False)

        self.assertFalse(result.ok)
        self.assertIn("toga", result.missing_required)
        self.assertIn("briefcase", result.missing_optional)

    def test_evaluate_preflight_can_require_briefcase(self):
        def fake_find_spec(name: str):
            return object() if name in {"toga", "requests"} else None

        with mock.patch("importlib.util.find_spec", side_effect=fake_find_spec):
            result = preflight.evaluate_preflight(require_briefcase=True, import_app=False)

        self.assertFalse(result.ok)
        self.assertIn("briefcase", result.missing_required)

    def test_main_reports_success_when_required_modules_and_import_are_available(self):
        fake_module = types.SimpleNamespace(main=lambda: None)

        def fake_find_spec(_name: str):
            return object()

        buf = io.StringIO()
        with mock.patch("importlib.util.find_spec", side_effect=fake_find_spec):
            with mock.patch("importlib.import_module", return_value=fake_module):
                with redirect_stdout(buf):
                    exit_code = preflight.main(["--skip-import-check"])

        output = buf.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("Result: PASS", output)
        self.assertIn("toga (required): ok", output)
        self.assertIn("Mobile.app_mobile import: skipped (Skipped by request.)", output)

    def test_main_reports_import_failure(self):
        def fake_find_spec(_name: str):
            return object()

        buf = io.StringIO()
        with mock.patch("importlib.util.find_spec", side_effect=fake_find_spec):
            with mock.patch("importlib.import_module", side_effect=RuntimeError("boom")):
                with redirect_stdout(buf):
                    exit_code = preflight.main([])

        output = buf.getvalue()
        self.assertEqual(exit_code, 1)
        self.assertIn("Mobile.app_mobile import: failed (boom)", output)
        self.assertIn("Result: FAIL", output)


if __name__ == "__main__":
    unittest.main()

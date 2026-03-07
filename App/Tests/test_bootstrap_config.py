from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from config.bootstrap import (  # noqa: E402
    load_bootstrap_config,
    mark_setup_completed,
    normalize_bootstrap_config,
    save_bootstrap_config,
    setup_completed,
)


class BootstrapConfigTests(unittest.TestCase):
    def test_normalize_bootstrap_config_defaults(self):
        payload = normalize_bootstrap_config({})
        self.assertEqual(payload["ui_language"], "en")
        self.assertEqual(payload["region_code"], "")
        self.assertFalse(setup_completed(payload))
        self.assertTrue(payload["connectivity_preferences"]["wifi_enabled"])

    def test_mark_setup_completed_sets_flag(self):
        payload = mark_setup_completed(
            {
                "ui_language": "es",
                "region_code": "US-NY",
                "connectivity_preferences": {"wifi_enabled": True, "bluetooth_enabled": False},
            }
        )
        self.assertEqual(payload["ui_language"], "es")
        self.assertTrue(setup_completed(payload))
        self.assertTrue(str(payload.get("setup_completed_at_utc", "")).strip())

    def test_save_and_load_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            appdata = Path(tmp).joinpath("AppData")
            with mock.patch.dict(os.environ, {"APPDATA": str(appdata)}, clear=False):
                saved = save_bootstrap_config(
                    {
                        "ui_language": "es",
                        "region_code": "US-TX",
                        "setup_completed_at_utc": "2026-01-01T00:00:00+00:00",
                        "connectivity_preferences": {"wifi_enabled": True, "bluetooth_enabled": True},
                    }
                )
                self.assertTrue(saved.exists())
                loaded = load_bootstrap_config()
                self.assertEqual(loaded["ui_language"], "es")
                self.assertEqual(loaded["region_code"], "US-TX")
                self.assertTrue(setup_completed(loaded))


if __name__ == "__main__":
    unittest.main()

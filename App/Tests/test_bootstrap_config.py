from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath
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
    user_config_dir,
    user_cache_dir,
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

    def test_user_cache_dir_windows_uses_localappdata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).joinpath("LocalAppData")
            with mock.patch("config.bootstrap.os.name", "nt"):
                with mock.patch.dict(os.environ, {"LOCALAPPDATA": str(root)}, clear=False):
                    self.assertEqual(user_cache_dir(), root.joinpath("EON-OpenSlicer", "cache"))

    def test_user_config_dir_windows_uses_appdata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).joinpath("AppData")
            with mock.patch("config.bootstrap.os.name", "nt"):
                with mock.patch.dict(os.environ, {"APPDATA": str(root)}, clear=False):
                    self.assertEqual(user_config_dir(), root.joinpath("EON-OpenSlicer"))

    def test_user_cache_dir_uses_xdg_cache_home_when_set(self):
        class _FakePosixPath(PurePosixPath):
            @classmethod
            def home(cls):
                return cls("/home/test")

        with tempfile.TemporaryDirectory() as tmp:
            root = _FakePosixPath("/tmp/xdg-cache")
            with mock.patch("config.bootstrap.os.name", "posix"):
                with mock.patch("config.bootstrap.Path", _FakePosixPath):
                    with mock.patch.dict(os.environ, {"XDG_CACHE_HOME": str(root)}, clear=False):
                        self.assertEqual(user_cache_dir(), root.joinpath("eon-openslicer"))

    def test_user_cache_dir_defaults_to_home_cache_directory(self):
        class _FakePosixPath(PurePosixPath):
            @classmethod
            def home(cls):
                return cls("/home/tester")

        with mock.patch("config.bootstrap.os.name", "posix"):
            with mock.patch("config.bootstrap.Path", _FakePosixPath):
                with mock.patch.dict(os.environ, {"XDG_CACHE_HOME": ""}, clear=False):
                    self.assertEqual(
                        user_cache_dir(),
                        _FakePosixPath.home().joinpath(".cache", "eon-openslicer"),
                    )


if __name__ == "__main__":
    unittest.main()

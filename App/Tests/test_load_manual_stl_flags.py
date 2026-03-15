import os
import sys
import unittest
from unittest import mock

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from gui.Windows.controller.load import LoadMixin  # noqa: E402


class _LoadController(LoadMixin):
    pass


class LoadManualStlFlagTests(unittest.TestCase):
    def test_non_windows_never_prefers_manual_mode(self):
        controller = _LoadController()
        with mock.patch("gui.Windows.controller.load.os.name", "posix"):
            with mock.patch.dict(
                os.environ,
                {
                    "EON_FORCE_MANUAL_STL_ENTRY": "1",
                    "EON_PREFER_MANUAL_STL_ENTRY": "1",
                },
                clear=True,
            ):
                self.assertFalse(controller._prefer_manual_stl_entry())

    def test_windows_force_flag_enables_manual_mode(self):
        controller = _LoadController()
        with mock.patch("gui.Windows.controller.load.os.name", "nt"):
            with mock.patch.dict(os.environ, {"EON_FORCE_MANUAL_STL_ENTRY": "1"}, clear=True):
                self.assertTrue(controller._prefer_manual_stl_entry())

    def test_windows_prefer_flag_enables_manual_mode(self):
        controller = _LoadController()
        with mock.patch("gui.Windows.controller.load.os.name", "nt"):
            with mock.patch.dict(os.environ, {"EON_PREFER_MANUAL_STL_ENTRY": "yes"}, clear=True):
                self.assertTrue(controller._prefer_manual_stl_entry())

    def test_windows_default_is_native_dialog(self):
        controller = _LoadController()
        with mock.patch("gui.Windows.controller.load.os.name", "nt"):
            with mock.patch.dict(os.environ, {}, clear=True):
                self.assertFalse(controller._prefer_manual_stl_entry())


if __name__ == "__main__":
    unittest.main()

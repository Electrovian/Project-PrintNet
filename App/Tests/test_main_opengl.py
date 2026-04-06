import os
import sys
import unittest
from unittest import mock

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import main  # noqa: E402


class MainOpenGLModeTests(unittest.TestCase):
    def test_normalize_opengl_mode_defaults_to_desktop_for_interactive_windows(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("EON_OPENGL_MODE", None)
            os.environ.pop("QT_OPENGL", None)
            os.environ.pop("QT_QPA_PLATFORM", None)
            with mock.patch.object(main.os, "name", "nt"):
                self.assertEqual(main.normalize_opengl_mode(None), "desktop")

    def test_normalize_opengl_mode_defaults_to_software_for_headless_platform(self):
        with mock.patch.dict(os.environ, {"QT_QPA_PLATFORM": "offscreen"}, clear=False):
            with mock.patch.object(main.os, "name", "nt"):
                self.assertEqual(main.normalize_opengl_mode(None), "software")

    def test_configure_opengl_mode_uses_qt_opengl_env_when_eon_override_is_missing(self):
        with mock.patch.dict(os.environ, {"QT_OPENGL": "desktop"}, clear=False):
            os.environ.pop("EON_OPENGL_MODE", None)
            with mock.patch.object(main, "ensure_qt_runtime_path") as ensure_runtime:
                with mock.patch.object(main.QtWidgets.QApplication, "instance", return_value=None):
                    with mock.patch.object(main.QtCore.QCoreApplication, "setAttribute") as set_attribute:
                        result = main.configure_opengl_mode()
                        selected_mode = os.environ.get("EON_OPENGL_MODE")
                        qt_mode = os.environ.get("QT_OPENGL")

        self.assertEqual(result, "desktop")
        self.assertEqual(selected_mode, "desktop")
        self.assertEqual(qt_mode, "desktop")
        ensure_runtime.assert_called_once_with()
        self.assertGreaterEqual(set_attribute.call_count, 1)

    def test_configure_opengl_mode_respects_explicit_mode_argument(self):
        with mock.patch.dict(os.environ, {"EON_OPENGL_MODE": "desktop", "QT_OPENGL": "desktop"}, clear=False):
            with mock.patch.object(main, "ensure_qt_runtime_path"):
                with mock.patch.object(main.QtWidgets.QApplication, "instance", return_value=None):
                    with mock.patch.object(main.QtCore.QCoreApplication, "setAttribute"):
                        result = main.configure_opengl_mode("software")
                        selected_mode = os.environ.get("EON_OPENGL_MODE")
                        qt_mode = os.environ.get("QT_OPENGL")

        self.assertEqual(result, "software")
        self.assertEqual(selected_mode, "software")
        self.assertEqual(qt_mode, "software")


if __name__ == "__main__":
    unittest.main()

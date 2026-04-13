import unittest
import os


def _configure_qt_test_environment() -> None:
    os.environ.setdefault("QT_OPENGL", "software")
    os.environ.setdefault("EON_OPENGL_MODE", "software")
    os.environ.setdefault("QT_QUICK_BACKEND", "software")


_configure_qt_test_environment()

try:
    from PyQt5 import QtWidgets, QtCore
except Exception:  # pragma: no cover - optional dependency in tests
    QtWidgets = None
    QtCore = None


class QtTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if QtWidgets is None:
            raise unittest.SkipTest("PyQt5 not available")
        cls._app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])

import unittest

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

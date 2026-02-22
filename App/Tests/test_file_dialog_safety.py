import os
import sys
import unittest
from unittest import mock

try:
    from PyQt5 import QtWidgets
except Exception:  # pragma: no cover - optional dependency in tests
    QtWidgets = None

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from gui.Windows.controller.load import LoadMixin
from gui.Windows.controller.ui import UiMixin


class _DialogController(LoadMixin, UiMixin):
    def __init__(self):
        self.main = QtWidgets.QWidget()
        self.loaded = []

    def _add_model_from_path_async(self, path: str):
        self.loaded.append(path)


class FileDialogSafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if QtWidgets is None:
            raise unittest.SkipTest("PyQt5 not available")
        cls._app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])

    def test_safe_open_file_names_uses_main_branch_call_shape(self):
        controller = _DialogController()
        with mock.patch.dict(os.environ, {"EON_USE_TK_FILE_DIALOG": "0"}):
            with mock.patch.object(
                QtWidgets.QFileDialog,
                "getOpenFileNames",
                return_value=([], ""),
            ) as mocked:
                controller._safe_get_open_file_names(
                    "Open STL files",
                    "",
                    "STL files (*.stl)",
                )
        self.assertTrue(mocked.called)
        self.assertEqual(len(mocked.call_args.args), 4)
        self.assertIn("options", mocked.call_args.kwargs)

    def test_tk_dialog_is_opt_in(self):
        controller = _DialogController()
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertFalse(controller._use_tk_file_dialog())

    def test_open_stl_dialog_uses_safe_dialog_result(self):
        controller = _DialogController()
        with mock.patch.object(controller, "_prefer_manual_stl_entry", return_value=False):
            with mock.patch.object(
                controller,
                "_safe_get_open_file_names",
                return_value=(["C:/tmp/one.stl", "C:/tmp/two.stl"], "STL files (*.stl)"),
            ):
                controller.open_stl_dialog()
        self.assertEqual(controller.loaded, ["C:/tmp/one.stl", "C:/tmp/two.stl"])

    def test_open_stl_dialog_uses_manual_fallback_when_picker_fails(self):
        controller = _DialogController()
        with mock.patch.object(
            controller,
            "_safe_get_open_file_names",
            side_effect=RuntimeError("dialog failed"),
        ):
            with mock.patch.object(
                controller,
                "_prompt_stl_paths_fallback",
                return_value=["C:/tmp/fallback.stl"],
            ):
                with mock.patch.object(QtWidgets.QMessageBox, "warning"):
                    controller.open_stl_dialog()
        self.assertEqual(controller.loaded, ["C:/tmp/fallback.stl"])

    def test_open_stl_dialog_manual_mode_bypasses_file_picker(self):
        controller = _DialogController()
        with mock.patch.object(controller, "_prefer_manual_stl_entry", return_value=True):
            with mock.patch.object(
                controller,
                "_safe_get_open_file_names",
                side_effect=AssertionError("file picker should not be called"),
            ):
                with mock.patch.object(
                    controller,
                    "_prompt_stl_paths_fallback",
                    return_value=["C:/tmp/manual.stl"],
                ):
                    controller.open_stl_dialog()
        self.assertEqual(controller.loaded, ["C:/tmp/manual.stl"])


if __name__ == "__main__":
    unittest.main()

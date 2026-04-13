import os
import sys
import unittest
from unittest import mock

from qt_harness import QtTestCase, QtWidgets

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_OPENGL", "software")
os.environ.setdefault("EON_OPENGL_MODE", "software")

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


class ViewerRuntimeTests(QtTestCase):
    def _build_viewer(self):
        from gui.viewer.core import Viewer3D

        viewer = Viewer3D()
        viewer.resize(800, 600)
        viewer.show()
        QtWidgets.QApplication.processEvents()
        self.addCleanup(viewer.close)
        return viewer

    @staticmethod
    def _mode_button(window, mode_id: str):
        for button in getattr(window, "_mode_tabs", []):
            if str(button.property("mode_id") or "").strip().lower() == mode_id:
                return button
        return None

    def test_gl_paint_failure_enters_degraded_state_once(self):
        viewer = self._build_viewer()

        with mock.patch.object(viewer, "_gl_context_ready", return_value=True):
            with mock.patch("gui.viewer.core.gl.GLViewWidget.paintGL", side_effect=RuntimeError("boom")) as paint:
                viewer.paintGL()
                viewer.paintGL()

        diagnostics = viewer.runtime_diagnostics()
        self.assertTrue(viewer.is_runtime_degraded())
        self.assertTrue(viewer._viewer_runtime_warning.isVisible())
        self.assertIn("RuntimeError: boom", str(diagnostics["viewer_runtime_error"]))
        self.assertEqual(int(diagnostics["viewer_runtime_failure_count"]), 1)
        self.assertEqual(paint.call_count, 1)

    def test_paint_skips_when_gl_context_is_not_ready(self):
        viewer = self._build_viewer()

        with mock.patch.object(viewer, "_gl_context_ready", return_value=False):
            with mock.patch("gui.viewer.core.gl.GLViewWidget.paintGL") as paint:
                result = viewer.paintGL()

        self.assertIsNone(result)
        self.assertFalse(viewer.is_runtime_degraded())
        paint.assert_not_called()

    def test_paint_skips_when_viewer_updates_are_disabled(self):
        viewer = self._build_viewer()
        viewer.setUpdatesEnabled(False)

        with mock.patch.object(viewer, "_gl_context_ready", return_value=True):
            with mock.patch("gui.viewer.core.gl.GLViewWidget.paintGL") as paint:
                result = viewer.paintGL()

        self.assertIsNone(result)
        self.assertFalse(viewer.is_runtime_degraded())
        paint.assert_not_called()

    def test_transient_gl_clear_error_does_not_degrade_viewer(self):
        viewer = self._build_viewer()
        transient = RuntimeError("GLError: invalid operation baseOperation = glClearColor")

        with mock.patch.object(viewer, "_gl_context_ready", return_value=True):
            with mock.patch("gui.viewer.core.gl.GLViewWidget.paintGL", side_effect=transient) as paint:
                result = viewer.paintGL()

        self.assertIsNone(result)
        self.assertFalse(viewer.is_runtime_degraded())
        self.assertEqual(paint.call_count, 1)

    def test_degraded_viewer_keeps_main_window_navigation_usable(self):
        from gui.main_window import MainWindow

        window = MainWindow(
            [
                {
                    "name": "Demo Core",
                    "connector_type": "local_file",
                    "bed_x": 256,
                    "bed_y": 256,
                    "bed_z": 256,
                }
            ],
            {},
        )
        window.resize(1400, 900)
        window.show()
        QtWidgets.QApplication.processEvents()
        self.addCleanup(window.close)

        window.viewer._enter_runtime_degraded("forced test failure")
        QtWidgets.QApplication.processEvents()

        self.assertTrue(window.viewer.is_runtime_degraded())

        files_button = self._mode_button(window, "files")
        device_button = self._mode_button(window, "device")
        prepare_button = self._mode_button(window, "prepare")

        self.assertIsNotNone(files_button)
        self.assertIsNotNone(device_button)
        self.assertIsNotNone(prepare_button)
        assert files_button is not None
        assert device_button is not None
        assert prepare_button is not None

        files_button.click()
        QtWidgets.QApplication.processEvents()
        self.assertIs(window._central_stack.currentWidget(), window.files_view)
        self.assertFalse(window.viewer.updatesEnabled())

        device_button.click()
        QtWidgets.QApplication.processEvents()
        self.assertIs(window._central_stack.currentWidget(), window.device_view)
        self.assertFalse(window.viewer.updatesEnabled())

        prepare_button.click()
        QtWidgets.QApplication.processEvents()
        self.assertIs(window._central_stack.currentWidget(), window.viewer)
        self.assertTrue(window.viewer.updatesEnabled())
        self.assertTrue(window.viewer._viewer_runtime_warning.isVisible())


if __name__ == "__main__":
    unittest.main()

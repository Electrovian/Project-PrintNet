import os
import sys
import unittest
from unittest import mock

from qt_harness import QtCore, QtTestCase, QtWidgets

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


class _FakeViewer(QtWidgets.QWidget):
    modelPicked = QtCore.pyqtSignal(int)
    modelMoved = QtCore.pyqtSignal(int)
    modelRotated = QtCore.pyqtSignal(int)
    selectionChanged = QtCore.pyqtSignal(list)
    simplifyRequested = QtCore.pyqtSignal(int)
    sceneChanged = QtCore.pyqtSignal()
    plateAutoOrientRequested = QtCore.pyqtSignal()
    plateArrangeRequested = QtCore.pyqtSignal()
    plateRemoveRequested = QtCore.pyqtSignal(int)
    plateLockChanged = QtCore.pyqtSignal(int, bool)
    plateNameChanged = QtCore.pyqtSignal(int, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.models = {}
        self.opts = {"fov": 60}
        self.preview_color_mode = None
        self.preview_feature_filter = None
        self._wireframe_enabled = False

    def apply_theme(self):
        return None

    def set_snap(self, *_args):
        return None

    def set_labels_visible(self, *_args):
        return None

    def set_bed_limits(self, *_args):
        return None

    def set_bed_visuals(self, *_args, **_kwargs):
        return None

    def reset_view(self):
        return None

    def set_view(self, *_args):
        return None

    def set_view_cube_visible(self, *_args):
        return None

    def set_wireframe_enabled(self, enabled):
        self._wireframe_enabled = bool(enabled)

    def get_wireframe_enabled(self):
        return bool(self._wireframe_enabled)

    def set_overhang_visible(self, *_args, **_kwargs):
        return None

    def set_prepare_tool(self, *_args):
        return None

    def set_interaction_enabled(self, *_args):
        return None

    def set_plate_overlay_visible(self, *_args):
        return None

    def set_preview_visible(self, *_args):
        return None

    def set_models_visible(self, *_args):
        return None

    def set_models_preview_alpha(self, *_args):
        return None

    def set_platform_visible(self, *_args):
        return None

    def set_nozzle_visible(self, *_args):
        return None

    def set_print_stats_visible(self, *_args):
        return None

    def set_preview_object_visible(self, *_args):
        return None

    def set_preview_color_mode(self, mode):
        self.preview_color_mode = mode

    def set_preview_feature_filter(self, features):
        self.preview_feature_filter = list(features) if features else None

    def get_preview_nozzle_state(self):
        return ((1.0, 2.0, 3.0), 120.0, True)

    def set_preview_step_index(self, *_args):
        return None

    def set_selected_models(self, *_args, **_kwargs):
        return None

    def serialize_scene(self):
        return {}

    def get_all_model_ids(self):
        return []

    def get_model_ids(self):
        return []

    def get_selected_models(self):
        return []

    def get_plate_ids(self):
        return []

    def get_plate_model_ids(self, _plate_id):
        return []


class _SizedPage(QtWidgets.QWidget):
    def __init__(self, size_hint: QtCore.QSize, minimum_size_hint: QtCore.QSize, parent=None):
        super().__init__(parent)
        self._size_hint = QtCore.QSize(size_hint)
        self._minimum_size_hint = QtCore.QSize(minimum_size_hint)

    def sizeHint(self):
        return QtCore.QSize(self._size_hint)

    def minimumSizeHint(self):
        return QtCore.QSize(self._minimum_size_hint)


class MainWindowGuiTests(QtTestCase):
    def setUp(self):
        settings = QtCore.QSettings("EON", "OpenSlicer")
        settings.clear()
        settings.sync()

    def _build_window(self):
        from gui.main_window import MainWindow

        printers = [
            {
                "name": "Alpha",
                "connector_type": "octoprint",
                "octoprint_url": "http://alpha.local",
                "bed_x": 256,
                "bed_y": 256,
                "bed_z": 256,
            },
            {
                "name": "Beta",
                "connector_type": "moonraker",
                "moonraker_url": "http://beta.local",
                "bed_x": 300,
                "bed_y": 300,
                "bed_z": 340,
            },
        ]
        patcher = mock.patch("gui.Windows.prepare.Viewer3D", _FakeViewer)
        patcher.start()
        self.addCleanup(patcher.stop)
        window = MainWindow(printers, {})
        window.show()
        QtWidgets.QApplication.processEvents()
        self.addCleanup(window.close)
        return window

    @staticmethod
    def _mode_button(window, *, mode_id=None, mode_key=None):
        for button in getattr(window, "_mode_tabs", []):
            if mode_id is not None and str(button.property("mode_id") or "").strip().lower() == mode_id:
                return button
            if mode_key is not None and str(button.property("mode_key") or "").strip().lower() == mode_key:
                return button
        return None

    def _click_mode(self, window, *, mode_id=None, mode_key=None):
        button = self._mode_button(window, mode_id=mode_id, mode_key=mode_key)
        self.assertIsNotNone(button)
        assert button is not None
        button.click()
        QtWidgets.QApplication.processEvents()
        return button

    def test_topbar_routes_switch_visible_surface_and_panels(self):
        window = self._build_window()

        mode_routes = [
            (str(button.property("mode_id")), str(button.property("mode_key")))
            for button in window._mode_tabs
        ]
        self.assertEqual(
            mode_routes,
            [
                ("files", "files"),
                ("activity", "activity"),
                ("prepare", "prepare"),
                ("preview", "preview"),
                ("device", "device"),
                ("project", "files"),
                ("calibration", "control"),
            ],
        )

        self._click_mode(window, mode_id="prepare")
        self.assertIs(window._central_stack.currentWidget(), window.viewer)
        self.assertTrue(window._settings_dock.isVisible())
        self.assertTrue(window.transform_toolbar.isVisible())
        self.assertFalse(window.preview_view._preview_panel.isVisible())

        self._click_mode(window, mode_id="preview")
        self.assertIs(window._central_stack.currentWidget(), window.viewer)
        self.assertFalse(window._settings_dock.isVisible())
        self.assertFalse(window.transform_toolbar.isVisible())
        self.assertTrue(window.preview_view._preview_panel.isVisible())

        self._click_mode(window, mode_id="files")
        self.assertIs(window._central_stack.currentWidget(), window.files_view)
        self.assertFalse(window.preview_view._preview_panel.isVisible())

        self._click_mode(window, mode_id="activity")
        self.assertIs(window._central_stack.currentWidget(), window.activity_view)

        window._topbar_print_btn.click()
        QtWidgets.QApplication.processEvents()
        self.assertIs(window._central_stack.currentWidget(), window.device_view)

        self._click_mode(window, mode_id="calibration")
        self.assertIs(window._central_stack.currentWidget(), window.control_view)

        window._home_btn.click()
        QtWidgets.QApplication.processEvents()
        self.assertIs(window._central_stack.currentWidget(), window.viewer)
        self.assertTrue(window._settings_dock.isVisible())

    def test_active_page_stacked_widget_uses_current_page_hints(self):
        from gui.main_window import _ActivePageStackedWidget

        stack = _ActivePageStackedWidget()
        self.addCleanup(stack.deleteLater)

        compact = _SizedPage(QtCore.QSize(320, 200), QtCore.QSize(280, 180), stack)
        wide = _SizedPage(QtCore.QSize(960, 720), QtCore.QSize(900, 680), stack)
        stack.addWidget(compact)
        stack.addWidget(wide)

        stack.setCurrentWidget(compact)
        self.assertEqual(stack.sizeHint(), QtCore.QSize(320, 200))
        self.assertEqual(stack.minimumSizeHint(), QtCore.QSize(280, 180))

        stack.setCurrentWidget(wide)
        self.assertEqual(stack.sizeHint(), QtCore.QSize(960, 720))
        self.assertEqual(stack.minimumSizeHint(), QtCore.QSize(900, 680))

    def test_printer_selection_and_refresh_stay_in_sync_across_views(self):
        window = self._build_window()

        self._click_mode(window, mode_id="preview")
        self.assertTrue(window.preview_view._printer_row.isVisible())
        window.device_view.select_printer_by_name("Beta")
        QtWidgets.QApplication.processEvents()

        self.assertEqual(window.device_view._printer_combo.currentText(), "Beta")
        self.assertEqual(window.control_view._printer_combo.currentText(), "Beta")
        self.assertEqual(window.preview_view._printer_combo.currentText(), "Beta")
        self.assertEqual(window.settings_panel._printer_combo.currentText(), "Beta")
        self.assertEqual(getattr(window.runtime_printer_state, "name", ""), "Beta")

        gamma = {
            "name": "Gamma",
            "connector_type": "prusalink",
            "prusalink_url": "http://gamma.local",
            "bed_x": 250,
            "bed_y": 210,
            "bed_z": 220,
        }
        window.printer_manager.printers = list(window.printer_manager.printers) + [gamma]
        window.printer_manager.active_printer = dict(gamma)
        window._refresh_printer_views()
        QtWidgets.QApplication.processEvents()

        self.assertEqual(window.device_view._printer_combo.count(), 3)
        self.assertEqual(window.control_view._printer_combo.count(), 3)
        self.assertEqual(window.preview_view._printer_combo.count(), 3)
        self.assertEqual(window.settings_panel._printer_combo.count(), 3)
        self.assertEqual(window.device_view._printer_combo.currentText(), "Gamma")
        self.assertEqual(window.control_view._printer_combo.currentText(), "Gamma")
        self.assertEqual(window.preview_view._printer_combo.currentText(), "Gamma")
        self.assertEqual(getattr(window.runtime_printer_state, "name", ""), "Gamma")


if __name__ == "__main__":
    unittest.main()

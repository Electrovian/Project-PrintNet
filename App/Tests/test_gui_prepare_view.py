import os
import sys
import unittest
from unittest import mock

from qt_harness import QtTestCase, QtWidgets

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


class _FakeViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(800, 600)
        self.theme_applied = False

    def apply_theme(self):
        self.theme_applied = True


class _PrepareMainStub(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.slice_calls = 0
        self.open_device_calls = 0

    def slice_current_plate(self):
        self.slice_calls += 1

    def _open_device_view(self):
        self.open_device_calls += 1

    def _handle_prepare_action(self, _action_id):
        return None

    def _on_transform_position_changed(self, *_args):
        return None

    def _on_transform_center_requested(self):
        return None

    def _on_transform_rotation_changed(self, *_args):
        return None

    def _on_transform_rotation_reset(self):
        return None

    def _on_transform_scale_changed(self, *_args):
        return None

    def _on_auto_orient_requested(self, *_args):
        return None

    def _on_auto_orient_reset(self):
        return None

    def _on_arrange_requested(self, *_args):
        return None

    def _on_arrange_selected_requested(self, *_args):
        return None

    def _on_arrange_reset(self):
        return None


class PrepareViewGuiTests(QtTestCase):
    def _build_view(self):
        from gui.Windows.prepare import PrepareView

        with mock.patch("gui.Windows.prepare.Viewer3D", _FakeViewer):
            main = _PrepareMainStub()
            main.resize(1280, 860)
            view = PrepareView(main)
            main.setCentralWidget(view.viewer)
            main.show()
            QtWidgets.QApplication.processEvents()
            self.addCleanup(main.close)
            return view, main

    def test_prepare_view_shows_docks_toolbar_and_floating_actions(self):
        with mock.patch.dict(os.environ, {"EON_FLOATING_PREPARE_ACTIONS": "1"}):
            view, main = self._build_view()

        main.viewer.resize(960, 720)
        view.show()
        QtWidgets.QApplication.processEvents()

        self.assertTrue(main._settings_dock.isVisible())
        self.assertTrue(main.transform_toolbar.isVisible())
        self.assertTrue(view._action_panel.isVisible())

        view.position_panels()
        QtWidgets.QApplication.processEvents()
        geometry = view._action_panel.geometry()
        self.assertGreaterEqual(geometry.x(), 0)
        self.assertGreaterEqual(geometry.y(), 0)
        self.assertLessEqual(geometry.right(), view.viewer.width())
        self.assertLessEqual(geometry.bottom(), view.viewer.height())

        main._popup_move.show()
        main._popup_rotate.show()
        view.hide()
        QtWidgets.QApplication.processEvents()

        self.assertFalse(main._settings_dock.isVisible())
        self.assertFalse(main.transform_toolbar.isVisible())
        self.assertFalse(view._action_panel.isVisible())
        self.assertFalse(main._popup_move.isVisible())
        self.assertFalse(main._popup_rotate.isVisible())

    def test_prepare_action_buttons_route_slice_and_print(self):
        with mock.patch.dict(os.environ, {"EON_FLOATING_PREPARE_ACTIONS": "0"}):
            view, main = self._build_view()

        view._slice_btn.click()
        view._print_btn.click()

        view.apply_theme()

        self.assertEqual(main.slice_calls, 1)
        self.assertEqual(main.open_device_calls, 1)
        self.assertIs(main.viewer, view.viewer)
        self.assertIs(main.settings_panel, view.settings_panel)
        self.assertIs(main.model_panel, view.model_panel)
        self.assertTrue(view.viewer.theme_applied)


if __name__ == "__main__":
    unittest.main()

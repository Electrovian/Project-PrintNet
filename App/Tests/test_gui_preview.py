import unittest
from typing import TYPE_CHECKING

from qt_harness import QtCore, QtTestCase, QtWidgets


class PreviewViewTests(QtTestCase):

    def _build(self):
        from gui.Windows.preview import PreviewView

        main = _DummyMain()
        viewer = _DummyViewer()
        view = PreviewView(main, viewer)
        return view, main, viewer

    def test_platform_nozzle_toggles(self):
        view, _main, viewer = self._build()
        self.assertTrue(view._platform_check.isChecked())
        self.assertTrue(view._nozzle_check.isChecked())
        self.assertTrue(viewer.platform_visible)
        self.assertTrue(viewer.nozzle_visible)

        view._platform_check.setChecked(False)
        view._nozzle_check.setChecked(False)
        self.assertFalse(viewer.platform_visible)
        self.assertFalse(viewer.nozzle_visible)

    def test_color_mode_mapping(self):
        view, _main, viewer = self._build()
        view._on_color_mode_changed("Speed")
        self.assertEqual(viewer.preview_color_mode, "speed")
        view._on_color_mode_changed("Flow")
        self.assertEqual(viewer.preview_color_mode, "flow")
        view._on_color_mode_changed("Line Type")
        self.assertEqual(viewer.preview_color_mode, "feature")

    def test_nozzle_info_updates(self):
        view, _main, _viewer = self._build()
        view._update_nozzle_info()
        text = view._nozzle_info.text()
        self.assertIn("X: 1.000", text)
        self.assertIn("Speed:", text)
        self.assertIn("Print", text)

    def test_feature_filter_sync(self):
        view, _main, viewer = self._build()
        first = view._line_table.item(0, 0)
        self.assertIsNotNone(first)
        assert first is not None
        assert QtCore is not None
        first.setCheckState(QtCore.Qt.Unchecked)
        view._sync_feature_filter()
        preview_feature_filter = viewer.preview_feature_filter
        self.assertIsInstance(preview_feature_filter, list)
        self.assertIsNotNone(preview_feature_filter)
        assert preview_feature_filter is not None
        self.assertGreater(len(preview_feature_filter), 0)


if TYPE_CHECKING:
    from PyQt5 import QtWidgets as _QtWidgets

    class _DummyMain(_QtWidgets.QWidget):
        printers: list[dict]
        sliced: bool
        opened: bool

        def slice_current_model(self) -> None: ...
        def _open_device_view(self) -> None: ...


    class _DummyViewer(_QtWidgets.QWidget):
        platform_visible: bool | None
        nozzle_visible: bool | None
        preview_color_mode: str | None
        preview_feature_filter: list | None

        def set_platform_visible(self, visible: bool) -> None: ...
        def set_nozzle_visible(self, visible: bool) -> None: ...
        def set_preview_color_mode(self, mode: str) -> None: ...
        def set_preview_feature_filter(self, features): ...
        def get_preview_nozzle_state(self): ...
elif QtWidgets is not None:
    class _DummyMain(QtWidgets.QWidget):
        def __init__(self):
            super().__init__()
            self.printers = [{"name": "Demo"}]
            self.sliced = False
            self.opened = False

        def slice_current_model(self):
            self.sliced = True

        def _open_device_view(self):
            self.opened = True


    class _DummyViewer(QtWidgets.QWidget):
        def __init__(self):
            super().__init__()
            self.platform_visible = None
            self.nozzle_visible = None
            self.preview_color_mode = None
            self.preview_feature_filter = None

        def set_platform_visible(self, visible: bool):
            self.platform_visible = bool(visible)

        def set_nozzle_visible(self, visible: bool):
            self.nozzle_visible = bool(visible)

        def set_preview_color_mode(self, mode: str):
            self.preview_color_mode = mode

        def set_preview_feature_filter(self, features):
            self.preview_feature_filter = list(features) if features else None

        def get_preview_nozzle_state(self):
            return ((1.0, 2.0, 3.0), 120.0, True)


if __name__ == "__main__":
    unittest.main()

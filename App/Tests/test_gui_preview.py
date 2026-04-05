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

    def test_preview_features_expand_line_type_table(self):
        from slicer_v2.legacy_gcode_preview import parse_gcode_preview

        view, _main, viewer = self._build()
        preview = parse_gcode_preview(
            [
                ";LAYER:0",
                ";TYPE:INFILL",
                "G1 X0 Y0 Z0.2 F1200",
                "G1 X10 Y0 E0.6 F1200",
            ]
        )
        preview.layers[0].segments[-1].feature = "custom_feature"
        view.set_preview_data(preview)

        keys = []
        for row in range(view._line_table.rowCount()):
            item = view._line_table.item(row, 0)
            if item is None:
                continue
            keys.append(str(item.data(QtCore.Qt.UserRole)))
        self.assertIn("custom_feature", keys)

        outer_row = None
        for row in range(view._line_table.rowCount()):
            item = view._line_table.item(row, 0)
            if item is not None and item.data(QtCore.Qt.UserRole) == "outer_wall":
                outer_row = row
                break
        self.assertIsNotNone(outer_row)
        assert outer_row is not None
        display_item = view._line_table.item(outer_row, 4)
        self.assertIsNotNone(display_item)
        assert display_item is not None
        display_item.setCheckState(QtCore.Qt.Unchecked)

        view._sync_feature_filter()
        self.assertIsInstance(viewer.preview_feature_filter, list)
        assert viewer.preview_feature_filter is not None
        self.assertIn("custom_feature", viewer.preview_feature_filter)

    def test_display_cell_click_toggles_feature_checkbox(self):
        view, _main, _viewer = self._build()
        display_item = view._line_table.item(0, 4)
        self.assertIsNotNone(display_item)
        assert display_item is not None
        display_item.setCheckState(QtCore.Qt.Checked)

        view._on_display_item_pressed(display_item)
        view._on_line_table_cell_clicked(0, 4)

        self.assertEqual(display_item.checkState(), QtCore.Qt.Unchecked)

    def test_display_indicator_click_does_not_double_toggle(self):
        view, _main, _viewer = self._build()
        display_item = view._line_table.item(0, 4)
        self.assertIsNotNone(display_item)
        assert display_item is not None
        display_item.setCheckState(QtCore.Qt.Checked)

        view._on_display_item_pressed(display_item)
        # Simulate Qt toggling when clicking directly on the checkbox indicator.
        display_item.setCheckState(QtCore.Qt.Unchecked)
        view._on_line_table_cell_clicked(0, 4)

        self.assertEqual(display_item.checkState(), QtCore.Qt.Unchecked)

    def test_update_stats_renders_ai_and_support_diagnostics(self):
        view, _main, _viewer = self._build()
        view.update_stats(
            {
                "ai_warnings": ["Thin walls detected"],
                "ai_suggestions": ["Enable supports for overhangs"],
                "support_diagnostics": {
                    "status": "warnings",
                    "support_type": "tree",
                    "support_style": "organic",
                    "diagnostics_source": "supports_stage",
                    "support_build_plate_only": True,
                    "support_region_count": 2,
                    "support_path_count": 5,
                    "unsupported_island_count_total": 1,
                    "tree_branch_count_total": 4,
                    "tree_trunk_count_total": 1,
                    "tree_merge_count_total": 1,
                    "tree_collision_avoid_count_total": 2,
                    "tree_pruned_branch_count_total": 1,
                    "tree_parent_assignment_count_total": 3,
                    "tree_branch_trunk_assignment_counts": {"child": 3, "trunk": 1},
                    "warnings": [
                        "support_planning:tree_style=organic",
                        "layer_1:tree_collision_avoided=2",
                    ],
                },
            }
        )
        text = view._diagnostics_value.toPlainText()
        self.assertIn("AI Checks", text)
        self.assertIn("Thin walls detected", text)
        self.assertIn("Support Diagnostics", text)
        self.assertIn("Status: warnings", text)
        self.assertIn("Style: organic", text)
        self.assertIn("Tree branches: 4", text)
        self.assertIn("layer_1:tree_collision_avoided=2", text)

    def test_update_stats_defaults_diagnostics_pane_when_empty(self):
        view, _main, _viewer = self._build()
        view.update_stats({})
        text = view._diagnostics_value.toPlainText()
        self.assertIn("AI Checks", text)
        self.assertIn("All checks passed.", text)
        self.assertIn("Support Diagnostics", text)
        self.assertIn("No support diagnostics available.", text)


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

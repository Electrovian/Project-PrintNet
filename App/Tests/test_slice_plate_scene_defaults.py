import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from gui.Windows.controller.print import PrintMixin  # noqa: E402
from gui.scene_state import SceneState  # noqa: E402
from slicer_v2.legacy_gcode_writer import SliceSettings  # noqa: E402


class _ViewerStub:
    def __init__(self):
        self.scene_state = SceneState()
        instance = self.scene_state.add_imported_object(
            "Part",
            "part.stl",
            [
                {
                    "name": "Part",
                    "vertices": [[0.0, 0.0, 0.0], [10.0, 0.0, 0.0], [0.0, 10.0, 0.0]],
                    "faces": [[0, 1, 2]],
                    "source_path": "part.stl",
                }
            ],
        )
        clone = self.scene_state.add_imported_object(
            "Part 2",
            "part-2.stl",
            [
                {
                    "name": "Part 2",
                    "vertices": [[0.0, 0.0, 0.0], [8.0, 0.0, 0.0], [0.0, 8.0, 0.0]],
                    "faces": [[0, 1, 2]],
                    "source_path": "part-2.stl",
                }
            ],
        )
        self._model_ids = [int(instance.id), int(clone.id)]

    def get_model_ids(self):
        return list(self._model_ids)


class _SettingsDefaultsController(PrintMixin):
    def __init__(self, settings, viewer):
        self._settings = settings
        self.viewer = viewer
        self.settings_panel = type(
            "_SettingsPanelStub",
            (),
            {"to_settings": lambda panel_self: self._settings},
        )()


class SlicePlateSceneDefaultsTests(unittest.TestCase):
    def test_settings_defaults_merge_scene_adaptive_layers(self):
        settings = SliceSettings()
        settings.adaptive_layering_enabled = False
        settings.adaptive_layer_ranges = ()
        viewer = _ViewerStub()
        viewer.scene_state.tool_state.adaptive_layer_ranges = {
            "1": [{"z_min_mm": 0.0, "z_max_mm": 5.0, "layer_height_mm": 0.12}]
        }
        controller = _SettingsDefaultsController(settings, viewer)

        resolved = controller._settings_with_slice_defaults()

        self.assertTrue(resolved.adaptive_layering_enabled)
        self.assertEqual(len(list(resolved.adaptive_layer_ranges)), 1)
        self.assertEqual(float(resolved.adaptive_layer_ranges[0]["layer_height_mm"]), 0.12)

    def test_settings_defaults_merge_overlapping_ranges_to_smallest_height(self):
        settings = SliceSettings()
        settings.adaptive_layering_enabled = False
        settings.adaptive_layer_ranges = ()
        viewer = _ViewerStub()
        viewer.scene_state.tool_state.adaptive_layer_ranges = {
            "1": [{"z_min_mm": 0.0, "z_max_mm": 5.0, "layer_height_mm": 0.20}],
            "2": [{"z_min_mm": 2.0, "z_max_mm": 4.0, "layer_height_mm": 0.10}],
        }
        controller = _SettingsDefaultsController(settings, viewer)

        resolved = controller._settings_with_slice_defaults()
        ranges = list(resolved.adaptive_layer_ranges)

        self.assertEqual(len(ranges), 3)
        self.assertEqual(ranges[0], {"z_min_mm": 0.0, "z_max_mm": 2.0, "layer_height_mm": 0.2})
        self.assertEqual(ranges[1], {"z_min_mm": 2.0, "z_max_mm": 4.0, "layer_height_mm": 0.1})
        self.assertEqual(ranges[2], {"z_min_mm": 4.0, "z_max_mm": 5.0, "layer_height_mm": 0.2})


if __name__ == "__main__":
    unittest.main()

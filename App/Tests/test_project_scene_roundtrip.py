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

from gui.Windows.controller.project import ProjectMixin  # noqa: E402
from gui.scene_state import SceneState  # noqa: E402
from slicer_v2.legacy_gcode_writer import SliceSettings  # noqa: E402


def _triangle_part(name: str, size: float = 10.0):
    return {
        "name": name,
        "vertices": [[0.0, 0.0, 0.0], [float(size), 0.0, 0.0], [0.0, float(size), 0.0]],
        "faces": [[0, 1, 2]],
        "source_path": f"{name}.stl",
    }


class _ViewerStub:
    def __init__(self):
        self.scene_state = SceneState()
        first = self.scene_state.add_imported_object("Base", "base.stl", [_triangle_part("Base")])
        second_plate = self.scene_state.create_plate("02")
        second = self.scene_state.add_imported_object("Lid", "lid.stl", [_triangle_part("Lid", 6.0)], plate_id=second_plate.id)
        self.scene_state.tool_state.annotations = {
            str(int(first.id)): {"support": [0, 1]},
            str(int(second.id)): {"fuzzy": [2]},
        }
        self.scene_state.tool_state.adaptive_layer_ranges = {
            str(int(first.id)): [{"z_min_mm": 0.0, "z_max_mm": 5.0, "layer_height_mm": 0.12}]
        }
        self.scene_state.selected_plate_id = int(second_plate.id)
        self.scene_state.selected_entity_ids = [int(second.id)]
        self.models = {}
        self._rebuild_models()

    def _rebuild_models(self):
        self.models = {}
        for instance_id, instance in self.scene_state.instances.items():
            obj = self.scene_state.objects.get(int(instance.object_id))
            self.models[int(instance_id)] = {
                "id": int(instance_id),
                "name": str(getattr(obj, "name", "") or f"Model {instance_id}"),
                "path": str(getattr(obj, "source_path", "") or ""),
                "plate_id": int(instance.plate_id),
                "object_id": int(instance.object_id),
            }

    def serialize_scene(self):
        return self.scene_state.to_dict()

    def restore_scene(self, payload):
        self.scene_state = SceneState.from_dict(payload)
        self._rebuild_models()

    def clear_all_models(self):
        self.scene_state = SceneState()
        self.models = {}

    def get_all_model_ids(self):
        return self.scene_state.get_all_instance_ids()

    def get_model_ids(self):
        return self.scene_state.get_plate_instance_ids(self.scene_state.selected_plate_id)

    def set_selected_models(self, ids, emit_signal=False):  # noqa: ARG002
        resolved = [int(item_id) for item_id in list(ids or []) if int(item_id) in self.scene_state.instances]
        self.scene_state.selected_entity_ids = resolved
        if resolved:
            plate_id = int(self.scene_state.instances[resolved[0]].plate_id)
            self.scene_state.selected_plate_id = plate_id


class _SettingsPanelStub:
    def __init__(self):
        self._settings = SliceSettings()
        self.applied = []

    def to_settings(self):
        return self._settings

    def apply_settings(self, payload):
        self.applied.append(dict(payload or {}))


class _ModelPanelStub:
    def __init__(self):
        self.list_widget = QtWidgets.QTreeWidget() if QtWidgets is not None else None
        self.refresh_calls = 0
        self.cleared = 0

    def refresh_from_viewer(self, viewer):  # noqa: ARG002
        self.refresh_calls += 1

    def clear_selection(self):
        self.cleared += 1


class _ProjectController(ProjectMixin):
    def __init__(self):
        self.main = QtWidgets.QWidget()
        self.viewer = _ViewerStub()
        self.model_panel = _ModelPanelStub()
        self.settings_panel = _SettingsPanelStub()
        self._current_project_path = None
        self._undo_in_progress = False
        self._undo_stack = []
        self._redo_stack = []
        self.current_model_id = None
        self.selected_in_panel = []
        self.popup_syncs = 0
        self.files_refreshes = 0
        self.undo_pushes = 0
        self._status_bar = QtWidgets.QStatusBar()

    def statusBar(self):
        return self._status_bar

    def _clear_all_models(self):
        self.viewer.clear_all_models()

    def _get_current_stl_path(self):
        return None

    def _select_model_in_panel(self, model_ids):
        if isinstance(model_ids, (list, tuple)):
            self.selected_in_panel = [int(item_id) for item_id in model_ids]
        elif model_ids is None:
            self.selected_in_panel = []
        else:
            self.selected_in_panel = [int(model_ids)]

    def _sync_popups(self):
        self.popup_syncs += 1

    def _push_undo_state(self):
        self.undo_pushes += 1
        self._undo_stack.append({"undo": self.undo_pushes})

    def _refresh_files_view(self):
        self.files_refreshes += 1


class ProjectSceneRoundTripTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if QtWidgets is None:
            raise unittest.SkipTest("PyQt5 not available")
        cls._app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])

    def test_serialize_project_emits_v2_scene_payload(self):
        controller = _ProjectController()

        payload = controller._serialize_project()

        self.assertEqual(payload["version"], 2)
        self.assertEqual(len(payload["plates"]), 2)
        self.assertEqual(len(payload["objects"]), 2)
        self.assertEqual(len(payload["instances"]), 2)
        self.assertEqual(payload["selected_plate_id"], 2)
        self.assertEqual(payload["selected_entity_ids"], [2])
        self.assertIn("settings", payload)
        self.assertIn("tool_state", payload)
        self.assertIn("annotations", payload["tool_state"])

    def test_load_project_data_restores_v2_scene_selection_and_settings(self):
        source = _ProjectController()
        payload = source._serialize_project()
        controller = _ProjectController()
        controller.viewer.clear_all_models()
        controller.current_model_id = None

        with mock.patch.object(QtWidgets.QMessageBox, "warning"):
            controller._load_project_data(payload, base_dir="")

        self.assertEqual(controller.viewer.scene_state.get_plate_ids(), [1, 2])
        self.assertEqual(controller.viewer.scene_state.selected_plate_id, 2)
        self.assertEqual(controller.viewer.scene_state.selected_entity_ids, [2])
        self.assertEqual(controller.current_model_id, 2)
        self.assertEqual(controller.selected_in_panel, [2])
        self.assertEqual(controller.model_panel.refresh_calls, 1)
        self.assertGreaterEqual(controller.files_refreshes, 1)
        self.assertGreaterEqual(controller.undo_pushes, 1)
        self.assertEqual(len(controller.settings_panel.applied), 1)
        self.assertTrue(controller.settings_panel.applied[0])


if __name__ == "__main__":
    unittest.main()

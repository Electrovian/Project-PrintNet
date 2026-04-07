import os
import sys
import tempfile
import unittest
from pathlib import Path

from qt_harness import QtTestCase, QtWidgets

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


class _Plate:
    def __init__(self, name):
        self.name = name


class _SceneState:
    def __init__(self):
        self.plates = {1: _Plate("Plate A"), 2: _Plate("Plate B")}


class _ViewerStub:
    def __init__(self, models):
        self.models = models
        self.scene_state = _SceneState()

    def get_plate_ids(self):
        return [1, 2]

    def get_plate_model_ids(self, plate_id):
        return [mid for mid, payload in self.models.items() if int(payload.get("plate_id", 0)) == int(plate_id)]


class FilesViewGuiTests(QtTestCase):
    def test_files_view_populates_filters_and_shows_empty_state(self):
        from gui.Windows.files import FilesView

        with tempfile.TemporaryDirectory() as tmp:
            alpha = Path(tmp).joinpath("alpha.stl")
            alpha.write_text("solid alpha", encoding="utf-8")
            beta = Path(tmp).joinpath("beta.3mf")
            beta.write_text("model beta", encoding="utf-8")

            view = FilesView()
            view.set_models(
                [
                    {"id": 1, "name": "Alpha", "path": str(alpha), "plate": "01"},
                    {"id": 2, "name": "Beta", "path": str(beta), "plate": "02"},
                ]
            )

            self.assertIs(view._stack.currentWidget(), view._table)
            self.assertEqual(view._table.rowCount(), 2)
            self.assertEqual(view._table.item(0, 1).text(), "01")
            self.assertEqual(view._table.item(0, 2).text(), "stl")

            view._search_input.setText("beta")
            QtWidgets.QApplication.processEvents()
            self.assertEqual(view._table.rowCount(), 1)
            self.assertEqual(view._table.item(0, 0).text(), "Beta")

            view._search_input.setText("missing")
            QtWidgets.QApplication.processEvents()
            self.assertIs(view._stack.currentWidget(), view._empty_label)

    def test_files_view_refresh_from_viewer_preserves_plate_labels(self):
        from gui.Windows.files import FilesView

        view = FilesView()
        viewer = _ViewerStub(
            {
                7: {"name": "gearbox.stl", "path": "C:/tmp/gearbox.stl", "plate_id": 1},
                8: {"name": "fan_duct.stl", "path": "C:/tmp/fan_duct.stl", "plate_id": 2},
            }
        )

        view.refresh_from_viewer(viewer)

        snapshot = view.models_snapshot()
        self.assertEqual(snapshot[0]["plate"], "Plate A")
        self.assertEqual(snapshot[1]["plate"], "Plate B")
        self.assertEqual(view._table.rowCount(), 2)


if __name__ == "__main__":
    unittest.main()

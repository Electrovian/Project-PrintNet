import os
import sys
import unittest

from qt_harness import QtCore, QtTestCase, QtWidgets

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


class ViewCubeOverlayTests(QtTestCase):
    def test_default_visible_faces_match_front_right_top_iso(self):
        from gui.widgets.view_cube_overlay import ViewCubeOverlay

        widget = ViewCubeOverlay()
        faces, corners, edges = widget._project_faces()
        visible_faces = {face["name"] for face in faces}

        self.assertEqual(visible_faces, {"front", "right", "top"})
        self.assertGreaterEqual(len(corners), 4)
        self.assertGreaterEqual(len(edges), 3)

    def test_cube_size_clamps_to_presentation_bounds(self):
        from gui.widgets.view_cube_overlay import ViewCubeOverlay

        widget = ViewCubeOverlay()
        widget.set_cube_size(10)
        self.assertEqual(widget.sizeHint(), QtCore.QSize(96, 96))

        widget.set_cube_size(400)
        self.assertEqual(widget.sizeHint(), QtCore.QSize(260, 260))


if __name__ == "__main__":
    unittest.main()

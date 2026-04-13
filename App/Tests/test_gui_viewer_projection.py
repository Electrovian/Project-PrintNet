import os
import sys
import unittest

import numpy as np

from qt_harness import QtTestCase, QtWidgets

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_OPENGL", "software")

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPO_ROOT = os.path.abspath(os.path.join(ROOT, ".."))
for candidate in (ROOT, REPO_ROOT):
    if candidate not in sys.path:
        sys.path.insert(0, candidate)


class ViewerProjectionTests(QtTestCase):
    def _build_viewer(self):
        from gui.viewer.core import Viewer3D

        viewer = Viewer3D()
        viewer.resize(800, 600)
        viewer.show()
        QtWidgets.QApplication.processEvents()
        self.addCleanup(viewer.close)
        return viewer

    def test_orthographic_projection_matrix_is_not_degenerate(self):
        viewer = self._build_viewer()

        viewer.set_projection_mode("ortho")
        matrix = viewer.projectionMatrix((0.0, 0.0, 800.0, 600.0), (0, 0, 800, 600))
        data = list(matrix.data())

        self.assertEqual(viewer.projection_mode(), "ortho")
        self.assertAlmostEqual(data[11], 0.0, places=6)
        self.assertAlmostEqual(data[15], 1.0, places=6)
        self.assertLess(data[10], 0.0)
        self.assertLess(data[14], 0.0)

    def test_orthographic_projection_keeps_origin_on_screen(self):
        viewer = self._build_viewer()

        viewer.set_projection_mode("ortho")
        projected = viewer._project_world_to_screen(np.array([0.0, 0.0, 0.0], dtype=float))

        self.assertIsNotNone(projected)
        assert projected is not None
        x, y, _z = projected
        self.assertGreaterEqual(x, 0.0)
        self.assertLessEqual(x, float(viewer.width()))
        self.assertGreaterEqual(y, 0.0)
        self.assertLessEqual(y, float(viewer.height()))

    def test_projection_mode_roundtrip_restores_perspective_fov(self):
        viewer = self._build_viewer()
        seen = []
        viewer.projectionModeChanged.connect(seen.append)

        viewer.set_projection_mode("ortho")
        self.assertEqual(viewer.projection_mode(), "ortho")
        self.assertAlmostEqual(float(viewer.opts["fov"]), 0.0, places=6)

        viewer.set_projection_mode("perspective")
        self.assertEqual(viewer.projection_mode(), "perspective")
        self.assertGreater(float(viewer.opts["fov"]), 1.0)
        self.assertEqual(seen, ["ortho", "perspective"])


if __name__ == "__main__":
    unittest.main()

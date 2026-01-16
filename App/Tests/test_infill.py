import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer import infill
from slicer.geometry import polygons_with_holes

class InfillTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        square = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 10.0), (0.0, 0.0)]
        cls._islands = polygons_with_holes([square])

    def test_rectilinear_infill(self):
        lines = infill.generate_infill(self._islands,
                                       density=0.25,
                                       angle_deg=45.0,
                                       layer_index=0,
                                       extrusion_width=0.4,
                                       pattern="rectilinear")
        self.assertGreater(len(lines), 0)

    def test_grid_infill(self):
        lines_rect = infill.generate_infill(self._islands,
                                            density=0.25,
                                            angle_deg=0.0,
                                            layer_index=0,
                                            extrusion_width=0.4,
                                            pattern="rectilinear")
        lines_grid = infill.generate_infill(self._islands,
                                            density=0.25,
                                            angle_deg=0.0,
                                            layer_index=0,
                                            extrusion_width=0.4,
                                            pattern="grid")
        self.assertGreaterEqual(len(lines_grid), len(lines_rect))

    def test_triangle_infill(self):
        lines = infill.generate_infill(self._islands,
                                       density=0.25,
                                       angle_deg=0.0,
                                       layer_index=0,
                                       extrusion_width=0.4,
                                       pattern="triangles")
        self.assertGreater(len(lines), 0)

if __name__ == "__main__":
    unittest.main()

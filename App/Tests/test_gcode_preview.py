import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer.gcode import parse_gcode_preview

class GCodePreviewTests(unittest.TestCase):
    def test_parse_gcode_preview_layers_and_features(self):
        lines = [
            ";TYPE:WALL-OUTER",
            "G1 X0 Y0 Z0.2 F1200",
            "G1 X10 Y0 E0.5",
            "G0 X10 Y10",
            ";TYPE:INFILL",
            "G1 X0 Y10 E1.0",
            "G0 Z0.4",
            ";TYPE:SUPPORT",
            "G1 X0 Y0 E1.5",
        ]
        preview = parse_gcode_preview(lines)
        self.assertEqual(len(preview.layers), 2)
        first_layer = preview.layers[0]
        self.assertIn("outer_wall", first_layer.features)
        self.assertIn("sparse_infill", first_layer.features)
        self.assertIn("travel", first_layer.features)
        second_layer = preview.layers[1]
        self.assertIn("support", second_layer.features)

if __name__ == "__main__":
    unittest.main()

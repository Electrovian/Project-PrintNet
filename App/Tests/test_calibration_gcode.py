import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer.gcode.writer import (
    SliceSettings,
    generate_flow_rate_test,
    generate_max_flowrate_test,
    generate_tolerance_test,
)


class CalibrationGcodeTests(unittest.TestCase):
    def test_flow_rate_gcode_contains_m221(self):
        settings = SliceSettings()
        gcode = generate_flow_rate_test(settings, 95, 105, 5)
        self.assertIn("M221", gcode)
        self.assertIn("; Flow rate test", gcode)

    def test_max_flowrate_gcode_contains_speed(self):
        settings = SliceSettings()
        gcode = generate_max_flowrate_test(settings, 60, 80, 10)
        self.assertIn("; Max flowrate test", gcode)
        self.assertIn("; SPEED:", gcode)

    def test_tolerance_gcode_contains_sizes(self):
        settings = SliceSettings()
        gcode = generate_tolerance_test(settings, [10.0, 12.0])
        self.assertIn("; Tolerance test", gcode)
        self.assertIn("; SIZE: 10.00mm", gcode)


if __name__ == "__main__":
    unittest.main()

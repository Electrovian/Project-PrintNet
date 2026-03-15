import math
import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer_v2.legacy_gcode_stats import estimate_gcode_stats
from slicer_v2.legacy_gcode_writer import GCodeWriter, SliceSettings

class GCodeExtrusionTests(unittest.TestCase):
    def test_extrusion_for_length(self):
        settings = SliceSettings(layer_height=0.2,
                                 extrusion_width=0.4,
                                 filament_diameter=1.75,
                                 extrusion_multiplier=1.0)
        writer = GCodeWriter(settings=settings)
        length = 10.0
        expected = (length * settings.layer_height * settings.extrusion_width) / (
            math.pi * (settings.filament_diameter / 2.0) ** 2
        )
        self.assertAlmostEqual(writer.extrusion_for_length(length), expected, places=6)

    def test_perimeter_loop_updates_e(self):
        settings = SliceSettings(layer_height=0.2,
                                 extrusion_width=0.4,
                                 filament_diameter=1.75,
                                 extrusion_multiplier=1.5)
        writer = GCodeWriter(settings=settings)
        writer.perimeter_loop([(0.0, 0.0), (10.0, 0.0)], z=0.2, speed=60.0)
        expected = writer.extrusion_for_length(10.0)
        self.assertAlmostEqual(writer.e_position, expected, places=6)

    def test_retract_and_unretract(self):
        settings = SliceSettings(retract_distance=1.0, retract_speed=20.0)
        writer = GCodeWriter(settings=settings)
        writer.move_extrude(1.0, 0.0, 0.2, speed=60.0, extrusion=0.5)
        self.assertFalse(writer.is_retracted)
        writer.move_travel(5.0, 0.0, 0.2, f=settings.travel_speed)
        self.assertTrue(writer.is_retracted)
        e_after_retract = writer.e_position
        writer.move_extrude(6.0, 0.0, 0.2, speed=60.0, extrusion=0.5)
        self.assertFalse(writer.is_retracted)
        self.assertGreater(writer.e_position, e_after_retract)

    def test_firmware_retract_emits_g10_g11(self):
        settings = SliceSettings(retract_style="firmware", retract_distance=1.0)
        writer = GCodeWriter(settings=settings)
        writer.retract()
        writer.unretract()
        gcode = writer.get_gcode()
        self.assertIn("G10", gcode)
        self.assertIn("G11", gcode)

    def test_estimate_gcode_stats(self):
        settings = SliceSettings(filament_diameter=1.75)
        lines = ["G1 X10 Y0 E1.0 F600"]
        stats = estimate_gcode_stats(lines, settings)
        self.assertIn("time", stats)
        length_mm_raw = stats.get("length_mm")
        if isinstance(length_mm_raw, (int, float)):
            length_mm = float(length_mm_raw)
        else:
            length_mm = 0.0
        self.assertGreater(length_mm, 0.0)

if __name__ == "__main__":
    unittest.main()


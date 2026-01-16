import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
TESTS = os.path.abspath(os.path.dirname(__file__))
if TESTS not in sys.path:
    sys.path.insert(0, TESTS)

from slicer.gcode.preview import parse_gcode_preview
from slicer.gcode.stats import estimate_gcode_stats
from harness import BaseTestCase


class GCodeExtraTests(BaseTestCase):
    def test_estimate_gcode_stats_relative(self):
        lines = [
            "G90",
            "G1 X10 Y0 F600",
            "G91",
            "G1 X10 Y0 F600",
        ]
        stats = estimate_gcode_stats(lines, settings=_dummy_settings())
        time_seconds_raw = stats.get("time_seconds")
        if isinstance(time_seconds_raw, (int, float)):
            time_seconds = float(time_seconds_raw)
        else:
            time_seconds = 0.0
        self.assertAlmostEqual(time_seconds, 2.0, places=2)

    def test_estimate_gcode_stats_extrusion_length(self):
        lines = [
            "G90",
            "M82",
            "G1 X10 Y0 E1.0 F600",
            "G1 X20 Y0 E2.0 F600",
        ]
        stats = estimate_gcode_stats(lines, settings=_dummy_settings())
        length_mm_raw = stats.get("length_mm")
        if isinstance(length_mm_raw, (int, float)):
            length_mm = float(length_mm_raw)
        else:
            length_mm = 0.0
        self.assertAlmostEqual(length_mm, 2.0, places=3)
        weight_str = str(stats.get("weight", "0"))
        weight_val = float(weight_str.split()[0]) if weight_str.split() else 0.0
        self.assertGreater(weight_val, 0.0)

    def test_parse_gcode_preview_arcs(self):
        lines = [
            "G90",
            "G1 X0 Y0 Z0.2 F600",
            "G2 X10 Y0 I5 J0 F600 E1.0",
        ]
        preview = parse_gcode_preview(lines)
        self.assertEqual(len(preview.layers), 1)
        self.assertGreater(len(preview.layers[0].segments), 1)


def _dummy_settings():
    from slicer.gcode.writer import SliceSettings

    return SliceSettings(
        layer_height=0.2,
        extrusion_width=0.4,
        filament_diameter=1.75,
        filament_density=1.24,
        print_speed=60.0,
        travel_speed=120.0,
    )


if __name__ == "__main__":
    unittest.main()

import os
import sys
import unittest

import trimesh

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer_v2.legacy_ai_checks import run_ai_checks
from slicer_v2.legacy_gcode_writer import SliceSettings


class AiChecksTests(unittest.TestCase):
    def test_ai_checks_emit_warnings_and_suggestions(self):
        mesh = trimesh.creation.box(extents=(10.0, 10.0, 2.0))
        settings = SliceSettings(
            support_enabled=False,
            nozzle_diameter=0.4,
            layer_height=0.35,
        )
        report = run_ai_checks([mesh], settings)
        self.assertIsInstance(report.warnings, list)
        self.assertIsInstance(report.suggestions, list)
        self.assertTrue(any("Overhangs detected" in msg for msg in report.warnings))
        self.assertTrue(any("Layer height is high" in msg for msg in report.suggestions))


if __name__ == "__main__":
    unittest.main()


import os
import sys
import unittest
from types import SimpleNamespace

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer_v2.gcode import run as run_gcode_stage  # noqa: E402
from slicer_v2.settings import normalize_settings  # noqa: E402
from slicer_v2.types import SlicerContext  # noqa: E402


class TestSlicerV2GCodeParity(unittest.TestCase):
    def test_gcode_stage_populates_parity_artifact_without_hard_errors(self) -> None:
        context = SlicerContext(
            job_id="gcode-parity-stage",
            mesh_path="gcode-parity.stl",
            resolved_settings=normalize_settings(
                {
                    "print_speed": 60.0,
                    "travel_speed": 150.0,
                    "gcode_validation_enabled": True,
                    "gcode_validation_strict": False,
                    "gcode_validation_bed_x_mm": 400.0,
                    "gcode_validation_bed_y_mm": 400.0,
                    "gcode_validation_bed_z_mm": 400.0,
                }
            ),
        )
        context.stage_artifacts["slice_grid"] = {"layer_heights_mm": [0.2, 0.2], "layer_z_values_mm": [0.1, 0.3]}
        context.stage_artifacts["perimeters"] = {
            "layer_plans": [SimpleNamespace(path_length_mm=110.0), SimpleNamespace(path_length_mm=105.0)]
        }
        context.stage_artifacts["infill"] = {
            "layer_plans": [SimpleNamespace(path_length_mm=45.0), SimpleNamespace(path_length_mm=48.0)]
        }
        context.stage_artifacts["supports"] = {
            "layer_plans": [SimpleNamespace(support_path_length_mm=8.0), SimpleNamespace(support_path_length_mm=10.0)]
        }
        context.stage_artifacts["bridges"] = {
            "layer_plans": [
                SimpleNamespace(solid_path_length_mm=12.0, bridge_path_length_mm=2.0),
                SimpleNamespace(solid_path_length_mm=13.0, bridge_path_length_mm=2.5),
            ]
        }
        context.stage_artifacts["travel"] = {
            "layer_travel_move_counts": [3, 3],
            "layer_travel_lengths_mm": [15.0, 16.0],
            "layer_travel_retract_counts": [1, 1],
            "layer_travel_z_hop_counts": [0, 0],
        }

        artifact = run_gcode_stage(context)
        self.assertTrue(artifact["gcode_validation_ok"])
        self.assertEqual(artifact["gcode_validation_error_count"], 0)
        self.assertIn("parity", context.stage_artifacts)
        parity = context.stage_artifacts["parity"]
        self.assertIn("gcode", parity)
        self.assertEqual(parity["gcode"]["gcode_validation_error_count"], 0)
        self.assertTrue(parity["gcode"]["gcode_validation_ok"])


if __name__ == "__main__":
    unittest.main()

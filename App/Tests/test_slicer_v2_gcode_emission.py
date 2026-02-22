import os
import re
import sys
import unittest
from types import SimpleNamespace

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer_v2.errors import SlicerV2GCodeEmissionError  # noqa: E402
from slicer_v2.gcode import run as run_gcode_stage  # noqa: E402
from slicer_v2.gcode_emission import emit_gcode_semantics  # noqa: E402
from slicer_v2.geometry import polygon_from_tuples  # noqa: E402
from slicer_v2.settings import normalize_settings  # noqa: E402
from slicer_v2.types import SlicerContext  # noqa: E402


def _extract_e_value(command: str) -> float:
    match = re.search(r"\bE(-?[0-9]+(?:\.[0-9]+)?)\b", command)
    if not match:
        raise AssertionError(f"E value not found in command: {command}")
    return float(match.group(1))


class TestSlicerV2GCodeEmission(unittest.TestCase):
    def test_absolute_extrusion_is_cumulative(self) -> None:
        layer_plans, _lines, _report = emit_gcode_semantics(
            layer_heights_mm=[0.2, 0.2],
            layer_z_values_mm=[0.1, 0.3],
            layer_path_lengths_mm=[50.0, 60.0],
            layer_filament_lengths_mm=[4.0, 5.0],
            layer_travel_move_counts=[1, 1],
            layer_travel_lengths_mm=[10.0, 12.0],
            print_speed_mm_s=60.0,
            travel_speed_mm_s=150.0,
            absolute_extrusion=True,
        )
        extrusion_values: list[float] = []
        for layer in layer_plans:
            for command in layer.commands:
                if command.semantic_tag != "extrusion_move":
                    continue
                extrusion_values.append(_extract_e_value(command.command))
        self.assertEqual(len(extrusion_values), 2)
        self.assertGreater(extrusion_values[1], extrusion_values[0])

    def test_relative_extrusion_is_per_move(self) -> None:
        layer_plans, _lines, _report = emit_gcode_semantics(
            layer_heights_mm=[0.2, 0.2],
            layer_z_values_mm=[0.1, 0.3],
            layer_path_lengths_mm=[50.0, 60.0],
            layer_filament_lengths_mm=[4.0, 5.0],
            layer_travel_move_counts=[1, 1],
            layer_travel_lengths_mm=[10.0, 12.0],
            print_speed_mm_s=60.0,
            travel_speed_mm_s=150.0,
            absolute_extrusion=False,
        )
        extrusion_values: list[float] = []
        for layer in layer_plans:
            for command in layer.commands:
                if command.semantic_tag != "extrusion_move":
                    continue
                extrusion_values.append(_extract_e_value(command.command))
        self.assertEqual(extrusion_values, [4.0, 5.0])

    def test_macro_injection(self) -> None:
        _layer_plans, lines, report = emit_gcode_semantics(
            layer_heights_mm=[0.2],
            layer_z_values_mm=[0.1],
            layer_path_lengths_mm=[20.0],
            layer_filament_lengths_mm=[2.0],
            layer_travel_move_counts=[1],
            layer_travel_lengths_mm=[5.0],
            print_speed_mm_s=60.0,
            travel_speed_mm_s=150.0,
            startup_macro=["M117 START"],
            end_macro=["M117 DONE"],
        )
        self.assertIn("M117 START", lines)
        self.assertIn("M117 DONE", lines)
        self.assertEqual(report.startup_macro_line_count, 1)
        self.assertEqual(report.end_macro_line_count, 1)

    def test_invalid_firmware_rejected(self) -> None:
        with self.assertRaises(SlicerV2GCodeEmissionError):
            emit_gcode_semantics(
                layer_heights_mm=[0.2],
                layer_z_values_mm=[0.1],
                layer_path_lengths_mm=[20.0],
                layer_filament_lengths_mm=[2.0],
                layer_travel_move_counts=[1],
                layer_travel_lengths_mm=[5.0],
                print_speed_mm_s=60.0,
                travel_speed_mm_s=150.0,
                firmware_flavor="unknown-fw",
            )

    def test_gcode_stage_integration_emits_semantics(self) -> None:
        context = SlicerContext(
            job_id="gcode-semantic-stage",
            mesh_path="fake.stl",
            resolved_settings=normalize_settings(
                {
                    "print_speed": 60.0,
                    "travel_speed": 150.0,
                    "gcode_absolute_extrusion": True,
                    "gcode_firmware_flavor": "marlin",
                    "gcode_startup_macro": ["M117 START"],
                    "gcode_end_macro": ["M117 END"],
                }
            ),
        )
        context.stage_artifacts["slice_grid"] = {"layer_heights_mm": [0.2, 0.2], "layer_z_values_mm": [0.1, 0.3]}
        context.stage_artifacts["perimeters"] = {
            "layer_plans": [SimpleNamespace(path_length_mm=100.0), SimpleNamespace(path_length_mm=95.0)]
        }
        context.stage_artifacts["infill"] = {
            "layer_plans": [SimpleNamespace(path_length_mm=40.0), SimpleNamespace(path_length_mm=44.0)]
        }
        context.stage_artifacts["supports"] = {
            "layer_plans": [SimpleNamespace(support_path_length_mm=10.0), SimpleNamespace(support_path_length_mm=12.0)]
        }
        context.stage_artifacts["bridges"] = {
            "layer_plans": [
                SimpleNamespace(solid_path_length_mm=15.0, bridge_path_length_mm=3.0),
                SimpleNamespace(solid_path_length_mm=16.0, bridge_path_length_mm=2.0),
            ]
        }
        context.stage_artifacts["travel"] = {
            "layer_travel_move_counts": [3, 3],
            "layer_travel_lengths_mm": [15.0, 16.0],
            "layer_travel_retract_counts": [1, 1],
            "layer_travel_z_hop_counts": [1, 0],
        }

        artifact = run_gcode_stage(context)
        self.assertIn("gcode_emission", artifact)
        self.assertIn("extrusion_flow", artifact)
        self.assertGreater(artifact["line_count"], 0)
        self.assertGreaterEqual(artifact["gcode_extrusion_command_count_total"], 1)
        self.assertIn("M117 START", artifact["lines"])
        self.assertIn("M117 END", artifact["lines"])
        self.assertEqual(artifact["seam_position"], "aligned")
        self.assertEqual(len(artifact["layer_xy_targets"]), 2)

    def test_seam_position_modes_affect_layer_targets(self) -> None:
        square = polygon_from_tuples([(0.0, 0.0), (20.0, 0.0), (20.0, 20.0), (0.0, 20.0)])
        layer_contours = [[square], [square], [square]]

        context_aligned = SlicerContext(
            job_id="gcode-seam-aligned",
            mesh_path="fake.stl",
            resolved_settings=normalize_settings(
                {
                    "print_speed": 60.0,
                    "travel_speed": 150.0,
                    "seam_position": "aligned",
                }
            ),
        )
        context_aligned.stage_artifacts["slice_grid"] = {
            "layer_heights_mm": [0.2, 0.2, 0.2],
            "layer_z_values_mm": [0.1, 0.3, 0.5],
        }
        context_aligned.stage_artifacts["regions"] = {"layer_contours": layer_contours}
        context_aligned.stage_artifacts["perimeters"] = {
            "layer_plans": [
                SimpleNamespace(path_length_mm=100.0),
                SimpleNamespace(path_length_mm=95.0),
                SimpleNamespace(path_length_mm=90.0),
            ]
        }
        context_aligned.stage_artifacts["infill"] = {
            "layer_plans": [
                SimpleNamespace(path_length_mm=40.0),
                SimpleNamespace(path_length_mm=44.0),
                SimpleNamespace(path_length_mm=42.0),
            ]
        }
        context_aligned.stage_artifacts["supports"] = {"layer_plans": []}
        context_aligned.stage_artifacts["bridges"] = {"layer_plans": []}
        context_aligned.stage_artifacts["travel"] = {
            "layer_travel_move_counts": [1, 1, 1],
            "layer_travel_lengths_mm": [10.0, 10.0, 10.0],
        }
        aligned_artifact = run_gcode_stage(context_aligned)
        aligned_targets = aligned_artifact["layer_xy_targets"]
        self.assertEqual(aligned_targets[0][2], aligned_targets[1][2])
        self.assertEqual(aligned_targets[0][3], aligned_targets[1][3])

        context_random = SlicerContext(
            job_id="gcode-seam-random",
            mesh_path="fake.stl",
            resolved_settings=normalize_settings(
                {
                    "print_speed": 60.0,
                    "travel_speed": 150.0,
                    "seam_position": "random",
                    "seam_random_seed": 123,
                }
            ),
        )
        context_random.stage_artifacts = dict(context_aligned.stage_artifacts)
        random_artifact = run_gcode_stage(context_random)
        random_targets = random_artifact["layer_xy_targets"]
        self.assertNotEqual(
            (random_targets[0][2], random_targets[0][3]),
            (random_targets[1][2], random_targets[1][3]),
        )


if __name__ == "__main__":
    unittest.main()

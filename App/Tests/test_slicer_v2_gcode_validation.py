import os
import sys
import unittest
from types import SimpleNamespace

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer_v2.errors import SlicerV2GCodeValidationError  # noqa: E402
from slicer_v2.gcode import run as run_gcode_stage  # noqa: E402
from slicer_v2.gcode_emission import emit_gcode_semantics  # noqa: E402
from slicer_v2.gcode_validation import validate_gcode_semantics  # noqa: E402
from slicer_v2.settings import normalize_settings  # noqa: E402
from slicer_v2.types import SlicerContext  # noqa: E402


def _build_stage_context(settings_override: dict[str, object] | None = None) -> SlicerContext:
    settings_payload: dict[str, object] = {
        "print_speed": 60.0,
        "travel_speed": 150.0,
        "gcode_absolute_extrusion": True,
        "gcode_firmware_flavor": "marlin",
        "gcode_validation_enabled": True,
        "gcode_validation_strict": False,
        "gcode_validation_bed_x_mm": 400.0,
        "gcode_validation_bed_y_mm": 400.0,
        "gcode_validation_bed_z_mm": 400.0,
    }
    if settings_override:
        settings_payload.update(settings_override)

    context = SlicerContext(
        job_id="gcode-validation-stage",
        mesh_path="fake.stl",
        resolved_settings=normalize_settings(settings_payload),
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
    return context


class TestSlicerV2GCodeValidation(unittest.TestCase):
    def test_validation_accepts_emitted_semantic_lines(self) -> None:
        _layer_plans, lines, _report = emit_gcode_semantics(
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
        validation = validate_gcode_semantics(
            lines,
            absolute_extrusion=True,
            bed_x_mm=400.0,
            bed_y_mm=400.0,
            bed_z_mm=400.0,
        )
        self.assertTrue(validation.ok)
        self.assertEqual(validation.error_count, 0)
        self.assertGreater(validation.movement_command_count, 0)

    def test_validation_detects_out_of_bounds_move(self) -> None:
        lines = ["G21", "G90", "M82", "G0 X500.0 Y10.0 Z0.2 F9000"]
        validation = validate_gcode_semantics(
            lines,
            absolute_extrusion=True,
            bed_x_mm=220.0,
            bed_y_mm=220.0,
            bed_z_mm=250.0,
        )
        self.assertFalse(validation.ok)
        self.assertGreaterEqual(validation.bounds_violation_count, 1)

    def test_validation_detects_non_monotonic_z(self) -> None:
        lines = ["G21", "G90", "M82", "G0 Z0.3 F9000", "G0 Z0.2 F9000"]
        validation = validate_gcode_semantics(
            lines,
            absolute_extrusion=True,
            bed_x_mm=220.0,
            bed_y_mm=220.0,
            bed_z_mm=250.0,
            require_monotonic_z=True,
        )
        self.assertFalse(validation.ok)
        self.assertEqual(validation.z_monotonicity_violation_count, 1)

    def test_validation_rejects_unannotated_absolute_retract(self) -> None:
        lines = ["G21", "G90", "M82", "G1 E5.00000 F3600", "G1 E4.00000 F3600"]
        validation = validate_gcode_semantics(lines, absolute_extrusion=True)
        self.assertFalse(validation.ok)
        self.assertGreaterEqual(validation.extrusion_monotonicity_violation_count, 1)

    def test_validation_allows_annotated_absolute_retract(self) -> None:
        lines = ["G21", "G90", "M82", "G1 E5.00000 F3600", "G1 E4.00000 F3600 ; retract"]
        validation = validate_gcode_semantics(lines, absolute_extrusion=True)
        self.assertTrue(validation.ok)
        self.assertGreaterEqual(validation.warning_count, 1)

    def test_gcode_stage_includes_validation_payload(self) -> None:
        context = _build_stage_context()
        artifact = run_gcode_stage(context)
        self.assertIn("gcode_validation", artifact)
        self.assertTrue(artifact["gcode_validation_ok"])
        self.assertEqual(artifact["gcode_validation_error_count"], 0)
        validation = artifact["gcode_validation"]
        self.assertEqual(validation["error_count"], 0)

    def test_strict_validation_raises_stage_error(self) -> None:
        context = _build_stage_context(
            {
                "gcode_validation_strict": True,
                "gcode_validation_bed_x_mm": 1.0,
                "gcode_validation_bed_y_mm": 1.0,
                "gcode_validation_bed_z_mm": 1.0,
            }
        )
        with self.assertRaises(SlicerV2GCodeValidationError):
            run_gcode_stage(context)


if __name__ == "__main__":
    unittest.main()

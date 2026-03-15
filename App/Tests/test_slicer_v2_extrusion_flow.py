import os
import sys
import unittest
from types import SimpleNamespace

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer_v2.errors import SlicerV2ExtrusionFlowError  # noqa: E402
from slicer_v2.extrusion_flow import build_extrusion_flow_model  # noqa: E402
from slicer_v2.gcode import run as run_gcode_stage  # noqa: E402
from slicer_v2.settings import normalize_settings  # noqa: E402
from slicer_v2.types import SlicerContext  # noqa: E402


class TestSlicerV2ExtrusionFlow(unittest.TestCase):
    def test_extrusion_flow_totals_positive(self) -> None:
        layer_plans, report = build_extrusion_flow_model(
            layer_heights_mm=[0.2, 0.2],
            layer_z_values_mm=[0.1, 0.3],
            perimeter_lengths_mm=[120.0, 110.0],
            infill_lengths_mm=[50.0, 55.0],
            support_lengths_mm=[10.0, 12.0],
            solid_lengths_mm=[15.0, 14.0],
            bridge_lengths_mm=[5.0, 6.0],
            line_width_mm=0.42,
            nozzle_diameter_mm=0.4,
            filament_diameter_mm=1.75,
        )
        self.assertEqual(len(layer_plans), 2)
        self.assertGreater(report.path_length_mm_total, 0.0)
        self.assertGreater(report.volume_mm3_total, 0.0)
        self.assertGreater(report.filament_length_mm_total, 0.0)
        self.assertGreaterEqual(report.filament_mass_g_total, 0.0)

    def test_flow_multiplier_changes_volume(self) -> None:
        _plans_a, report_a = build_extrusion_flow_model(
            layer_heights_mm=[0.2],
            layer_z_values_mm=[0.1],
            perimeter_lengths_mm=[100.0],
            infill_lengths_mm=[40.0],
            support_lengths_mm=[0.0],
            solid_lengths_mm=[10.0],
            bridge_lengths_mm=[0.0],
            line_width_mm=0.4,
            nozzle_diameter_mm=0.4,
            filament_diameter_mm=1.75,
            flow_multiplier=1.0,
        )
        _plans_b, report_b = build_extrusion_flow_model(
            layer_heights_mm=[0.2],
            layer_z_values_mm=[0.1],
            perimeter_lengths_mm=[100.0],
            infill_lengths_mm=[40.0],
            support_lengths_mm=[0.0],
            solid_lengths_mm=[10.0],
            bridge_lengths_mm=[0.0],
            line_width_mm=0.4,
            nozzle_diameter_mm=0.4,
            filament_diameter_mm=1.75,
            flow_multiplier=1.2,
        )
        self.assertGreater(report_b.volume_mm3_total, report_a.volume_mm3_total)
        self.assertGreater(report_b.filament_length_mm_total, report_a.filament_length_mm_total)

    def test_invalid_filament_diameter_rejected(self) -> None:
        with self.assertRaises(SlicerV2ExtrusionFlowError):
            build_extrusion_flow_model(
                layer_heights_mm=[0.2],
                layer_z_values_mm=[0.1],
                perimeter_lengths_mm=[100.0],
                infill_lengths_mm=[40.0],
                support_lengths_mm=[0.0],
                solid_lengths_mm=[10.0],
                bridge_lengths_mm=[0.0],
                line_width_mm=0.4,
                nozzle_diameter_mm=0.4,
                filament_diameter_mm=0.0,
            )

    def test_settings_alias_normalization_for_flow(self) -> None:
        normalized = normalize_settings(
            {
                "flow": "1.15",
                "wall_flow": "1.02",
                "infill_flow": "0.97",
                "support_flow": "1.05",
                "solid_flow": "1.08",
                "filament_density": "1.24",
                "filament_cost_per_kg": "24.5",
                "small_feature_threshold": "3.0",
                "small_feature_flow_boost": "1.1",
            }
        )
        self.assertEqual(normalized["flow_multiplier"], 1.15)
        self.assertEqual(normalized["perimeter_flow_ratio"], 1.02)
        self.assertEqual(normalized["infill_flow_ratio"], 0.97)
        self.assertEqual(normalized["support_flow_ratio"], 1.05)
        self.assertEqual(normalized["solid_flow_ratio"], 1.08)
        self.assertEqual(normalized["filament_density_g_cm3"], 1.24)
        self.assertEqual(normalized["filament_cost_usd_per_kg"], 24.5)
        self.assertEqual(normalized["small_feature_threshold_mm"], 3.0)
        self.assertEqual(normalized["small_feature_flow_boost_ratio"], 1.1)

    def test_gcode_stage_integration_includes_extrusion_flow(self) -> None:
        context = SlicerContext(
            job_id="extrusion-flow-stage",
            mesh_path="fake.stl",
            resolved_settings=normalize_settings(
                {
                    "print_speed": 60.0,
                    "layer_height": 0.2,
                    "infill_percent": 20.0,
                    "flow_multiplier": 1.0,
                    "filament_diameter": 1.75,
                    "nozzle_diameter": 0.4,
                    "extrusion_width": 0.4,
                }
            ),
        )
        context.stage_artifacts["slice_grid"] = {"layer_heights_mm": [0.2, 0.2], "layer_z_values_mm": [0.1, 0.3]}
        context.stage_artifacts["perimeters"] = {
            "layer_plans": [SimpleNamespace(path_length_mm=120.0), SimpleNamespace(path_length_mm=115.0)]
        }
        context.stage_artifacts["infill"] = {
            "layer_plans": [SimpleNamespace(path_length_mm=60.0), SimpleNamespace(path_length_mm=62.0)]
        }
        context.stage_artifacts["supports"] = {
            "layer_plans": [SimpleNamespace(support_path_length_mm=10.0), SimpleNamespace(support_path_length_mm=12.0)]
        }
        context.stage_artifacts["bridges"] = {
            "layer_plans": [
                SimpleNamespace(solid_path_length_mm=20.0, bridge_path_length_mm=5.0),
                SimpleNamespace(solid_path_length_mm=22.0, bridge_path_length_mm=6.0),
            ]
        }

        artifact = run_gcode_stage(context)
        self.assertIn("extrusion_flow", artifact)
        self.assertGreater(artifact["extrusion_volume_mm3_total"], 0.0)
        self.assertGreater(artifact["estimated_filament_mm"], 0.0)
        self.assertEqual(len(artifact["layer_extrusion_volumes_mm3"]), 2)


if __name__ == "__main__":
    unittest.main()

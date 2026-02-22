import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer_v2 import slice_grid  # noqa: E402
from slicer_v2.adaptive_layers import build_layer_plan  # noqa: E402
from slicer_v2.errors import SlicerV2AdaptiveLayerError  # noqa: E402
from slicer_v2.settings import normalize_settings  # noqa: E402
from slicer_v2.types import SlicerContext  # noqa: E402


class TestSlicerV2AdaptiveLayers(unittest.TestCase):
    def test_fixed_plan_closes_exact_height(self) -> None:
        plan = build_layer_plan(
            {"layer_height": 0.2},
            z_min_mm=0.0,
            z_max_mm=1.0,
            model_height_mm=1.0,
        )
        self.assertEqual(plan.report.strategy, "fixed")
        self.assertEqual(plan.report.layer_count, 5)
        self.assertAlmostEqual(sum(plan.layer_heights_mm), 1.0, places=6)
        self.assertEqual(len(plan.layer_z_values_mm), plan.report.layer_count)

    def test_adaptive_plan_uses_manual_range_refinement(self) -> None:
        fixed_plan = build_layer_plan(
            {"layer_height": 0.25},
            z_min_mm=0.0,
            z_max_mm=1.2,
            model_height_mm=1.2,
        )
        adaptive_plan = build_layer_plan(
            {
                "layer_height": 0.25,
                "adaptive_layering_enabled": True,
                "adaptive_layer_min": 0.1,
                "adaptive_layer_max": 0.3,
                "adaptive_layer_ranges": (
                    {"z_min_mm": 0.4, "z_max_mm": 0.8, "layer_height_mm": 0.1},
                ),
            },
            z_min_mm=0.0,
            z_max_mm=1.2,
            model_height_mm=1.2,
        )
        self.assertEqual(adaptive_plan.report.strategy, "adaptive")
        self.assertGreater(adaptive_plan.report.manual_adjustment_count, 0)
        self.assertAlmostEqual(sum(adaptive_plan.layer_heights_mm), 1.2, places=6)
        self.assertGreaterEqual(adaptive_plan.report.layer_count, fixed_plan.report.layer_count)
        self.assertTrue(any(height <= 0.11 for height in adaptive_plan.layer_heights_mm))

    def test_top_bottom_refine_enables_adaptive_strategy(self) -> None:
        plan = build_layer_plan(
            {
                "layer_height": 0.24,
                "adaptive_top_bottom_refine_mm": 0.35,
                "adaptive_layer_min": 0.12,
                "adaptive_layer_max": 0.3,
            },
            z_min_mm=0.0,
            z_max_mm=1.0,
            model_height_mm=1.0,
        )
        self.assertEqual(plan.report.strategy, "adaptive")
        self.assertGreater(plan.report.boundary_adjustment_count, 0)

    def test_invalid_min_max_raises_error(self) -> None:
        with self.assertRaises(SlicerV2AdaptiveLayerError):
            build_layer_plan(
                {
                    "layer_height": 0.2,
                    "adaptive_layering_enabled": True,
                    "adaptive_layer_min": 0.25,
                    "adaptive_layer_max": 0.1,
                },
                z_min_mm=0.0,
                z_max_mm=1.0,
                model_height_mm=1.0,
            )

    def test_settings_normalization_for_adaptive_ranges(self) -> None:
        normalized = normalize_settings(
            {
                "adaptive_layering": "yes",
                "adaptive_layer_min_mm": "0.09",
                "adaptive_layer_max_mm": "0.28",
                "adaptive_layer_ranges": '[{"z_min_mm": 0.0, "z_max_mm": 0.5, "layer_height": 0.1}]',
            }
        )
        self.assertTrue(normalized["adaptive_layering_enabled"])
        self.assertEqual(normalized["adaptive_layer_min"], 0.09)
        self.assertEqual(normalized["adaptive_layer_max"], 0.28)
        self.assertEqual(len(normalized["adaptive_layer_ranges"]), 1)

    def test_slice_grid_stage_uses_adaptive_plan(self) -> None:
        context = SlicerContext(
            job_id="adaptive-stage",
            mesh_path="fake.stl",
            resolved_settings=normalize_settings(
                {
                    "layer_height": 0.2,
                    "adaptive_layering_enabled": True,
                    "adaptive_layer_min": 0.1,
                    "adaptive_layer_max": 0.3,
                    "adaptive_layer_ranges": (
                        {"z_min_mm": 0.2, "z_max_mm": 0.6, "layer_height_mm": 0.1},
                    ),
                }
            ),
        )
        context.stage_artifacts["mesh"] = {
            "z_min_mm": 0.0,
            "z_max_mm": 1.0,
        }
        artifact = slice_grid.run(context)
        self.assertEqual(artifact["adaptive_layering_strategy"], "adaptive")
        self.assertTrue(artifact["adaptive_layering_enabled"])
        self.assertEqual(len(artifact["layer_z_values_mm"]), artifact["layer_count"])
        self.assertAlmostEqual(sum(artifact["layer_heights_mm"]), 1.0, places=3)


if __name__ == "__main__":
    unittest.main()


import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer_v2.errors import SlicerV2SettingsNormalizationError  # noqa: E402
from slicer_v2.settings import (  # noqa: E402
    DEFAULT_SETTINGS,
    normalize_settings,
    normalize_settings_with_report,
)


class TestSlicerV2SettingsNormalization(unittest.TestCase):
    def test_defaults_when_no_input(self) -> None:
        normalized, report = normalize_settings_with_report(None)
        self.assertEqual(normalized["layer_height"], DEFAULT_SETTINGS["layer_height"])
        self.assertEqual(normalized["infill_percent"], DEFAULT_SETTINGS["infill_percent"])
        self.assertEqual(report.input_key_count, 0)
        self.assertEqual(report.warning_count, 0)

    def test_alias_coercion_and_clamp(self) -> None:
        normalized, report = normalize_settings_with_report(
            {
                "layer_height_mm": "0.35",
                "wall_loops": "99",
                "sparse_infill_density": "0.25",
                "default_speed": "-10",
            }
        )
        self.assertEqual(normalized["layer_height"], 0.35)
        self.assertEqual(normalized["perimeter_count"], 20)
        self.assertEqual(normalized["infill_percent"], 25.0)
        self.assertEqual(normalized["print_speed"], 1.0)
        self.assertGreaterEqual(report.alias_applied_count, 4)
        self.assertGreaterEqual(report.coerced_value_count, 4)
        self.assertGreaterEqual(report.clamped_value_count, 2)

    def test_choice_and_bool_normalization(self) -> None:
        normalized, report = normalize_settings_with_report(
            {
                "infill_pattern": "TRIANGLES",
                "support_enable": "yes",
                "support_style": "organic",
                "seam_position": "back",
                "bridge_enabled": "off",
                "sparse_infill_rotate_template": "0,90",
                "infill_anchor_length": "25%",
                "infill_combination": "true",
                "infill_combination_max_layer_height": "0.48",
                "internal_bridge_angle": "33",
                "internal_bridge_flow": "1.2",
                "bridge_over_infill": "off",
                "bridge_over_infill_min_ratio": "0.2",
                "bridge_over_infill_samples": "9",
                "infill_antivibration": "yes",
                "infill_antivibration_short_line": "5.5",
                "infill_antivibration_max_skips": "3",
                "infill_antivibration_min_depth": "7",
                "seam_seed": "42",
                "wall_transition_smoothing": "0.4",
                "junction_compensation": "on",
                "junction_sharp_angle": "125",
                "tree_branch_merge_distance": "1.6",
                "tree_branch_growth": "1.12",
                "tree_min_branch_radius": "0.28",
            }
        )
        self.assertEqual(normalized["infill_pattern"], "triangle")
        self.assertTrue(normalized["support_enabled"])
        self.assertEqual(normalized["support_type"], "tree")
        self.assertEqual(normalized["seam_position"], "rear")
        self.assertFalse(normalized["bridge_enabled"])
        self.assertEqual(normalized["infill_angle_template"], "0,90")
        self.assertEqual(normalized["infill_anchor"], "25%")
        self.assertTrue(normalized["infill_combination_enabled"])
        self.assertEqual(normalized["infill_combination_max_layer_height_mm"], 0.48)
        self.assertEqual(normalized["internal_bridge_angle_deg"], 33.0)
        self.assertEqual(normalized["internal_bridge_flow_ratio"], 1.2)
        self.assertFalse(normalized["bridge_over_infill_enabled"])
        self.assertEqual(normalized["bridge_over_infill_min_candidate_ratio"], 0.2)
        self.assertEqual(normalized["bridge_over_infill_sample_count"], 9)
        self.assertTrue(normalized["infill_antivibration_enabled"])
        self.assertEqual(normalized["infill_antivibration_short_line_threshold_mm"], 5.5)
        self.assertEqual(normalized["infill_antivibration_max_skips_allowed"], 3)
        self.assertEqual(normalized["infill_antivibration_min_depth_for_line_removing"], 7)
        self.assertEqual(normalized["seam_random_seed"], 42)
        self.assertEqual(normalized["arachne_transition_smoothing"], 0.4)
        self.assertTrue(normalized["arachne_junction_compensation_enabled"])
        self.assertEqual(normalized["arachne_junction_sharp_angle_deg"], 125.0)
        self.assertEqual(normalized["tree_support_branch_merge_distance_ratio"], 1.6)
        self.assertEqual(normalized["tree_support_branch_growth_ratio"], 1.12)
        self.assertEqual(normalized["tree_support_min_branch_radius_mm"], 0.28)
        self.assertEqual(report.warning_count, 0)

    def test_infill_pattern_extended_aliases(self) -> None:
        normalized = normalize_settings(
            {
                "infill_pattern": "3dhoneycomb",
            }
        )
        self.assertEqual(normalized["infill_pattern"], "3d_honeycomb")

    def test_unknown_key_reporting(self) -> None:
        normalized, report = normalize_settings_with_report({"custom_vendor_flag": "abc"})
        self.assertIn("custom_vendor_flag", normalized)
        self.assertIn("custom_vendor_flag", report.unknown_keys)
        self.assertEqual(report.unknown_key_count, 1)

    def test_strict_mode_fails_on_warning(self) -> None:
        with self.assertRaises(SlicerV2SettingsNormalizationError):
            normalize_settings_with_report({"support_enabled": "maybe"}, strict=True)

    def test_non_dict_payload_rejected(self) -> None:
        with self.assertRaises(SlicerV2SettingsNormalizationError):
            normalize_settings("bad-input")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()

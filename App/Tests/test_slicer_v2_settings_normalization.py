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
        self.assertEqual(normalized["support_style"], "organic")
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

    def test_overlap_and_support_aliases_with_percent_distance_conversion(self) -> None:
        normalized = normalize_settings(
            {
                "extrusion_width": 0.6,
                "infill_overlap": "22%",
                "top_bottom_infill_wall_overlap": "35%",
                "support_on_build_plate_only": "true",
                "support_object_xy_distance": "50%",
                "support_top_z_distance": "25%",
                "support_bottom_z_distance": "50%",
                "support_interface_top_layers": "3",
                "support_interface_bottom_layers": "1",
                "support_base_pattern_spacing": "200%",
                "support_interface_spacing": "150%",
                "support_bottom_interface_spacing": "120%",
                "support_threshold_overlap": "45%",
                "support_threshold_angle": "58",
                "support_critical_regions_only": "true",
                "support_remove_small_overhang": "1",
                "tree_support_branch_angle": "32",
                "tree_support_wall_count": "2",
                "support_tree_branch_distance": "250%",
                "support_tree_branch_distance_organic": "300%",
                "support_tree_top_rate": "65%",
                "support_tree_branch_diameter_angle": "12",
                "support_tree_angle_organic": "28",
                "tree_support_branch_diameter": "200%",
                "support_tree_branch_diameter_organic": "175%",
                "tree_support_tip_diameter": "100%",
                "tree_support_auto_brim": "yes",
                "tree_support_brim_width": "50%",
            }
        )
        self.assertEqual(normalized["infill_wall_overlap_percent"], 22.0)
        self.assertEqual(normalized["top_bottom_infill_wall_overlap_percent"], 35.0)
        self.assertTrue(normalized["support_build_plate_only"])
        self.assertAlmostEqual(float(normalized["support_xy_gap_mm"]), 0.30, places=3)
        self.assertAlmostEqual(float(normalized["support_z_gap_mm"]), 0.15, places=3)
        self.assertAlmostEqual(float(normalized["support_bottom_z_gap_mm"]), 0.30, places=3)
        self.assertEqual(normalized["support_interface_top_layers"], 3)
        self.assertEqual(normalized["support_interface_bottom_layers"], 1)
        self.assertAlmostEqual(float(normalized["support_base_spacing_mm"]), 1.2, places=3)
        self.assertAlmostEqual(float(normalized["support_interface_spacing_mm"]), 0.9, places=3)
        self.assertAlmostEqual(float(normalized["support_bottom_interface_spacing_mm"]), 0.72, places=3)
        self.assertEqual(normalized["support_threshold_angle_deg"], 58.0)
        self.assertEqual(normalized["support_threshold_overlap_percent"], 45.0)
        self.assertTrue(normalized["support_critical_regions_only"])
        self.assertTrue(normalized["support_remove_small_overhang"])
        self.assertEqual(normalized["tree_support_branch_angle_deg"], 32.0)
        self.assertEqual(normalized["tree_support_wall_count"], 2)
        self.assertAlmostEqual(float(normalized["tree_support_branch_distance_mm"]), 1.5, places=3)
        self.assertAlmostEqual(float(normalized["tree_support_branch_distance_organic_mm"]), 1.8, places=3)
        self.assertEqual(normalized["tree_support_top_rate_percent"], 65.0)
        self.assertEqual(normalized["tree_support_branch_diameter_angle_deg"], 12.0)
        self.assertEqual(normalized["tree_support_branch_angle_organic_deg"], 28.0)
        self.assertAlmostEqual(float(normalized["tree_support_branch_diameter_mm"]), 1.2, places=3)
        self.assertAlmostEqual(float(normalized["tree_support_branch_diameter_organic_mm"]), 1.05, places=3)
        self.assertAlmostEqual(float(normalized["tree_support_tip_diameter_mm"]), 0.6, places=3)
        self.assertTrue(normalized["tree_support_auto_brim"])
        self.assertAlmostEqual(float(normalized["tree_support_brim_width_mm"]), 0.3, places=3)

    def test_percent_distance_uses_final_extrusion_width_even_when_key_order_varies(self) -> None:
        normalized = normalize_settings(
            {
                "support_object_xy_distance": "100%",
                "support_top_z_distance": "50%",
                "extrusion_width": 0.8,
            }
        )
        self.assertAlmostEqual(float(normalized["support_xy_gap_mm"]), 0.8, places=3)
        self.assertAlmostEqual(float(normalized["support_z_gap_mm"]), 0.4, places=3)

    def test_legacy_interface_and_z_gap_aliases_sync_to_new_fields(self) -> None:
        normalized = normalize_settings(
            {
                "interface_layers": 4,
                "support_z_gap": 0.35,
            }
        )
        self.assertEqual(normalized["support_interface_layers"], 4)
        self.assertEqual(normalized["support_interface_top_layers"], 4)
        self.assertAlmostEqual(float(normalized["support_bottom_z_gap_mm"]), 0.35, places=3)

    def test_support_interface_bottom_layers_preserves_negative_one_sentinel(self) -> None:
        normalized = normalize_settings(
            {
                "support_interface_layers": 3,
                "support_interface_bottom_layers": -1,
            }
        )
        self.assertEqual(normalized["support_interface_layers"], 3)
        self.assertEqual(normalized["support_interface_top_layers"], 3)
        self.assertEqual(normalized["support_interface_bottom_layers"], -1)

    def test_support_style_derives_support_type_only_when_type_missing(self) -> None:
        style_only = normalize_settings({"support_style": "organic"})
        self.assertEqual(style_only["support_style"], "organic")
        self.assertEqual(style_only["support_type"], "tree")

        explicit_type = normalize_settings({"support_style": "organic", "support_type": "normal"})
        self.assertEqual(explicit_type["support_style"], "organic")
        self.assertEqual(explicit_type["support_type"], "normal")

    def test_strict_mode_fails_on_warning(self) -> None:
        with self.assertRaises(SlicerV2SettingsNormalizationError):
            normalize_settings_with_report({"support_enabled": "maybe"}, strict=True)

    def test_non_dict_payload_rejected(self) -> None:
        with self.assertRaises(SlicerV2SettingsNormalizationError):
            normalize_settings("bad-input")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()

import unittest

from qt_harness import QtTestCase
from slicer_v2.legacy_gcode_writer import SliceSettings


class SettingsPanelTests(QtTestCase):

    def test_apply_settings_roundtrip(self):
        from gui.settings_panel import SettingsPanel

        panel = SettingsPanel()
        tooltip_targets = panel._hover_tooltips
        self.assertIn(panel._filament_color_button, tooltip_targets)
        self.assertIn(panel._filament_button, tooltip_targets)
        self.assertIn(panel._label_layer_height, tooltip_targets)
        self.assertIn(panel._label_first_layer_height, tooltip_targets)
        self.assertIn(panel._label_seam_position, tooltip_targets)
        self.assertIn(panel._label_precise_wall, tooltip_targets)
        self.assertIn(panel._label_one_wall_top, tooltip_targets)
        self.assertIn(panel._label_one_wall_first, tooltip_targets)
        panel.set_printers([{"name": "Test Printer", "bed_x": 1, "bed_y": 2, "bed_z": 3}])
        self.assertEqual(panel._printer_combo.count(), 1)
        current_printer = panel.current_printer()
        self.assertIsNotNone(current_printer)
        assert current_printer is not None
        self.assertEqual(current_printer.get("name"), "Test Printer")
        settings = SliceSettings(
            layer_height=0.24,
            first_layer_height=0.28,
            seam_position="random",
            precise_wall=True,
            only_one_wall_top=True,
            only_one_wall_first_layer=True,
            perimeter_count=3,
            top_layers=4,
            bottom_layers=2,
            infill_percent=22.0,
            infill_pattern="grid",
            support_enabled=True,
            support_type="tree",
            support_style="tree",
            overhang_angle=50.0,
            support_build_plate_only=True,
            support_z_gap=0.35,
            support_xy_gap=0.45,
            interface_layers=3,
            interface_density=0.75,
            support_spacing=2.5,
            support_speed=70.0,
            support_interface_speed=55.0,
            support_pattern="grid",
            support_interface_pattern="triangle",
            support_filament_base="support",
            support_filament_interface="support",
            tree_branch_angle=35.0,
            tree_merge_distance=3.5,
            prime_tower_enabled=True,
            prime_tower_width=40.0,
            prime_tower_square=False,
            prime_tower_volume=60.0,
            flush_into_infill=True,
            flush_into_support=True,
            skirt_loops=2,
            skirt_height=3,
            brim_type="outer",
            brim_width=6.5,
            print_sequence="by_object",
            spiral_vase=True,
            ignore_inner_color=True,
            timelapse_mode="smooth",
            fuzzy_skin="light",
            filament_name="Test PLA",
            filament_color="#00ff00",
        )

        panel.apply_settings(settings)
        updated = panel.to_settings()

        self.assertAlmostEqual(updated.layer_height, 0.24, places=3)
        self.assertAlmostEqual(updated.first_layer_height, 0.28, places=3)
        self.assertEqual(updated.seam_position, "random")
        self.assertTrue(updated.precise_wall)
        self.assertTrue(updated.only_one_wall_top)
        self.assertTrue(updated.only_one_wall_first_layer)
        self.assertEqual(updated.perimeter_count, 3)
        self.assertEqual(updated.top_layers, 4)
        self.assertEqual(updated.bottom_layers, 2)
        self.assertEqual(updated.infill_percent, 22.0)
        self.assertEqual(updated.infill_pattern, "grid")
        self.assertTrue(updated.support_enabled)
        self.assertEqual(updated.support_type, "tree")
        self.assertEqual(updated.support_style, "tree")
        self.assertAlmostEqual(updated.overhang_angle, 50.0, places=1)
        self.assertTrue(updated.support_build_plate_only)
        self.assertAlmostEqual(updated.support_z_gap, 0.35, places=2)
        self.assertAlmostEqual(updated.support_xy_gap, 0.45, places=2)
        self.assertEqual(updated.interface_layers, 3)
        self.assertAlmostEqual(updated.interface_density, 0.75, places=2)
        self.assertAlmostEqual(updated.support_spacing, 2.5, places=2)
        self.assertAlmostEqual(updated.support_speed, 70.0, places=2)
        self.assertAlmostEqual(updated.support_interface_speed, 55.0, places=2)
        self.assertEqual(updated.support_pattern, "grid")
        self.assertEqual(updated.support_interface_pattern, "triangle")
        self.assertEqual(updated.support_filament_base, "support")
        self.assertEqual(updated.support_filament_interface, "support")
        self.assertAlmostEqual(updated.tree_branch_angle, 35.0, places=2)
        self.assertAlmostEqual(updated.tree_merge_distance, 3.5, places=2)
        self.assertTrue(updated.prime_tower_enabled)
        self.assertAlmostEqual(updated.prime_tower_width, 40.0, places=2)
        self.assertFalse(updated.prime_tower_square)
        self.assertAlmostEqual(updated.prime_tower_volume, 60.0, places=2)
        self.assertTrue(updated.flush_into_infill)
        self.assertTrue(updated.flush_into_support)
        self.assertEqual(updated.skirt_loops, 2)
        self.assertEqual(updated.skirt_height, 3)
        self.assertEqual(updated.brim_type, "outer")
        self.assertAlmostEqual(updated.brim_width, 6.5, places=2)
        self.assertEqual(updated.print_sequence, "by_object")
        self.assertTrue(updated.spiral_vase)
        self.assertTrue(updated.ignore_inner_color)
        self.assertEqual(updated.timelapse_mode, "smooth")
        self.assertEqual(updated.fuzzy_skin, "light")
        self.assertEqual(updated.filament_name, "Test PLA")
        self.assertEqual(updated.filament_color.lower(), "#00ff00")


if __name__ == "__main__":
    unittest.main()


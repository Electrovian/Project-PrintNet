import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from profiles_import.mapping import ProfileMappingError, discover_resolve_and_map_profiles


class TestProfileSettingsMapping(unittest.TestCase):
    def _make_vendor_root(self, root: Path, vendor: str = "VendorA") -> Path:
        vendor_dir = root / vendor
        (vendor_dir / "machine").mkdir(parents=True, exist_ok=True)
        (vendor_dir / "process").mkdir(parents=True, exist_ok=True)
        (vendor_dir / "filament").mkdir(parents=True, exist_ok=True)
        return vendor_dir

    def _write_vendor_index(self, root: Path, vendor: str = "VendorA") -> None:
        (root / f"{vendor}.json").write_text(
            """
{
  "name": "VendorA",
  "machine_model_list": [{"name":"MachineA","sub_path":"machine/MachineA.json"}],
  "process_list": [{"name":"ProcessA","sub_path":"process/ProcessA.json"}],
  "filament_list": [{"name":"FilamentA","sub_path":"filament/FilamentA.json"}]
}
""".strip(),
            encoding="utf-8",
        )

    def test_process_and_filament_mapping_core_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            vendor_dir = self._make_vendor_root(root)
            self._write_vendor_index(root)
            (vendor_dir / "machine" / "MachineA.json").write_text(
                '{"type":"machine_model","name":"MachineA","nozzle_diameter":"0.4"}',
                encoding="utf-8",
            )
            (vendor_dir / "process" / "ProcessA.json").write_text(
                '{"type":"process","name":"ProcessA","layer_height":"0.2","sparse_infill_density":"25%","support_enable":"1","line_width":"0.45","wall_loops":"2"}',
                encoding="utf-8",
            )
            (vendor_dir / "filament" / "FilamentA.json").write_text(
                '{"type":"filament","name":"FilamentA","filament_type":"PLA","filament_colour":"#101010","filament_density":"1.24"}',
                encoding="utf-8",
            )

            report = discover_resolve_and_map_profiles(str(root))

            process = next(p for p in report.profiles if p.category == "process" and p.name == "ProcessA")
            filament = next(p for p in report.profiles if p.category == "filament" and p.name == "FilamentA")
            self.assertEqual(process.mapped_settings["layer_height"], 0.2)
            self.assertEqual(process.mapped_settings["infill_percent"], 25.0)
            self.assertTrue(process.mapped_settings["support_enabled"])
            self.assertEqual(process.mapped_settings["extrusion_width"], 0.45)
            self.assertEqual(process.mapped_settings["perimeter_count"], 2)
            self.assertEqual(filament.mapped_settings["filament_name"], "PLA")
            self.assertEqual(filament.mapped_settings["filament_color"], "#101010")
            self.assertEqual(filament.mapped_settings["filament_density"], 1.24)

    def test_inheritance_override_is_reflected_in_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            vendor_dir = self._make_vendor_root(root)
            self._write_vendor_index(root)
            (vendor_dir / "machine" / "MachineA.json").write_text(
                '{"type":"machine_model","name":"MachineA"}',
                encoding="utf-8",
            )
            (vendor_dir / "filament" / "FilamentA.json").write_text(
                '{"type":"filament","name":"FilamentA"}',
                encoding="utf-8",
            )
            (vendor_dir / "process" / "ProcessA.json").write_text(
                '{"type":"process","name":"ProcessA","line_width":"0.42"}',
                encoding="utf-8",
            )
            (vendor_dir / "process" / "ProcessChild.json").write_text(
                '{"type":"process","name":"ProcessChild","inherits":"ProcessA","line_width":"0.48"}',
                encoding="utf-8",
            )

            report = discover_resolve_and_map_profiles(str(root))
            child = next(
                p for p in report.profiles if p.category == "process" and p.name == "ProcessChild"
            )
            self.assertEqual(child.mapped_settings["extrusion_width"], 0.48)

    def test_machine_bed_shape_and_firmware_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            vendor_dir = self._make_vendor_root(root)
            self._write_vendor_index(root)
            (vendor_dir / "machine" / "MachineA.json").write_text(
                '{"type":"machine_model","name":"MachineA","bed_shape":"0x0,220x0,220x220,0x220","gcode_flavor":"klipper"}',
                encoding="utf-8",
            )
            (vendor_dir / "process" / "ProcessA.json").write_text(
                '{"type":"process","name":"ProcessA"}',
                encoding="utf-8",
            )
            (vendor_dir / "filament" / "FilamentA.json").write_text(
                '{"type":"filament","name":"FilamentA"}',
                encoding="utf-8",
            )

            report = discover_resolve_and_map_profiles(str(root))
            machine = next(p for p in report.profiles if p.category == "machine" and p.name == "MachineA")
            self.assertEqual(machine.mapped_settings["bed_x"], 220.0)
            self.assertEqual(machine.mapped_settings["bed_y"], 220.0)
            self.assertEqual(machine.mapped_settings["firmware_flavor"], "klipper")

    def test_unknown_keys_are_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            vendor_dir = self._make_vendor_root(root)
            self._write_vendor_index(root)
            (vendor_dir / "machine" / "MachineA.json").write_text(
                '{"type":"machine_model","name":"MachineA"}',
                encoding="utf-8",
            )
            (vendor_dir / "process" / "ProcessA.json").write_text(
                '{"type":"process","name":"ProcessA","mystery_key":"abc"}',
                encoding="utf-8",
            )
            (vendor_dir / "filament" / "FilamentA.json").write_text(
                '{"type":"filament","name":"FilamentA"}',
                encoding="utf-8",
            )

            report = discover_resolve_and_map_profiles(str(root))
            process = next(p for p in report.profiles if p.category == "process" and p.name == "ProcessA")
            self.assertIn("mystery_key", process.unknown_keys)
            self.assertGreaterEqual(report.unknown_key_count, 1)

    def test_high_impact_support_and_overlap_keys_are_mapped(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            vendor_dir = self._make_vendor_root(root)
            self._write_vendor_index(root)
            (vendor_dir / "machine" / "MachineA.json").write_text(
                '{"type":"machine_model","name":"MachineA"}',
                encoding="utf-8",
            )
            (vendor_dir / "process" / "ProcessA.json").write_text(
                (
                    '{"type":"process","name":"ProcessA","line_width":"0.6",'
                    '"infill_wall_overlap":"18%","top_bottom_infill_wall_overlap":"25%",'
                    '"support_style":"organic",'
                    '"support_on_build_plate_only":"1","support_object_xy_distance":"50%",'
                    '"support_top_z_distance":"25%","support_material_bottom_contact_distance":"50%",'
                    '"support_threshold_angle":"57","support_critical_regions_only":"true",'
                    '"support_remove_small_overhang":"1",'
                    '"support_material_interface_layers":"3","support_material_bottom_interface_layers":"-1",'
                    '"support_base_pattern_spacing":"200%","support_interface_spacing":"150%",'
                    '"support_bottom_interface_spacing":"120%",'
                    '"support_threshold_overlap":"40%",'
                    '"tree_support_branch_angle":"30","support_tree_angle_organic":"24","tree_support_wall_count":"2",'
                    '"support_tree_branch_distance":"250%","support_tree_branch_distance_organic":"300%",'
                    '"support_tree_top_rate":"60%","support_tree_branch_diameter_angle":"12",'
                    '"tree_support_branch_diameter":"200%","support_tree_branch_diameter_organic":"170%",'
                    '"tree_support_tip_diameter":"100%",'
                    '"tree_support_auto_brim":"true","tree_support_brim_width":"50%"}'
                ),
                encoding="utf-8",
            )
            (vendor_dir / "filament" / "FilamentA.json").write_text(
                '{"type":"filament","name":"FilamentA"}',
                encoding="utf-8",
            )

            report = discover_resolve_and_map_profiles(str(root))
            process = next(p for p in report.profiles if p.category == "process" and p.name == "ProcessA")
            self.assertEqual(process.mapped_settings["infill_wall_overlap_percent"], 18.0)
            self.assertEqual(process.mapped_settings["top_bottom_infill_wall_overlap_percent"], 25.0)
            self.assertTrue(process.mapped_settings["support_build_plate_only"])
            self.assertEqual(process.mapped_settings["support_style"], "organic")
            self.assertEqual(process.mapped_settings["support_type"], "tree")
            self.assertAlmostEqual(process.mapped_settings["support_xy_gap_mm"], 0.3, places=3)
            self.assertAlmostEqual(process.mapped_settings["support_z_gap_mm"], 0.15, places=3)
            self.assertAlmostEqual(process.mapped_settings["support_bottom_z_gap_mm"], 0.3, places=3)
            self.assertEqual(process.mapped_settings["support_threshold_angle_deg"], 57.0)
            self.assertTrue(process.mapped_settings["support_critical_regions_only"])
            self.assertTrue(process.mapped_settings["support_remove_small_overhang"])
            self.assertEqual(process.mapped_settings["support_interface_top_layers"], 3)
            self.assertEqual(process.mapped_settings["support_interface_bottom_layers"], -1)
            self.assertAlmostEqual(process.mapped_settings["support_base_spacing_mm"], 1.2, places=3)
            self.assertAlmostEqual(process.mapped_settings["support_interface_spacing_mm"], 0.9, places=3)
            self.assertAlmostEqual(process.mapped_settings["support_bottom_interface_spacing_mm"], 0.72, places=3)
            self.assertEqual(process.mapped_settings["support_threshold_overlap_percent"], 40.0)
            self.assertEqual(process.mapped_settings["tree_support_branch_angle_deg"], 30.0)
            self.assertEqual(process.mapped_settings["tree_support_branch_angle_organic_deg"], 24.0)
            self.assertEqual(process.mapped_settings["tree_support_wall_count"], 2)
            self.assertAlmostEqual(process.mapped_settings["tree_support_branch_distance_mm"], 1.5, places=3)
            self.assertAlmostEqual(process.mapped_settings["tree_support_branch_distance_organic_mm"], 1.8, places=3)
            self.assertEqual(process.mapped_settings["tree_support_top_rate_percent"], 60.0)
            self.assertEqual(process.mapped_settings["tree_support_branch_diameter_angle_deg"], 12.0)
            self.assertAlmostEqual(process.mapped_settings["tree_support_branch_diameter_mm"], 1.2, places=3)
            self.assertAlmostEqual(process.mapped_settings["tree_support_branch_diameter_organic_mm"], 1.02, places=3)
            self.assertAlmostEqual(process.mapped_settings["tree_support_tip_diameter_mm"], 0.6, places=3)
            self.assertTrue(process.mapped_settings["tree_support_auto_brim"])
            self.assertAlmostEqual(process.mapped_settings["tree_support_brim_width_mm"], 0.3, places=3)
            self.assertEqual(process.unknown_keys, [])

    def test_strict_mode_fails_when_mapping_warnings_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            vendor_dir = self._make_vendor_root(root)
            self._write_vendor_index(root)
            (vendor_dir / "machine" / "MachineA.json").write_text(
                '{"type":"machine_model","name":"MachineA"}',
                encoding="utf-8",
            )
            (vendor_dir / "process" / "ProcessA.json").write_text(
                '{"type":"process","name":"ProcessA","layer_height":"not-a-number"}',
                encoding="utf-8",
            )
            (vendor_dir / "filament" / "FilamentA.json").write_text(
                '{"type":"filament","name":"FilamentA"}',
                encoding="utf-8",
            )

            with self.assertRaises(ProfileMappingError):
                discover_resolve_and_map_profiles(str(root), mapping_strict=True)


if __name__ == "__main__":
    unittest.main()

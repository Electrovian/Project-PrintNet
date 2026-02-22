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

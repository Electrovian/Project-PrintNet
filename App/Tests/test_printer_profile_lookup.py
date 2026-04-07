import os
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from config import printer_profile_lookup as lookup  # noqa: E402


class PrinterProfileLookupTests(unittest.TestCase):
    def test_pick_record_requires_matching_preferred_kind(self):
        machine = lookup.MachinePresetRecord(
            path=Path("Anker M5 0.2 nozzle.py"),
            name="Anker M5 0.2 nozzle",
            kind="machine",
            payload={},
        )
        picked = lookup._pick_record([machine], preferred_kind="machine_model")
        self.assertIsNone(picked)

    def test_resolve_plate_config_keeps_generic_machine_model_profile(self):
        machine_nozzle = lookup.MachinePresetRecord(
            path=Path("profiles/Anker M5 0.2 nozzle.py"),
            name="Anker M5 0.2 nozzle",
            kind="machine",
            payload={
                "name": "Anker M5 0.2 nozzle",
                "type": "machine",
            },
        )
        machine_model = lookup.MachinePresetRecord(
            path=Path("profiles/Anker M5.py"),
            name="Anker M5",
            kind="machine_model",
            payload={
                "name": "Anker M5",
                "type": "machine_model",
            },
        )
        by_name = {
            lookup._normalize_name("Anker M5 0.2 nozzle"): [machine_nozzle],
            lookup._normalize_name("Anker M5"): [machine_nozzle, machine_model],
        }
        by_model = {}
        with mock.patch.object(lookup, "_index_machine_presets", return_value=(by_name, by_model)):
            resolved = lookup.resolve_printer_plate_config({"name": "Anker M5 0.2 nozzle"})
        self.assertEqual(resolved.get("machine_profile_path"), str(machine_nozzle.path))
        self.assertEqual(resolved.get("machine_model_path"), str(machine_model.path))

    def test_custom_profile_resolves_eon_bed_texture_asset(self):
        resolved = lookup.resolve_printer_plate_config({"name": "MyKlipper 0.4 nozzle"})
        texture_path = Path(str(resolved.get("bed_texture_path") or ""))

        self.assertTrue(texture_path.is_file())
        self.assertEqual(texture_path.name, "eonslicer_bed_texture.svg")
        self.assertTrue(str(resolved.get("machine_profile_path") or "").endswith("MyKlipper 0.4 nozzle.py"))
        self.assertTrue(str(resolved.get("machine_model_path") or "").endswith("MyKlipper.py"))


if __name__ == "__main__":
    unittest.main()

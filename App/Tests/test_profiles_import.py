import tempfile
import unittest
from pathlib import Path

from profiles_import.importer import import_profiles


class ProfilesImportTests(unittest.TestCase):

    def test_import_profiles_builds_resolved_profiles(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "machine.json").write_text(
                '{"id":"machine-a","vendor":"Acme","model":"A1","bed_x":220,"bed_y":220,"bed_z":250,"nozzles":["0.4","0.6"]}',
                encoding="utf-8",
            )
            (root / "process.json").write_text(
                '{"id":"proc-fast","layer_height":0.2,"print_speed":120}',
                encoding="utf-8",
            )
            (root / "filament.json").write_text(
                '{"id":"pla","filament_type":"PLA","filament_diameter":1.75,"temperature":210}',
                encoding="utf-8",
            )

            report = import_profiles(str(root), import_version="v1")

            self.assertTrue(report.success)
            self.assertEqual(len(report.machines), 1)
            self.assertEqual(len(report.processes), 1)
            self.assertEqual(len(report.filaments), 1)
            self.assertEqual(len(report.nozzles), 2)
            self.assertEqual(len(report.resolved_profiles), 2)

    def test_import_profiles_flags_inheritance_cycle(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "machine-a.json").write_text(
                '{"id":"machine-a","inherits":"machine-b","bed_x":220,"bed_y":220,"bed_z":250}',
                encoding="utf-8",
            )
            (root / "machine-b.json").write_text(
                '{"id":"machine-b","inherits":"machine-a","bed_x":220,"bed_y":220,"bed_z":250}',
                encoding="utf-8",
            )

            report = import_profiles(str(root), import_version="v1")
            categories = {failure.category for failure in report.failures}
            self.assertIn("inherit_cycle", categories)

    def test_import_profiles_tolerates_malformed_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "bad.json").write_text('{"id": "oops"', encoding="utf-8")
            (root / "machine.json").write_text(
                '{"id":"machine-a","bed_x":220,"bed_y":220,"bed_z":250}',
                encoding="utf-8",
            )

            report = import_profiles(str(root), import_version="v1")
            categories = {failure.category for failure in report.failures}
            self.assertIn("invalid_json", categories)
            self.assertGreaterEqual(len(report.machines), 1)


if __name__ == "__main__":
    unittest.main()

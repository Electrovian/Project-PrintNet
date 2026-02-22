import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from profiles_import.discovery import ProfileDiscoveryError, discover_printer_profile_files


class TestPrinterProfileFileDiscovery(unittest.TestCase):
    def _create_basic_fixture(self, root: Path) -> None:
        (root / "VendorOne.json").write_text('{"name":"VendorOne"}', encoding="utf-8")
        (root / "blacklist.json").write_text("{}", encoding="utf-8")
        (root / "VendorOne" / "machine").mkdir(parents=True, exist_ok=True)
        (root / "VendorOne" / "process").mkdir(parents=True, exist_ok=True)
        (root / "VendorOne" / "filament").mkdir(parents=True, exist_ok=True)
        (root / "VendorOne" / "machine" / "machine_a.json").write_text("{}", encoding="utf-8")
        (root / "VendorOne" / "process" / "process_a.json").write_text("{}", encoding="utf-8")
        (root / "VendorOne" / "filament" / "filament_a.json").write_text("{}", encoding="utf-8")

    def test_discover_basic_vendor_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._create_basic_fixture(root)

            report = discover_printer_profile_files(str(root))

            self.assertEqual(report.vendor_count, 1)
            self.assertEqual(report.total_index_files, 1)
            self.assertEqual(report.total_machine_files, 1)
            self.assertEqual(report.total_process_files, 1)
            self.assertEqual(report.total_filament_files, 1)
            self.assertEqual(report.vendors[0].vendor, "VendorOne")
            self.assertEqual(report.vendors[0].warnings, [])

    def test_warns_when_index_or_directory_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "VendorTwo.json").write_text("{}", encoding="utf-8")
            (root / "VendorThree" / "machine").mkdir(parents=True, exist_ok=True)
            (root / "VendorThree" / "machine" / "m.json").write_text("{}", encoding="utf-8")

            report = discover_printer_profile_files(str(root))
            vendor_names = {v.vendor for v in report.vendors}

            self.assertIn("VendorTwo", vendor_names)
            self.assertIn("VendorThree", vendor_names)
            self.assertTrue(any("index_file_missing" in warning for warning in report.warnings))
            self.assertTrue(any("vendor_directory_missing" in warning for warning in report.warnings))

    def test_missing_source_raises_error(self) -> None:
        with self.assertRaises(ProfileDiscoveryError):
            discover_printer_profile_files("Z:/this/path/should/not/exist")

    def test_strict_mode_fails_on_warning(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "VendorOnlyIndex.json").write_text("{}", encoding="utf-8")

            with self.assertRaises(ProfileDiscoveryError):
                discover_printer_profile_files(str(root), strict=True)


if __name__ == "__main__":
    unittest.main()

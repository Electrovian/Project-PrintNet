import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from profiles_import.discovery import discover_printer_profile_files
from profiles_import.parsing import (
    ProfileParsingError,
    parse_vendor_index_file,
    parse_vendor_profile_files,
)


class TestVendorProfileParsing(unittest.TestCase):
    def _fixture_root(self) -> tempfile.TemporaryDirectory:
        return tempfile.TemporaryDirectory()

    def _create_minimal_vendor(self, root: Path, vendor_name: str = "VendorA") -> None:
        (root / f"{vendor_name}.json").write_text(
            """
{
  "name": "VendorA",
  "machine_model_list": [{"name":"M1","sub_path":"machine/M1.json"}],
  "process_list": [{"name":"P1","sub_path":"process/P1.json"}],
  "filament_list": [{"name":"F1","sub_path":"filament/F1.json"}]
}
""".strip(),
            encoding="utf-8",
        )
        (root / vendor_name / "machine").mkdir(parents=True, exist_ok=True)
        (root / vendor_name / "process").mkdir(parents=True, exist_ok=True)
        (root / vendor_name / "filament").mkdir(parents=True, exist_ok=True)
        (root / vendor_name / "machine" / "M1.json").write_text(
            '{"type":"machine_model","name":"M1"}',
            encoding="utf-8",
        )
        (root / vendor_name / "process" / "P1.json").write_text(
            '{"type":"process","name":"P1"}',
            encoding="utf-8",
        )
        (root / vendor_name / "filament" / "F1.json").write_text(
            '{"type":"filament","name":"F1"}',
            encoding="utf-8",
        )

    def test_parse_vendor_index_file(self) -> None:
        with self._fixture_root() as tmp:
            root = Path(tmp)
            self._create_minimal_vendor(root)

            index = parse_vendor_index_file(str(root), "VendorA.json")
            self.assertEqual(index.vendor, "VendorA")
            self.assertEqual(len(index.machine_entries), 1)
            self.assertEqual(len(index.process_entries), 1)
            self.assertEqual(len(index.filament_entries), 1)
            self.assertEqual(index.warnings, [])

    def test_parse_vendor_profiles_success(self) -> None:
        with self._fixture_root() as tmp:
            root = Path(tmp)
            self._create_minimal_vendor(root)
            discovery = discover_printer_profile_files(str(root))

            parsed = parse_vendor_profile_files(str(root), discovery)
            self.assertEqual(parsed.vendor_count, 1)
            self.assertEqual(parsed.total_machine_files_parsed, 1)
            self.assertEqual(parsed.total_process_files_parsed, 1)
            self.assertEqual(parsed.total_filament_files_parsed, 1)
            self.assertEqual(parsed.total_type_mismatches, 0)
            self.assertEqual(parsed.total_warnings, 0)

    def test_type_mismatch_generates_warning(self) -> None:
        with self._fixture_root() as tmp:
            root = Path(tmp)
            self._create_minimal_vendor(root)
            (root / "VendorA" / "process" / "P1.json").write_text(
                '{"type":"filament","name":"P1"}',
                encoding="utf-8",
            )
            discovery = discover_printer_profile_files(str(root))

            parsed = parse_vendor_profile_files(str(root), discovery)
            self.assertEqual(parsed.total_type_mismatches, 1)
            self.assertGreater(parsed.total_warnings, 0)

    def test_strict_mode_raises_on_warning(self) -> None:
        with self._fixture_root() as tmp:
            root = Path(tmp)
            self._create_minimal_vendor(root)
            (root / "VendorA" / "machine" / "M1.json").write_text(
                '{"name":"M1"}',
                encoding="utf-8",
            )
            discovery = discover_printer_profile_files(str(root))
            with self.assertRaises(ProfileParsingError):
                parse_vendor_profile_files(str(root), discovery, strict=True)

    def test_invalid_json_raises(self) -> None:
        with self._fixture_root() as tmp:
            root = Path(tmp)
            self._create_minimal_vendor(root)
            (root / "VendorA" / "filament" / "F1.json").write_text("{ bad json", encoding="utf-8")
            discovery = discover_printer_profile_files(str(root))
            with self.assertRaises(ProfileParsingError):
                parse_vendor_profile_files(str(root), discovery)


if __name__ == "__main__":
    unittest.main()

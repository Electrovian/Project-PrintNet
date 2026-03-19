import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from profiles_import.json_catalog import (  # noqa: E402
    JSON_BUCKET_MISC,
    JSON_BUCKET_ROOT_AUX,
    JSON_BUCKET_VENDOR_FILAMENT,
    JSON_BUCKET_VENDOR_INDEX,
    JSON_BUCKET_VENDOR_MACHINE,
    JSON_BUCKET_VENDOR_PROCESS,
    JsonConfigCatalogError,
    discover_json_config_catalog,
)


class TestProfileJsonCatalog(unittest.TestCase):
    def _create_fixture(self, root: Path) -> None:
        (root / "VendorA.json").write_text('{"name":"VendorA"}', encoding="utf-8")
        (root / "blacklist.json").write_text("{}", encoding="utf-8")
        (root / "VendorA" / "machine").mkdir(parents=True, exist_ok=True)
        (root / "VendorA" / "process").mkdir(parents=True, exist_ok=True)
        (root / "VendorA" / "filament").mkdir(parents=True, exist_ok=True)
        (root / "VendorA" / "meta").mkdir(parents=True, exist_ok=True)
        (root / "VendorA" / "machine" / "M1.json").write_text(
            '{"type":"machine_model","name":"M1"}',
            encoding="utf-8",
        )
        (root / "VendorA" / "process" / "P1.json").write_text(
            '{"type":"process","name":"P1"}',
            encoding="utf-8",
        )
        (root / "VendorA" / "filament" / "F1.json").write_text(
            '{"type":"filament","name":"F1"}',
            encoding="utf-8",
        )
        (root / "VendorA" / "meta" / "extra.json").write_text(
            '{"note":"extra"}',
            encoding="utf-8",
        )

    def test_catalog_captures_all_json_files_and_buckets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._create_fixture(root)
            report = discover_json_config_catalog(str(root))

            self.assertEqual(report.total_json_files, 6)
            self.assertEqual(report.bucket_counts.get(JSON_BUCKET_VENDOR_INDEX), 1)
            self.assertEqual(report.bucket_counts.get(JSON_BUCKET_ROOT_AUX), 1)
            self.assertEqual(report.bucket_counts.get(JSON_BUCKET_VENDOR_MACHINE), 1)
            self.assertEqual(report.bucket_counts.get(JSON_BUCKET_VENDOR_PROCESS), 1)
            self.assertEqual(report.bucket_counts.get(JSON_BUCKET_VENDOR_FILAMENT), 1)
            self.assertEqual(report.bucket_counts.get(JSON_BUCKET_MISC), 1)
            self.assertEqual(len(report.all_json_files), 6)
            self.assertEqual(report.invalid_json_count, 0)
            self.assertEqual(report.warning_count, 0)

    def test_validate_json_reports_invalid_payloads(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._create_fixture(root)
            (root / "VendorA" / "process" / "P1.json").write_text("{ broken", encoding="utf-8")

            report = discover_json_config_catalog(str(root), validate_json=True)
            self.assertEqual(report.invalid_json_count, 1)
            self.assertEqual(len(report.invalid_json_files), 1)
            self.assertIn("VendorA/process/P1.json", report.invalid_json_files)
            self.assertGreater(report.warning_count, 0)

    def test_strict_mode_raises_on_validation_warning(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._create_fixture(root)
            (root / "VendorA" / "filament" / "F1.json").write_text("{ broken", encoding="utf-8")

            with self.assertRaises(JsonConfigCatalogError):
                discover_json_config_catalog(str(root), validate_json=True, strict=True)


if __name__ == "__main__":
    unittest.main()


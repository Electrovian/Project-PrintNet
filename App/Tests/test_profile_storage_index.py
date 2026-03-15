import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from profiles_import.storage import (  # noqa: E402
    ProfileStorageError,
    discover_resolve_map_build_and_persist_profile_storage_index,
    load_profile_storage_index,
    query_profile_storage_index,
)


class TestProfileStorageIndex(unittest.TestCase):
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
  "process_list": [
    {"name":"ProcessFast","sub_path":"process/ProcessFast.json"},
    {"name":"ProcessQuality","sub_path":"process/ProcessQuality.json"}
  ],
  "filament_list": [{"name":"FilamentA","sub_path":"filament/FilamentA.json"}]
}
""".strip(),
            encoding="utf-8",
        )

    def _write_valid_profiles(self, vendor_dir: Path) -> None:
        (vendor_dir / "machine" / "MachineA.json").write_text(
            '{"type":"machine_model","name":"MachineA","nozzle_diameter":"0.4","bed_shape":"0x0,220x0,220x220,0x220"}',
            encoding="utf-8",
        )
        (vendor_dir / "process" / "ProcessFast.json").write_text(
            '{"type":"process","name":"ProcessFast","layer_height":"0.28","sparse_infill_density":"20%","outer_wall_speed":"80"}',
            encoding="utf-8",
        )
        (vendor_dir / "process" / "ProcessQuality.json").write_text(
            '{"type":"process","name":"ProcessQuality","layer_height":"0.16","sparse_infill_density":"15%","outer_wall_speed":"45"}',
            encoding="utf-8",
        )
        (vendor_dir / "filament" / "FilamentA.json").write_text(
            '{"type":"filament","name":"FilamentA","filament_type":"PLA","filament_colour":"#121212"}',
            encoding="utf-8",
        )

    def test_build_index_and_query_vendor_category(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            vendor_dir = self._make_vendor_root(root)
            self._write_vendor_index(root)
            self._write_valid_profiles(vendor_dir)
            index_path = root / "index.json"

            index = discover_resolve_map_build_and_persist_profile_storage_index(
                str(root),
                str(index_path),
            )
            vendor_rows = query_profile_storage_index(index, vendor="VendorA", limit=20)
            process_rows = query_profile_storage_index(index, category="process", limit=20)

            self.assertEqual(index.record_count, 4)
            self.assertEqual(len(vendor_rows), 4)
            self.assertEqual(len(process_rows), 2)
            self.assertEqual(index.total_json_file_count, 5)
            self.assertEqual(index.json_file_count_by_bucket.get("vendor_index"), 1)
            self.assertEqual(index.json_file_count_by_bucket.get("vendor_machine"), 1)
            self.assertEqual(index.json_file_count_by_bucket.get("vendor_process"), 2)
            self.assertEqual(index.json_file_count_by_bucket.get("vendor_filament"), 1)
            self.assertEqual(len(index.json_files), 5)
            self.assertEqual(index.unmapped_profile_json_files, [])

    def test_query_by_name_contains_and_setting_key(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            vendor_dir = self._make_vendor_root(root)
            self._write_vendor_index(root)
            self._write_valid_profiles(vendor_dir)
            index_path = root / "index.json"

            index = discover_resolve_map_build_and_persist_profile_storage_index(
                str(root),
                str(index_path),
            )
            fast_rows = query_profile_storage_index(
                index,
                category="process",
                name_contains="fast",
                limit=10,
            )
            layer_rows = query_profile_storage_index(
                index,
                mapped_key="layer_height",
                limit=10,
            )

            self.assertEqual(len(fast_rows), 1)
            self.assertEqual(fast_rows[0].name, "ProcessFast")
            self.assertGreaterEqual(len(layer_rows), 2)

    def test_persist_and_load_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            vendor_dir = self._make_vendor_root(root)
            self._write_vendor_index(root)
            self._write_valid_profiles(vendor_dir)
            index_path = root / "index.json"

            created = discover_resolve_map_build_and_persist_profile_storage_index(
                str(root),
                str(index_path),
            )
            loaded = load_profile_storage_index(str(index_path))
            loaded_rows = query_profile_storage_index(loaded, vendor="VendorA", limit=20)

            self.assertEqual(loaded.record_count, created.record_count)
            self.assertEqual(loaded.vendor_count, created.vendor_count)
            self.assertEqual(len(loaded_rows), 4)
            self.assertEqual(loaded.total_json_file_count, created.total_json_file_count)
            self.assertEqual(loaded.json_file_count_by_bucket, created.json_file_count_by_bucket)
            self.assertEqual(loaded.unmapped_profile_json_files, created.unmapped_profile_json_files)

    def test_strict_storage_fails_when_mapping_has_warnings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            vendor_dir = self._make_vendor_root(root)
            self._write_vendor_index(root)
            self._write_valid_profiles(vendor_dir)
            (vendor_dir / "process" / "ProcessFast.json").write_text(
                '{"type":"process","name":"ProcessFast","layer_height":"not-a-number"}',
                encoding="utf-8",
            )
            index_path = root / "index.json"

            with self.assertRaises(ProfileStorageError):
                discover_resolve_map_build_and_persist_profile_storage_index(
                    str(root),
                    str(index_path),
                    storage_strict=True,
                )

    def test_load_rejects_invalid_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            broken = Path(tmp) / "broken.json"
            broken.write_text("{", encoding="utf-8")
            with self.assertRaises(ProfileStorageError):
                load_profile_storage_index(str(broken))


if __name__ == "__main__":
    unittest.main()

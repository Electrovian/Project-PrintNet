import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from profiles_import.discovery import discover_printer_profile_files
from profiles_import.inheritance import (
    ProfileInheritanceError,
    discover_and_resolve_profile_inheritance,
    resolve_profile_inheritance,
)


class TestProfileInheritanceMerge(unittest.TestCase):
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
  "process_list": [{"name":"ProcessBase","sub_path":"process/ProcessBase.json"}],
  "filament_list": [{"name":"FilamentA","sub_path":"filament/FilamentA.json"}]
}
""".strip(),
            encoding="utf-8",
        )

    def _write_base_docs(self, vendor_dir: Path) -> None:
        (vendor_dir / "machine" / "MachineA.json").write_text(
            '{"type":"machine_model","name":"MachineA"}',
            encoding="utf-8",
        )
        (vendor_dir / "filament" / "FilamentA.json").write_text(
            '{"type":"filament","name":"FilamentA"}',
            encoding="utf-8",
        )

    def test_merge_precedence_child_overrides_parent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            vendor_dir = self._make_vendor_root(root)
            self._write_vendor_index(root)
            self._write_base_docs(vendor_dir)
            (vendor_dir / "process" / "ProcessBase.json").write_text(
                '{"type":"process","name":"ProcessBase","line_width":"0.45","outer_wall_speed":"40"}',
                encoding="utf-8",
            )
            (vendor_dir / "process" / "ProcessChild.json").write_text(
                '{"type":"process","name":"ProcessChild","inherits":"ProcessBase","outer_wall_speed":"60"}',
                encoding="utf-8",
            )

            report = discover_and_resolve_profile_inheritance(str(root))
            child = next(
                p for p in report.resolved_profiles if p.category == "process" and p.name == "ProcessChild"
            )
            self.assertEqual(child.resolved_data["outer_wall_speed"], "60")
            self.assertEqual(child.resolved_data["line_width"], "0.45")
            self.assertEqual(child.chain_names, ["ProcessBase", "ProcessChild"])

    def test_missing_parent_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            vendor_dir = self._make_vendor_root(root)
            self._write_vendor_index(root)
            self._write_base_docs(vendor_dir)
            (vendor_dir / "process" / "ProcessBase.json").write_text(
                '{"type":"process","name":"ProcessBase","inherits":"NoSuchParent"}',
                encoding="utf-8",
            )

            report = discover_and_resolve_profile_inheritance(str(root))
            self.assertGreaterEqual(report.missing_parent_count, 1)

    def test_cycle_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            vendor_dir = self._make_vendor_root(root)
            self._write_vendor_index(root)
            self._write_base_docs(vendor_dir)
            (vendor_dir / "process" / "A.json").write_text(
                '{"type":"process","name":"A","inherits":"B"}',
                encoding="utf-8",
            )
            (vendor_dir / "process" / "B.json").write_text(
                '{"type":"process","name":"B","inherits":"A"}',
                encoding="utf-8",
            )

            report = discover_and_resolve_profile_inheritance(str(root))
            self.assertGreaterEqual(report.cycle_count, 1)

    def test_max_depth_is_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            vendor_dir = self._make_vendor_root(root)
            self._write_vendor_index(root)
            self._write_base_docs(vendor_dir)
            (vendor_dir / "process" / "A.json").write_text(
                '{"type":"process","name":"A"}',
                encoding="utf-8",
            )
            (vendor_dir / "process" / "B.json").write_text(
                '{"type":"process","name":"B","inherits":"A"}',
                encoding="utf-8",
            )
            (vendor_dir / "process" / "C.json").write_text(
                '{"type":"process","name":"C","inherits":"B"}',
                encoding="utf-8",
            )

            discovery = discover_printer_profile_files(str(root))
            report = resolve_profile_inheritance(str(root), discovery, max_chain_depth=1)
            self.assertGreaterEqual(report.max_depth_exceeded_count, 1)

    def test_strict_mode_fails_when_warnings_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            vendor_dir = self._make_vendor_root(root)
            self._write_vendor_index(root)
            self._write_base_docs(vendor_dir)
            (vendor_dir / "process" / "ProcessBase.json").write_text(
                '{"type":"process","name":"ProcessBase","inherits":"MissingParent"}',
                encoding="utf-8",
            )
            discovery = discover_printer_profile_files(str(root))

            with self.assertRaises(ProfileInheritanceError):
                resolve_profile_inheritance(str(root), discovery, strict=True)


if __name__ == "__main__":
    unittest.main()

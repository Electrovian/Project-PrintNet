import os
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from printer_presets import startup_validation as sv


class StartupValidationTests(unittest.TestCase):
    def test_profile_py_path_from_storage_json_suffix(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            resolved = sv._profile_py_path_from_storage("profiles/VendorA/machine/M1.json", root)
            self.assertEqual(resolved, root / "VendorA" / "machine" / "M1.py")

    def test_profile_py_path_from_storage_non_json_suffix(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            resolved = sv._profile_py_path_from_storage("profiles/VendorA/process/P1", root)
            self.assertEqual(resolved, root / "VendorA" / "process" / "P1.py")

    def test_profile_py_path_from_storage_rejects_non_profiles_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(RuntimeError):
                sv._profile_py_path_from_storage("seed_resources/profiles/VendorA.json", root)

    def test_rule_for_path_selects_expected_rule_variants(self) -> None:
        printers_module = Path("seed/printers/printers_data.py").resolve()
        self.assertIs(sv._rule_for_path(printers_module, printers_module), sv._PRINTERS_RULE)
        self.assertIs(
            sv._rule_for_path(Path("seed/python_vendors/__init__.py").resolve(), printers_module),
            sv._VENDOR_INIT_RULE,
        )
        self.assertIs(
            sv._rule_for_path(Path("seed/python_vendors/acme.py").resolve(), printers_module),
            sv._VENDOR_ALL_RULE,
        )
        self.assertIs(
            sv._rule_for_path(Path("seed/python_vendors/global_profiles_data.py").resolve(), printers_module),
            sv._VENDOR_SKIP_RULE,
        )
        self.assertIs(sv._rule_for_path(Path("seed/vendor/file.py").resolve(), printers_module), sv._PROFILE_RULE)

    def test_is_dict_like_probe_accepts_dict_prefixes(self) -> None:
        self.assertTrue(sv._is_dict_like_probe("   {'a': 1}"))
        self.assertTrue(sv._is_dict_like_probe(" ( dict(a=1)"))
        self.assertTrue(sv._is_dict_like_probe("  (OrderedDict())"))
        self.assertFalse(sv._is_dict_like_probe(" [1,2,3]"))

    def test_assignment_value_is_dict_via_ast_variants(self) -> None:
        self.assertTrue(sv._assignment_value_is_dict_via_ast("DATA = {'a': 1}\n", "DATA"))
        self.assertTrue(sv._assignment_value_is_dict_via_ast("DATA = dict(a=1)\n", "DATA"))
        self.assertFalse(sv._assignment_value_is_dict_via_ast("DATA = [1,2,3]\n", "DATA"))
        self.assertIsNone(sv._assignment_value_is_dict_via_ast("OTHER = {}\n", "DATA"))

    def test_validate_source_against_rule_missing_symbol(self) -> None:
        with self.assertRaises(RuntimeError) as ctx:
            sv._validate_source_against_rule("VALUE = {}\n", sv._PROFILE_RULE)
        self.assertIn("DATA_PAYLOAD_MISSING", str(ctx.exception))

    def test_validate_source_against_rule_reports_not_dict(self) -> None:
        with self.assertRaises(RuntimeError) as ctx:
            sv._validate_source_against_rule("DATA = [1,2,3]\n", sv._PROFILE_RULE)
        self.assertIn("DATA_PAYLOAD_NOT_DICT", str(ctx.exception))

    def test_validate_source_against_rule_passes_non_dict_required(self) -> None:
        sv._validate_source_against_rule("ALL = [1,2,3]\n", sv._VENDOR_ALL_RULE)

    def test_validate_file_uses_full_content_when_prefix_is_truncated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "profile.py"
            path.write_text((" " * (sv._CACHE_SCAN_BYTES + 16)) + "DATA = {'ok': 1}\n", encoding="utf-8")
            sv._validate_file(path, sv._PROFILE_RULE)

    def test_load_validation_cache_ignores_invalid_payloads(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cache_path = Path(tmp) / "cache.json"
            cache_path.write_text('{"version":999,"files":{"x":{"sig":"1","tag":"t"}}}', encoding="utf-8")
            with mock.patch.object(sv, "_validation_cache_path", return_value=cache_path):
                loaded = sv._load_validation_cache()
            self.assertEqual(loaded, {})

    def test_save_validation_cache_writes_expected_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cache_path = Path(tmp) / "cache.json"
            payload = {"a.py": {"sig": "10:123", "tag": "_:0"}}
            with mock.patch.object(sv, "_validation_cache_path", return_value=cache_path):
                sv._save_validation_cache(payload)
            raw = cache_path.read_text(encoding="utf-8")
            self.assertIn('"version":1', raw)
            self.assertIn('"a.py"', raw)

    def test_validate_preset_python_files_errors_for_missing_profiles_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            profiles_root = Path(tmp) / "missing_profiles"
            printers_path = Path(tmp) / "printers_data.py"
            printers_path.write_text("PRINTERS_DATA = {}\n", encoding="utf-8")
            with self.assertRaises(sv.PresetValidationError) as ctx:
                sv.validate_preset_python_files(profiles_root=profiles_root, printers_data_path=printers_path)
            self.assertIn("PRESET_PROFILES_ROOT_NOT_FOUND", str(ctx.exception))

    def test_validate_preset_python_files_errors_for_missing_printers_data(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            profiles_root = Path(tmp) / "profiles"
            profiles_root.mkdir(parents=True, exist_ok=True)
            printers_path = Path(tmp) / "missing_printers_data.py"
            with self.assertRaises(sv.PresetValidationError) as ctx:
                sv.validate_preset_python_files(profiles_root=profiles_root, printers_data_path=printers_path)
            self.assertIn("PRESET_PRINTERS_DATA_NOT_FOUND", str(ctx.exception))

    def test_validate_preset_python_files_success_with_progress_and_cache(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profiles_root = root / "profiles"
            printers_path = root / "printers_data.py"
            profile_py = profiles_root / "VendorA" / "machine" / "M1.py"
            profile_py.parent.mkdir(parents=True, exist_ok=True)
            profile_py.write_text("DATA = {'name': 'M1'}\n", encoding="utf-8")
            printers_path.write_text("PRINTERS_DATA = {'M1': {'name': 'M1'}}\n", encoding="utf-8")

            docs = [SimpleNamespace(storage_path="profiles/VendorA/machine/M1.json")]
            progress = []

            with mock.patch.object(sv.preset_store, "iter_documents", return_value=iter(docs)):
                with mock.patch.object(sv, "_load_validation_cache", return_value={}):
                    with mock.patch.object(sv, "_save_validation_cache") as save_mock:
                        report = sv.validate_preset_python_files(
                            profiles_root=profiles_root,
                            printers_data_path=printers_path,
                            on_progress=lambda idx, total, path: progress.append((idx, total, path)),
                        )

            self.assertEqual(report.failed_count, 0)
            self.assertEqual(report.checked_count, 2)
            self.assertEqual(report.total_files, 2)
            self.assertEqual(len(progress), 2)
            save_mock.assert_called_once()

    def test_validate_preset_python_files_reports_missing_profile_py_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profiles_root = root / "profiles"
            profiles_root.mkdir(parents=True, exist_ok=True)
            printers_path = root / "printers_data.py"
            printers_path.write_text("PRINTERS_DATA = {}\n", encoding="utf-8")

            docs = [SimpleNamespace(storage_path="profiles/VendorA/machine/MISSING.json")]
            with mock.patch.object(sv.preset_store, "iter_documents", return_value=iter(docs)):
                with mock.patch.object(sv, "_load_validation_cache", return_value={}):
                    with mock.patch.object(sv, "_save_validation_cache"):
                        with self.assertRaises(sv.PresetValidationError) as ctx:
                            sv.validate_preset_python_files(
                                profiles_root=profiles_root,
                                printers_data_path=printers_path,
                            )
            self.assertIn("MISSING_PROFILE_PY_FILE", str(ctx.exception))

    def test_validate_preset_python_files_uses_cache_to_skip_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profiles_root = root / "profiles"
            printers_path = root / "printers_data.py"
            profile_py = profiles_root / "VendorA" / "process" / "P1.py"
            profile_py.parent.mkdir(parents=True, exist_ok=True)
            profile_py.write_text("DATA = {'name': 'P1'}\n", encoding="utf-8")
            printers_path.write_text("PRINTERS_DATA = {'P1': {'name': 'P1'}}\n", encoding="utf-8")

            docs = [SimpleNamespace(storage_path="profiles/VendorA/process/P1.json")]
            profile_sig = sv._file_signature(profile_py)
            printer_sig = sv._file_signature(printers_path)

            cache = {
                str(profile_py.resolve()): {"sig": profile_sig, "tag": sv._rule_cache_tag(sv._PROFILE_RULE)},
                str(printers_path.resolve()): {"sig": printer_sig, "tag": sv._rule_cache_tag(sv._PRINTERS_RULE)},
            }

            with mock.patch.object(sv.preset_store, "iter_documents", return_value=iter(docs)):
                with mock.patch.object(sv, "_load_validation_cache", return_value=cache):
                    with mock.patch.object(sv, "_validate_file") as validate_mock:
                        with mock.patch.object(sv, "_save_validation_cache"):
                            report = sv.validate_preset_python_files(
                                profiles_root=profiles_root,
                                printers_data_path=printers_path,
                            )
            self.assertEqual(report.checked_count, 2)
            validate_mock.assert_not_called()

    def test_validate_preset_python_files_failure_reason_includes_exception_type(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profiles_root = root / "profiles"
            printers_path = root / "printers_data.py"
            profile_py = profiles_root / "VendorA" / "filament" / "F1.py"
            profile_py.parent.mkdir(parents=True, exist_ok=True)
            profile_py.write_text("DATA = {'name': 'F1'}\n", encoding="utf-8")
            printers_path.write_text("PRINTERS_DATA = {'F1': {'name': 'F1'}}\n", encoding="utf-8")

            docs = [SimpleNamespace(storage_path="profiles/VendorA/filament/F1.json")]
            with mock.patch.object(sv.preset_store, "iter_documents", return_value=iter(docs)):
                with mock.patch.object(sv, "_load_validation_cache", return_value={}):
                    with mock.patch.object(sv, "_save_validation_cache"):
                        with mock.patch.object(sv, "_validate_file", side_effect=ValueError("boom")):
                            with self.assertRaises(sv.PresetValidationError) as ctx:
                                sv.validate_preset_python_files(
                                    profiles_root=profiles_root,
                                    printers_data_path=printers_path,
                                )
            self.assertIn("ValueError:boom", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import trimesh

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from slicer_v2.pipeline import STAGE_SEQUENCE  # noqa: E402
from testing.fff_parity import compare_report_payloads, run_fff_corpus  # noqa: E402


class TestSlicerV2FffCorpus(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture_dir = ROOT / "Tests" / "fixtures" / "fff_parity"
        cls.profile_path = cls.fixture_dir / "profile_fff_default.json"
        cls.expected_stage_order = [name for name, _runner in STAGE_SEQUENCE]

    def _write_box_mesh(self, tmpdir: Path) -> Path:
        mesh_path = tmpdir / "demo_box.stl"
        trimesh.creation.box(extents=(12.0, 12.0, 12.0)).export(mesh_path)
        return mesh_path

    def _write_manifest(self, tmpdir: Path, mesh_path: Path, *, name: str = "fff_parity_demo") -> Path:
        manifest_path = tmpdir / "manifest.json"
        manifest_payload = {
            "name": name,
            "models": [
                {
                    "id": "demo_box",
                    "path": str(mesh_path),
                    "settings_override": {},
                }
            ],
        }
        manifest_path.write_text(json.dumps(manifest_payload, indent=2), encoding="utf-8")
        return manifest_path

    def test_fff_corpus_runner_emits_metrics_and_self_comparison(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            mesh_path = self._write_box_mesh(tmpdir)
            manifest_path = self._write_manifest(tmpdir, mesh_path)

            report = run_fff_corpus(
                manifest_path=manifest_path,
                profile_path=self.profile_path,
                continue_on_error=True,
            )

        self.assertEqual(report["model_count"], 1)
        self.assertEqual(report["executed_model_count"], 1)
        self.assertEqual(report["failed_model_count"], 0)
        self.assertEqual(report["stage_order_expected"], self.expected_stage_order)
        self.assertEqual(report["results"][0]["status"], "ok")
        self.assertIn("metrics", report["results"][0])

        comparison = compare_report_payloads(report, report)
        self.assertTrue(comparison["ok"])
        self.assertEqual(comparison["issue_count"], 0)
        self.assertEqual(comparison["compared_model_count"], 1)

    def test_fff_corpus_runner_fails_loudly_when_mesh_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            manifest_path = self._write_manifest(tmpdir, tmpdir / "missing_mesh.stl")

            with self.assertRaises(FileNotFoundError) as exc_info:
                run_fff_corpus(
                    manifest_path=manifest_path,
                    profile_path=self.profile_path,
                    continue_on_error=True,
                )

        self.assertIn("FFF_PARITY_CORPUS_MISSING_MODELS", str(exc_info.exception))

    def test_zero_compare_is_not_green(self) -> None:
        comparison = compare_report_payloads(
            {"model_count": 0, "results": []},
            {"model_count": 0, "results": []},
        )

        self.assertFalse(comparison["ok"])
        self.assertEqual(comparison["issue_count"], 1)
        self.assertEqual(comparison["issues"][0]["code"], "no_comparable_models")

    def test_cli_runs_as_module_and_script(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            mesh_path = self._write_box_mesh(tmpdir)
            manifest_path = self._write_manifest(tmpdir, mesh_path)
            module_output = tmpdir / "module_output.json"
            script_output = tmpdir / "script_output.json"

            module_result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "App.testing.fff_parity",
                    "--manifest",
                    str(manifest_path),
                    "--profile",
                    str(self.profile_path),
                    "--output",
                    str(module_output),
                    "--max-models",
                    "1",
                ],
                cwd=str(REPO_ROOT),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(module_result.returncode, 0, msg=module_result.stdout + module_result.stderr)
            module_payload = json.loads(module_output.read_text(encoding="utf-8"))
            self.assertEqual(module_payload["results"][0]["status"], "ok")

            script_result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "testing" / "fff_parity.py"),
                    "--manifest",
                    str(manifest_path),
                    "--profile",
                    str(self.profile_path),
                    "--output",
                    str(script_output),
                    "--max-models",
                    "1",
                ],
                cwd=str(REPO_ROOT),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(script_result.returncode, 0, msg=script_result.stdout + script_result.stderr)
            script_payload = json.loads(script_output.read_text(encoding="utf-8"))
            self.assertEqual(script_payload["executed_model_count"], 1)
            self.assertEqual(script_payload["stage_order_expected"], self.expected_stage_order)


if __name__ == "__main__":
    unittest.main()

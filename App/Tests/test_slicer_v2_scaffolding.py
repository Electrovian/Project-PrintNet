import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer_v2.cli import main as slicer_v2_cli_main  # noqa: E402
from slicer_v2.context import create_context  # noqa: E402
from slicer_v2.errors import SlicerV2CancelledError, SlicerV2ValidationError  # noqa: E402
from slicer_v2.pipeline import STAGE_SEQUENCE, run_pipeline  # noqa: E402


def _write_minimal_stl(path: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "solid eon",
                "facet normal 0 0 1",
                "outer loop",
                "vertex 0 0 0",
                "vertex 1 0 0",
                "vertex 0 1 0",
                "endloop",
                "endfacet",
                "endsolid eon",
            ]
        ),
        encoding="utf-8",
    )


class TestSlicerV2Scaffolding(unittest.TestCase):
    def test_pipeline_executes_expected_stage_order(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mesh = Path(tmp) / "part.stl"
            _write_minimal_stl(mesh)
            context = create_context(job_id="job-1", mesh_path=str(mesh))
            result = run_pipeline(context)

            expected = [name for name, _runner in STAGE_SEQUENCE]
            self.assertEqual(result.context.stage_order_executed, expected)
            self.assertTrue(result.validation.ok)

    def test_pipeline_creates_artifacts_for_all_stages(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mesh = Path(tmp) / "part.stl"
            _write_minimal_stl(mesh)
            context = create_context(job_id="job-2", mesh_path=str(mesh))
            result = run_pipeline(context)
            for stage_name, _runner in STAGE_SEQUENCE:
                self.assertIn(stage_name, result.context.stage_artifacts)

    def test_validation_rejects_missing_mesh(self) -> None:
        context = create_context(job_id="job-3", mesh_path="C:/missing/mesh.stl")
        with self.assertRaises(SlicerV2ValidationError):
            run_pipeline(context)

    def test_pipeline_cancellation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mesh = Path(tmp) / "part.stl"
            _write_minimal_stl(mesh)
            context = create_context(job_id="job-4", mesh_path=str(mesh))
            context.cancellation_requested = True
            with self.assertRaises(SlicerV2CancelledError):
                run_pipeline(context)

    def test_cli_generates_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mesh = Path(tmp) / "part.stl"
            report = Path(tmp) / "report.json"
            _write_minimal_stl(mesh)

            exit_code = slicer_v2_cli_main(
                [
                    "--mesh-path",
                    str(mesh),
                    "--layer-height",
                    "0.2",
                    "--report-path",
                    str(report),
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertTrue(report.exists())
            payload = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(payload["return_code"], 0)
            self.assertEqual(payload["plate_index"], 1)
            self.assertIn("prepare_time", payload)
            self.assertIn("export_time", payload)
            self.assertIsInstance(payload["sliced_plates"], list)


if __name__ == "__main__":
    unittest.main()

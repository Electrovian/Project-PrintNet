import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer_v2.pipeline import STAGE_SEQUENCE  # noqa: E402
from testing.fff_parity import compare_report_payloads, run_fff_corpus  # noqa: E402


class TestSlicerV2FffCorpus(unittest.TestCase):
    def test_fff_corpus_runner_emits_metrics_and_self_comparison(self) -> None:
        fixture_dir = Path(ROOT) / "Tests" / "fixtures" / "fff_parity"
        manifest = json.loads((fixture_dir / "corpus_manifest.json").read_text(encoding="utf-8"))
        profile_path = fixture_dir / "profile_fff_default.json"

        stl_models = [
            item for item in manifest.get("models", []) if isinstance(item, dict) and str(item.get("path", "")).lower().endswith(".stl")
        ]
        self.assertGreaterEqual(len(stl_models), 1)

        with tempfile.TemporaryDirectory() as tmp:
            manifest_path = Path(tmp) / "manifest.json"
            manifest_payload = {
                "name": "fff_parity_stl_subset",
                "models": stl_models[:2],
            }
            manifest_path.write_text(json.dumps(manifest_payload, indent=2), encoding="utf-8")

            report = run_fff_corpus(
                manifest_path=manifest_path,
                profile_path=profile_path,
                continue_on_error=True,
            )

        self.assertEqual(report["model_count"], len(stl_models[:2]))
        self.assertEqual(report["stage_order_expected"], [name for name, _runner in STAGE_SEQUENCE])
        self.assertIn("results", report)

        comparison = compare_report_payloads(report, report)
        self.assertTrue(comparison["ok"])
        self.assertEqual(comparison["issue_count"], 0)


if __name__ == "__main__":
    unittest.main()

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_OPENGL", "software")

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

try:
    from testing import visual_audit  # noqa: E402
except Exception:
    visual_audit = None


@unittest.skipIf(visual_audit is None, "visual audit entrypoint unavailable")
class VisualAuditEntrypointTests(unittest.TestCase):
    def test_demo_scenario_generates_timestamped_pngs_and_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp).joinpath("audit")
            app = visual_audit.QtWidgets.QApplication.instance()
            if app is None:
                app = visual_audit.QtWidgets.QApplication(["visual-audit-test"])
            baseline_top_levels = {id(widget) for widget in app.topLevelWidgets()}
            report = visual_audit.run_demo_audit(output_dir=output_dir)
            visual_audit.QtWidgets.QApplication.processEvents()
            remaining_top_levels = {id(widget) for widget in app.topLevelWidgets()}

            self.assertTrue(report["ok"])
            self.assertEqual(report["scenario"], "demo")
            self.assertGreaterEqual(report["screenshot_count"], 9)
            self.assertEqual(report["renderer_mode"], "software")
            self.assertFalse(report["viewer_runtime_degraded"])
            self.assertTrue(output_dir.exists())
            self.assertEqual(remaining_top_levels - baseline_top_levels, set())

            png_files = sorted(output_dir.glob("*.png"))
            self.assertGreaterEqual(len(png_files), 9)
            for path in png_files:
                self.assertRegex(path.name, r"^\d{8}T\d{6}\d{6}Z_[a-z0-9_]+\.png$")
                self.assertGreater(path.stat().st_size, 0)

            manifest_path = output_dir / "visual_audit_manifest.json"
            self.assertTrue(manifest_path.exists())
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertTrue(manifest["ok"])
            self.assertEqual(manifest["scenario"], "demo")
            self.assertEqual(manifest["screenshot_count"], len(png_files))
            self.assertEqual(manifest["renderer_mode"], "software")
            self.assertFalse(manifest["viewer_runtime_degraded"])

            names = {item["name"] for item in manifest["screenshots"]}
            self.assertIn("startup", names)
            self.assertIn("files_empty", names)
            self.assertIn("files_populated", names)
            self.assertIn("activity_banners", names)
            self.assertIn("prepare_default", names)
            self.assertIn("prepare_navigator_closeup", names)
            self.assertIn("preview_tree_support", names)
            self.assertIn("preview_navigator_closeup", names)
            self.assertIn("preview_organic_support", names)
            self.assertIn("device_live_status", names)
            self.assertIn("control_calibration", names)

    def test_main_rejects_unsupported_scenarios(self):
        code = visual_audit.main(["--scenario", "not-real"])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()

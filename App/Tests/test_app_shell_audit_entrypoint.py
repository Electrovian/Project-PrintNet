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
    from testing import app_shell_audit  # noqa: E402
except Exception:
    app_shell_audit = None


@unittest.skipIf(app_shell_audit is None, "app shell audit entrypoint unavailable")
class AppShellAuditEntrypointTests(unittest.TestCase):
    def test_full_shell_audit_generates_reports_and_inventory(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp).joinpath("audit")
            report = app_shell_audit.run_full_shell_audit(output_dir=output_dir)

            self.assertTrue(report["ok"])
            self.assertEqual(report["scenario"], "full-shell")
            self.assertGreaterEqual(report["screenshot_count"], 10)
            self.assertGreater(report["action_count"], 20)
            self.assertEqual(report["unknown_controls"], [])
            self.assertEqual(report["renderer_mode"], "software")
            self.assertFalse(report["viewer_runtime_degraded"])

            manifest_path = output_dir / "app_shell_audit_manifest.json"
            inventory_path = output_dir / "control_inventory.json"
            ledger_path = output_dir / "logs" / "action_ledger.jsonl"
            self.assertTrue(manifest_path.exists())
            self.assertTrue(inventory_path.exists())
            self.assertTrue(ledger_path.exists())

            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
            self.assertTrue(manifest["ok"])
            self.assertEqual(manifest["scenario"], "full-shell")
            self.assertEqual(manifest["screenshot_count"], len(manifest["screenshots"]))
            self.assertEqual(manifest["renderer_mode"], "software")
            self.assertFalse(manifest["viewer_runtime_degraded"])
            self.assertGreater(inventory["control_count"], 50)
            self.assertEqual(inventory["unknown_controls"], [])

            names = {item["name"] for item in manifest["screenshots"]}
            self.assertIn("startup", names)
            self.assertIn("topbar_file_menu", names)
            self.assertIn("files_empty", names)
            self.assertIn("files_populated", names)
            self.assertIn("activity_me", names)
            self.assertIn("activity_printers", names)
            self.assertIn("prepare_default", names)
            self.assertIn("preview_main", names)
            self.assertIn("device_main", names)
            self.assertIn("control_main", names)
            self.assertIn("settings_panel", names)

            ledger_lines = [line for line in ledger_path.read_text(encoding="utf-8").splitlines() if line.strip()]
            self.assertGreater(len(ledger_lines), 20)

    def test_main_rejects_unsupported_scenarios(self):
        code = app_shell_audit.main(["--scenario", "not-real"])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()

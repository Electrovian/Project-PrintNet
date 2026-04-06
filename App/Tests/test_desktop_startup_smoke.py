import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

try:
    from testing import desktop_startup_smoke  # noqa: E402
except Exception:
    desktop_startup_smoke = None


@unittest.skipIf(desktop_startup_smoke is None, "desktop startup smoke unavailable")
class DesktopStartupSmokeTests(unittest.TestCase):
    def test_run_startup_smoke_builds_window_and_uses_isolated_runtime_root(self):
        fake_window = mock.Mock()
        fake_window.windowTitle.return_value = "EON-OpenSlicer"
        fake_window.isVisible.return_value = True
        fake_window.isMaximized.return_value = False

        fake_activity_logger = mock.Mock()
        fake_crash_reporter = mock.Mock()

        with mock.patch.object(desktop_startup_smoke.app_main, "_run_preset_startup_validation"):
            with mock.patch.object(desktop_startup_smoke.app_main, "configure_opengl_mode", return_value="software") as configure:
                with mock.patch.object(
                    desktop_startup_smoke.app_main,
                    "load_printer_config",
                    return_value=([{"name": "Alpha"}], {}),
                ):
                    with mock.patch.object(desktop_startup_smoke.app_main, "MainWindow", return_value=fake_window):
                        with mock.patch.object(
                            desktop_startup_smoke.app_main,
                            "ActivityLogger",
                            return_value=fake_activity_logger,
                        ):
                            with mock.patch.object(
                                desktop_startup_smoke.app_main,
                                "CrashReporter",
                                return_value=fake_crash_reporter,
                            ):
                                report = desktop_startup_smoke.run_startup_smoke()

        self.assertTrue(report["ok"])
        self.assertEqual(report["printer_count"], 1)
        self.assertEqual(report["window_title"], "EON-OpenSlicer")
        self.assertTrue(report["window_visible"])
        self.assertEqual(report["renderer_mode"], "software")
        self.assertFalse(report["viewer_runtime_degraded"])
        self.assertEqual(report["viewer_runtime_failure_count"], 0)
        self.assertFalse(Path(str(report["runtime_root"])).exists())
        fake_activity_logger.track_widget_tree.assert_called_once_with(fake_window)
        fake_window.showMaximized.assert_called_once()
        fake_window.close.assert_called_once()
        fake_crash_reporter.install.assert_called_once()
        fake_crash_reporter.install_faulthandler.assert_called_once()
        fake_crash_reporter.install_watchdog.assert_called_once()
        configure.assert_called_once_with()

    def test_run_startup_smoke_reports_desktop_renderer_override(self):
        fake_window = mock.Mock()
        fake_window.windowTitle.return_value = "EON-OpenSlicer"
        fake_window.isVisible.return_value = True
        fake_window.isMaximized.return_value = True

        with mock.patch.object(desktop_startup_smoke.app_main, "_run_preset_startup_validation"):
            with mock.patch.object(desktop_startup_smoke.app_main, "configure_opengl_mode", return_value="desktop"):
                with mock.patch.object(
                    desktop_startup_smoke.app_main,
                    "load_printer_config",
                    return_value=([{"name": "Alpha"}], {}),
                ):
                    with mock.patch.object(desktop_startup_smoke.app_main, "MainWindow", return_value=fake_window):
                        with mock.patch.object(desktop_startup_smoke.app_main, "ActivityLogger", return_value=mock.Mock()):
                            with mock.patch.object(desktop_startup_smoke.app_main, "CrashReporter", return_value=mock.Mock()):
                                report = desktop_startup_smoke.run_startup_smoke()

        self.assertEqual(report["renderer_mode"], "desktop")
        self.assertFalse(report["viewer_runtime_degraded"])

    def test_main_writes_success_report(self):
        payload = {
            "ok": True,
            "started_at_utc": "2026-04-05T00:00:00+00:00",
            "duration_s": 0.1,
            "printer_count": 2,
        }
        with tempfile.TemporaryDirectory() as tmp:
            report_path = Path(tmp) / "report.json"
            with mock.patch.object(desktop_startup_smoke, "run_startup_smoke", return_value=payload):
                code = desktop_startup_smoke.main(["--report", str(report_path)])
            self.assertEqual(code, 0)
            written = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(written["printer_count"], 2)
            self.assertTrue(written["ok"])

    def test_main_writes_failure_report_and_returns_nonzero(self):
        with tempfile.TemporaryDirectory() as tmp:
            report_path = Path(tmp) / "failure.json"
            with mock.patch.object(
                desktop_startup_smoke,
                "run_startup_smoke",
                side_effect=RuntimeError("boom"),
            ):
                code = desktop_startup_smoke.main(["--report", str(report_path)])
            self.assertEqual(code, 1)
            written = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertFalse(written["ok"])
            self.assertIn("RuntimeError: boom", written["error"])


if __name__ == "__main__":
    unittest.main()

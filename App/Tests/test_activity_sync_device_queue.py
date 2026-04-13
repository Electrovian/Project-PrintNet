import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from gui.Windows.controller.activity_sync import (  # noqa: E402
    _device_queue_rows_from_jobs_by_id,
    _resolve_uploaded_model_path,
)


class ActivitySyncDeviceQueueTests(unittest.TestCase):
    def test_resolve_uploaded_model_path_uses_configured_upload_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            expected = Path(tmp).joinpath("queued-part.stl").resolve()
            expected.write_text("solid part", encoding="utf-8")
            with mock.patch.dict(os.environ, {"EON_WEB_QUEUE_UPLOAD_DIR": tmp}, clear=False):
                resolved = _resolve_uploaded_model_path("../queued-part.stl")
            self.assertEqual(resolved, expected)

    def test_device_queue_rows_only_include_actionable_jobs(self):
        with tempfile.TemporaryDirectory() as tmp:
            queued_file = Path(tmp).joinpath("queued.stl")
            queued_file.write_text("solid part", encoding="utf-8")
            with mock.patch.dict(os.environ, {"EON_WEB_QUEUE_UPLOAD_DIR": tmp}, clear=False):
                rows = _device_queue_rows_from_jobs_by_id(
                    {
                        "job-2": {
                            "job_id": "job-2",
                            "model_name": "done.stl",
                            "status": "completed",
                            "requested_by": "student-2",
                            "printer_id": "printer-2",
                            "created_at_utc": "2026-01-01T00:00:02+00:00",
                            "_seq": 2,
                        },
                        "job-1": {
                            "job_id": "job-1",
                            "model_name": "queued.stl",
                            "status": "pending_printer",
                            "requested_by": "student-1",
                            "printer_id": "",
                            "created_at_utc": "2026-01-01T00:00:01+00:00",
                            "_seq": 1,
                        },
                    }
                )
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["job_id"], "job-1")
        self.assertEqual(rows[0]["job_label"], "queued.stl")
        self.assertEqual(rows[0]["printer"], "Unassigned")
        self.assertTrue(rows[0]["importable"])
        self.assertTrue(rows[0]["import_path"].endswith("queued.stl"))

    def test_device_queue_import_loads_selected_model_path(self):
        from gui.Windows.controller.activity_sync import ActivitySyncMixin

        class _StatusBar:
            def __init__(self):
                self.messages = []

            def showMessage(self, message):
                self.messages.append(str(message))

        class Harness(ActivitySyncMixin):
            def __init__(self):
                self.main = object()
                self.loaded = []
                self.modes = []
                self._status_bar = _StatusBar()

            def _add_model_from_path_async(self, path: str) -> None:
                self.loaded.append(path)

            def _activate_mode(self, mode: str) -> None:
                self.modes.append(mode)

            def statusBar(self):
                return self._status_bar

        with tempfile.TemporaryDirectory() as tmp:
            queued_file = Path(tmp).joinpath("queued.stl")
            queued_file.write_text("solid part", encoding="utf-8")
            harness = Harness()
            with mock.patch.dict(os.environ, {"EON_WEB_QUEUE_UPLOAD_DIR": tmp}, clear=False):
                harness._on_device_queue_import_requested(
                    {
                        "job_id": "job-3",
                        "model_name": "queued.stl",
                        "importable": True,
                        "import_path": str(queued_file),
                    }
                )
        self.assertEqual(harness.loaded, [str(queued_file)])
        self.assertEqual(harness.modes, ["prepare"])
        self.assertEqual(harness._status_bar.messages, ["Importing queued job: queued.stl"])


if __name__ == "__main__":
    unittest.main()

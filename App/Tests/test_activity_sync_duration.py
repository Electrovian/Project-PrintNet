import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

try:
    from gui.Windows.controller.activity_sync import _job_to_activity_entry  # noqa: E402
except Exception:
    _job_to_activity_entry = None


class ActivitySyncDurationTests(unittest.TestCase):
    @unittest.skipIf(_job_to_activity_entry is None, "activity sync module unavailable")
    def test_completed_duration_prefers_print_start_over_submit_time(self):
        job = {
            "job_id": "job-1",
            "model_name": "part.stl",
            "status": "completed",
            "profile_id": "p-default-pla",
            "printer_id": "printer-01",
            "requested_by": "student-1",
            "queue": "default",
            "created_at_utc": "2026-01-01T00:00:00+00:00",
            "print_started_at_utc": "2026-01-01T06:00:00+00:00",
            "updated_at_utc": "2026-01-01T06:10:00+00:00",
            "_seq": 10,
        }
        entry = _job_to_activity_entry(job)
        self.assertEqual(entry["duration"], "10m")

    @unittest.skipIf(_job_to_activity_entry is None, "activity sync module unavailable")
    def test_completed_duration_falls_back_to_submit_time_without_print_start(self):
        job = {
            "job_id": "job-2",
            "model_name": "legacy.stl",
            "status": "completed",
            "profile_id": "p-default-pla",
            "printer_id": "printer-01",
            "requested_by": "student-1",
            "queue": "default",
            "created_at_utc": "2026-01-01T00:00:00+00:00",
            "updated_at_utc": "2026-01-01T00:10:00+00:00",
            "_seq": 11,
        }
        entry = _job_to_activity_entry(job)
        self.assertEqual(entry["duration"], "10m")


if __name__ == "__main__":
    unittest.main()

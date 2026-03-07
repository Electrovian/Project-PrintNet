import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

try:
    from gui.Windows.controller.activity_sync import _merge_feed_items  # noqa: E402
except Exception:
    _merge_feed_items = None


class ActivitySyncDeltaTests(unittest.TestCase):
    @unittest.skipIf(_merge_feed_items is None, "activity sync module unavailable")
    def test_merge_feed_items_prefers_latest_seq(self):
        baseline = {
            "job-1": {
                "job_id": "job-1",
                "model_name": "old.stl",
                "status": "queued",
                "profile_id": "p-default-pla",
                "printer_id": "printer-01",
                "requested_by": "student-1",
                "queue": "default",
                "created_at_utc": "2026-01-01T00:00:00+00:00",
                "updated_at_utc": "2026-01-01T00:00:00+00:00",
                "_seq": 2,
            }
        }
        feed_items = [
            {
                "seq": 1,
                "job_id": "job-1",
                "status": "queued",
                "model_name": "stale.stl",
                "profile_id": "p-default-pla",
                "printer_id": "printer-01",
                "requested_by": "student-1",
                "queue": "default",
                "ts_utc": "2026-01-01T00:00:01+00:00",
            },
            {
                "seq": 3,
                "job_id": "job-1",
                "status": "running",
                "model_name": "new.stl",
                "profile_id": "p-default-pla",
                "printer_id": "printer-01",
                "requested_by": "student-1",
                "queue": "default",
                "ts_utc": "2026-01-01T00:00:02+00:00",
            },
        ]
        merged = _merge_feed_items(baseline, feed_items)
        self.assertEqual(merged["job-1"]["status"], "running")
        self.assertEqual(merged["job-1"]["model_name"], "new.stl")
        self.assertEqual(int(merged["job-1"]["_seq"]), 3)


if __name__ == "__main__":
    unittest.main()

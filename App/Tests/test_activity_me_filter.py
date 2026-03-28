import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

try:
    from gui.Windows.controller.activity_sync import ActivitySyncMixin  # noqa: E402
except Exception:
    ActivitySyncMixin = None


class ActivityMeFilterTests(unittest.TestCase):
    @unittest.skipIf(ActivitySyncMixin is None, "activity sync module unavailable")
    def test_build_me_rows_falls_back_to_all_rows_when_me_hint_missing(self):
        holder = type("Holder", (), {"_activity_me_user": ""})()
        rows = [
            {"job_id": "1", "user": "alice"},
            {"job_id": "2", "user": "bob"},
        ]
        filtered = ActivitySyncMixin._build_me_rows(holder, rows)
        self.assertEqual(filtered, rows)

    @unittest.skipIf(ActivitySyncMixin is None, "activity sync module unavailable")
    def test_build_me_rows_returns_empty_when_no_user_matches(self):
        holder = type("Holder", (), {"_activity_me_user": "mitchell"})()
        rows = [
            {"job_id": "1", "user": "alice"},
            {"job_id": "2", "user": "bob"},
        ]
        filtered = ActivitySyncMixin._build_me_rows(holder, rows)
        self.assertEqual(filtered, [])

    @unittest.skipIf(ActivitySyncMixin is None, "activity sync module unavailable")
    def test_build_me_rows_returns_only_matching_user_rows(self):
        holder = type("Holder", (), {"_activity_me_user": "mitchell"})()
        rows = [
            {"job_id": "1", "user": "alice"},
            {"job_id": "2", "user": "Mitchell"},
        ]
        filtered = ActivitySyncMixin._build_me_rows(holder, rows)
        self.assertEqual(filtered, [{"job_id": "2", "user": "Mitchell"}])


if __name__ == "__main__":
    unittest.main()

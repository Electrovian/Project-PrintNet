import os
import sys
import unittest
from unittest import mock

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

try:
    from gui.Windows.controller.activity_sync import ActivitySyncMixin  # noqa: E402
except Exception:
    ActivitySyncMixin = None


class ActivityMeFilterTests(unittest.TestCase):
    @unittest.skipIf(ActivitySyncMixin is None, "activity sync module unavailable")
    def test_resolve_activity_me_user_prefers_blank_config_over_os_username(self):
        holder = type("Holder", (), {})()
        with mock.patch.dict(os.environ, {"USERNAME": "Elect"}, clear=False):
            with mock.patch(
                "gui.Windows.controller.activity_sync._load_activity_sync_config",
                return_value={
                    "available": True,
                    "base_url": "http://127.0.0.1:8000/api/v1",
                    "service_token": "printnet-local-activity",
                    "me_user": "",
                },
            ):
                resolved = ActivitySyncMixin._resolve_activity_me_user(holder)
        self.assertEqual(resolved, "")

    @unittest.skipIf(ActivitySyncMixin is None, "activity sync module unavailable")
    def test_resolve_activity_me_user_falls_back_to_os_username_without_config(self):
        holder = type("Holder", (), {})()
        with mock.patch.dict(os.environ, {"USERNAME": "Elect"}, clear=False):
            with mock.patch(
                "gui.Windows.controller.activity_sync._load_activity_sync_config",
                return_value={"available": False, "base_url": "", "service_token": "", "me_user": ""},
            ):
                resolved = ActivitySyncMixin._resolve_activity_me_user(holder)
        self.assertEqual(resolved, "elect")

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

import os
import sys
import unittest
from datetime import datetime, timedelta

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from gui.activity_logger import _utc_timestamp as activity_utc_timestamp  # noqa: E402
from gui.crash_reporter import _utc_timestamp as crash_utc_timestamp  # noqa: E402


class TimestampHelperTests(unittest.TestCase):
    def test_activity_logger_timestamp_is_utc_and_z_suffixed(self):
        value = activity_utc_timestamp()
        self.assertTrue(value.endswith("Z"))
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        self.assertEqual(parsed.tzinfo.utcoffset(parsed), timedelta(0))

    def test_crash_reporter_timestamp_is_utc_and_z_suffixed(self):
        value = crash_utc_timestamp()
        self.assertTrue(value.endswith("Z"))
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        self.assertEqual(parsed.tzinfo.utcoffset(parsed), timedelta(0))


if __name__ == "__main__":
    unittest.main()

import os
import sys
import tempfile
import unittest
from unittest import mock

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from gui.activity_logger import ActivityLogger  # noqa: E402


def _close_logger(logger: ActivityLogger) -> None:
    handlers = list(getattr(logger, "_logger").handlers)
    for handler in handlers:
        try:
            handler.close()
        except Exception:
            pass
        try:
            logger._logger.removeHandler(handler)
        except Exception:
            pass


class ActivityLoggerStdoutTests(unittest.TestCase):
    def test_stdout_disabled_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict(os.environ, {}, clear=True):
                logger = ActivityLogger(log_dir=tmp)
            try:
                with mock.patch("builtins.print") as printed:
                    logger.log_action("clicked")
                printed.assert_not_called()
            finally:
                _close_logger(logger)

    def test_stdout_enabled_prints_action_event(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict(os.environ, {"EON_ACTIVITY_LOG_STDOUT": "1"}, clear=True):
                logger = ActivityLogger(log_dir=tmp)
            try:
                with mock.patch("builtins.print") as printed:
                    logger.log_action("clicked")
                printed.assert_called_once()
                payload = str(printed.call_args.args[0])
                self.assertIn('"event": "action"', payload)
                self.assertIn('"action": "clicked"', payload)
            finally:
                _close_logger(logger)

    def test_stdout_event_filter_blocks_non_matching_events(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict(
                os.environ,
                {
                    "EON_ACTIVITY_LOG_STDOUT": "1",
                    "EON_ACTIVITY_LOG_STDOUT_EVENTS": "mouse_press",
                },
                clear=True,
            ):
                logger = ActivityLogger(log_dir=tmp)
            try:
                with mock.patch("builtins.print") as printed:
                    logger.log_action("clicked")
                printed.assert_not_called()
            finally:
                _close_logger(logger)

    def test_stdout_event_filter_allows_all_keyword(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict(
                os.environ,
                {
                    "EON_ACTIVITY_LOG_STDOUT": "1",
                    "EON_ACTIVITY_LOG_STDOUT_EVENTS": "all",
                },
                clear=True,
            ):
                logger = ActivityLogger(log_dir=tmp)
            try:
                with mock.patch("builtins.print") as printed:
                    logger.log_action("clicked")
                printed.assert_called_once()
            finally:
                _close_logger(logger)


if __name__ == "__main__":
    unittest.main()

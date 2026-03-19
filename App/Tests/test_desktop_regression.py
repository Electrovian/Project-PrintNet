import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from testing.desktop_regression import (  # noqa: E402
    CommandExecutionResult,
    DesktopRegressionError,
    RegressionCase,
    RegressionRunConfig,
    default_desktop_regression_cases,
    report_metadata,
    run_regression_cases,
    summarize_failures,
)


def _executor_success(_command, _timeout_s, _working_directory):
    return CommandExecutionResult(exit_code=0, stdout="ok", stderr="", timed_out=False)


def _executor_failure(_command, _timeout_s, _working_directory):
    return CommandExecutionResult(exit_code=1, stdout="", stderr="failed", timed_out=False)


def _executor_timeout(_command, _timeout_s, _working_directory):
    return CommandExecutionResult(exit_code=124, stdout="", stderr="timeout", timed_out=True)


class DesktopRegressionTests(unittest.TestCase):
    def test_default_cases_have_unique_ids(self):
        cases = default_desktop_regression_cases()
        ids = [case.case_id for case in cases]
        self.assertEqual(len(cases), len(set(ids)))
        self.assertGreaterEqual(len(cases), 4)

    def test_run_regression_cases_success(self):
        cases = (
            RegressionCase(case_id="one", modules=("App.Tests.test_desktop_plate_flow",), max_seconds=5.0),
            RegressionCase(case_id="two", modules=("App.Tests.test_runtime_printer_state",), max_seconds=5.0),
        )
        report = run_regression_cases(cases, executor=_executor_success)
        self.assertTrue(report.ok)
        self.assertEqual(report.case_count, 2)
        self.assertEqual(report.failed_case_count, 0)
        self.assertEqual(len(summarize_failures(report)), 0)

    def test_run_regression_cases_failure_stop_on_failure(self):
        cases = (
            RegressionCase(case_id="fail", modules=("App.Tests.test_desktop_plate_flow",), max_seconds=5.0),
            RegressionCase(case_id="next", modules=("App.Tests.test_runtime_printer_state",), max_seconds=5.0),
        )
        report = run_regression_cases(
            cases,
            config=RegressionRunConfig(stop_on_failure=True),
            executor=_executor_failure,
        )
        self.assertFalse(report.ok)
        self.assertEqual(report.case_count, 1)
        self.assertEqual(report.failed_case_ids, ("fail",))

    def test_run_regression_cases_marks_timeout_failure(self):
        cases = (RegressionCase(case_id="timeout", modules=("App.Tests.test_desktop_plate_flow",), max_seconds=5.0),)
        report = run_regression_cases(cases, executor=_executor_timeout)
        self.assertFalse(report.ok)
        self.assertEqual(report.failed_case_count, 1)
        self.assertTrue(report.results[0].timed_out)

    def test_invalid_case_raises(self):
        with self.assertRaises(DesktopRegressionError):
            run_regression_cases((RegressionCase(case_id="", modules=("App.Tests.test_desktop_plate_flow",), max_seconds=5.0),))

    def test_report_metadata_shape(self):
        cases = (RegressionCase(case_id="one", modules=("App.Tests.test_desktop_plate_flow",), max_seconds=5.0),)
        report = run_regression_cases(cases, executor=_executor_success)
        metadata = report_metadata(report)
        self.assertTrue(metadata["ok"])
        self.assertEqual(metadata["case_count"], 1)
        self.assertEqual(metadata["failed_case_count"], 0)


if __name__ == "__main__":
    unittest.main()

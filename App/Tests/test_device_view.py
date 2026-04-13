import unittest

from qt_harness import QtTestCase


class DeviceViewTests(QtTestCase):

    def test_live_status_formatting(self):
        from gui.Windows.device import DeviceView

        view = DeviceView()
        view.update_live_status(
            head_pos=(1.2345, 2.3456, 3.4567),
            time_left_s=3661,
            pla_remaining_m=1.234,
            pla_low=True,
        )

        self.assertEqual(view._head_pos_value.text(), "X: 1.23  Y: 2.35  Z: 3.46")
        self.assertEqual(view._time_left_value.text(), "1h01m")
        self.assertEqual(view._pla_status_value.text(), "LOW (1.23 m left)")

    def test_live_status_empty(self):
        from gui.Windows.device import DeviceView

        view = DeviceView()
        view.update_live_status()

        self.assertEqual(view._head_pos_value.text(), "n/a")
        self.assertEqual(view._time_left_value.text(), "n/a")
        self.assertEqual(view._pla_status_value.text(), "n/a")

    def test_queue_jobs_populate_and_emit_import(self):
        from gui.Windows.device import DeviceView

        view = DeviceView()
        received = []
        view.queue_job_import_requested.connect(lambda payload: received.append(dict(payload)))
        view.set_queue_jobs(
            [
                {
                    "job_id": "job-1",
                    "job_label": "widget.stl",
                    "status": "pending_printer",
                    "user": "student-1",
                    "printer": "Unassigned",
                    "importable": True,
                    "import_hint": "ready",
                }
            ]
        )

        self.assertEqual(view._queue_table.rowCount(), 1)
        self.assertTrue(view._queue_placeholder.isHidden())
        self.assertTrue(view._queue_import_btn.isEnabled())

        view._emit_queue_import()
        self.assertEqual(received, [{"job_id": "job-1", "job_label": "widget.stl", "status": "pending_printer", "user": "student-1", "printer": "Unassigned", "importable": True, "import_hint": "ready"}])

    def test_queue_jobs_disable_import_when_model_unavailable(self):
        from gui.Windows.device import DeviceView

        view = DeviceView()
        view.set_queue_jobs(
            [
                {
                    "job_id": "job-2",
                    "job_label": "missing.stl",
                    "status": "pending_printer",
                    "user": "student-2",
                    "printer": "Unassigned",
                    "importable": False,
                    "import_hint": "missing",
                }
            ]
        )

        self.assertEqual(view._queue_table.rowCount(), 1)
        self.assertFalse(view._queue_import_btn.isEnabled())
        self.assertEqual(view._queue_import_btn.toolTip(), "missing")


if __name__ == "__main__":
    unittest.main()

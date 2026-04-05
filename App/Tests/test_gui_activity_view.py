import os
import sys
import unittest

from qt_harness import QtTestCase, QtWidgets

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


class ActivityViewGuiTests(QtTestCase):
    def test_activity_view_populates_stats_filters_and_restore_state(self):
        from gui.Windows.activity import ActivityView

        view = ActivityView()
        me_entries = [
            {
                "job": "Widget A",
                "status": "completed",
                "duration": "01:20",
                "material": "PLA",
                "when": "2026-04-05T10:00:00+00:00",
                "user": "Alice",
                "printer": "A1",
            },
            {
                "job": "Widget B",
                "status": "printing",
                "duration": "00:25",
                "material": "PETG",
                "when": "2026-04-05T12:00:00+00:00",
                "user": "Alice",
                "printer": "A2",
            },
        ]
        printer_entries = [
            {
                "job": "Rack",
                "status": "queued",
                "duration": "00:00",
                "material": "PLA",
                "when": "2026-04-04T12:00:00+00:00",
                "user": "Bob",
                "printer": "B1",
            }
        ]
        view.set_me_activity(me_entries)
        view.set_printer_activity(printer_entries)
        view.set_compliance_banner("Cloud activity is restricted.")
        view.set_cache_banner("Showing cached history.")

        self.assertEqual(view._me_table.rowCount(), 2)
        self.assertEqual(view._stats_values["jobs"].text(), "2")
        self.assertEqual(view._stats_values["printing"].text(), "1")
        self.assertFalse(view._compliance_banner.isHidden())
        self.assertFalse(view._cache_banner.isHidden())

        view._search_input.setText("widget b")
        QtWidgets.QApplication.processEvents()
        self.assertEqual(view._me_table.rowCount(), 1)

        view._printers_btn.click()
        QtWidgets.QApplication.processEvents()
        self.assertIs(view._stack.currentWidget(), view._printer_table)
        self.assertEqual(view._printer_table.rowCount(), 0)

        view.restore_view_state({"tab": "me", "date_filter_index": 0, "search_query": ""})
        QtWidgets.QApplication.processEvents()
        self.assertIs(view._stack.currentWidget(), view._me_table)
        self.assertEqual(view._me_table.rowCount(), 2)


if __name__ == "__main__":
    unittest.main()

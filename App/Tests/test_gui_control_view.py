import os
import sys
import unittest

from qt_harness import QtTestCase, QtWidgets

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


class _RuntimeState:
    def __init__(self, name="Alpha"):
        self.name = name


class _ControlParent(QtWidgets.QWidget):
    def __init__(self, name="Alpha"):
        super().__init__()
        self.runtime_printer_state = _RuntimeState(name)


class ControlViewGuiTests(QtTestCase):
    def test_control_view_updates_details_and_emits_selection(self):
        from gui.Windows.control import ControlView

        parent = _ControlParent(name="Alpha")
        view = ControlView(parent)
        self.addCleanup(parent.close)
        events = []
        view.printer_changed.connect(lambda printer: events.append(dict(printer)))
        printers = [
            {
                "name": "Alpha",
                "connector_type": "octoprint",
                "octoprint_url": "http://alpha.local",
                "bed_x": 256,
                "bed_y": 256,
                "bed_z": 256,
            },
            {
                "name": "Beta",
                "connector_type": "moonraker",
                "bed_x": 300,
                "bed_y": 300,
                "bed_z": 340,
            },
        ]

        view.set_printers(printers)
        view.select_printer_by_name("Beta")

        self.assertEqual(view._printer_combo.currentText(), "Beta")
        self.assertEqual(view.current_printer().get("name"), "Beta")
        self.assertIn("connector", view._printer_details.text().lower())
        self.assertTrue(view._jog_mode_btn.isChecked())
        self.assertFalse(view._telemetry_nozzle.text() == "")
        self.assertEqual(events[-1]["name"], "Beta")

    def test_control_view_handles_empty_state(self):
        from gui.Windows.control import ControlView

        parent = _ControlParent()
        view = ControlView(parent)
        self.addCleanup(parent.close)
        view.set_printers([])

        self.assertFalse(view._printer_combo.isEnabled())
        self.assertIn("no printer", view._printer_details.text().lower())


if __name__ == "__main__":
    unittest.main()

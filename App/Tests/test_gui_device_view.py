import os
import sys
import unittest

from qt_harness import QtTestCase, QtWidgets

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


class _RuntimeState:
    def __init__(self, name="Beta"):
        self.name = name


class _DeviceParent(QtWidgets.QWidget):
    def __init__(self, name="Beta"):
        super().__init__()
        self.runtime_printer_state = _RuntimeState(name)


class DeviceViewGuiTests(QtTestCase):
    def test_device_view_empty_and_populated_states(self):
        from gui.Windows.device import DeviceView

        parent = _DeviceParent()
        view = DeviceView(parent)
        self.addCleanup(parent.close)
        view.set_printers([])

        self.assertFalse(view._printer_combo.isEnabled())
        self.assertFalse(view._send_btn.isEnabled())
        self.assertIn("no printer", view._printer_details.text().lower())

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
                "connector_type": "bambu_lan",
                "bed_x": 256,
                "bed_y": 256,
                "bed_z": 256,
            },
        ]
        view.set_printers(printers)

        self.assertTrue(view._printer_combo.isEnabled())
        self.assertEqual(view._printer_combo.currentText(), "Beta")
        self.assertTrue(view._send_btn.isEnabled())
        self.assertEqual(len(view.findChildren(QtWidgets.QLabel, "DevicePrinterName")), 2)

    def test_device_view_emits_send_and_diagnostics_for_selected_printer(self):
        from gui.Windows.device import DeviceView

        parent = _DeviceParent(name="Alpha")
        view = DeviceView(parent)
        self.addCleanup(parent.close)
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
                "moonraker_url": "http://beta.local",
                "bed_x": 300,
                "bed_y": 300,
                "bed_z": 340,
            },
        ]
        sent = []
        diagnostics = []
        view.send_requested.connect(lambda printer: sent.append(dict(printer)))
        view.diagnostics_requested.connect(lambda printer: diagnostics.append(dict(printer)))
        view.set_printers(printers)
        view.select_printer_by_name("Beta")

        view._send_btn.click()
        view._diagnostics_btn.click()

        self.assertEqual(sent[-1]["name"], "Beta")
        self.assertEqual(diagnostics[-1]["name"], "Beta")
        self.assertIn("http://beta.local", view._printer_details.text())


if __name__ == "__main__":
    unittest.main()

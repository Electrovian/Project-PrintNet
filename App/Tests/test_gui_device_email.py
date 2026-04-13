import os
import sys
import unittest
from unittest import mock

from qt_harness import QtCore, QtTestCase, QtWidgets

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


class _FakeController(QtCore.QObject):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main = main_window
        self.email_calls = 0

    def _on_device_send_requested(self, *_args):
        return None

    def _on_device_save_requested(self, *_args):
        return None

    def _on_device_email_requested(self, *_args):
        self.email_calls += 1

    def open_stl_dialog(self):
        return None

    def initialize(self):
        return None


class _FakePrepareView:
    def __init__(self, main_window):
        self.main = main_window
        self.viewer = QtWidgets.QWidget(main_window)


class _FakePreviewView(QtCore.QObject):
    printer_changed = QtCore.pyqtSignal(object)

    def __init__(self, main_window, viewer):
        super().__init__(main_window)
        self.main = main_window
        self.viewer = viewer


class _FakeDeviceView(QtWidgets.QWidget):
    send_requested = QtCore.pyqtSignal(object)
    save_requested = QtCore.pyqtSignal()
    email_requested = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def set_printers(self, _printers):
        return None


class _FakeControlView(QtWidgets.QWidget):
    printer_changed = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

    def set_printers(self, _printers):
        return None


class _FakeFilesView(QtWidgets.QWidget):
    add_files_requested = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)


class _FakeActivityView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


class _FakeSharedView:
    def __init__(self, main_window):
        self.main = main_window

    def build_menubar(self):
        return None

    def build_topbar(self):
        return None

    def build_shortcut_actions(self):
        return None


class _FakePrinterManager:
    def __init__(self, printers, airtable_cfg):
        self.printers = list(printers or [])
        self.airtable_cfg = dict(airtable_cfg or {})


class _DeviceViewStub:
    def __init__(self, printer):
        self._printer = dict(printer or {})

    def current_printer(self):
        return dict(self._printer)


class _ViewerStub:
    def get_current_plate_name(self):
        return "Plate 1"

    def get_model_ids(self):
        return []


class _FakeEmailDialog:
    accepted_payload = {
        "recipient": "ops@example.com",
        "subject": "Print job handoff",
        "note": "Watch the first layer.",
    }

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def exec_(self):
        return QtWidgets.QDialog.Accepted

    def payload(self):
        return dict(type(self).accepted_payload)


class _HarnessStatusBar:
    def __init__(self):
        self.messages = []

    def showMessage(self, message):
        self.messages.append(str(message))


class _PrintControllerHarness:
    def __init__(self):
        self.main = QtWidgets.QWidget()
        self.viewer = _ViewerStub()
        self.device_view = _DeviceViewStub(
            {
                "name": "Alpha",
                "connector_type": "octoprint",
                "octoprint_url": "http://alpha.local",
            }
        )
        self._ui_settings = QtCore.QSettings("EON", "OpenSlicer")
        self._ui_settings.clear()
        self.current_model_id = None
        self._current_project_path = os.path.join(ROOT, "demo-project.3mf")
        self._last_gcode_path = os.path.join(ROOT, "demo-output.gcode")
        self.runtime_printer_state = type("RuntimeState", (), {"name": "Alpha"})()
        self._status_bar = _HarnessStatusBar()

    def statusBar(self):
        return self._status_bar


class DeviceEmailGuiTests(QtTestCase):
    def setUp(self):
        settings = QtCore.QSettings("EON", "OpenSlicer")
        settings.clear()
        settings.sync()

    def test_main_window_wires_device_email_signal(self):
        from gui.main_window import MainWindow

        with mock.patch("gui.main_window.MainController", _FakeController), \
             mock.patch("gui.main_window.PrepareView", _FakePrepareView), \
             mock.patch("gui.main_window.PreviewView", _FakePreviewView), \
             mock.patch("gui.main_window.DeviceView", _FakeDeviceView), \
             mock.patch("gui.main_window.ControlView", _FakeControlView), \
             mock.patch("gui.main_window.FilesView", _FakeFilesView), \
             mock.patch("gui.main_window.ActivityView", _FakeActivityView), \
             mock.patch("gui.main_window.SharedView", _FakeSharedView), \
             mock.patch("gui.main_window.PrinterManager", _FakePrinterManager):
            window = MainWindow([], {})
            self.addCleanup(window.close)
            self.assertGreater(int(window.device_view.receivers(window.device_view.email_requested)), 0)

    def test_device_email_uses_smtp_when_available(self):
        from gui.Windows.controller.print import PrintMixin

        class Harness(_PrintControllerHarness, PrintMixin):
            pass

        harness = Harness()
        with mock.patch("gui.Windows.controller.print.EmailComposeDialog", _FakeEmailDialog), \
             mock.patch("gui.Windows.controller.print.send_email_via_smtp", return_value={"sender": "no-reply@example.com"}) as send_mock, \
             mock.patch("gui.Windows.controller.print.QtWidgets.QMessageBox.information") as info_mock, \
             mock.patch("gui.Windows.controller.print.QtGui.QDesktopServices.openUrl", return_value=True) as open_url_mock:
            harness._on_device_email_requested()

        send_mock.assert_called_once()
        info_mock.assert_called_once()
        open_url_mock.assert_not_called()
        self.assertEqual(harness._ui_settings.value("email/last_recipient"), "ops@example.com")

    def test_device_email_falls_back_to_mailto_when_smtp_fails(self):
        from gui.Windows.controller.print import PrintMixin
        from integrations.email_delivery import EmailConfigurationError

        class Harness(_PrintControllerHarness, PrintMixin):
            pass

        harness = Harness()
        with mock.patch("gui.Windows.controller.print.EmailComposeDialog", _FakeEmailDialog), \
             mock.patch(
                 "gui.Windows.controller.print.send_email_via_smtp",
                 side_effect=EmailConfigurationError("SMTP is not configured."),
             ), \
             mock.patch(
                 "gui.Windows.controller.print.QtWidgets.QMessageBox.question",
                 return_value=QtWidgets.QMessageBox.Yes,
             ), \
             mock.patch("gui.Windows.controller.print.QtGui.QDesktopServices.openUrl", return_value=True) as open_url_mock:
            harness._on_device_email_requested()

        open_url_mock.assert_called_once()
        qurl = open_url_mock.call_args[0][0]
        self.assertIn("mailto:ops%40example.com", qurl.toString())


if __name__ == "__main__":
    unittest.main()

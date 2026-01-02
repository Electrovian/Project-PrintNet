# gui/main_window.py
import os

from PyQt5 import QtWidgets, QtGui, QtCore

from .Windows.prepare import PrepareView
from .Windows.preview import PreviewView
from .Windows.device import DeviceView
from .Windows.shared_view import SharedView
from .Windows.controller import MainController
from config.defaults import DEFAULTS

from integrations.printer_manager import PrinterManager

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, printers, airtable_cfg, parent=None):
        super().__init__(parent)
        self.setWindowTitle(DEFAULTS["app"]["title"])
        size = DEFAULTS["app"]["size"]
        self.resize(size[0], size[1])
        self.setAcceptDrops(True)

        icon_path = os.path.join(ASSETS_DIR, "icons", "app_icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QtGui.QIcon(icon_path))

        self.printers = printers
        self.airtable_cfg = airtable_cfg
        self.printer_manager = PrinterManager(printers=self.printers, airtable_cfg=self.airtable_cfg)

        self.pool = QtCore.QThreadPool.globalInstance()
        max_threads = max(1, (os.cpu_count() or 2) - 1)
        self.pool.setMaxThreadCount(max_threads)
        self._build_ui()

    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        self.controller = MainController(self)

        self.prepare_view = PrepareView(self)
        self.viewer = self.prepare_view.viewer

        self._central_stack = QtWidgets.QStackedWidget(self)
        self._central_stack.addWidget(self.viewer)

        self.device_view = DeviceView(self)
        self.device_view.set_printers(self.printers)
        self._central_stack.addWidget(self.device_view)

        self.setCentralWidget(self._central_stack)

        self.preview_view = PreviewView(self, self.viewer)

        self.shared_view = SharedView(self)
        self.shared_view.build_menubar()
        self.shared_view.build_topbar()
        self.shared_view.build_shortcut_actions()
        self.device_view.send_requested.connect(self.controller._on_device_send_requested)
        self.device_view.save_requested.connect(self.controller._on_device_save_requested)
        self.controller.initialize()


    def __getattr__(self, name):
        controller = self.__dict__.get("controller")
        if controller is not None and hasattr(controller, name):
            return getattr(controller, name)
        raise AttributeError(f"{type(self).__name__} has no attribute {name!r}")

    def dragEnterEvent(self, a0: QtGui.QDragEnterEvent):
        if hasattr(self, "controller"):
            return self.controller.dragEnterEvent(a0)
        return super().dragEnterEvent(a0)

    def dropEvent(self, a0: QtGui.QDropEvent):
        if hasattr(self, "controller"):
            return self.controller.dropEvent(a0)
        return super().dropEvent(a0)

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        super().resizeEvent(a0)
        if hasattr(self, "controller"):
            self.controller.resizeEvent(a0)

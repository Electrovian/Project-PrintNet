# gui/main_window.py
import os
from typing import Optional, TYPE_CHECKING

from PyQt5 import QtWidgets, QtGui, QtCore

from .Windows.prepare import PrepareView
from .Windows.preview import PreviewView
from .Windows.device import DeviceView
from .Windows.control import ControlView
from .Windows.files import FilesView
from .Windows.activity import ActivityView
from .Windows.shared_view import SharedView
from .Windows.controller import MainController
from config.defaults import DEFAULTS
from config.performance import resolve_performance_limits

from integrations.printer_manager import PrinterManager

if TYPE_CHECKING:
    from .activity_logger import ActivityLogger
    from .crash_reporter import CrashReporter

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
        self.activity_logger: Optional["ActivityLogger"] = None
        self.crash_reporter: Optional["CrashReporter"] = None

        self.pool = QtCore.QThreadPool.globalInstance()
        limits = resolve_performance_limits(DEFAULTS.get("performance"))
        self.performance_limits = limits
        self.pool.setMaxThreadCount(int(limits.get("max_threads", 1)))
        self._build_ui()
        self._apply_windows_titlebar_theme()

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

        self.control_view = ControlView(self)
        self.control_view.set_printers(self.printers)
        self._central_stack.addWidget(self.control_view)

        self.files_view = FilesView(self)
        self._central_stack.addWidget(self.files_view)

        self.activity_view = ActivityView(self)
        self._central_stack.addWidget(self.activity_view)

        self.setCentralWidget(self._central_stack)

        self.preview_view = PreviewView(self, self.viewer)

        self.shared_view = SharedView(self)
        self.shared_view.build_menubar()
        self.shared_view.build_topbar()
        self.shared_view.build_shortcut_actions()
        self.device_view.send_requested.connect(self.controller._on_device_send_requested)
        self.device_view.save_requested.connect(self.controller._on_device_save_requested)
        self.files_view.add_files_requested.connect(self.open_stl_dialog)
        self.controller.initialize()


    def __getattr__(self, name):
        controller = self.__dict__.get("controller")
        if controller is not None:
            if name in controller.__dict__:
                return controller.__dict__[name]
            if getattr(type(controller), name, None) is not None:
                return object.__getattribute__(controller, name)
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

    def apply_titlebar_theme(self):
        self._apply_windows_titlebar_theme()

    def _apply_windows_titlebar_theme(self):
        if os.name != "nt":
            return
        try:
            import ctypes
        except Exception:
            return
        try:
            hwnd = int(self.winId())
        except Exception:
            return
        value = ctypes.c_int(1)
        dwmapi = ctypes.windll.dwmapi
        for attr in (20, 19):
            try:
                dwmapi.DwmSetWindowAttribute(
                    hwnd,
                    attr,
                    ctypes.byref(value),
                    ctypes.sizeof(value),
                )
                break
            except Exception:
                continue

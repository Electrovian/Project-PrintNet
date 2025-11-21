import os
from pathlib import Path

from PyQt5 import QtWidgets, QtGui, QtCore

from .viewer_3d import Viewer3D
from .settings_panel import SettingsPanel
from .job_queue_panel import JobQueuePanel
from .controls import TransformToolbar

from slicer.slicer import slice_file
from slicer.gcode import SliceSettings

from integrations.printer_manager import PrinterManager

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, printers, airtable_cfg, parent=None):
        super().__init__(parent)
        self.setWindowTitle("OpenSlicer")
        self.resize(1280, 720)
        self.setAcceptDrops(True)

        icon_path = os.path.join(ASSETS_DIR, "icons", "app_icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QtGui.QIcon(icon_path))

        self.current_stl_path = None
        self.printers = printers
        self.airtable_cfg = airtable_cfg

        self.printer_manager = PrinterManager(printers=self.printers,
                                              airtable_cfg=self.airtable_cfg)

        self._build_ui()

    # UI ------------------------------------------------------------------
    def _build_ui(self):
        self.viewer = Viewer3D(self)

        self.settings_panel = SettingsPanel(self)
        settings_dock = QtWidgets.QDockWidget("Settings", self)
        settings_dock.setWidget(self.settings_panel)
        settings_dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea |
                                      QtCore.Qt.RightDockWidgetArea)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, settings_dock)

        self.job_queue_panel = JobQueuePanel(self)
        job_dock = QtWidgets.QDockWidget("Job Queue", self)
        job_dock.setWidget(self.job_queue_panel)
        job_dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea |
                                 QtCore.Qt.RightDockWidgetArea)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, job_dock)

        self.setCentralWidget(self.viewer)

        self._build_menubar()
        self._build_toolbar()

        # Connect job queue button
        self.job_queue_panel.add_btn.clicked.connect(self._add_current_model_to_queue)

        self.statusBar().showMessage("Ready")

    def _build_menubar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("&File")
        open_action = QtWidgets.QAction("Open STL...", self)
        open_action.triggered.connect(self.open_stl_dialog)
        file_menu.addAction(open_action)

        exit_action = QtWidgets.QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def _build_toolbar(self):
        tb = self.addToolBar("Main")
        tb.setMovable(False)

        self.open_action = QtWidgets.QAction("Open", self)
        self.open_action.triggered.connect(self.open_stl_dialog)
        tb.addAction(self.open_action)

        self.slice_action = QtWidgets.QAction("Slice", self)
        self.slice_action.triggered.connect(self.slice_current_model)
        tb.addAction(self.slice_action)

        self.print_action = QtWidgets.QAction("Send to Printer", self)
        self.print_action.triggered.connect(self.print_current_model)
        tb.addAction(self.print_action)

        tb.addSeparator()

        self.transform_toolbar = TransformToolbar(self)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.transform_toolbar)
        self.transform_toolbar.lay_flat_action.triggered.connect(self._lay_flat)
        self.transform_toolbar.center_action.triggered.connect(self._center_model)
        self.transform_toolbar.reset_action.triggered.connect(self._reset_view)

    # Drag & drop ---------------------------------------------------------
    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.toLocalFile().lower().endswith(".stl"):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event: QtGui.QDropEvent):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path.lower().endswith(".stl"):
                self.load_stl(path)
                break

    # Actions -------------------------------------------------------------
    def open_stl_dialog(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open STL", "", "STL files (*.stl)")
        if path:
            self.load_stl(path)

    def load_stl(self, path: str):
        self.current_stl_path = path
        self.viewer.load_stl(path)
        name = os.path.basename(path)
        self.statusBar().showMessage(f"Loaded {name}")

    def slice_current_model(self):
        if not self.current_stl_path:
            QtWidgets.QMessageBox.warning(
                self, "No model", "Load an STL file first.")
            return
        settings = self.settings_panel.to_settings()
        self.statusBar().showMessage("Slicing...")
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        try:
            gcode_path = slice_file(self.current_stl_path,
                                    settings=settings)
        except Exception as exc:
            QtWidgets.QApplication.restoreOverrideCursor()
            QtWidgets.QMessageBox.critical(
                self, "Slicing error", str(exc))
            self.statusBar().showMessage("Slicing failed")
            return
        QtWidgets.QApplication.restoreOverrideCursor()
        self.statusBar().showMessage(f"Sliced to {gcode_path}")
        QtWidgets.QMessageBox.information(
            self, "Slicing complete", f"G-code written to:\n{gcode_path}")

    def print_current_model(self):
        if not self.current_stl_path:
            QtWidgets.QMessageBox.warning(
                self, "No model", "Load and slice a model first.")
            return
        settings = self.settings_panel.to_settings()
        self.statusBar().showMessage("Slicing & sending to printer...")
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        try:
            result = self.printer_manager.slice_and_print(self.current_stl_path,
                                                          settings=settings)
        except Exception as exc:
            QtWidgets.QApplication.restoreOverrideCursor()
            QtWidgets.QMessageBox.critical(
                self, "Print error", str(exc))
            self.statusBar().showMessage("Print failed")
            return
        QtWidgets.QApplication.restoreOverrideCursor()
        self.statusBar().showMessage(result)
        QtWidgets.QMessageBox.information(self, "Print", result)

    def _add_current_model_to_queue(self):
        if not self.current_stl_path:
            QtWidgets.QMessageBox.warning(
                self, "No model", "Load a model before adding to queue.")
            return
        desc = f"Local: {os.path.basename(self.current_stl_path)}"
        payload = {"stl_path": self.current_stl_path}
        self.job_queue_panel.add_job(desc, payload)

    # Transform stubs -----------------------------------------------------
    def _lay_flat(self):
        QtWidgets.QMessageBox.information(
            self, "Lay Flat",
            "Lay Flat is not implemented yet; extend viewer/mesh to add it.")

    def _center_model(self):
        QtWidgets.QMessageBox.information(
            self, "Center",
            "Center model is not implemented yet; you can implement transforms in viewer_3d.")

    def _reset_view(self):
        self.viewer.opts['distance'] = 300
        self.viewer.opts['elevation'] = 30
        self.viewer.opts['azimuth'] = -45
        self.viewer.update()

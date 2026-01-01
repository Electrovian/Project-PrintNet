# gui/main_window.py
import os
import numpy as np
import trimesh

from PyQt5 import QtWidgets, QtGui, QtCore

from .viewer_3d import Viewer3D
from .settings_panel import SettingsPanel
from .job_queue_panel import JobQueuePanel
from .controls import TransformToolbar
from .model_panel import ModelPanel
from .transform_panel import TransformPanel
from .workers import Worker

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

        self.current_model_id = None
        self.printers = printers
        self.airtable_cfg = airtable_cfg
        self.printer_manager = PrinterManager(printers=self.printers, airtable_cfg=self.airtable_cfg)

        self.pool = QtCore.QThreadPool.globalInstance()
        self._build_ui()

    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        self.viewer = Viewer3D(self)

        # Settings dock (right)
        self.settings_panel = SettingsPanel(self)
        settings_dock = QtWidgets.QDockWidget("Settings", self)
        settings_dock.setWidget(self.settings_panel)
        settings_dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, settings_dock)

        # Models dock (left)
        self.model_panel = ModelPanel(self)
        model_dock = QtWidgets.QDockWidget("Models", self)
        model_dock.setWidget(self.model_panel)
        model_dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, model_dock)

        # Transform dock (left)
        self.transform_panel = TransformPanel(self)
        transform_dock = QtWidgets.QDockWidget("Transform", self)
        transform_dock.setWidget(self.transform_panel)
        transform_dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, transform_dock)

        # Job queue dock (right)
        self.job_queue_panel = JobQueuePanel(self)
        job_dock = QtWidgets.QDockWidget("Job Queue", self)
        job_dock.setWidget(self.job_queue_panel)
        job_dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, job_dock)

        self.setCentralWidget(self.viewer)

        self._build_menubar()
        self._build_toolbar()

        # Connect signals (panels)
        self.model_panel.model_selected.connect(self._on_model_selected)
        self.model_panel.request_remove.connect(self._on_model_remove)

        # TransformPanel: live position + apply scale + snap
        self.transform_panel.scale_applied.connect(self._on_apply_scale)
        self.transform_panel.position_changed.connect(self._on_position_changed)
        self.transform_panel.snap_changed.connect(self._on_snap_changed)

        self.job_queue_panel.add_btn.clicked.connect(self._add_current_model_to_queue)

        # Viewer3D: pick + drag move
        self.viewer.modelPicked.connect(self._on_viewer_model_picked)
        self.viewer.modelMoved.connect(self._on_viewer_model_moved)

        # Initialize snap settings into viewer
        snap_enabled, snap_step = self.transform_panel.get_snap()
        self.viewer.set_snap(snap_enabled, snap_step)

        self.statusBar().showMessage("Ready")

    def _build_menubar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("&File")

        open_action = QtWidgets.QAction("Open STL(s)...", self)
        open_action.triggered.connect(self.open_stl_dialog)
        file_menu.addAction(open_action)

        clear_action = QtWidgets.QAction("Clear All Models", self)
        clear_action.triggered.connect(self._clear_all_models)
        file_menu.addAction(clear_action)

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

    # -------------------------------------------------------- drag & drop
    def dragEnterEvent(self, a0: QtGui.QDragEnterEvent):
        event = a0
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.toLocalFile().lower().endswith(".stl"):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, a0: QtGui.QDropEvent):
        event = a0
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path.lower().endswith(".stl"):
                self._add_model_from_path_async(path)

    # -------------------------------------------------------------- open
    def open_stl_dialog(self):
        paths, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Open STL files", "", "STL files (*.stl)"
        )
        for path in paths:
            self._add_model_from_path_async(path)

    # -------------------------------------------------- Model selection/removal
    def _on_model_selected(self, model_id: int):
        self.current_model_id = model_id
        self.viewer.set_selected_model(model_id)

        name = self.viewer.get_model_name(model_id) or "Model"
        self.statusBar().showMessage(f"Selected {name}")

        # Sync transform panel with model's current offset if known
        m = self.viewer.models.get(model_id)
        if m is not None:
            self.transform_panel.set_position(float(m["offset"][0]), float(m["offset"][1]))

    def _on_model_remove(self, model_id: int):
        self.viewer.remove_model(model_id)
        self.model_panel.remove_model(model_id)

        if self.current_model_id == model_id:
            remaining = self.viewer.get_model_ids()
            self.current_model_id = remaining[0] if remaining else None
            self.viewer.set_selected_model(self.current_model_id)

        self.statusBar().showMessage("Model removed")

    def _clear_all_models(self):
        self.viewer.clear_all_models()
        self.model_panel.list_widget.clear()
        self.current_model_id = None
        self.viewer.set_selected_model(None)
        self.statusBar().showMessage("Cleared all models")

    # ------------------------------------------------------------ transforms (panel -> viewer)
    def _on_apply_scale(self, scale_factor: float):
        if self.current_model_id is None:
            QtWidgets.QMessageBox.warning(self, "No model selected", "Select a model in the Models panel first.")
            return
        x = float(self.transform_panel.pos_x_spin.value())
        y = float(self.transform_panel.pos_y_spin.value())
        self.viewer.set_model_transform(self.current_model_id, scale=scale_factor, offset_xy=(x, y))
        self.statusBar().showMessage(f"Scale applied: {scale_factor:.3f}")

    def _on_position_changed(self, x: float, y: float):
        # live position (typing/spinbox) -> updates viewer immediately
        if self.current_model_id is None:
            return
        scale_factor = float(self.transform_panel.scale_spin.value()) / 100.0
        self.viewer.set_model_transform(self.current_model_id, scale=scale_factor, offset_xy=(x, y))

    def _on_snap_changed(self, enabled: bool, step_mm: float):
        self.viewer.set_snap(enabled, step_mm)

    def _center_model(self):
        if self.current_model_id is None:
            return
        self.transform_panel.set_position(0.0, 0.0)
        scale_factor = float(self.transform_panel.scale_spin.value()) / 100.0
        self.viewer.set_model_transform(self.current_model_id, scale=scale_factor, offset_xy=(0.0, 0.0))

    def _lay_flat(self):
        QtWidgets.QMessageBox.information(self, "Lay Flat", "Not implemented yet (orientation work comes next).")

    def _reset_view(self):
        self.viewer.opts["distance"] = 300.0 # pyright: ignore[reportArgumentType]
        self.viewer.opts["elevation"] = 30.0 # pyright: ignore[reportArgumentType]
        self.viewer.opts["azimuth"] = -45.0 # pyright: ignore[reportArgumentType]
        self.viewer.update()

    # ------------------------------------------------------------ transforms (viewer -> panel)
    def _on_viewer_model_picked(self, model_id: int):
        # Make viewer click behave like selecting in the Models panel
        self.current_model_id = model_id
        self.viewer.set_selected_model(model_id)

        # Select in model panel list (without emitting loops)
        lw = self.model_panel.list_widget
        block = lw.blockSignals(True)
        try:
            for row in range(lw.count()):
                item = lw.item(row)
                if item is None:
                    continue
                if item.data(QtCore.Qt.UserRole) == model_id:
                    lw.setCurrentItem(item)
                    break
        finally:
            lw.blockSignals(block)

        # Sync transform panel from viewer model
        m = self.viewer.models.get(model_id)
        if m is not None:
            self.transform_panel.set_position(float(m["offset"][0]), float(m["offset"][1]))

    def _on_viewer_model_moved(self, model_id: int, x: float, y: float):
        if self.current_model_id != model_id:
            self.current_model_id = model_id
            self.viewer.set_selected_model(model_id)

        # Update transform panel live (no feedback loop)
        self.transform_panel.set_position(x, y, block_signals=True)

        # viewer already updated its transform during drag, but keep this for consistency
        self.viewer.set_model_transform(model_id, offset_xy=(x, y))

    # ------------------------------------------------------------- async load
    def _add_model_from_path_async(self, path: str):
        dlg = self._busy_dialog("Loading", f"Loading STL:\n{os.path.basename(path)}")
        dlg.show()

        def load_mesh(p):
            mesh = trimesh.load(p, force="mesh")
            if isinstance(mesh, trimesh.Scene):
                mesh = trimesh.util.concatenate(mesh.dump())
            elif not isinstance(mesh, trimesh.Trimesh):
                # fallback: concatenate any geometry collection into a Trimesh
                mesh = trimesh.util.concatenate(mesh)  # type: ignore[arg-type]
            vertices = np.array(mesh.vertices, dtype=float)
            faces = np.array(mesh.faces, dtype=int)
            return {"path": p, "name": os.path.basename(p), "v": vertices, "f": faces}

        worker = Worker(load_mesh, path)

        def on_done(payload):
            dlg.close()
            model_id = self.viewer.add_model_from_data(payload["name"], payload["path"], payload["v"], payload["f"])
            self.model_panel.add_model(payload["name"], model_id)

            self.current_model_id = model_id
            self.viewer.set_selected_model(model_id)

            # Initialize UI position from model offset
            m = self.viewer.models.get(model_id)
            if m is not None:
                self.transform_panel.set_position(float(m["offset"][0]), float(m["offset"][1]))

            self.statusBar().showMessage(f"Loaded {payload['name']}")

        def on_err(msg):
            dlg.close()
            QtWidgets.QMessageBox.critical(self, "Load error", msg)

        worker.signals.finished.connect(on_done)
        worker.signals.error.connect(on_err)
        self.pool.start(worker)

    # ----------------------------------------------------------- slice/print
    def _get_current_stl_path(self):
        if self.current_model_id is None:
            return None
        return self.viewer.get_model_path(self.current_model_id)

    def slice_current_model(self):
        stl_path = self._get_current_stl_path()
        if not stl_path:
            QtWidgets.QMessageBox.warning(self, "No model", "Load and select an STL first.")
            return

        settings = self.settings_panel.to_settings()
        dlg = self._busy_dialog("Slicing", "Slicing model...\nPlease wait.")
        dlg.show()

        worker = Worker(slice_file, stl_path, settings)

        def on_done(gcode_path):
            dlg.close()
            self.statusBar().showMessage(f"Sliced to {gcode_path}")
            QtWidgets.QMessageBox.information(self, "Slicing complete", f"G-code written to:\n{gcode_path}")

        def on_err(msg):
            dlg.close()
            self.statusBar().showMessage("Slicing failed")
            QtWidgets.QMessageBox.critical(self, "Slicing error", msg)

        worker.signals.finished.connect(on_done)
        worker.signals.error.connect(on_err)
        self.pool.start(worker)

    def print_current_model(self):
        stl_path = self._get_current_stl_path()
        if not stl_path:
            QtWidgets.QMessageBox.warning(self, "No model", "Load and select a model first.")
            return

        settings = self.settings_panel.to_settings()
        dlg = self._busy_dialog("Print", "Slicing & sending to printer...\nPlease wait.")
        dlg.show()

        def do_print(p, s):
            return self.printer_manager.slice_and_print(p, settings=s)

        worker = Worker(do_print, stl_path, settings)

        def on_done(msg):
            dlg.close()
            self.statusBar().showMessage(str(msg))
            QtWidgets.QMessageBox.information(self, "Print", str(msg))

        def on_err(msg):
            dlg.close()
            self.statusBar().showMessage("Print failed")
            QtWidgets.QMessageBox.critical(self, "Print error", msg)

        worker.signals.finished.connect(on_done)
        worker.signals.error.connect(on_err)
        self.pool.start(worker)

    # -------------------------------------------------------------- job queue
    def _add_current_model_to_queue(self):
        stl_path = self._get_current_stl_path()
        if not stl_path:
            QtWidgets.QMessageBox.warning(self, "No model", "Select a model before adding to queue.")
            return
        desc = f"Local: {os.path.basename(stl_path)}"
        payload = {"stl_path": stl_path}
        self.job_queue_panel.add_job(desc, payload)

    # -------------------------------------------------------------- helpers
    def _busy_dialog(self, title: str, label: str):
        dlg = QtWidgets.QProgressDialog(label, "", 0, 0, self)
        dlg.setWindowTitle(title)
        dlg.setWindowModality(QtCore.Qt.ApplicationModal)
        dlg.setAutoClose(True)
        dlg.setAutoReset(True)
        dlg.setRange(0, 0)
        return dlg

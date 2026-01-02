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
from .workers import Worker
from .popups import MovePopup, RotatePopup, ScalePopup, AutoOrientPopup, ArrangePopup

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

        # Job queue dock (right)
        self.job_queue_panel = JobQueuePanel(self)
        job_dock = QtWidgets.QDockWidget("Job Queue", self)
        job_dock.setWidget(self.job_queue_panel)
        job_dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, job_dock)

        self.setCentralWidget(self.viewer)

        self._build_menubar()
        self._build_toolbar()

        self._popup_move = MovePopup(self)
        self._popup_rotate = RotatePopup(self)
        self._popup_scale = ScalePopup(self)
        self._popup_auto_orient = AutoOrientPopup(self)
        self._popup_arrange = ArrangePopup(self)
        for popup in (
            self._popup_move,
            self._popup_rotate,
            self._popup_scale,
            self._popup_auto_orient,
            self._popup_arrange,
        ):
            popup.hide()

        self._popup_move.position_changed.connect(self._on_transform_position_changed)
        self._popup_move.center_requested.connect(self._on_transform_center_requested)
        self._popup_scale.scale_changed.connect(self._on_transform_scale_changed)
        self._popup_auto_orient.orient_requested.connect(self._on_auto_orient_requested)
        self._popup_auto_orient.reset_requested.connect(self._on_auto_orient_reset)
        self._popup_arrange.arrange_requested.connect(self._on_arrange_requested)
        self._popup_arrange.arrange_selected_requested.connect(self._on_arrange_selected_requested)
        self._popup_arrange.reset_requested.connect(self._on_arrange_reset)

        # Connect signals (panels)
        self.model_panel.model_selected.connect(self._on_model_selected)
        self.model_panel.request_remove.connect(self._on_model_remove)

        self.job_queue_panel.add_btn.clicked.connect(self._add_current_model_to_queue)

        # Viewer3D: pick + drag move
        self.viewer.modelPicked.connect(self._on_viewer_model_picked)
        self.viewer.modelMoved.connect(self._on_viewer_model_moved)

        # Initialize snap settings into viewer (defaults for now)
        self.viewer.set_snap(False, 1.0)

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
        self.transform_toolbar.addRequested.connect(self.open_stl_dialog)
        self.transform_toolbar.moveRequested.connect(self._on_move_tool)
        self.transform_toolbar.rotateRequested.connect(self._on_rotate_tool)
        self.transform_toolbar.scaleRequested.connect(self._on_scale_tool)
        self.transform_toolbar.autoOrientRequested.connect(self._on_auto_orient_tool)
        self.transform_toolbar.autoArrangeRequested.connect(self._on_arrange_tool)
        self.transform_toolbar.layOnFaceRequested.connect(self._lay_on_face)

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

        self.viewer.set_gizmo_mode("move")
        self._sync_popups()

    def _on_model_remove(self, model_id: int):
        self.viewer.remove_model(model_id)
        self.model_panel.remove_model(model_id)

        if self.current_model_id == model_id:
            remaining = self.viewer.get_model_ids()
            self.current_model_id = remaining[0] if remaining else None
            self.viewer.set_selected_model(self.current_model_id)

        self.statusBar().showMessage("Model removed")
        self._sync_popups()

    def _clear_all_models(self):
        self.viewer.clear_all_models()
        self.model_panel.list_widget.clear()
        self.current_model_id = None
        self.viewer.set_selected_model(None)
        self.statusBar().showMessage("Cleared all models")
        self._sync_popups()

    # ------------------------------------------------------------ transforms (toolbar -> viewer)
    def _enable_move_gizmo(self):
        self.viewer.set_gizmo_mode("move")

    def _enable_rotate_gizmo(self):
        self.viewer.set_gizmo_mode("rotate")
        QtWidgets.QMessageBox.information(self, "Rotate", "Rotate gizmo is not implemented yet.")

    def _prompt_scale_model(self):
        if self.current_model_id is None:
            QtWidgets.QMessageBox.warning(self, "No model selected", "Select a model first.")
            return
        m = self.viewer.models.get(self.current_model_id)
        if m is None:
            return
        current_pct = float(m["scale"]) * 100.0
        val, ok = QtWidgets.QInputDialog.getDouble(
            self,
            "Scale Model",
            "Scale (%)",
            value=current_pct,
            min=1.0,
            max=500.0,
            decimals=2,
        )
        if not ok:
            return
        new_scale = float(val) / 100.0
        self.viewer.set_model_transform(self.current_model_id, scale=new_scale, offset_xyz=m["offset"])
        self.statusBar().showMessage(f"Scale applied: {new_scale:.3f}")

    def _lay_on_face(self):
        QtWidgets.QMessageBox.information(self, "Lay on Face", "Not implemented yet.")

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

        self.viewer.set_gizmo_mode("move")

    def _on_viewer_model_moved(self, model_id: int, x: float, y: float):
        if self.current_model_id != model_id:
            self.current_model_id = model_id
            self.viewer.set_selected_model(model_id)

        self.statusBar().showMessage(f"Moved model {model_id}: x={x:.2f} y={y:.2f}")
        self._sync_popups()

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

    # ------------------------------------------------------ toolbar popups
    def _on_move_tool(self):
        self._enable_move_gizmo()
        self._toggle_popup(self._popup_move)

    def _on_rotate_tool(self):
        self._enable_rotate_gizmo()
        self._toggle_popup(self._popup_rotate)

    def _on_scale_tool(self):
        self._toggle_popup(self._popup_scale)

    def _on_auto_orient_tool(self):
        self._toggle_popup(self._popup_auto_orient)

    def _on_arrange_tool(self):
        self._toggle_popup(self._popup_arrange)

    def _toggle_popup(self, popup):
        if popup.isVisible():
            popup.hide()
            return
        self._hide_all_popups(except_popup=popup)
        self._position_popup(popup)
        self._sync_popups()
        popup.show()
        popup.raise_()

    def _hide_all_popups(self, except_popup=None):
        for popup in (
            self._popup_move,
            self._popup_rotate,
            self._popup_scale,
            self._popup_auto_orient,
            self._popup_arrange,
        ):
            if popup is not except_popup:
                popup.hide()

    def _position_popup(self, popup):
        if not hasattr(self, "transform_toolbar"):
            return
        toolbar = self.transform_toolbar
        pos = toolbar.mapTo(self, QtCore.QPoint(8, toolbar.height() + 6))
        popup.move(pos)

    def _sync_popups(self):
        if self.current_model_id is None:
            self._popup_move.set_position(0.0, 0.0, 0.0)
            self._popup_scale.set_scale(100.0, 100.0, 100.0)
            self._popup_scale.set_size(0.0, 0.0, 0.0)
            return

        transform = self.viewer.get_model_transform(self.current_model_id)
        if transform is None:
            return
        scale, offset = transform
        self._popup_move.set_position(float(offset[0]), float(offset[1]), float(offset[2]))
        scale_pct = float(scale) * 100.0
        self._popup_scale.set_scale(scale_pct, scale_pct, scale_pct)

        bounds = self.viewer.get_model_bounds(self.current_model_id)
        if bounds is not None:
            mn, mx = bounds
            size = (float(mx[0] - mn[0]), float(mx[1] - mn[1]), float(mx[2] - mn[2]))
            self._popup_scale.set_size(size[0], size[1], size[2])

    def _on_transform_position_changed(self, x: float, y: float, z: float):
        if self.current_model_id is None:
            return
        self.viewer.set_model_transform(self.current_model_id, offset_xyz=(x, y, z))

    def _on_transform_center_requested(self):
        if self.current_model_id is None:
            return
        self.viewer.set_model_transform(self.current_model_id, offset_xyz=(0.0, 0.0, 0.0))
        self._sync_popups()

    def _on_transform_scale_changed(self, x: float, y: float, z: float):
        if self.current_model_id is None:
            return
        scale = max(0.01, float(x) / 100.0)
        m = self.viewer.models.get(self.current_model_id)
        if m is None:
            return
        self.viewer.set_model_transform(self.current_model_id, scale=scale, offset_xyz=m["offset"])
        self._sync_popups()

    def _on_auto_orient_requested(self, mode: str):
        _ = mode
        QtWidgets.QMessageBox.information(self, "Auto Orient", "Auto orient is not implemented yet.")

    def _on_auto_orient_reset(self):
        QtWidgets.QMessageBox.information(self, "Auto Orient", "Auto orient is not implemented yet.")

    def _on_arrange_requested(self):
        QtWidgets.QMessageBox.information(self, "Arrange", "Arrange is not implemented yet.")

    def _on_arrange_selected_requested(self):
        QtWidgets.QMessageBox.information(self, "Arrange", "Arrange selected is not implemented yet.")

    def _on_arrange_reset(self):
        QtWidgets.QMessageBox.information(self, "Arrange", "Arrange is not implemented yet.")

    # -------------------------------------------------------------- helpers
    def _busy_dialog(self, title: str, label: str):
        dlg = QtWidgets.QProgressDialog(label, "", 0, 0, self)
        dlg.setWindowTitle(title)
        dlg.setWindowModality(QtCore.Qt.ApplicationModal)
        dlg.setAutoClose(True)
        dlg.setAutoReset(True)
        dlg.setRange(0, 0)
        return dlg

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        super().resizeEvent(a0)
        for popup in (
            self._popup_move,
            self._popup_rotate,
            self._popup_scale,
            self._popup_auto_orient,
            self._popup_arrange,
        ):
            if popup.isVisible():
                self._position_popup(popup)

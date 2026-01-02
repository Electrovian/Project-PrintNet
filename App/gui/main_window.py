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
from .theme import set_theme, THEMES, theme_css, theme_qcolor

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
        max_threads = max(1, (os.cpu_count() or 2) - 1)
        self.pool.setMaxThreadCount(max_threads)
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
        self._build_topbar()
        self._build_toolbar()
        self._build_action_panel()

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
        self._popup_rotate.rotation_changed.connect(self._on_transform_rotation_changed)
        self._popup_rotate.reset_requested.connect(self._on_transform_rotation_reset)
        self._popup_scale.scale_changed.connect(self._on_transform_scale_changed)
        self._popup_auto_orient.orient_requested.connect(self._on_auto_orient_requested)
        self._popup_auto_orient.reset_requested.connect(self._on_auto_orient_reset)
        self._popup_arrange.arrange_requested.connect(self._on_arrange_requested)
        self._popup_arrange.arrange_selected_requested.connect(self._on_arrange_selected_requested)
        self._popup_arrange.reset_requested.connect(self._on_arrange_reset)

        self._apply_theme()

        # Connect signals (panels)
        self.model_panel.model_selected.connect(self._on_model_selected)
        self.model_panel.request_remove.connect(self._on_model_remove)

        self.job_queue_panel.add_btn.clicked.connect(self._add_current_model_to_queue)

        # Viewer3D: pick + drag move
        self.viewer.modelPicked.connect(self._on_viewer_model_picked)
        self.viewer.modelMoved.connect(self._on_viewer_model_moved)
        self.viewer.modelRotated.connect(self._on_viewer_model_rotated)

        # Initialize snap settings into viewer (defaults for now)
        self.viewer.set_snap(False, 1.0)

        self.statusBar().showMessage("Ready")

    def _build_menubar(self):
        menubar = self.menuBar()
        menubar.setVisible(False)

        self._file_menu = QtWidgets.QMenu("File", self)
        self._view_menu = QtWidgets.QMenu("View", self)

        new_action = QtWidgets.QAction("New Project", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self._new_project)
        self._file_menu.addAction(new_action)

        self.open_action = QtWidgets.QAction("Open Project...", self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.triggered.connect(self.open_stl_dialog)
        self._file_menu.addAction(self.open_action)

        recent_menu = QtWidgets.QMenu("Recent Projects", self._file_menu)
        recent_menu.setEnabled(False)
        self._file_menu.addMenu(recent_menu)

        self._file_menu.addSeparator()

        save_action = QtWidgets.QAction("Save Project", self)
        save_action.setShortcut("Ctrl+S")
        save_action.setEnabled(False)
        self._file_menu.addAction(save_action)

        save_as_action = QtWidgets.QAction("Save Project as...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self._not_implemented)
        self._file_menu.addAction(save_as_action)

        self._file_menu.addSeparator()

        import_menu = QtWidgets.QMenu("Import", self._file_menu)
        import_stl_action = QtWidgets.QAction("Import STL(s)...", self)
        import_stl_action.triggered.connect(self.open_stl_dialog)
        import_menu.addAction(import_stl_action)
        self._file_menu.addMenu(import_menu)

        export_menu = QtWidgets.QMenu("Export", self._file_menu)
        export_action = QtWidgets.QAction("Export G-code...", self)
        export_action.triggered.connect(self._not_implemented)
        export_menu.addAction(export_action)
        self._file_menu.addMenu(export_menu)

        upload_action = QtWidgets.QAction("Upload (3mf) to CrealityCloud", self)
        upload_action.setEnabled(False)
        self._file_menu.addAction(upload_action)

        self._file_menu.addSeparator()

        quit_action = QtWidgets.QAction("Quit", self)
        quit_action.triggered.connect(self.close)
        self._file_menu.addAction(quit_action)

        theme_menu = self._view_menu.addMenu("Theme")
        self._theme_group = QtWidgets.QActionGroup(self)
        self._theme_group.setExclusive(True)
        for name in THEMES.keys():
            label = name.capitalize()
            action = QtWidgets.QAction(label, self)
            action.setCheckable(True)
            action.setData(name)
            if name == "current":
                action.setChecked(True)
            action.triggered.connect(self._on_theme_selected)
            self._theme_group.addAction(action)
            theme_menu.addAction(action)

        menubar.addMenu(self._file_menu)
        menubar.addMenu(self._view_menu)
        for action in self._file_menu.actions() + self._view_menu.actions():
            self.addAction(action)

    def _build_toolbar(self):
        self.transform_toolbar = TransformToolbar(self)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.transform_toolbar)
        self.transform_toolbar.setMovable(False)
        self.transform_toolbar.addRequested.connect(self.open_stl_dialog)
        self.transform_toolbar.moveRequested.connect(self._on_move_tool)
        self.transform_toolbar.rotateRequested.connect(self._on_rotate_tool)
        self.transform_toolbar.scaleRequested.connect(self._on_scale_tool)
        self.transform_toolbar.autoOrientRequested.connect(self._on_auto_orient_tool)
        self.transform_toolbar.autoArrangeRequested.connect(self._on_arrange_tool)
        self.transform_toolbar.layOnFaceRequested.connect(self._lay_on_face)

    def _build_topbar(self):
        self._topbar = QtWidgets.QFrame(self)
        self._topbar.setObjectName("TopBar")
        layout = QtWidgets.QHBoxLayout(self._topbar)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(6)

        self._logo_btn = QtWidgets.QToolButton(self._topbar)
        self._logo_btn.setIcon(self._triangle_icon())
        self._logo_btn.setIconSize(QtCore.QSize(18, 18))
        self._logo_btn.setAutoRaise(True)
        self._logo_btn.setCursor(QtCore.Qt.PointingHandCursor)
        layout.addWidget(self._logo_btn)

        self._file_btn = QtWidgets.QToolButton(self._topbar)
        self._file_btn.setObjectName("FileButton")
        self._file_btn.setText("File")
        self._file_btn.setIcon(self._hamburger_icon())
        self._file_btn.setIconSize(QtCore.QSize(16, 16))
        self._file_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self._file_btn.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self._file_btn.setMenu(self._file_menu)
        layout.addWidget(self._file_btn)

        self._file_caret_btn = QtWidgets.QToolButton(self._topbar)
        self._file_caret_btn.setObjectName("CaretButton")
        self._file_caret_btn.setIcon(self._caret_icon())
        self._file_caret_btn.setIconSize(QtCore.QSize(12, 12))
        self._file_caret_btn.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self._file_caret_btn.setMenu(self._file_menu)
        self._file_caret_btn.setAutoRaise(True)
        layout.addWidget(self._file_caret_btn)

        layout.addWidget(self._topbar_separator())

        self._save_btn = self._top_icon_btn(self._save_icon(), "Save", self._not_implemented)
        self._undo_btn = self._top_icon_btn(self._undo_icon(), "Undo", self._not_implemented)
        self._redo_btn = self._top_icon_btn(self._redo_icon(), "Redo", self._not_implemented)
        layout.addWidget(self._save_btn)
        layout.addWidget(self._undo_btn)
        layout.addWidget(self._redo_btn)

        layout.addStretch(1)

        self._mode_tabs = []
        self._mode_group = QtWidgets.QButtonGroup(self)
        for label in ("Online Models", "Prepare", "Preview", "Device"):
            btn = QtWidgets.QToolButton(self._topbar)
            btn.setText(label)
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            btn.setCursor(QtCore.Qt.PointingHandCursor)
            btn.setObjectName("ModeTab")
            self._mode_group.addButton(btn)
            layout.addWidget(btn)
            self._mode_tabs.append(btn)
        if self._mode_tabs:
            self._mode_tabs[1].setChecked(True)

        self.setMenuWidget(self._topbar)
        self._apply_topbar_theme()

    def _build_action_panel(self):
        self._action_panel = QtWidgets.QFrame(self.viewer)
        self._action_panel.setObjectName("ActionPanel")
        panel_layout = QtWidgets.QVBoxLayout(self._action_panel)
        panel_layout.setContentsMargins(10, 8, 10, 8)
        panel_layout.setSpacing(6)

        self._slice_btn = QtWidgets.QPushButton("Slice plate", self._action_panel)
        self._slice_btn.clicked.connect(self.slice_current_model)
        panel_layout.addWidget(self._slice_btn)

        self._print_btn = QtWidgets.QPushButton("Send print", self._action_panel)
        self._print_btn.clicked.connect(self.print_current_model)
        panel_layout.addWidget(self._print_btn)

        self._position_action_panel()
        self._apply_action_panel_theme()

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

    def _prompt_scale_model(self):
        if self.current_model_id is None:
            QtWidgets.QMessageBox.warning(self, "No model selected", "Select a model first.")
            return
        m = self.viewer.models.get(self.current_model_id)
        if m is None:
            return
        scale_val = m.get("scale", 1.0)
        if isinstance(scale_val, (list, tuple, np.ndarray)):
            current_pct = float(scale_val[0]) * 100.0
        else:
            current_pct = float(scale_val) * 100.0
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
        self.viewer.set_model_transform(
            self.current_model_id,
            scale=(new_scale, new_scale, new_scale),
            offset_xyz=m["offset"],
        )
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

    def _on_viewer_model_rotated(self, model_id: int, x: float, y: float, z: float):
        if self.current_model_id != model_id:
            self.current_model_id = model_id
            self.viewer.set_selected_model(model_id)
        self.statusBar().showMessage(f"Rotated model {model_id}: x={x:.2f} y={y:.2f} z={z:.2f}")
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
        self._toggle_popup(self._popup_move, self.transform_toolbar.move_action)

    def _on_rotate_tool(self):
        self._enable_rotate_gizmo()
        self._toggle_popup(self._popup_rotate, self.transform_toolbar.rotate_action)

    def _on_scale_tool(self):
        self._toggle_popup(self._popup_scale, self.transform_toolbar.scale_action)

    def _on_auto_orient_tool(self):
        self._toggle_popup(self._popup_auto_orient, self.transform_toolbar.auto_orient_action)

    def _on_arrange_tool(self):
        self._toggle_popup(self._popup_arrange, self.transform_toolbar.auto_arrange_action)

    def _toggle_popup(self, popup, action=None):
        if popup.isVisible():
            popup.hide()
            return
        self._hide_all_popups(except_popup=popup)
        if action is not None:
            popup._anchor_action = action
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
        action = getattr(popup, "_anchor_action", None)
        popup.adjustSize()
        if action is not None:
            btn = toolbar.widgetForAction(action)
            if btn is not None:
                anchor = btn.mapTo(self, QtCore.QPoint(btn.width() // 2, btn.height()))
                x = anchor.x() - popup.width() // 2
                x = max(8, min(x, self.width() - popup.width() - 8))
                y = anchor.y() + 6
                popup.move(QtCore.QPoint(x, y))
                return

        pos = toolbar.mapTo(self, QtCore.QPoint(8, toolbar.height() + 6))
        popup.move(pos)

    def _sync_popups(self):
        if self.current_model_id is None:
            self._popup_move.set_position(0.0, 0.0, 0.0)
            self._popup_rotate.set_rotation(0.0, 0.0, 0.0)
            self._popup_scale.set_scale(100.0, 100.0, 100.0)
            self._popup_scale.set_size(0.0, 0.0, 0.0)
            self._popup_move.center_btn.setEnabled(False)
            return

        transform = self.viewer.get_model_transform(self.current_model_id)
        if transform is None:
            return
        scale, offset = transform
        self._popup_move.set_position(float(offset[0]), float(offset[1]), float(offset[2]))
        self._popup_move.center_btn.setEnabled(True)
        scale_pct = np.array(scale, dtype=float) * 100.0
        self._popup_scale.set_scale(float(scale_pct[0]), float(scale_pct[1]), float(scale_pct[2]))

        rotation = self.viewer.get_model_rotation(self.current_model_id)
        if rotation is not None:
            self._popup_rotate.set_rotation(float(rotation[0]), float(rotation[1]), float(rotation[2]))

        bounds = self.viewer.get_model_bounds(self.current_model_id)
        if bounds is not None:
            mn, mx = bounds
            size = (float(mx[0] - mn[0]), float(mx[1] - mn[1]), float(mx[2] - mn[2]))
            self._popup_scale.set_size(size[0], size[1], size[2])

    def _apply_theme(self):
        self.viewer.apply_theme()
        for popup in (
            self._popup_move,
            self._popup_rotate,
            self._popup_scale,
            self._popup_auto_orient,
            self._popup_arrange,
        ):
            popup.apply_theme()
        self._apply_topbar_theme()
        self._apply_action_panel_theme()

    def _on_theme_selected(self):
        action = self.sender()
        if action is None or not isinstance(action, QtWidgets.QAction):
            return
        name = action.data()
        if name:
            set_theme(str(name))
            self._apply_theme()

    def _on_transform_position_changed(self, x: float, y: float, z: float):
        if self.current_model_id is None:
            return
        self.viewer.set_model_transform(self.current_model_id, offset_xyz=(x, y, z))

    def _on_transform_rotation_changed(self, x: float, y: float, z: float):
        if self.current_model_id is None:
            return
        self.viewer.set_model_transform(self.current_model_id, rotation_xyz=(x, y, z))
        self._sync_popups()

    def _on_transform_rotation_reset(self):
        if self.current_model_id is None:
            return
        self.viewer.set_model_transform(self.current_model_id, rotation_xyz=(0.0, 0.0, 0.0))
        self._sync_popups()

    def _on_transform_center_requested(self):
        if self.current_model_id is None:
            return
        self.viewer.set_model_transform(self.current_model_id, offset_xyz=(0.0, 0.0, 0.0))
        self._sync_popups()

    def _on_transform_scale_changed(self, x: float, y: float, z: float):
        if self.current_model_id is None:
            return
        scale = np.array([x, y, z], dtype=float) / 100.0
        scale = np.maximum(scale, 0.01)
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

    def _new_project(self):
        self._clear_all_models()

    def _not_implemented(self):
        QtWidgets.QMessageBox.information(self, "Not implemented", "This feature is not implemented yet.")

    def _apply_topbar_theme(self):
        if not hasattr(self, "_topbar"):
            return
        self._topbar.setStyleSheet(
            "QFrame#TopBar {"
            f"  background: {theme_css('topbar_bg')};"
            f"  border-bottom: 1px solid {theme_css('topbar_border')};"
            "}"
            "QToolButton {"
            f"  color: {theme_css('topbar_text')};"
            "  border: 1px solid transparent;"
            "  border-radius: 4px;"
            "  padding: 4px 8px;"
            "}"
            "QToolButton:hover {"
            f"  background: {theme_css('menu_hover_bg')};"
            "}"
            "QToolButton#FileButton {"
            f"  border: 1px solid {theme_css('topbar_accent')};"
            "  padding: 4px 10px;"
            "}"
            "QToolButton#CaretButton {"
            "  padding: 4px;"
            "}"
            "QToolButton#ModeTab {"
            "  padding: 6px 12px;"
            "  border-radius: 6px;"
            "}"
            "QToolButton#ModeTab:checked {"
            f"  background: {theme_css('topbar_accent')};"
            f"  color: {theme_css('popup_text')};"
            "  font-weight: 600;"
            "  border: 1px solid transparent;"
            "}"
        )
        self._file_btn.setIcon(self._hamburger_icon())
        self._file_caret_btn.setIcon(self._caret_icon())
        self._logo_btn.setIcon(self._triangle_icon())
        for btn, icon_fn in (
            (self._save_btn, self._save_icon),
            (self._undo_btn, self._undo_icon),
            (self._redo_btn, self._redo_icon),
        ):
            btn.setIcon(icon_fn())

        menu_style = (
            "QMenu {"
            f"  background: {theme_css('menu_bg')};"
            f"  color: {theme_css('menu_text')};"
            f"  border: 1px solid {theme_css('menu_border')};"
            "  padding: 4px;"
            "}"
            "QMenu::item {"
            "  padding: 4px 20px;"
            "  margin: 2px 4px;"
            "}"
            "QMenu::item:selected {"
            f"  background: {theme_css('menu_hover_bg')};"
            "}"
            "QMenu::separator {"
            f"  height: 1px; background: {theme_css('menu_sep')}; margin: 4px 6px;"
            "}"
            "QMenu::item:disabled {"
            f"  color: {theme_css('menu_disabled_text')};"
            "}"
        )
        self._file_menu.setStyleSheet(menu_style)
        self._view_menu.setStyleSheet(menu_style)

    def _apply_action_panel_theme(self):
        if not hasattr(self, "_action_panel"):
            return
        self._action_panel.setStyleSheet(
            "QFrame#ActionPanel {"
            f"  background: {theme_css('action_panel_bg')};"
            f"  border: 1px solid {theme_css('action_panel_border')};"
            "  border-radius: 6px;"
            "}"
            "QPushButton {"
            f"  background: {theme_css('action_button_bg')};"
            f"  color: {theme_css('action_button_text')};"
            f"  border: 1px solid {theme_css('action_panel_border')};"
            "  border-radius: 4px;"
            "  padding: 6px 16px;"
            "}"
            "QPushButton:hover {"
            f"  background: {theme_css('action_button_hover_bg')};"
            "}"
            "QPushButton:pressed {"
            f"  background: {theme_css('action_button_active_bg')};"
            "}"
        )

    def _position_action_panel(self):
        if not hasattr(self, "_action_panel"):
            return
        margin = 16
        self._action_panel.adjustSize()
        x = max(0, self.viewer.width() - self._action_panel.width() - margin)
        y = max(0, self.viewer.height() - self._action_panel.height() - margin)
        self._action_panel.move(x, y)

    def _topbar_separator(self):
        sep = QtWidgets.QFrame(self._topbar)
        sep.setFrameShape(QtWidgets.QFrame.VLine)
        sep.setFrameShadow(QtWidgets.QFrame.Sunken)
        sep.setStyleSheet(f"color: {theme_css('topbar_border')};")
        sep.setFixedHeight(20)
        return sep

    def _top_icon_btn(self, icon: QtGui.QIcon, tooltip: str, slot):
        btn = QtWidgets.QToolButton(self._topbar)
        btn.setIcon(icon)
        btn.setIconSize(QtCore.QSize(16, 16))
        btn.setToolTip(tooltip)
        btn.setAutoRaise(True)
        btn.setCursor(QtCore.Qt.PointingHandCursor)
        btn.clicked.connect(slot)
        return btn

    def _hamburger_icon(self):
        return QtGui.QIcon(self._paint_icon("hamburger"))

    def _caret_icon(self):
        return QtGui.QIcon(self._paint_icon("caret"))

    def _triangle_icon(self):
        return QtGui.QIcon(self._paint_icon("triangle"))

    def _save_icon(self):
        return QtGui.QIcon(self._paint_icon("save"))

    def _undo_icon(self):
        return QtGui.QIcon(self._paint_icon("undo"))

    def _redo_icon(self):
        return QtGui.QIcon(self._paint_icon("redo"))

    def _paint_icon(self, kind: str):
        size = 18
        pm = QtGui.QPixmap(size, size)
        pm.fill(QtCore.Qt.transparent)
        p = QtGui.QPainter(pm)
        p.setRenderHint(QtGui.QPainter.Antialiasing, True)
        color = theme_qcolor("topbar_icon")
        pen = QtGui.QPen(color, 2)
        p.setPen(pen)
        p.setBrush(QtGui.QBrush(color))

        if kind == "hamburger":
            for y in (4, 9, 14):
                p.drawLine(3, y, size - 3, y)
        elif kind == "caret":
            pts = [QtCore.QPointF(4, 6), QtCore.QPointF(size - 4, 6), QtCore.QPointF(size / 2, 12)]
            p.drawPolygon(QtGui.QPolygonF(pts))
        elif kind == "triangle":
            pts = [QtCore.QPointF(size / 2, 2), QtCore.QPointF(size - 2, size - 2), QtCore.QPointF(2, size - 2)]
            p.setBrush(QtGui.QBrush(theme_qcolor("topbar_accent")))
            p.setPen(QtGui.QPen(theme_qcolor("topbar_accent"), 2))
            p.drawPolygon(QtGui.QPolygonF(pts))
        elif kind == "save":
            p.drawRect(4, 4, size - 8, size - 8)
            p.drawLine(6, 7, size - 6, 7)
        elif kind == "undo":
            path = QtGui.QPainterPath()
            path.moveTo(12, 5)
            path.cubicTo(6, 5, 6, 14, 12, 14)
            p.drawPath(path)
            p.drawLine(6, 5, 3, 7)
            p.drawLine(6, 5, 3, 3)
        elif kind == "redo":
            path = QtGui.QPainterPath()
            path.moveTo(6, 5)
            path.cubicTo(12, 5, 12, 14, 6, 14)
            p.drawPath(path)
            p.drawLine(12, 5, 15, 7)
            p.drawLine(12, 5, 15, 3)
        p.end()
        return pm

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
        self._position_action_panel()

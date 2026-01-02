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
from config.defaults import DEFAULTS

from slicer.slicer import slice_file
from slicer.gcode import SliceSettings

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
        self._settings_dock = QtWidgets.QDockWidget("Printer", self)
        self._settings_dock.setWidget(self.settings_panel)
        self._settings_dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self._settings_dock)

        # Models dock (left)
        self.model_panel = ModelPanel(self)
        self._model_dock = QtWidgets.QDockWidget("Models", self)
        self._model_dock.setWidget(self.model_panel)
        self._model_dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self._model_dock)

        # Job queue dock (right)
        self.job_queue_panel = JobQueuePanel(self)
        self._job_dock = QtWidgets.QDockWidget("Job Queue", self)
        self._job_dock.setWidget(self.job_queue_panel)
        self._job_dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self._job_dock)

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
        self.viewer.set_snap(
            DEFAULTS["viewer"]["snap_enabled"],
            DEFAULTS["viewer"]["snap_step"],
        )

        self.statusBar().showMessage(DEFAULTS["app"]["status_ready"])

    def _build_menubar(self):
        menubar = self.menuBar()
        menubar.setVisible(False)

        self._file_menu = QtWidgets.QMenu("File", self)
        self._edit_menu = QtWidgets.QMenu("Edit", self)
        self._view_menu = QtWidgets.QMenu("View", self)
        self._prefs_menu = QtWidgets.QMenu("Preferences", self)
        self._calib_menu = QtWidgets.QMenu("Calibration", self)
        self._help_menu = QtWidgets.QMenu("Help", self)
        self._main_menu = QtWidgets.QMenu(self)

        new_action = QtWidgets.QAction("New Project", self)
        new_action.setIcon(self._maybe_icon("menu_new.png"))
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self._new_project)
        self._file_menu.addAction(new_action)

        self.open_action = QtWidgets.QAction("Open Project...", self)
        self.open_action.setIcon(self._maybe_icon("menu_open.png"))
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.triggered.connect(self.open_stl_dialog)
        self._file_menu.addAction(self.open_action)

        recent_menu = QtWidgets.QMenu("Recent Projects", self._file_menu)
        recent_menu.setIcon(self._maybe_icon("menu_recent.png"))
        recent_menu.setEnabled(False)
        self._file_menu.addMenu(recent_menu)

        self._file_menu.addSeparator()

        save_action = QtWidgets.QAction("Save Project", self)
        save_action.setIcon(self._maybe_icon("menu_save.png"))
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self._not_implemented)
        self._file_menu.addAction(save_action)

        save_as_action = QtWidgets.QAction("Save Project as...", self)
        save_as_action.setIcon(self._maybe_icon("menu_save_as.png"))
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self._not_implemented)
        self._file_menu.addAction(save_as_action)

        self._file_menu.addSeparator()

        import_menu = QtWidgets.QMenu("Import", self._file_menu)
        import_menu.setIcon(self._maybe_icon("menu_import.png"))
        import_stl_action = QtWidgets.QAction("Import STL(s)...", self)
        import_stl_action.setIcon(self._maybe_icon("menu_import_stl.png"))
        import_stl_action.triggered.connect(self.open_stl_dialog)
        import_menu.addAction(import_stl_action)
        self._file_menu.addMenu(import_menu)

        export_menu = QtWidgets.QMenu("Export", self._file_menu)
        export_menu.setIcon(self._maybe_icon("menu_export.png"))
        export_action = QtWidgets.QAction("Export G-code...", self)
        export_action.setIcon(self._maybe_icon("menu_export_gcode.png"))
        export_action.triggered.connect(self.export_gcode)
        export_menu.addAction(export_action)
        self._file_menu.addMenu(export_menu)

        self._file_menu.addSeparator()

        quit_action = QtWidgets.QAction("Quit", self)
        quit_action.setIcon(self._maybe_icon("menu_quit.png"))
        quit_action.triggered.connect(self.close)
        self._file_menu.addAction(quit_action)

        self._build_edit_menu()
        self._build_view_menu()
        self._build_prefs_menu()
        self._build_calib_menu()
        self._build_help_menu()

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
        menubar.addMenu(self._edit_menu)
        menubar.addMenu(self._view_menu)
        menubar.addMenu(self._prefs_menu)
        menubar.addMenu(self._calib_menu)
        menubar.addMenu(self._help_menu)

        for menu in (
            self._file_menu,
            self._edit_menu,
            self._view_menu,
            self._prefs_menu,
            self._calib_menu,
            self._help_menu,
        ):
            for action in menu.actions():
                self.addAction(action)

        self._main_menu.addMenu(self._edit_menu)
        self._main_menu.addMenu(self._view_menu)
        self._main_menu.addMenu(self._prefs_menu)
        self._main_menu.addMenu(self._calib_menu)
        self._main_menu.addMenu(self._help_menu)

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
        margins = DEFAULTS["ui"]["topbar_margins"]
        layout.setContentsMargins(margins[0], margins[1], margins[2], margins[3])
        layout.setSpacing(DEFAULTS["ui"]["topbar_spacing"])

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
        self._file_caret_btn.setMenu(self._main_menu)
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
        for label in ("Prepare", "Preview", "Device"):
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
            self._mode_tabs[0].setChecked(True)
        if len(self._mode_tabs) >= 3:
            self._mode_tabs[1].setEnabled(False)
            self._mode_tabs[1].setToolTip("Preview is not implemented yet.")
            self._mode_tabs[2].setEnabled(False)
            self._mode_tabs[2].setToolTip("Device is not implemented yet.")

        self.setMenuWidget(self._topbar)
        self._apply_topbar_theme()

    def _build_action_panel(self):
        self._action_panel = QtWidgets.QFrame(self.viewer)
        self._action_panel.setObjectName("ActionPanel")
        panel_layout = QtWidgets.QVBoxLayout(self._action_panel)
        panel_margins = DEFAULTS["ui"]["action_panel_margins"]
        panel_layout.setContentsMargins(panel_margins[0], panel_margins[1], panel_margins[2], panel_margins[3])
        panel_layout.setSpacing(DEFAULTS["ui"]["action_panel_spacing"])

        self._slice_btn = QtWidgets.QPushButton("Slice plate", self._action_panel)
        self._slice_btn.clicked.connect(self.slice_current_model)
        panel_layout.addWidget(self._slice_btn)

        self._print_btn = QtWidgets.QPushButton("Send print", self._action_panel)
        self._print_btn.clicked.connect(self.print_current_model)
        panel_layout.addWidget(self._print_btn)

        self._position_action_panel()
        self._apply_action_panel_theme()

    def _build_edit_menu(self):
        undo_action = QtWidgets.QAction("Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self._not_implemented)
        self._edit_menu.addAction(undo_action)

        redo_action = QtWidgets.QAction("Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self._not_implemented)
        self._edit_menu.addAction(redo_action)

        self._edit_menu.addSeparator()

        cut_action = QtWidgets.QAction("Cut", self)
        cut_action.setShortcut("Ctrl+X")
        cut_action.triggered.connect(self._not_implemented)
        self._edit_menu.addAction(cut_action)

        copy_action = QtWidgets.QAction("Copy", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self._not_implemented)
        self._edit_menu.addAction(copy_action)

        paste_action = QtWidgets.QAction("Paste", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self._not_implemented)
        self._edit_menu.addAction(paste_action)

        delete_selected_action = QtWidgets.QAction("Delete Selected", self)
        delete_selected_action.setShortcut("Del")
        delete_selected_action.triggered.connect(self._delete_selected_model)
        self._edit_menu.addAction(delete_selected_action)

        delete_all_action = QtWidgets.QAction("Delete All", self)
        delete_all_action.setShortcut("Ctrl+D")
        delete_all_action.triggered.connect(self._clear_all_models)
        self._edit_menu.addAction(delete_all_action)

        clone_action = QtWidgets.QAction("Clone Selected", self)
        clone_action.setShortcut("Ctrl+K")
        clone_action.triggered.connect(self._not_implemented)
        self._edit_menu.addAction(clone_action)

        self._edit_menu.addSeparator()

        select_all_action = QtWidgets.QAction("Select All", self)
        select_all_action.setShortcut("Ctrl+A")
        select_all_action.triggered.connect(self._not_implemented)
        self._edit_menu.addAction(select_all_action)

        deselect_action = QtWidgets.QAction("Deselect All", self)
        deselect_action.setShortcut("Esc")
        deselect_action.triggered.connect(self._deselect_all_models)
        self._edit_menu.addAction(deselect_action)

    def _build_view_menu(self):
        default_view = QtWidgets.QAction("Default View", self)
        default_view.setShortcut("Ctrl+0")
        default_view.triggered.connect(self.viewer.reset_view)
        self._view_menu.addAction(default_view)

        view_actions = [
            ("Top", "Ctrl+1", (0.0, 90.0)),
            ("Bottom", "Ctrl+2", (0.0, -90.0)),
            ("Front", "Ctrl+3", (90.0, 0.0)),
            ("Rear", "Ctrl+4", (-90.0, 0.0)),
            ("Left", "Ctrl+5", (180.0, 0.0)),
            ("Right", "Ctrl+6", (0.0, 0.0)),
        ]
        for label, shortcut, (az, el) in view_actions:
            action = QtWidgets.QAction(label, self)
            action.setShortcut(shortcut)
            action.triggered.connect(lambda _=False, a=az, e=el: self._set_view_preset(a, e))
            self._view_menu.addAction(action)

        self._view_menu.addSeparator()

        self._projection_group = QtWidgets.QActionGroup(self)
        perspective_action = QtWidgets.QAction("Use Perspective View", self)
        perspective_action.setCheckable(True)
        ortho_action = QtWidgets.QAction("Use Orthogonal View", self)
        ortho_action.setCheckable(True)
        self._projection_group.addAction(perspective_action)
        self._projection_group.addAction(ortho_action)
        perspective_action.setChecked(True)
        perspective_action.triggered.connect(lambda: self._set_projection_mode("perspective"))
        ortho_action.triggered.connect(lambda: self._set_projection_mode("ortho"))
        self._view_menu.addAction(perspective_action)
        self._view_menu.addAction(ortho_action)

        self._view_menu.addSeparator()

        wireframe_action = QtWidgets.QAction("Show Wireframe", self)
        wireframe_action.triggered.connect(self._not_implemented)
        self._view_menu.addAction(wireframe_action)

        gcode_action = QtWidgets.QAction("Show G-code Window", self)
        gcode_action.setEnabled(False)
        self._view_menu.addAction(gcode_action)

        navigator_action = QtWidgets.QAction("Show 3D Navigator", self)
        navigator_action.setCheckable(True)
        navigator_action.setChecked(True)
        navigator_action.triggered.connect(self._toggle_view_cube)
        self._view_menu.addAction(navigator_action)

        reset_layout_action = QtWidgets.QAction("Reset Window Layout", self)
        reset_layout_action.triggered.connect(self._reset_window_layout)
        self._view_menu.addAction(reset_layout_action)

        self._view_menu.addSeparator()

        labels_action = QtWidgets.QAction("Show Labels", self)
        labels_action.setShortcut("Ctrl+E")
        labels_action.triggered.connect(self._not_implemented)
        self._view_menu.addAction(labels_action)

        overhang_action = QtWidgets.QAction("Show Overhang", self)
        overhang_action.triggered.connect(self._not_implemented)
        self._view_menu.addAction(overhang_action)

    def _build_prefs_menu(self):
        prefs_action = QtWidgets.QAction("Printer Preferences", self)
        prefs_action.setShortcut("Ctrl+P")
        prefs_action.triggered.connect(self._show_settings_panel)
        self._prefs_menu.addAction(prefs_action)

    def _build_calib_menu(self):
        for label in (
            "Temperature",
            "Flow rate",
            "Pressure advance",
            "Retraction test",
            "Tolerance Test",
            "Max flowrate",
            "Tutorial",
        ):
            action = QtWidgets.QAction(label, self)
            action.triggered.connect(self._not_implemented)
            self._calib_menu.addAction(action)

    def _build_help_menu(self):
        for label in (
            "Keyboard Shortcuts",
            "Show Configuration Folder",
            "Check for Updates",
        ):
            action = QtWidgets.QAction(label, self)
            action.triggered.connect(self._not_implemented)
            self._help_menu.addAction(action)

        self._help_menu.addSeparator()

        for label in (
            "User Course",
            "About Us",
            "User Feedback",
            "Log View",
            "User Guide",
        ):
            action = QtWidgets.QAction(label, self)
            action.triggered.connect(self._not_implemented)
            self._help_menu.addAction(action)

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
        if self.current_model_id is None:
            QtWidgets.QMessageBox.warning(self, "No model", "Select a model first.")
            return
        ok = self.viewer.lay_on_face(self.current_model_id)
        if not ok:
            QtWidgets.QMessageBox.warning(self, "Lay on Face", "Unable to orient model.")
            return
        self._sync_popups()

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

        worker = Worker(slice_file, stl_path, settings=settings)

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

    def export_gcode(self):
        stl_path = self._get_current_stl_path()
        if not stl_path:
            QtWidgets.QMessageBox.warning(self, "No model", "Load and select a model first.")
            return

        base = os.path.splitext(os.path.basename(stl_path))[0]
        suggested = os.path.join(os.path.dirname(stl_path), f"{base}.gcode")
        out_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Export G-code",
            suggested,
            "G-code files (*.gcode);;All files (*.*)",
        )
        if not out_path:
            return
        if not out_path.lower().endswith(".gcode"):
            out_path = f"{out_path}.gcode"

        settings = self.settings_panel.to_settings()
        dlg = self._busy_dialog("Export", "Exporting G-code...\nPlease wait.")
        dlg.show()

        worker = Worker(slice_file, stl_path, output_gcode_path=out_path, settings=settings)

        def on_done(gcode_path):
            dlg.close()
            self.statusBar().showMessage(f"Exported G-code to {gcode_path}")
            QtWidgets.QMessageBox.information(self, "Export complete", f"G-code written to:\n{gcode_path}")

        def on_err(msg):
            dlg.close()
            self.statusBar().showMessage("Export failed")
            QtWidgets.QMessageBox.critical(self, "Export error", msg)

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
        opts = self._popup_arrange.get_options()
        model_ids = self.viewer.get_model_ids()
        if not model_ids:
            QtWidgets.QMessageBox.warning(self, "Arrange", "Load models first.")
            return
        ok = self.viewer.arrange_models(
            model_ids,
            spacing=opts["spacing"],
            auto_rotate=opts["auto_rotate"],
            align_y=opts["align_y"],
        )
        if not ok:
            QtWidgets.QMessageBox.warning(self, "Arrange", "Unable to arrange models.")
            return
        self._sync_popups()

    def _on_arrange_selected_requested(self):
        if self.current_model_id is None:
            QtWidgets.QMessageBox.warning(self, "Arrange", "Select a model first.")
            return
        opts = self._popup_arrange.get_options()
        ok = self.viewer.arrange_models(
            [self.current_model_id],
            spacing=opts["spacing"],
            auto_rotate=opts["auto_rotate"],
            align_y=opts["align_y"],
        )
        if not ok:
            QtWidgets.QMessageBox.warning(self, "Arrange", "Unable to arrange model.")
            return
        self._sync_popups()

    def _on_arrange_reset(self):
        self._sync_popups()

    def _new_project(self):
        self._clear_all_models()

    def _not_implemented(self):
        QtWidgets.QMessageBox.information(self, "Not implemented", "This feature is not implemented yet.")

    def _delete_selected_model(self):
        if self.current_model_id is None:
            return
        self._on_model_remove(self.current_model_id)

    def _deselect_all_models(self):
        self.current_model_id = None
        self.viewer.set_selected_model(None)
        self.model_panel.list_widget.clearSelection()
        self._sync_popups()

    def _show_settings_panel(self):
        if hasattr(self, "_settings_dock"):
            self._settings_dock.show()
            self._settings_dock.raise_()
            self.settings_panel.setFocus(QtCore.Qt.OtherFocusReason)

    def _set_view_preset(self, azimuth: float, elevation: float):
        self.viewer.set_view(float(azimuth), float(elevation))

    def _set_projection_mode(self, mode: str):
        if mode == "ortho":
            self.viewer.opts["fov"] = 0  # pyright: ignore[reportArgumentType]
        else:
            self.viewer.opts["fov"] = 60  # pyright: ignore[reportArgumentType]
        self.viewer.update()

    def _toggle_view_cube(self, checked: bool):
        self.viewer.set_view_cube_visible(bool(checked))

    def _reset_window_layout(self):
        if hasattr(self, "_model_dock"):
            self._model_dock.show()
            self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self._model_dock)
        if hasattr(self, "_settings_dock"):
            self._settings_dock.show()
            self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self._settings_dock)
        if hasattr(self, "_job_dock"):
            self._job_dock.show()
            self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self._job_dock)

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
            "QToolButton:disabled {"
            f"  color: {theme_css('menu_disabled_text')};"
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
        for menu in (
            self._file_menu,
            self._edit_menu,
            self._view_menu,
            self._prefs_menu,
            self._calib_menu,
            self._help_menu,
            self._main_menu,
        ):
            menu.setStyleSheet(menu_style)

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
        margin = DEFAULTS["ui"]["action_panel_margin"]
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

    def _maybe_icon(self, filename: str):
        path = os.path.join(ASSETS_DIR, "icons", filename)
        if os.path.exists(path):
            return QtGui.QIcon(path)
        return QtGui.QIcon()

    def _hamburger_icon(self):
        icon = self._maybe_icon("top_hamburger.png")
        if not icon.isNull():
            return icon
        return QtGui.QIcon(self._paint_icon("hamburger"))

    def _caret_icon(self):
        icon = self._maybe_icon("top_caret.png")
        if not icon.isNull():
            return icon
        return QtGui.QIcon(self._paint_icon("caret"))

    def _triangle_icon(self):
        icon = self._maybe_icon("top_logo.png")
        if not icon.isNull():
            return icon
        return QtGui.QIcon(self._paint_icon("triangle"))

    def _save_icon(self):
        icon = self._maybe_icon("top_save.png")
        if not icon.isNull():
            return icon
        return QtGui.QIcon(self._paint_icon("save"))

    def _undo_icon(self):
        icon = self._maybe_icon("top_undo.png")
        if not icon.isNull():
            return icon
        return QtGui.QIcon(self._paint_icon("undo"))

    def _redo_icon(self):
        icon = self._maybe_icon("top_redo.png")
        if not icon.isNull():
            return icon
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

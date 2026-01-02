# gui/main_window.py
import json
import os
from dataclasses import asdict
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
from .theme import (
    export_theme,
    get_theme_name,
    register_theme,
    set_theme,
    THEMES,
    theme_css,
    theme_qcolor,
)
from .shortcuts import shortcut_key, shortcut_label, shortcuts_by_category
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
        self._build_shortcut_actions()

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

        self._current_project_path = None
        self._labels_visible = True
        self._model_clipboard = []
        self._undo_stack = []
        self._redo_stack = []
        self._undo_stack_limit = 50
        self._undo_in_progress = False
        self._undo_timer = QtCore.QTimer(self)
        self._undo_timer.setSingleShot(True)
        self._undo_timer.timeout.connect(self._finalize_undo_snapshot)
        self._pending_undo_snapshot = False
        self._push_undo_state()
        self.viewer.set_labels_visible(self._labels_visible)
        if hasattr(self, "_labels_action"):
            self._labels_action.setChecked(self._labels_visible)

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

        new_action = QtWidgets.QAction(shortcut_label("new_project"), self)
        new_action.setIcon(self._maybe_icon("menu_new.png"))
        new_action.setShortcut(shortcut_key("new_project"))
        new_action.triggered.connect(self._new_project)

        self.open_action = QtWidgets.QAction(shortcut_label("open_project"), self)
        self.open_action.setIcon(self._maybe_icon("menu_open.png"))
        self.open_action.setShortcut(shortcut_key("open_project"))
        self.open_action.triggered.connect(self._open_project)

        recent_menu = QtWidgets.QMenu("Recent Projects", self._file_menu)
        recent_menu.setIcon(self._maybe_icon("menu_recent.png"))
        recent_menu.setEnabled(False)

        save_action = QtWidgets.QAction(shortcut_label("save_project"), self)
        save_action.setIcon(self._maybe_icon("menu_save.png"))
        save_action.setShortcut(shortcut_key("save_project"))
        save_action.triggered.connect(self._save_project)
        self._save_action = save_action

        save_as_action = QtWidgets.QAction(shortcut_label("save_project_as"), self)
        save_as_action.setIcon(self._maybe_icon("menu_save_as.png"))
        save_as_action.setShortcut(shortcut_key("save_project_as"))
        save_as_action.triggered.connect(self._save_project_as)
        self._save_as_action = save_as_action

        import_menu = QtWidgets.QMenu("Import", self._file_menu)
        import_menu.setIcon(self._maybe_icon("menu_import.png"))
        import_stl_action = QtWidgets.QAction("Import STL(s)...", self)
        import_stl_action.setIcon(self._maybe_icon("menu_import_stl.png"))
        import_stl_action.setShortcut(shortcut_key("import_geometry"))
        import_stl_action.triggered.connect(self.open_stl_dialog)
        import_menu.addAction(import_stl_action)

        export_menu = QtWidgets.QMenu("Export", self._file_menu)
        export_menu.setIcon(self._maybe_icon("menu_export.png"))
        export_action = QtWidgets.QAction("Export G-code...", self)
        export_action.setIcon(self._maybe_icon("menu_export_gcode.png"))
        export_action.setShortcut(shortcut_key("export_gcode"))
        export_action.triggered.connect(self.export_gcode)
        export_menu.addAction(export_action)

        quit_action = QtWidgets.QAction("Quit", self)
        quit_action.setIcon(self._maybe_icon("menu_quit.png"))
        quit_action.triggered.connect(self.close)
        self._file_menu.addActions([new_action, self.open_action])
        self._file_menu.addMenu(recent_menu)
        self._file_menu.addSeparator()
        self._file_menu.addActions([save_action, save_as_action])
        self._file_menu.addSeparator()
        self._file_menu.addMenu(import_menu)
        self._file_menu.addMenu(export_menu)
        self._file_menu.addSeparator()
        self._file_menu.addActions([quit_action])

        self._build_edit_menu()
        self._build_view_menu()
        self._build_prefs_menu()
        self._build_calib_menu()
        self._build_help_menu()

        theme_menu = self._view_menu.addMenu("Theme")
        self._theme_menu = theme_menu
        self._theme_group = QtWidgets.QActionGroup(self)
        self._theme_group.setExclusive(True)
        current_theme = get_theme_name()
        for name in THEMES.keys():
            label = name.capitalize()
            action = QtWidgets.QAction(label, self)
            action.setCheckable(True)
            action.setData(name)
            if name == current_theme:
                action.setChecked(True)
            action.triggered.connect(self._on_theme_selected)
            self._theme_group.addAction(action)
            theme_menu.addAction(action)

        self._theme_menu_separator = theme_menu.addSeparator()

        customize_action = QtWidgets.QAction("Customize Theme...", self)
        customize_action.triggered.connect(self._open_theme_editor)
        theme_menu.addAction(customize_action)

        load_action = QtWidgets.QAction("Load Theme...", self)
        load_action.triggered.connect(self._load_theme_from_file)
        theme_menu.addAction(load_action)

        save_action = QtWidgets.QAction("Save Current Theme...", self)
        save_action.triggered.connect(self._save_theme_to_file)
        theme_menu.addAction(save_action)

        for menu in (
            self._file_menu,
            self._edit_menu,
            self._view_menu,
            self._prefs_menu,
            self._calib_menu,
            self._help_menu,
        ):
            menubar.addMenu(menu)
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

        self._save_btn = self._top_icon_btn(self._save_icon(), "Save", self._save_project)
        self._undo_btn = self._top_icon_btn(self._undo_icon(), "Undo", self._undo)
        self._redo_btn = self._top_icon_btn(self._redo_icon(), "Redo", self._redo)
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

    def _build_shortcut_actions(self):
        self._slice_action = QtWidgets.QAction(self)
        self._slice_action.setShortcut(shortcut_key("slice_plate"))
        self._slice_action.triggered.connect(self.slice_current_model)
        self.addAction(self._slice_action)

        self._print_action = QtWidgets.QAction(self)
        self._print_action.setShortcut(shortcut_key("print_plate"))
        self._print_action.triggered.connect(self.print_current_model)
        self.addAction(self._print_action)

        self._switch_tab_action = QtWidgets.QAction(self)
        self._switch_tab_action.setShortcut(shortcut_key("switch_table_page"))
        self._switch_tab_action.triggered.connect(self._switch_mode_tab)
        self.addAction(self._switch_tab_action)

        self._3dconnexion_action = QtWidgets.QAction(self)
        self._3dconnexion_action.setShortcut(shortcut_key("show_3dconnexion"))
        self._3dconnexion_action.triggered.connect(self._not_implemented)
        self.addAction(self._3dconnexion_action)

        self._position_action_panel()
        self._apply_action_panel_theme()

    def _build_edit_menu(self):
        undo_action = QtWidgets.QAction(shortcut_label("undo"), self)
        undo_action.setShortcut(shortcut_key("undo"))
        undo_action.triggered.connect(self._undo)
        self._edit_menu.addAction(undo_action)
        self._undo_action = undo_action

        redo_action = QtWidgets.QAction(shortcut_label("redo"), self)
        redo_action.setShortcut(shortcut_key("redo"))
        redo_action.triggered.connect(self._redo)
        self._edit_menu.addAction(redo_action)
        self._redo_action = redo_action

        self._edit_menu.addSeparator()

        cut_action = QtWidgets.QAction(shortcut_label("cut"), self)
        cut_action.setShortcut(shortcut_key("cut"))
        cut_action.triggered.connect(self._cut_selected)
        self._edit_menu.addAction(cut_action)

        copy_action = QtWidgets.QAction(shortcut_label("copy"), self)
        copy_action.setShortcut(shortcut_key("copy"))
        copy_action.triggered.connect(self._copy_selected)
        self._edit_menu.addAction(copy_action)

        paste_action = QtWidgets.QAction(shortcut_label("paste"), self)
        paste_action.setShortcut(shortcut_key("paste"))
        paste_action.triggered.connect(self._paste_clipboard)
        self._edit_menu.addAction(paste_action)

        delete_selected_action = QtWidgets.QAction(shortcut_label("delete_selected"), self)
        delete_selected_action.setShortcut(shortcut_key("delete_selected"))
        delete_selected_action.triggered.connect(self._delete_selected_model)
        self._edit_menu.addAction(delete_selected_action)

        delete_all_action = QtWidgets.QAction(shortcut_label("delete_all"), self)
        delete_all_action.setShortcut(shortcut_key("delete_all"))
        delete_all_action.triggered.connect(self._clear_all_models)
        self._edit_menu.addAction(delete_all_action)

        clone_action = QtWidgets.QAction(shortcut_label("clone_selected"), self)
        clone_action.setShortcut(shortcut_key("clone_selected"))
        clone_action.triggered.connect(self._clone_selected)
        self._edit_menu.addAction(clone_action)

        self._edit_menu.addSeparator()

        select_all_action = QtWidgets.QAction(shortcut_label("select_all"), self)
        select_all_action.setShortcut(shortcut_key("select_all"))
        select_all_action.triggered.connect(self._select_all_models)
        self._edit_menu.addAction(select_all_action)

        deselect_action = QtWidgets.QAction(shortcut_label("deselect_all"), self)
        deselect_action.setShortcut(shortcut_key("deselect_all"))
        deselect_action.triggered.connect(self._deselect_all_models)
        self._edit_menu.addAction(deselect_action)

    def _build_view_menu(self):
        default_view = QtWidgets.QAction(shortcut_label("view_default"), self)
        default_view.setShortcut(shortcut_key("view_default"))
        default_view.triggered.connect(self.viewer.reset_view)
        self._view_menu.addAction(default_view)

        view_actions = [
            ("view_top", (0.0, 90.0)),
            ("view_bottom", (0.0, -90.0)),
            ("view_front", (90.0, 0.0)),
            ("view_rear", (-90.0, 0.0)),
            ("view_left", (180.0, 0.0)),
            ("view_right", (0.0, 0.0)),
        ]
        for action_id, (az, el) in view_actions:
            action = QtWidgets.QAction(shortcut_label(action_id), self)
            action.setShortcut(shortcut_key(action_id))
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

        labels_action = QtWidgets.QAction(shortcut_label("show_labels"), self)
        labels_action.setShortcut(shortcut_key("show_labels"))
        labels_action.setCheckable(True)
        labels_action.setChecked(False)
        labels_action.toggled.connect(self._set_labels_visible)
        self._view_menu.addAction(labels_action)
        self._labels_action = labels_action

        overhang_action = QtWidgets.QAction("Show Overhang", self)
        overhang_action.triggered.connect(self._not_implemented)
        self._view_menu.addAction(overhang_action)

    def _build_prefs_menu(self):
        prefs_action = QtWidgets.QAction(shortcut_label("preferences"), self)
        prefs_action.setShortcut(shortcut_key("preferences"))
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
            if label == "Keyboard Shortcuts":
                action.setShortcut(shortcut_key("show_shortcuts"))
                action.triggered.connect(self._show_shortcuts_dialog)
            else:
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
        self._remove_models([model_id])

    def _clear_all_models(self):
        model_ids = self.viewer.get_model_ids()
        if not model_ids:
            self.current_model_id = None
            self.viewer.set_selected_model(None)
            self.model_panel.list_widget.clearSelection()
            self._sync_popups()
            return
        self._remove_models(model_ids)
        self.statusBar().showMessage("Cleared all models")

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
        self._schedule_undo_snapshot()

    def _lay_on_face(self):
        if self.current_model_id is None:
            QtWidgets.QMessageBox.warning(self, "No model", "Select a model first.")
            return
        ok = self.viewer.lay_on_face(self.current_model_id)
        if not ok:
            QtWidgets.QMessageBox.warning(self, "Lay on Face", "Unable to orient model.")
            return
        self._sync_popups()
        self._schedule_undo_snapshot()

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
        self._schedule_undo_snapshot()

    def _on_viewer_model_rotated(self, model_id: int, x: float, y: float, z: float):
        if self.current_model_id != model_id:
            self.current_model_id = model_id
            self.viewer.set_selected_model(model_id)
        self.statusBar().showMessage(f"Rotated model {model_id}: x={x:.2f} y={y:.2f} z={z:.2f}")
        self._sync_popups()
        self._schedule_undo_snapshot()

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
            self._push_undo_state()

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
            self._set_theme_checked(str(name))

    def _set_theme_checked(self, name: str):
        if not hasattr(self, "_theme_group"):
            return
        for action in self._theme_group.actions():
            if action.data() == name:
                action.setChecked(True)
                break

    def _ensure_theme_action(self, name: str):
        if not hasattr(self, "_theme_group"):
            return None
        for action in self._theme_group.actions():
            if action.data() == name:
                return action
        if not hasattr(self, "_theme_menu"):
            return None
        label = name.capitalize()
        action = QtWidgets.QAction(label, self)
        action.setCheckable(True)
        action.setData(name)
        action.triggered.connect(self._on_theme_selected)
        self._theme_group.addAction(action)
        if hasattr(self, "_theme_menu_separator") and self._theme_menu_separator is not None:
            self._theme_menu.insertAction(self._theme_menu_separator, action)
        else:
            self._theme_menu.addAction(action)
        return action

    def _open_theme_editor(self):
        theme = export_theme()
        if theme is None:
            QtWidgets.QMessageBox.warning(self, "Theme", "No theme data available.")
            return

        dlg = QtWidgets.QDialog(self)
        dlg.setWindowTitle("Customize Theme")
        dlg.setModal(True)

        layout = QtWidgets.QVBoxLayout(dlg)
        editor = QtWidgets.QTextEdit(dlg)
        editor.setPlainText(json.dumps(theme, indent=2, ensure_ascii=True))
        layout.addWidget(editor)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Apply | QtWidgets.QDialogButtonBox.Close,
            parent=dlg,
        )
        layout.addWidget(buttons)

        def apply_changes():
            try:
                data = json.loads(editor.toPlainText())
            except json.JSONDecodeError as exc:
                QtWidgets.QMessageBox.warning(self, "Theme", f"Invalid JSON: {exc}")
                return
            theme_data = register_theme("custom", data)
            if theme_data is None:
                QtWidgets.QMessageBox.warning(self, "Theme", "Theme data must be a JSON object.")
                return
            set_theme("custom")
            self._apply_theme()
            self._ensure_theme_action("custom")
            self._set_theme_checked("custom")
            self.statusBar().showMessage("Custom theme applied")

        buttons.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(apply_changes)
        buttons.rejected.connect(dlg.close)

        dlg.resize(720, 560)
        dlg.exec_()

    def _load_theme_from_file(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Load Theme",
            "",
            "Theme JSON (*.json);;All files (*.*)",
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except Exception as exc:
            QtWidgets.QMessageBox.warning(self, "Theme", str(exc))
            return

        theme_name = os.path.splitext(os.path.basename(path))[0]
        theme_payload = data
        if isinstance(data, dict) and "theme" in data:
            theme_payload = data.get("theme")
            name_value = data.get("name")
            if isinstance(name_value, str) and name_value:
                theme_name = name_value

        theme_data = register_theme(theme_name, theme_payload)
        if theme_data is None:
            QtWidgets.QMessageBox.warning(self, "Theme", "Theme data must be a JSON object.")
            return
        set_theme(theme_name)
        self._apply_theme()
        self._ensure_theme_action(theme_name)
        self._set_theme_checked(theme_name)
        self.statusBar().showMessage(f"Loaded theme: {theme_name}")

    def _save_theme_to_file(self):
        theme = export_theme()
        if theme is None:
            QtWidgets.QMessageBox.warning(self, "Theme", "No theme data available.")
            return
        default_name = f"{get_theme_name()}.json"
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save Theme",
            default_name,
            "Theme JSON (*.json);;All files (*.*)",
        )
        if not path:
            return
        if not path.lower().endswith(".json"):
            path = f"{path}.json"
        payload = {"name": get_theme_name(), "theme": theme}
        try:
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, indent=2, ensure_ascii=True)
        except Exception as exc:
            QtWidgets.QMessageBox.warning(self, "Theme", str(exc))
            return
        self.statusBar().showMessage(f"Saved theme to {path}")

    def _on_transform_position_changed(self, x: float, y: float, z: float):
        if self.current_model_id is None:
            return
        self.viewer.set_model_transform(self.current_model_id, offset_xyz=(x, y, z))
        self._schedule_undo_snapshot()

    def _on_transform_rotation_changed(self, x: float, y: float, z: float):
        if self.current_model_id is None:
            return
        self.viewer.set_model_transform(self.current_model_id, rotation_xyz=(x, y, z))
        self._sync_popups()
        self._schedule_undo_snapshot()

    def _on_transform_rotation_reset(self):
        if self.current_model_id is None:
            return
        self.viewer.set_model_transform(self.current_model_id, rotation_xyz=(0.0, 0.0, 0.0))
        self._sync_popups()
        self._schedule_undo_snapshot()

    def _on_transform_center_requested(self):
        if self.current_model_id is None:
            return
        self.viewer.set_model_transform(self.current_model_id, offset_xyz=(0.0, 0.0, 0.0))
        self._sync_popups()
        self._schedule_undo_snapshot()

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
        self._schedule_undo_snapshot()

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
        self._push_undo_state()

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
        self._push_undo_state()

    def _on_arrange_reset(self):
        self._sync_popups()

    def _new_project(self):
        self._current_project_path = None
        self._clear_all_models()

    def _not_implemented(self):
        QtWidgets.QMessageBox.information(self, "Not implemented", "This feature is not implemented yet.")

    def _save_project(self):
        if self._current_project_path:
            self._write_project_file(self._current_project_path)
            return
        self._save_project_as()

    def _save_project_as(self):
        suggested = self._current_project_path or ""
        if not suggested:
            stl_path = self._get_current_stl_path()
            if stl_path:
                base = os.path.splitext(os.path.basename(stl_path))[0]
                suggested = os.path.join(os.path.dirname(stl_path), f"{base}.osproj")
        out_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save Project",
            suggested,
            "OpenSlicer Project (*.osproj);;All files (*.*)",
        )
        if not out_path:
            return
        if not out_path.lower().endswith(".osproj"):
            out_path = f"{out_path}.osproj"
        self._write_project_file(out_path)

    def _open_project(self):
        start_dir = ""
        if self._current_project_path:
            start_dir = os.path.dirname(self._current_project_path)
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Open Project",
            start_dir,
            "OpenSlicer Project (*.osproj);;All files (*.*)",
        )
        if not path:
            return
        self._load_project_file(path)

    def _write_project_file(self, path: str):
        payload = self._serialize_project()
        try:
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, indent=2, ensure_ascii=True)
        except Exception as exc:
            QtWidgets.QMessageBox.critical(self, "Save error", str(exc))
            return
        self._current_project_path = path
        self.statusBar().showMessage(f"Saved project to {path}")

    def _load_project_file(self, path: str):
        try:
            with open(path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except Exception as exc:
            QtWidgets.QMessageBox.critical(self, "Open error", str(exc))
            return
        self._current_project_path = path
        base_dir = os.path.dirname(path)
        self._load_project_data(data, base_dir)
        self.statusBar().showMessage(f"Loaded project from {path}")

    def _load_project_data(self, data: dict, base_dir: str):
        if not isinstance(data, dict):
            QtWidgets.QMessageBox.warning(self, "Open error", "Invalid project file.")
            return

        if "settings" in data:
            self.settings_panel.apply_settings(data.get("settings") or {})

        models = data.get("models", [])
        if not isinstance(models, list):
            QtWidgets.QMessageBox.warning(self, "Open error", "Project models list is invalid.")
            return

        missing = []
        new_ids = []

        self._undo_in_progress = True
        try:
            lw = self.model_panel.list_widget
            block = lw.blockSignals(True)
            try:
                self.viewer.clear_all_models()
                self.model_panel.list_widget.clear()
                for entry in models:
                    if not isinstance(entry, dict):
                        continue
                    name = entry.get("name", "")
                    model_path = entry.get("path", "")
                    vertices = entry.get("vertices")
                    faces = entry.get("faces")

                    resolved_path = model_path
                    if model_path and base_dir and not os.path.isabs(model_path):
                        resolved_path = os.path.join(base_dir, model_path)

                    use_path = bool(resolved_path and os.path.exists(resolved_path))
                    if use_path:
                        try:
                            mesh = trimesh.load(resolved_path, force="mesh")
                            if isinstance(mesh, trimesh.Scene):
                                mesh = trimesh.util.concatenate(mesh.dump())
                            elif not isinstance(mesh, trimesh.Trimesh):
                                mesh = trimesh.util.concatenate(mesh)  # type: ignore[arg-type]
                            vertices = np.array(mesh.vertices, dtype=float)
                            faces = np.array(mesh.faces, dtype=int)
                        except Exception:
                            use_path = False

                    if not use_path:
                        if vertices is None or faces is None:
                            missing.append(model_path or name or "Unnamed model")
                            continue
                    model_id = self.viewer.add_model_from_data(
                        name,
                        resolved_path if use_path else model_path,
                        vertices,
                        faces,
                    )
                    self.model_panel.add_model(name, model_id)

                    self.viewer.set_model_transform(
                        model_id,
                        scale=entry.get("scale"),
                        rotation_xyz=entry.get("rotation"),
                        offset_xyz=entry.get("offset"),
                    )
                    new_ids.append(model_id)
            finally:
                lw.blockSignals(block)
        finally:
            self._undo_in_progress = False

        selected_index = data.get("selected_index")
        selected_id = None
        if new_ids:
            if isinstance(selected_index, int) and 0 <= selected_index < len(new_ids):
                selected_id = new_ids[selected_index]
            else:
                selected_id = new_ids[-1]
        self.current_model_id = selected_id
        self.viewer.set_selected_model(selected_id)
        if selected_id is not None:
            self._select_model_in_panel(selected_id)
        else:
            self.model_panel.list_widget.clearSelection()
        self._sync_popups()

        self._undo_stack.clear()
        self._redo_stack.clear()
        self._push_undo_state()

        if missing:
            QtWidgets.QMessageBox.warning(
                self,
                "Open warning",
                "Some models could not be loaded:\n" + "\n".join(missing),
            )

    def _serialize_project(self) -> dict:
        models = []
        for m in self.viewer.models.values():
            scale = self._scale_to_vec(m.get("scale", 1.0))
            rotation = self._vec3(m.get("rotation", [0.0, 0.0, 0.0]))
            offset = self._vec3(m.get("offset", [0.0, 0.0, 0.0]))
            entry = {
                "name": m.get("name", ""),
                "path": m.get("path", ""),
                "scale": [float(v) for v in scale],
                "rotation": [float(v) for v in rotation],
                "offset": [float(v) for v in offset],
            }
            if not entry["path"]:
                entry["vertices"] = np.asarray(m.get("base_vertices", []), dtype=float).tolist()
                entry["faces"] = np.asarray(m.get("faces", []), dtype=int).tolist()
            models.append(entry)

        settings = self.settings_panel.to_settings()
        return {
            "version": 1,
            "models": models,
            "settings": asdict(settings),
            "selected_index": self._selected_model_index(),
        }

    def _set_labels_visible(self, visible: bool):
        self._labels_visible = bool(visible)
        self.viewer.set_labels_visible(self._labels_visible)
        state = "on" if self._labels_visible else "off"
        self.statusBar().showMessage(f"Labels {state}")

    def _switch_mode_tab(self):
        if not hasattr(self, "_mode_tabs"):
            return
        enabled_tabs = [btn for btn in self._mode_tabs if btn.isEnabled()]
        if not enabled_tabs:
            return
        current_idx = 0
        for idx, btn in enumerate(enabled_tabs):
            if btn.isChecked():
                current_idx = idx
                break
        next_idx = (current_idx + 1) % len(enabled_tabs)
        enabled_tabs[next_idx].setChecked(True)

    def _show_shortcuts_dialog(self):
        dlg = QtWidgets.QDialog(self)
        dlg.setWindowTitle("Keyboard Shortcuts")
        dlg.setModal(True)
        layout = QtWidgets.QVBoxLayout(dlg)

        tabs = QtWidgets.QTabWidget(dlg)
        grouped = shortcuts_by_category()
        for category, items in grouped.items():
            table = QtWidgets.QTableWidget(len(items), 2, tabs)
            table.setHorizontalHeaderLabels(["Shortcut", "Description"])
            table.verticalHeader().setVisible(False)
            table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
            for row, item in enumerate(items):
                table.setItem(row, 0, QtWidgets.QTableWidgetItem(item.keys))
                table.setItem(row, 1, QtWidgets.QTableWidgetItem(item.label))
            table.horizontalHeader().setStretchLastSection(True)
            tabs.addTab(table, category)

        layout.addWidget(tabs)

        btn_row = QtWidgets.QHBoxLayout()
        btn_row.addStretch(1)
        close_btn = QtWidgets.QPushButton("Close", dlg)
        close_btn.clicked.connect(dlg.close)
        btn_row.addWidget(close_btn)
        layout.addLayout(btn_row)

        dlg.resize(760, 520)
        dlg.exec_()

    def _select_all_models(self):
        lw = self.model_panel.list_widget
        if lw.count() == 0:
            return
        lw.selectAll()
        item = lw.currentItem() or lw.item(0)
        if item is None:
            return
        model_id = item.data(QtCore.Qt.UserRole)
        self.current_model_id = model_id
        self.viewer.set_selected_model(model_id)
        self.statusBar().showMessage("Selected all models")

    def _selected_model_ids(self):
        lw = self.model_panel.list_widget
        selected = []
        for row in range(lw.count()):
            item = lw.item(row)
            if item is not None and item.isSelected():
                selected.append(item.data(QtCore.Qt.UserRole))
        if not selected and self.current_model_id is not None:
            selected.append(self.current_model_id)
        return selected

    def _copy_selected(self):
        model_ids = self._selected_model_ids()
        if not model_ids:
            return
        payloads = self._capture_models_payload(model_ids)
        if not payloads:
            return
        self._model_clipboard = payloads
        self.statusBar().showMessage(f"Copied {len(payloads)} model(s)")

    def _cut_selected(self):
        model_ids = self._selected_model_ids()
        if not model_ids:
            return
        payloads = self._capture_models_payload(model_ids)
        if not payloads:
            return
        self._model_clipboard = payloads
        self._remove_models(model_ids)
        self.statusBar().showMessage(f"Cut {len(payloads)} model(s)")

    def _paste_clipboard(self):
        if not self._model_clipboard:
            return
        new_ids = self._apply_model_payloads(self._model_clipboard, offset_step=(10.0, 10.0, 0.0))
        if new_ids:
            self._push_undo_state()
            self.statusBar().showMessage(f"Pasted {len(new_ids)} model(s)")

    def _clone_selected(self):
        model_ids = self._selected_model_ids()
        if not model_ids:
            return
        payloads = self._capture_models_payload(model_ids)
        if not payloads:
            return
        new_ids = self._apply_model_payloads(payloads, offset_step=(10.0, 10.0, 0.0))
        if new_ids:
            self._push_undo_state()
            self.statusBar().showMessage(f"Cloned {len(new_ids)} model(s)")

    def _capture_models_payload(self, model_ids):
        payloads = []
        for model_id in model_ids:
            payload = self._capture_model_payload(model_id)
            if payload is not None:
                payloads.append(payload)
        return payloads

    def _capture_model_payload(self, model_id: int):
        m = self.viewer.models.get(model_id)
        if not m:
            return None
        return {
            "name": m.get("name", f"Model {model_id}"),
            "path": m.get("path", ""),
            "base_vertices": np.asarray(m.get("base_vertices", []), dtype=float).copy(),
            "faces": np.asarray(m.get("faces", []), dtype=int).copy(),
            "scale": self._scale_to_vec(m.get("scale", 1.0)),
            "rotation": self._vec3(m.get("rotation", [0.0, 0.0, 0.0])),
            "offset": self._vec3(m.get("offset", [0.0, 0.0, 0.0])),
        }

    def _apply_model_payloads(self, payloads, offset_step=(0.0, 0.0, 0.0)):
        if not payloads:
            return []
        new_ids = []
        for idx, payload in enumerate(payloads):
            model_id = self.viewer.add_model_from_data(
                payload["name"],
                payload["path"],
                payload["base_vertices"],
                payload["faces"],
            )
            delta = np.array(offset_step, dtype=float) * float(idx + 1)
            offset = np.array(payload["offset"], dtype=float) + delta
            self.viewer.set_model_transform(
                model_id,
                scale=payload["scale"],
                rotation_xyz=payload["rotation"],
                offset_xyz=offset,
            )
            self.model_panel.add_model(payload["name"], model_id)
            new_ids.append(model_id)
        if new_ids:
            self._select_model_in_panel(new_ids[-1])
            self.current_model_id = new_ids[-1]
            self.viewer.set_selected_model(new_ids[-1])
            self._sync_popups()
        return new_ids

    def _remove_models(self, model_ids):
        model_ids = [mid for mid in model_ids if mid in self.viewer.models]
        if not model_ids:
            return
        lw = self.model_panel.list_widget
        block = lw.blockSignals(True)
        try:
            for model_id in model_ids:
                self.viewer.remove_model(model_id)
                self.model_panel.remove_model(model_id)
        finally:
            lw.blockSignals(block)

        remaining = self.viewer.get_model_ids()
        self.current_model_id = remaining[0] if remaining else None
        self.viewer.set_selected_model(self.current_model_id)
        if self.current_model_id is not None:
            self._select_model_in_panel(self.current_model_id)
        else:
            self.model_panel.list_widget.clearSelection()
        if len(model_ids) == 1:
            self.statusBar().showMessage("Model removed")
        else:
            self.statusBar().showMessage(f"Removed {len(model_ids)} models")
        self._sync_popups()
        self._push_undo_state()

    def _select_model_in_panel(self, model_id: int):
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

    def _selected_model_index(self):
        model_ids = list(self.viewer.models.keys())
        if self.current_model_id in model_ids:
            return model_ids.index(self.current_model_id)
        return None

    def _vec3(self, value, default=(0.0, 0.0, 0.0)) -> np.ndarray:
        if value is None:
            return np.array(default, dtype=float)
        try:
            arr = np.asarray(value, dtype=float).reshape(-1)
        except Exception:
            return np.array(default, dtype=float)
        if arr.size != 3:
            return np.array(default, dtype=float)
        return arr.astype(float)

    def _scale_to_vec(self, scale) -> np.ndarray:
        if isinstance(scale, np.ndarray):
            arr = scale.astype(float).reshape(-1)
            if arr.size == 3:
                return arr
            if arr.size == 1:
                val = float(arr[0])
                return np.array([val, val, val], dtype=float)
        if isinstance(scale, (list, tuple)) and len(scale) == 3:
            return np.array([float(scale[0]), float(scale[1]), float(scale[2])], dtype=float)
        try:
            val = float(scale)
        except Exception:
            val = 1.0
        return np.array([val, val, val], dtype=float)

    def _capture_state(self):
        model_ids = list(self.viewer.models.keys())
        selected_index = self._selected_model_index()
        payloads = self._capture_models_payload(model_ids)
        return {
            "models": payloads,
            "selected_index": selected_index,
        }

    def _state_signature(self, state) -> tuple:
        model_sigs = []
        for payload in state.get("models", []):
            scale = tuple(float(v) for v in np.asarray(payload["scale"], dtype=float).reshape(-1))
            rotation = tuple(float(v) for v in np.asarray(payload["rotation"], dtype=float).reshape(-1))
            offset = tuple(float(v) for v in np.asarray(payload["offset"], dtype=float).reshape(-1))
            verts_shape = np.asarray(payload["base_vertices"]).shape
            faces_shape = np.asarray(payload["faces"]).shape
            model_sigs.append(
                (
                    payload.get("name", ""),
                    payload.get("path", ""),
                    scale,
                    rotation,
                    offset,
                    verts_shape,
                    faces_shape,
                )
            )
        return (state.get("selected_index"), tuple(model_sigs))

    def _push_undo_state(self):
        if self._undo_in_progress:
            return
        if self._pending_undo_snapshot:
            self._undo_timer.stop()
            self._pending_undo_snapshot = False
        state = self._capture_state()
        signature = self._state_signature(state)
        if self._undo_stack and self._undo_stack[-1].get("signature") == signature:
            return
        state["signature"] = signature
        self._undo_stack.append(state)
        if len(self._undo_stack) > self._undo_stack_limit:
            self._undo_stack.pop(0)
        self._redo_stack.clear()
        self._update_undo_redo_state()

    def _schedule_undo_snapshot(self, delay_ms: int = 250):
        if self._undo_in_progress:
            return
        self._pending_undo_snapshot = True
        self._undo_timer.start(delay_ms)

    def _finalize_undo_snapshot(self):
        if not self._pending_undo_snapshot:
            return
        self._pending_undo_snapshot = False
        self._push_undo_state()

    def _restore_state(self, state):
        self._undo_in_progress = True
        try:
            lw = self.model_panel.list_widget
            block = lw.blockSignals(True)
            try:
                self.viewer.clear_all_models()
                self.model_panel.list_widget.clear()
                new_ids = []
                for payload in state.get("models", []):
                    model_id = self.viewer.add_model_from_data(
                        payload["name"],
                        payload["path"],
                        payload["base_vertices"],
                        payload["faces"],
                    )
                    self.model_panel.add_model(payload["name"], model_id)
                    self.viewer.set_model_transform(
                        model_id,
                        scale=payload["scale"],
                        rotation_xyz=payload["rotation"],
                        offset_xyz=payload["offset"],
                    )
                    new_ids.append(model_id)
            finally:
                lw.blockSignals(block)

            selected_index = state.get("selected_index")
            selected_id = None
            if new_ids:
                if selected_index is not None and 0 <= selected_index < len(new_ids):
                    selected_id = new_ids[selected_index]
                else:
                    selected_id = new_ids[-1]
            self.current_model_id = selected_id
            self.viewer.set_selected_model(selected_id)
            if selected_id is not None:
                self._select_model_in_panel(selected_id)
            else:
                self.model_panel.list_widget.clearSelection()
            self._sync_popups()
        finally:
            self._undo_in_progress = False
        self._update_undo_redo_state()

    def _undo(self):
        if len(self._undo_stack) <= 1:
            return
        current = self._undo_stack.pop()
        self._redo_stack.append(current)
        self._restore_state(self._undo_stack[-1])

    def _redo(self):
        if not self._redo_stack:
            return
        state = self._redo_stack.pop()
        self._undo_stack.append(state)
        self._restore_state(state)

    def _update_undo_redo_state(self):
        can_undo = len(self._undo_stack) > 1
        can_redo = bool(self._redo_stack)
        if hasattr(self, "_undo_action"):
            self._undo_action.setEnabled(can_undo)
        if hasattr(self, "_redo_action"):
            self._redo_action.setEnabled(can_redo)
        if hasattr(self, "_undo_btn"):
            self._undo_btn.setEnabled(can_undo)
        if hasattr(self, "_redo_btn"):
            self._redo_btn.setEnabled(can_redo)

    def _delete_selected_model(self):
        model_ids = self._selected_model_ids()
        if not model_ids:
            return
        self._remove_models(model_ids)

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

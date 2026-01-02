import os

from PyQt5 import QtWidgets, QtGui, QtCore

from ..theme import THEMES, get_theme_name, theme_css, theme_qcolor
from ..shortcuts import shortcut_key, shortcut_label, shortcuts_by_category
from config.defaults import DEFAULTS

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets")


class SharedView(QtCore.QObject):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main = main_window

    def build_menubar(self):
        menubar = self.main.menuBar()
        menubar.setVisible(False)

        self.main._file_menu = QtWidgets.QMenu("File", self.main)
        self.main._edit_menu = QtWidgets.QMenu("Edit", self.main)
        self.main._view_menu = QtWidgets.QMenu("View", self.main)
        self.main._prefs_menu = QtWidgets.QMenu("Preferences", self.main)
        self.main._calib_menu = QtWidgets.QMenu("Calibration", self.main)
        self.main._help_menu = QtWidgets.QMenu("Help", self.main)
        self.main._main_menu = QtWidgets.QMenu(self.main)

        new_action = QtWidgets.QAction(shortcut_label("new_project"), self.main)
        new_action.setIcon(self._maybe_icon("menu_new.png"))
        new_action.setShortcut(shortcut_key("new_project"))
        new_action.triggered.connect(self.main._new_project)

        self.main.open_action = QtWidgets.QAction(shortcut_label("open_project"), self.main)
        self.main.open_action.setIcon(self._maybe_icon("menu_open.png"))
        self.main.open_action.setShortcut(shortcut_key("open_project"))
        self.main.open_action.triggered.connect(self.main._open_project)

        recent_menu = QtWidgets.QMenu("Recent Projects", self.main._file_menu)
        recent_menu.setIcon(self._maybe_icon("menu_recent.png"))
        recent_menu.setEnabled(False)

        save_action = QtWidgets.QAction(shortcut_label("save_project"), self.main)
        save_action.setIcon(self._maybe_icon("menu_save.png"))
        save_action.setShortcut(shortcut_key("save_project"))
        save_action.triggered.connect(self.main._save_project)
        self.main._save_action = save_action

        save_as_action = QtWidgets.QAction(shortcut_label("save_project_as"), self.main)
        save_as_action.setIcon(self._maybe_icon("menu_save_as.png"))
        save_as_action.setShortcut(shortcut_key("save_project_as"))
        save_as_action.triggered.connect(self.main._save_project_as)
        self.main._save_as_action = save_as_action

        import_menu = QtWidgets.QMenu("Import", self.main._file_menu)
        import_menu.setIcon(self._maybe_icon("menu_import.png"))
        import_stl_action = QtWidgets.QAction("Import STL(s)...", self.main)
        import_stl_action.setIcon(self._maybe_icon("menu_import_stl.png"))
        import_stl_action.setShortcut(shortcut_key("import_geometry"))
        import_stl_action.triggered.connect(self.main.open_stl_dialog)
        import_menu.addAction(import_stl_action)

        export_menu = QtWidgets.QMenu("Export", self.main._file_menu)
        export_menu.setIcon(self._maybe_icon("menu_export.png"))
        export_action = QtWidgets.QAction("Export G-code...", self.main)
        export_action.setIcon(self._maybe_icon("menu_export_gcode.png"))
        export_action.setShortcut(shortcut_key("export_gcode"))
        export_action.triggered.connect(self.main.export_gcode)
        export_menu.addAction(export_action)

        quit_action = QtWidgets.QAction("Quit", self.main)
        quit_action.setIcon(self._maybe_icon("menu_quit.png"))
        quit_action.triggered.connect(self.main.close)
        self.main._file_menu.addActions([new_action, self.main.open_action])
        self.main._file_menu.addMenu(recent_menu)
        self.main._file_menu.addSeparator()
        self.main._file_menu.addActions([save_action, save_as_action])
        self.main._file_menu.addSeparator()
        self.main._file_menu.addMenu(import_menu)
        self.main._file_menu.addMenu(export_menu)
        self.main._file_menu.addSeparator()
        self.main._file_menu.addActions([quit_action])

        self._build_edit_menu()
        self._build_view_menu()
        self._build_prefs_menu()
        self._build_calib_menu()
        self._build_help_menu()

        theme_menu = self.main._view_menu.addMenu("Theme")
        self.main._theme_menu = theme_menu
        self.main._theme_group = QtWidgets.QActionGroup(self.main)
        self.main._theme_group.setExclusive(True)
        current_theme = get_theme_name()
        for name in THEMES.keys():
            label = name.capitalize()
            action = QtWidgets.QAction(label, self.main)
            action.setCheckable(True)
            action.setData(name)
            if name == current_theme:
                action.setChecked(True)
            action.triggered.connect(self.main._on_theme_selected)
            self.main._theme_group.addAction(action)
            theme_menu.addAction(action)

        self.main._theme_menu_separator = theme_menu.addSeparator()

        customize_action = QtWidgets.QAction("Customize Theme...", self.main)
        customize_action.triggered.connect(self.main._open_theme_editor)
        theme_menu.addAction(customize_action)

        load_action = QtWidgets.QAction("Load Theme...", self.main)
        load_action.triggered.connect(self.main._load_theme_from_file)
        theme_menu.addAction(load_action)

        save_action = QtWidgets.QAction("Save Current Theme...", self.main)
        save_action.triggered.connect(self.main._save_theme_to_file)
        theme_menu.addAction(save_action)

        for menu in (
            self.main._file_menu,
            self.main._edit_menu,
            self.main._view_menu,
            self.main._prefs_menu,
            self.main._calib_menu,
            self.main._help_menu,
        ):
            menubar.addMenu(menu)
            for action in menu.actions():
                self.main.addAction(action)

        self.main._main_menu.addMenu(self.main._edit_menu)
        self.main._main_menu.addMenu(self.main._view_menu)
        self.main._main_menu.addMenu(self.main._prefs_menu)
        self.main._main_menu.addMenu(self.main._calib_menu)
        self.main._main_menu.addMenu(self.main._help_menu)

    def build_topbar(self):
        topbar = QtWidgets.QFrame(self.main)
        topbar.setObjectName("TopBar")
        layout = QtWidgets.QHBoxLayout(topbar)
        margins = DEFAULTS["ui"]["topbar_margins"]
        layout.setContentsMargins(margins[0], margins[1], margins[2], margins[3])
        layout.setSpacing(DEFAULTS["ui"]["topbar_spacing"])

        logo_btn = QtWidgets.QToolButton(topbar)
        logo_btn.setIcon(self._triangle_icon())
        logo_btn.setIconSize(QtCore.QSize(18, 18))
        logo_btn.setAutoRaise(True)
        logo_btn.setCursor(QtCore.Qt.PointingHandCursor)
        layout.addWidget(logo_btn)

        file_btn = QtWidgets.QToolButton(topbar)
        file_btn.setObjectName("FileButton")
        file_btn.setText("File")
        file_btn.setIcon(self._hamburger_icon())
        file_btn.setIconSize(QtCore.QSize(16, 16))
        file_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        file_btn.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        file_btn.setMenu(self.main._file_menu)
        layout.addWidget(file_btn)

        file_caret_btn = QtWidgets.QToolButton(topbar)
        file_caret_btn.setObjectName("CaretButton")
        file_caret_btn.setIcon(self._caret_icon())
        file_caret_btn.setIconSize(QtCore.QSize(12, 12))
        file_caret_btn.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        file_caret_btn.setMenu(self.main._main_menu)
        file_caret_btn.setAutoRaise(True)
        layout.addWidget(file_caret_btn)

        layout.addWidget(self._topbar_separator(topbar))

        save_btn = self._top_icon_btn(topbar, self._save_icon(), "Save", self.main._save_project)
        undo_btn = self._top_icon_btn(topbar, self._undo_icon(), "Undo", self.main._undo)
        redo_btn = self._top_icon_btn(topbar, self._redo_icon(), "Redo", self.main._redo)
        layout.addWidget(save_btn)
        layout.addWidget(undo_btn)
        layout.addWidget(redo_btn)

        layout.addStretch(1)

        mode_tabs = []
        mode_group = QtWidgets.QButtonGroup(self.main)
        for label in ("Prepare", "Preview", "Device"):
            btn = QtWidgets.QToolButton(topbar)
            btn.setText(label)
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            btn.setCursor(QtCore.Qt.PointingHandCursor)
            btn.setObjectName("ModeTab")
            mode_group.addButton(btn)
            layout.addWidget(btn)
            mode_tabs.append(btn)
        if mode_tabs:
            mode_tabs[0].setChecked(True)
        mode_group.buttonClicked.connect(self.main._on_mode_tab_changed)

        self.main.setMenuWidget(topbar)

        self.main._topbar = topbar
        self.main._logo_btn = logo_btn
        self.main._file_btn = file_btn
        self.main._file_caret_btn = file_caret_btn
        self.main._save_btn = save_btn
        self.main._undo_btn = undo_btn
        self.main._redo_btn = redo_btn
        self.main._mode_tabs = mode_tabs
        self.main._mode_group = mode_group

        self.apply_theme()

    def build_shortcut_actions(self):
        self.main._slice_action = QtWidgets.QAction(self.main)
        self.main._slice_action.setShortcut(shortcut_key("slice_plate"))
        self.main._slice_action.triggered.connect(self.main.slice_current_model)
        self.main.addAction(self.main._slice_action)

        self.main._print_action = QtWidgets.QAction(self.main)
        self.main._print_action.setShortcut(shortcut_key("print_plate"))
        self.main._print_action.triggered.connect(self.main._open_device_view)
        self.main.addAction(self.main._print_action)

        self.main._switch_tab_action = QtWidgets.QAction(self.main)
        self.main._switch_tab_action.setShortcut(shortcut_key("switch_table_page"))
        self.main._switch_tab_action.triggered.connect(self.main._switch_mode_tab)
        self.main.addAction(self.main._switch_tab_action)

        self.main._3dconnexion_action = QtWidgets.QAction(self.main)
        self.main._3dconnexion_action.setShortcut(shortcut_key("show_3dconnexion"))
        self.main._3dconnexion_action.triggered.connect(self.main._not_implemented)
        self.main.addAction(self.main._3dconnexion_action)

    def apply_theme(self):
        if not hasattr(self.main, "_topbar"):
            return
        self.main._topbar.setStyleSheet(
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
        self.main._file_btn.setIcon(self._hamburger_icon())
        self.main._file_caret_btn.setIcon(self._caret_icon())
        self.main._logo_btn.setIcon(self._triangle_icon())
        for btn, icon_fn in (
            (self.main._save_btn, self._save_icon),
            (self.main._undo_btn, self._undo_icon),
            (self.main._redo_btn, self._redo_icon),
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
            self.main._file_menu,
            self.main._edit_menu,
            self.main._view_menu,
            self.main._prefs_menu,
            self.main._calib_menu,
            self.main._help_menu,
            self.main._main_menu,
        ):
            menu.setStyleSheet(menu_style)

    def show_shortcuts_dialog(self):
        dlg = QtWidgets.QDialog(self.main)
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

    def _build_edit_menu(self):
        undo_action = QtWidgets.QAction(shortcut_label("undo"), self.main)
        undo_action.setShortcut(shortcut_key("undo"))
        undo_action.triggered.connect(self.main._undo)
        self.main._edit_menu.addAction(undo_action)
        self.main._undo_action = undo_action

        redo_action = QtWidgets.QAction(shortcut_label("redo"), self.main)
        redo_action.setShortcut(shortcut_key("redo"))
        redo_action.triggered.connect(self.main._redo)
        self.main._edit_menu.addAction(redo_action)
        self.main._redo_action = redo_action

        self.main._edit_menu.addSeparator()

        cut_action = QtWidgets.QAction(shortcut_label("cut"), self.main)
        cut_action.setShortcut(shortcut_key("cut"))
        cut_action.triggered.connect(self.main._cut_selected)
        self.main._edit_menu.addAction(cut_action)

        copy_action = QtWidgets.QAction(shortcut_label("copy"), self.main)
        copy_action.setShortcut(shortcut_key("copy"))
        copy_action.triggered.connect(self.main._copy_selected)
        self.main._edit_menu.addAction(copy_action)

        paste_action = QtWidgets.QAction(shortcut_label("paste"), self.main)
        paste_action.setShortcut(shortcut_key("paste"))
        paste_action.triggered.connect(self.main._paste_clipboard)
        self.main._edit_menu.addAction(paste_action)

        delete_selected_action = QtWidgets.QAction(shortcut_label("delete_selected"), self.main)
        delete_selected_action.setShortcut(shortcut_key("delete_selected"))
        delete_selected_action.triggered.connect(self.main._delete_selected_model)
        self.main._edit_menu.addAction(delete_selected_action)

        delete_all_action = QtWidgets.QAction(shortcut_label("delete_all"), self.main)
        delete_all_action.setShortcut(shortcut_key("delete_all"))
        delete_all_action.triggered.connect(self.main._clear_all_models)
        self.main._edit_menu.addAction(delete_all_action)

        clone_action = QtWidgets.QAction(shortcut_label("clone_selected"), self.main)
        clone_action.setShortcut(shortcut_key("clone_selected"))
        clone_action.triggered.connect(self.main._clone_selected)
        self.main._edit_menu.addAction(clone_action)

        self.main._edit_menu.addSeparator()

        select_all_action = QtWidgets.QAction(shortcut_label("select_all"), self.main)
        select_all_action.setShortcut(shortcut_key("select_all"))
        select_all_action.triggered.connect(self.main._select_all_models)
        self.main._edit_menu.addAction(select_all_action)

        deselect_action = QtWidgets.QAction(shortcut_label("deselect_all"), self.main)
        deselect_action.setShortcut(shortcut_key("deselect_all"))
        deselect_action.triggered.connect(self.main._deselect_all_models)
        self.main._edit_menu.addAction(deselect_action)

    def _build_view_menu(self):
        default_view = QtWidgets.QAction(shortcut_label("view_default"), self.main)
        default_view.setShortcut(shortcut_key("view_default"))
        default_view.triggered.connect(self.main.viewer.reset_view)
        self.main._view_menu.addAction(default_view)

        view_actions = [
            ("view_top", (0.0, 90.0)),
            ("view_bottom", (0.0, -90.0)),
            ("view_front", (90.0, 0.0)),
            ("view_rear", (-90.0, 0.0)),
            ("view_left", (180.0, 0.0)),
            ("view_right", (0.0, 0.0)),
        ]
        for action_id, (az, el) in view_actions:
            action = QtWidgets.QAction(shortcut_label(action_id), self.main)
            action.setShortcut(shortcut_key(action_id))
            action.triggered.connect(lambda _=False, a=az, e=el: self.main._set_view_preset(a, e))
            self.main._view_menu.addAction(action)

        self.main._view_menu.addSeparator()

        self.main._projection_group = QtWidgets.QActionGroup(self.main)
        perspective_action = QtWidgets.QAction("Use Perspective View", self.main)
        perspective_action.setCheckable(True)
        ortho_action = QtWidgets.QAction("Use Orthogonal View", self.main)
        ortho_action.setCheckable(True)
        self.main._projection_group.addAction(perspective_action)
        self.main._projection_group.addAction(ortho_action)
        perspective_action.setChecked(True)
        perspective_action.triggered.connect(lambda: self.main._set_projection_mode("perspective"))
        ortho_action.triggered.connect(lambda: self.main._set_projection_mode("ortho"))
        self.main._view_menu.addAction(perspective_action)
        self.main._view_menu.addAction(ortho_action)

        self.main._view_menu.addSeparator()

        wireframe_action = QtWidgets.QAction("Show Wireframe", self.main)
        wireframe_action.triggered.connect(self.main._not_implemented)
        self.main._view_menu.addAction(wireframe_action)

        gcode_action = QtWidgets.QAction("Show G-code Window", self.main)
        gcode_action.setEnabled(False)
        self.main._view_menu.addAction(gcode_action)

        navigator_action = QtWidgets.QAction("Show 3D Navigator", self.main)
        navigator_action.setCheckable(True)
        navigator_action.setChecked(True)
        navigator_action.triggered.connect(self.main._toggle_view_cube)
        self.main._view_menu.addAction(navigator_action)

        reset_layout_action = QtWidgets.QAction("Reset Window Layout", self.main)
        reset_layout_action.triggered.connect(self.main._reset_window_layout)
        self.main._view_menu.addAction(reset_layout_action)

        self.main._view_menu.addSeparator()

        labels_action = QtWidgets.QAction(shortcut_label("show_labels"), self.main)
        labels_action.setShortcut(shortcut_key("show_labels"))
        labels_action.setCheckable(True)
        labels_action.setChecked(False)
        labels_action.toggled.connect(self.main._set_labels_visible)
        self.main._view_menu.addAction(labels_action)
        self.main._labels_action = labels_action

        overhang_action = QtWidgets.QAction("Show Overhang", self.main)
        overhang_action.triggered.connect(self.main._not_implemented)
        self.main._view_menu.addAction(overhang_action)

    def _build_prefs_menu(self):
        prefs_action = QtWidgets.QAction(shortcut_label("preferences"), self.main)
        prefs_action.setShortcut(shortcut_key("preferences"))
        prefs_action.triggered.connect(self.main._show_settings_panel)
        self.main._prefs_menu.addAction(prefs_action)

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
            action = QtWidgets.QAction(label, self.main)
            action.triggered.connect(self.main._not_implemented)
            self.main._calib_menu.addAction(action)

    def _build_help_menu(self):
        for label in (
            "Keyboard Shortcuts",
            "Show Configuration Folder",
            "Check for Updates",
        ):
            action = QtWidgets.QAction(label, self.main)
            if label == "Keyboard Shortcuts":
                action.setShortcut(shortcut_key("show_shortcuts"))
                action.triggered.connect(self.show_shortcuts_dialog)
            else:
                action.triggered.connect(self.main._not_implemented)
            self.main._help_menu.addAction(action)

        self.main._help_menu.addSeparator()

        for label in (
            "User Course",
            "About Us",
            "User Feedback",
            "Log View",
            "User Guide",
        ):
            action = QtWidgets.QAction(label, self.main)
            action.triggered.connect(self.main._not_implemented)
            self.main._help_menu.addAction(action)

    def _topbar_separator(self, parent):
        sep = QtWidgets.QFrame(parent)
        sep.setFrameShape(QtWidgets.QFrame.VLine)
        sep.setFrameShadow(QtWidgets.QFrame.Sunken)
        sep.setStyleSheet(f"color: {theme_css('topbar_border')};")
        sep.setFixedHeight(20)
        return sep

    def _top_icon_btn(self, parent, icon: QtGui.QIcon, tooltip: str, slot):
        btn = QtWidgets.QToolButton(parent)
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
        painter = QtGui.QPainter(pm)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        color = theme_qcolor("topbar_icon")
        pen = QtGui.QPen(color, 2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(color))

        if kind == "hamburger":
            for y in (4, 9, 14):
                painter.drawLine(3, y, size - 3, y)
        elif kind == "caret":
            pts = [QtCore.QPointF(4, 6), QtCore.QPointF(size - 4, 6), QtCore.QPointF(size / 2, 12)]
            painter.drawPolygon(QtGui.QPolygonF(pts))
        elif kind == "triangle":
            pts = [QtCore.QPointF(size / 2, 2), QtCore.QPointF(size - 2, size - 2), QtCore.QPointF(2, size - 2)]
            painter.setBrush(QtGui.QBrush(theme_qcolor("topbar_accent")))
            painter.setPen(QtGui.QPen(theme_qcolor("topbar_accent"), 2))
            painter.drawPolygon(QtGui.QPolygonF(pts))
        elif kind == "save":
            painter.drawRect(4, 4, size - 8, size - 8)
            painter.drawLine(6, 7, size - 6, 7)
        elif kind == "undo":
            path = QtGui.QPainterPath()
            path.moveTo(12, 5)
            path.cubicTo(6, 5, 6, 14, 12, 14)
            painter.drawPath(path)
            painter.drawLine(6, 5, 3, 7)
            painter.drawLine(6, 5, 3, 3)
        elif kind == "redo":
            path = QtGui.QPainterPath()
            path.moveTo(6, 5)
            path.cubicTo(12, 5, 12, 14, 6, 14)
            painter.drawPath(path)
            painter.drawLine(12, 5, 15, 7)
            painter.drawLine(12, 5, 15, 3)
        painter.end()
        return pm

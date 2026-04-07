import os

from PyQt5 import QtWidgets, QtGui, QtCore

from ..i18n import tr
from ..theme import THEMES, get_theme_name, theme_css, theme_qcolor
from ..shortcuts import shortcut_key, shortcut_label, shortcuts_by_category
from ..resource_paths import assets_dir
from config.defaults import DEFAULTS

ASSETS_DIR = assets_dir()


class SharedView(QtCore.QObject):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main = main_window

    @staticmethod
    def _t(key: str, default: str = "", **kwargs: object) -> str:
        return tr(key, default=default, **kwargs)

    def build_menubar(self):
        menubar = self.main.menuBar()
        menubar.setVisible(False)

        self.main._file_menu = QtWidgets.QMenu(self._t("menu.file", "File"), self.main)
        self.main._edit_menu = QtWidgets.QMenu(self._t("menu.edit", "Edit"), self.main)
        self.main._view_menu = QtWidgets.QMenu(self._t("menu.view", "View"), self.main)
        self.main._prefs_menu = QtWidgets.QMenu(self._t("menu.preferences", "Preferences"), self.main)
        self.main._calib_menu = QtWidgets.QMenu(self._t("menu.calibration", "Calibration"), self.main)
        self.main._help_menu = QtWidgets.QMenu(self._t("menu.help", "Help"), self.main)
        self.main._main_menu = QtWidgets.QMenu(self.main)

        new_action = QtWidgets.QAction(shortcut_label("new_project"), self.main)
        new_action.setIcon(self._maybe_icon("menu_new.png"))
        new_action.setShortcut(shortcut_key("new_project"))
        new_action.triggered.connect(self.main._new_project)

        self.main.open_action = QtWidgets.QAction(shortcut_label("open_project"), self.main)
        self.main.open_action.setIcon(self._maybe_icon("menu_open.png"))
        self.main.open_action.setShortcut(shortcut_key("open_project"))
        self.main.open_action.triggered.connect(self.main._open_project)

        recent_menu = QtWidgets.QMenu(self._t("menu.recent_projects", "Recent Projects"), self.main._file_menu)
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

        import_menu = QtWidgets.QMenu(self._t("menu.import", "Import"), self.main._file_menu)
        import_menu.setIcon(self._maybe_icon("menu_import.png"))
        import_stl_action = QtWidgets.QAction(self._t("menu.import_stl", "Import STL(s)..."), self.main)
        import_stl_action.setIcon(self._maybe_icon("menu_import_stl.png"))
        import_stl_action.setShortcut(shortcut_key("import_geometry"))
        import_stl_action.triggered.connect(self.main.open_stl_dialog)
        import_menu.addAction(import_stl_action)

        export_menu = QtWidgets.QMenu(self._t("menu.export", "Export"), self.main._file_menu)
        export_menu.setIcon(self._maybe_icon("menu_export.png"))
        export_action = QtWidgets.QAction(self._t("menu.export_gcode", "Export G-code..."), self.main)
        export_action.setIcon(self._maybe_icon("menu_export_gcode.png"))
        export_action.setShortcut(shortcut_key("export_gcode"))
        export_action.triggered.connect(self.main.export_gcode)
        export_menu.addAction(export_action)

        quit_action = QtWidgets.QAction(self._t("menu.quit", "Quit"), self.main)
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

        theme_menu = self.main._view_menu.addMenu(self._t("menu.theme", "Theme"))
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

        customize_action = QtWidgets.QAction(self._t("menu.customize_theme", "Customize Theme..."), self.main)
        customize_action.triggered.connect(self.main._open_theme_editor)
        theme_menu.addAction(customize_action)

        load_action = QtWidgets.QAction(self._t("menu.load_theme", "Load Theme..."), self.main)
        load_action.triggered.connect(self.main._load_theme_from_file)
        theme_menu.addAction(load_action)

        save_action = QtWidgets.QAction(self._t("menu.save_theme", "Save Current Theme..."), self.main)
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
        topbar_layout = QtWidgets.QVBoxLayout(topbar)
        topbar_layout.setContentsMargins(0, 0, 0, 0)
        topbar_layout.setSpacing(0)

        margins = DEFAULTS["ui"]["topbar_margins"]
        spacing = DEFAULTS["ui"]["topbar_spacing"]

        head_row = QtWidgets.QFrame(topbar)
        head_row.setObjectName("TopBarHead")
        head_layout = QtWidgets.QHBoxLayout(head_row)
        head_layout.setContentsMargins(margins[0], margins[1], margins[2], 2)
        head_layout.setSpacing(spacing)

        logo_btn = QtWidgets.QToolButton(head_row)
        logo_btn.setObjectName("LogoButton")
        logo_btn.setIcon(self._triangle_icon())
        logo_btn.setIconSize(QtCore.QSize(18, 18))
        logo_btn.setAutoRaise(True)
        logo_btn.setCursor(QtCore.Qt.PointingHandCursor)
        head_layout.addWidget(logo_btn)

        file_btn = QtWidgets.QToolButton(head_row)
        file_btn.setObjectName("FileButton")
        file_btn.setText(self._t("topbar.file", "File"))
        file_btn.setIcon(self._hamburger_icon())
        file_btn.setIconSize(QtCore.QSize(16, 16))
        file_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        file_btn.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        file_btn.setMenu(self.main._file_menu)
        head_layout.addWidget(file_btn)

        file_caret_btn = QtWidgets.QToolButton(head_row)
        file_caret_btn.setObjectName("CaretButton")
        file_caret_btn.setIcon(self._caret_icon())
        file_caret_btn.setIconSize(QtCore.QSize(12, 12))
        file_caret_btn.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        file_caret_btn.setMenu(self.main._main_menu)
        file_caret_btn.setAutoRaise(True)
        head_layout.addWidget(file_caret_btn)

        head_layout.addWidget(self._topbar_separator(head_row))

        save_btn = self._top_icon_btn(
            head_row,
            self._save_icon(),
            self._t("topbar.tooltip.save", "Save"),
            self.main._save_project,
        )
        undo_btn = self._top_icon_btn(
            head_row,
            self._undo_icon(),
            self._t("topbar.tooltip.undo", "Undo"),
            self.main._undo,
        )
        redo_btn = self._top_icon_btn(
            head_row,
            self._redo_icon(),
            self._t("topbar.tooltip.redo", "Redo"),
            self.main._redo,
        )
        head_layout.addWidget(save_btn)
        head_layout.addWidget(undo_btn)
        head_layout.addWidget(redo_btn)

        calib_btn = QtWidgets.QToolButton(head_row)
        calib_btn.setObjectName("CalibQuickButton")
        calib_btn.setText(self._t("menu.calibration", "Calibration"))
        calib_btn.setIcon(self._calibration_icon())
        calib_btn.setIconSize(QtCore.QSize(14, 14))
        calib_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        calib_btn.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        calib_btn.setMenu(self.main._calib_menu)
        calib_btn.setCursor(QtCore.Qt.PointingHandCursor)
        head_layout.addWidget(calib_btn)

        head_layout.addStretch(1)

        title_label = QtWidgets.QLabel(self._t("topbar.project_title", "Untitled"), head_row)
        title_label.setObjectName("TopbarProjectTitle")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        head_layout.addWidget(title_label)

        head_layout.addStretch(1)
        topbar_layout.addWidget(head_row)

        mode_row = QtWidgets.QFrame(topbar)
        mode_row.setObjectName("TopBarModes")
        mode_layout = QtWidgets.QHBoxLayout(mode_row)
        mode_layout.setContentsMargins(margins[0], 2, margins[2], margins[3])
        mode_layout.setSpacing(max(4, spacing))

        home_btn = QtWidgets.QToolButton(mode_row)
        home_btn.setObjectName("HomeButton")
        home_btn.setIcon(self._home_icon())
        home_btn.setIconSize(QtCore.QSize(18, 18))
        home_btn.setToolTip(self._t("topbar.tooltip.home", "Home"))
        home_btn.setAutoRaise(True)
        home_btn.setCursor(QtCore.Qt.PointingHandCursor)
        mode_layout.addWidget(home_btn)
        mode_layout.addSpacing(4)

        mode_tabs = []
        mode_group = QtWidgets.QButtonGroup(self.main)
        mode_specs = (
            ("topbar.mode.files", "Files", "files", "files"),
            ("topbar.mode.activity", "Activity", "activity", "activity"),
            ("topbar.mode.prepare", "Prepare", "prepare", "prepare"),
            ("topbar.mode.preview", "Preview", "preview", "preview"),
            ("topbar.mode.device", "Device", "device", "device"),
            ("topbar.mode.project", "Project", "project", "files"),
            ("topbar.mode.calibration", "Calibration", "calibration", "control"),
        )
        for key, fallback, mode_id, mode_route in mode_specs:
            btn = QtWidgets.QToolButton(mode_row)
            btn.setText(self._t(key, fallback))
            btn.setProperty("mode_key", mode_route)
            btn.setProperty("mode_id", mode_id)
            btn.setIcon(self._mode_tab_icon(mode_id))
            btn.setIconSize(QtCore.QSize(14, 14))
            btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            btn.setCursor(QtCore.Qt.PointingHandCursor)
            btn.setObjectName("ModeTab")
            mode_group.addButton(btn)
            mode_layout.addWidget(btn)
            mode_tabs.append(btn)
        if mode_tabs:
            default_tab = None
            for btn in mode_tabs:
                if str(btn.property("mode_key") or "").strip().lower() == "prepare":
                    default_tab = btn
                    break
            (default_tab or mode_tabs[0]).setChecked(True)

        mode_group.buttonClicked.connect(self.main._on_mode_tab_changed)

        mode_layout.addStretch(1)

        slice_btn = QtWidgets.QPushButton(self._t("topbar.action.slice_plate", "Slice plate"), mode_row)
        slice_btn.setObjectName("TopbarActionButton")
        slice_btn.setProperty("kind", "primary")
        slice_handler = getattr(self.main, "slice_current_plate", None)
        if not callable(slice_handler):
            slice_handler = getattr(self.main, "slice_current_model", None)
        if callable(slice_handler):
            slice_btn.clicked.connect(slice_handler)
        mode_layout.addWidget(slice_btn)

        print_btn = QtWidgets.QPushButton(self._t("topbar.action.print", "Select print"), mode_row)
        print_btn.setObjectName("TopbarActionButton")
        print_btn.setProperty("kind", "secondary")
        print_btn.clicked.connect(self.main._open_device_view)
        mode_layout.addWidget(print_btn)

        topbar_layout.addWidget(mode_row)

        def _go_prepare():
            for btn in mode_tabs:
                if str(btn.property("mode_key") or "").strip().lower() == "prepare":
                    btn.setChecked(True)
                    break
            self.main._activate_mode("prepare")

        home_btn.clicked.connect(_go_prepare)

        self.main.setMenuWidget(topbar)

        self.main._topbar = topbar
        self.main._topbar_head = head_row
        self.main._topbar_modes = mode_row
        self.main._logo_btn = logo_btn
        self.main._file_btn = file_btn
        self.main._file_caret_btn = file_caret_btn
        self.main._save_btn = save_btn
        self.main._undo_btn = undo_btn
        self.main._redo_btn = redo_btn
        self.main._calib_btn = calib_btn
        self.main._home_btn = home_btn
        self.main._topbar_title_label = title_label
        self.main._topbar_slice_btn = slice_btn
        self.main._topbar_print_btn = print_btn
        self.main._mode_tabs = mode_tabs
        self.main._mode_group = mode_group

        self.apply_theme()

    def build_shortcut_actions(self):
        self.main._slice_action = QtWidgets.QAction(self.main)
        self.main._slice_action.setShortcut(shortcut_key("slice_plate"))
        slice_handler = getattr(self.main, "slice_current_plate", None)
        if not callable(slice_handler):
            slice_handler = getattr(self.main, "slice_current_model", None)
        if callable(slice_handler):
            self.main._slice_action.triggered.connect(slice_handler)
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
        self.main._3dconnexion_action.triggered.connect(self.main._show_3dconnexion_dialog)
        self.main.addAction(self.main._3dconnexion_action)

    def apply_theme(self):
        if not hasattr(self.main, "_topbar"):
            return
        self.main._topbar.setStyleSheet(
            "QFrame#TopBar {"
            f"  background: {theme_css('topbar_bg')};"
            "}"
            "QFrame#TopBarHead {"
            f"  background: {theme_css('topbar_bg')};"
            f"  border-bottom: 1px solid {theme_css('topbar_border')};"
            "}"
            "QFrame#TopBarModes {"
            f"  background: {theme_css('topbar_bg')};"
            "}"
            "QToolButton {"
            f"  color: {theme_css('topbar_text')};"
            "  border: 1px solid transparent;"
            "  border-radius: 4px;"
            "  padding: 4px 7px;"
            "}"
            "QToolButton:hover {"
            f"  background: {theme_css('menu_hover_bg')};"
            "}"
            "QToolButton:disabled {"
            f"  color: {theme_css('menu_disabled_text')};"
            "}"
            "QToolButton#FileButton {"
            f"  border: 1px solid {theme_css('topbar_accent')};"
            "  padding: 4px 9px;"
            "}"
            "QToolButton#CaretButton {"
            "  padding: 4px;"
            "}"
            "QToolButton#HomeButton {"
            "  padding: 5px;"
            "  border-radius: 4px;"
            "}"
            "QToolButton#ModeTab {"
            "  padding: 6px 10px;"
            "  border-radius: 5px;"
            "}"
            "QToolButton#ModeTab:checked {"
            f"  background: {theme_css('topbar_accent')};"
            f"  color: {theme_css('popup_text')};"
            "  font-weight: 600;"
            "  border: 1px solid transparent;"
            "}"
            "QLabel#TopbarProjectTitle {"
            f"  color: {theme_css('topbar_text')};"
            "  font-weight: 500;"
            "  padding: 0 6px;"
            "}"
            "QPushButton#TopbarActionButton {"
            f"  background: {theme_css('action_button_bg')};"
            f"  color: {theme_css('action_button_text')};"
            f"  border: 1px solid {theme_css('action_panel_border')};"
            "  border-radius: 13px;"
            "  padding: 4px 14px;"
            "  font-weight: 600;"
            "}"
            "QPushButton#TopbarActionButton[kind=\"primary\"] {"
            f"  background: {theme_css('action_button_hover_bg')};"
            "}"
            "QPushButton#TopbarActionButton[kind=\"secondary\"] {"
            f"  background: {theme_css('action_button_bg')};"
            "}"
            "QPushButton#TopbarActionButton:hover {"
            f"  background: {theme_css('action_button_active_bg')};"
            "}"
        )
        self.main._file_btn.setIcon(self._hamburger_icon())
        self.main._file_caret_btn.setIcon(self._caret_icon())
        self.main._logo_btn.setIcon(self._triangle_icon())
        if hasattr(self.main, "_calib_btn") and self.main._calib_btn is not None:
            self.main._calib_btn.setIcon(self._calibration_icon())
        if hasattr(self.main, "_home_btn") and self.main._home_btn is not None:
            self.main._home_btn.setIcon(self._home_icon())
        for btn, icon_fn in (
            (self.main._save_btn, self._save_icon),
            (self.main._undo_btn, self._undo_icon),
            (self.main._redo_btn, self._redo_icon),
        ):
            btn.setIcon(icon_fn())
        for btn in getattr(self.main, "_mode_tabs", []):
            mode_id = str(btn.property("mode_id") or "").strip().lower()
            btn.setIcon(self._mode_tab_icon(mode_id))

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

        dock_border = theme_css("popup_border")
        dock_bg = theme_css("popup_bg")
        dock_text = theme_css("popup_text")
        input_bg = theme_css("popup_input_bg")
        input_border = theme_css("popup_input_border")
        input_text = theme_css("popup_input_text")
        accent = theme_css("topbar_accent")
        hover = theme_css("menu_hover_bg")
        self.main.setStyleSheet(
            "QMainWindow {"
            f"  background: {dock_bg};"
            "}"
            "QDockWidget {"
            f"  border: 1px solid {dock_border};"
            f"  background: {dock_bg};"
            "}"
            "QDockWidget::title {"
            f"  background: {dock_bg};"
            f"  color: {dock_text};"
            f"  border-bottom: 1px solid {dock_border};"
            "  padding: 4px 8px;"
            "}"
            "QDockWidget::close-button, QDockWidget::float-button {"
            "  border: none;"
            "  background: transparent;"
            "}"
            "QMainWindow::separator {"
            f"  background: {dock_border};"
            "  width: 1px;"
            "  height: 1px;"
            "}"
            "QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {"
            f"  background: {input_bg};"
            f"  color: {input_text};"
            f"  border: 1px solid {input_border};"
            "  border-radius: 4px;"
            "  padding: 4px 8px;"
            "  selection-background-color: rgba(58, 116, 255, 110);"
            "}"
            "QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {"
            f"  border: 1px solid {accent};"
            "}"
            "QComboBox QAbstractItemView {"
            f"  background: {input_bg};"
            f"  color: {input_text};"
            f"  border: 1px solid {input_border};"
            f"  selection-background-color: {hover};"
            "}"
            "QTableWidget::item:selected {"
            "  background: rgba(58, 116, 255, 90);"
            "}"
            "QPushButton {"
            f"  background: {theme_css('action_button_bg')};"
            f"  color: {theme_css('action_button_text')};"
            f"  border: 1px solid {theme_css('action_panel_border')};"
            "  border-radius: 4px;"
            "  padding: 6px 10px;"
            "}"
            "QPushButton:hover {"
            f"  background: {theme_css('action_button_hover_bg')};"
            "}"
        )

    def show_shortcuts_dialog(self):
        dlg = QtWidgets.QDialog(self.main)
        dlg.setWindowTitle(self._t("dialog.shortcuts.title", "Keyboard Shortcuts"))
        dlg.setModal(True)
        layout = QtWidgets.QVBoxLayout(dlg)

        tabs = QtWidgets.QTabWidget(dlg)
        grouped = shortcuts_by_category()
        for category, items in grouped.items():
            table = QtWidgets.QTableWidget(len(items), 2, tabs)
            table.setHorizontalHeaderLabels(
                [
                    self._t("dialog.shortcuts.column.shortcut", "Shortcut"),
                    self._t("dialog.shortcuts.column.description", "Description"),
                ]
            )
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
        close_btn = QtWidgets.QPushButton(self._t("dialog.button.close", "Close"), dlg)
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
            ("view_front", (0.0, 0.0)),
            ("view_rear", (180.0, 0.0)),
            ("view_left", (-90.0, 0.0)),
            ("view_right", (90.0, 0.0)),
        ]
        for action_id, (az, el) in view_actions:
            action = QtWidgets.QAction(shortcut_label(action_id), self.main)
            action.setShortcut(shortcut_key(action_id))
            action.triggered.connect(lambda _=False, a=az, e=el: self.main._set_view_preset(a, e))
            self.main._view_menu.addAction(action)

        self.main._view_menu.addSeparator()

        self.main._projection_group = QtWidgets.QActionGroup(self.main)
        perspective_action = QtWidgets.QAction(self._t("menu.view.use_perspective", "Use Perspective View"), self.main)
        perspective_action.setCheckable(True)
        ortho_action = QtWidgets.QAction(self._t("menu.view.use_orthogonal", "Use Orthogonal View"), self.main)
        ortho_action.setCheckable(True)
        self.main._projection_group.addAction(perspective_action)
        self.main._projection_group.addAction(ortho_action)
        perspective_action.setChecked(True)
        perspective_action.triggered.connect(lambda: self.main._set_projection_mode("perspective"))
        ortho_action.triggered.connect(lambda: self.main._set_projection_mode("ortho"))
        self.main._view_menu.addAction(perspective_action)
        self.main._view_menu.addAction(ortho_action)
        self.main._perspective_action = perspective_action
        self.main._ortho_action = ortho_action

        self.main._view_menu.addSeparator()

        wireframe_action = QtWidgets.QAction(self._t("menu.view.show_wireframe", "Show Wireframe"), self.main)
        wireframe_action.setCheckable(True)
        wireframe_action.setChecked(
            bool(getattr(self.main.viewer, "get_wireframe_enabled", lambda: False)())
        )
        wireframe_action.toggled.connect(self.main._toggle_wireframe)
        self.main._view_menu.addAction(wireframe_action)
        self.main._wireframe_action = wireframe_action

        gcode_action = QtWidgets.QAction(self._t("menu.view.show_gcode_window", "Show G-code Window"), self.main)
        gcode_action.setEnabled(False)
        self.main._view_menu.addAction(gcode_action)

        navigator_action = QtWidgets.QAction(self._t("menu.view.show_3d_navigator", "Show 3D Navigator"), self.main)
        navigator_action.setCheckable(True)
        navigator_action.setChecked(True)
        navigator_action.triggered.connect(self.main._toggle_view_cube)
        self.main._view_menu.addAction(navigator_action)

        reset_layout_action = QtWidgets.QAction(self._t("menu.view.reset_window_layout", "Reset Window Layout"), self.main)
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

        overhang_action = QtWidgets.QAction(self._t("menu.view.show_overhang", "Show Overhang"), self.main)
        overhang_action.setCheckable(True)
        overhang_action.setChecked(False)
        overhang_action.toggled.connect(self.main._toggle_overhang)
        self.main._view_menu.addAction(overhang_action)
        self.main._overhang_action = overhang_action

    def _build_prefs_menu(self):
        prefs_action = QtWidgets.QAction(shortcut_label("preferences"), self.main)
        prefs_action.setShortcut(shortcut_key("preferences"))
        prefs_action.triggered.connect(self.main._show_settings_panel)
        self.main._prefs_menu.addAction(prefs_action)

    def _build_calib_menu(self):
        calib_actions = (
            (self._t("menu.calibration.temperature", "Temperature"), self.main._calibrate_temperature),
            (self._t("menu.calibration.flow_rate", "Flow rate"), self.main._calibrate_flow_rate),
            (self._t("menu.calibration.pressure_advance", "Pressure advance"), self.main._calibrate_pressure_advance),
            (self._t("menu.calibration.retraction_test", "Retraction test"), self.main._calibrate_retraction),
            (self._t("menu.calibration.tolerance_test", "Tolerance Test"), self.main._calibrate_tolerance),
            (self._t("menu.calibration.max_flowrate", "Max flowrate"), self.main._calibrate_max_flowrate),
            (self._t("menu.calibration.tutorial", "Tutorial"), self.main._open_calibration_tutorial),
        )
        for label, handler in calib_actions:
            action = QtWidgets.QAction(label, self.main)
            action.triggered.connect(handler)
            self.main._calib_menu.addAction(action)

    def _build_help_menu(self):
        quick_actions = (
            ("menu.help.keyboard_shortcuts", "Keyboard Shortcuts"),
            ("menu.help.show_configuration_folder", "Show Configuration Folder"),
            ("menu.help.check_updates", "Check for Updates"),
        )
        for key, fallback in quick_actions:
            label = self._t(key, fallback)
            action = QtWidgets.QAction(label, self.main)
            if key == "menu.help.keyboard_shortcuts":
                action.setShortcut(shortcut_key("show_shortcuts"))
                action.triggered.connect(self.show_shortcuts_dialog)
            else:
                if key == "menu.help.show_configuration_folder":
                    action.triggered.connect(self.main._open_config_folder)
                else:
                    action.triggered.connect(self.main._check_for_updates)
            self.main._help_menu.addAction(action)

        self.main._help_menu.addSeparator()

        detail_actions = (
            ("menu.help.user_course", "User Course"),
            ("menu.help.about_us", "About Us"),
            ("menu.help.user_feedback", "User Feedback"),
            ("menu.help.log_view", "Log View"),
            ("menu.help.user_guide", "User Guide"),
        )
        for key, fallback in detail_actions:
            label = self._t(key, fallback)
            action = QtWidgets.QAction(label, self.main)
            if key == "menu.help.user_feedback":
                action.triggered.connect(self.main._open_feedback)
            elif key == "menu.help.user_course":
                action.triggered.connect(self.main._open_user_course)
            elif key == "menu.help.about_us":
                action.triggered.connect(self.main._open_about_dialog)
            elif key == "menu.help.log_view":
                action.triggered.connect(self.main._open_log_view)
            elif key == "menu.help.user_guide":
                action.triggered.connect(self.main._open_user_guide)
            else:
                action.triggered.connect(self.main._open_user_guide)
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

    def _home_icon(self):
        icon = self._maybe_icon("top_home.png")
        if not icon.isNull():
            return icon
        return QtGui.QIcon(self._paint_icon("home"))

    def _calibration_icon(self):
        icon = self._maybe_icon("top_calibration.png")
        if not icon.isNull():
            return icon
        return QtGui.QIcon(self._paint_icon("calibration"))

    def _mode_tab_icon(self, mode_id: str):
        mode_key = str(mode_id or "").strip().lower()
        if mode_key in (
            "files",
            "activity",
            "prepare",
            "preview",
            "device",
            "project",
            "calibration",
        ):
            return QtGui.QIcon(self._paint_icon(mode_key))
        return QtGui.QIcon(self._paint_icon("triangle"))

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
        elif kind == "home":
            painter.setBrush(QtCore.Qt.NoBrush)
            house = QtGui.QPolygonF(
                [
                    QtCore.QPointF(3, 8),
                    QtCore.QPointF(9, 3),
                    QtCore.QPointF(15, 8),
                    QtCore.QPointF(15, 15),
                    QtCore.QPointF(3, 15),
                ]
            )
            painter.drawPolygon(house)
            painter.drawLine(9, 15, 9, 11)
        elif kind == "prepare":
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.drawPolygon(
                QtGui.QPolygonF(
                    [
                        QtCore.QPointF(9, 3),
                        QtCore.QPointF(14, 6),
                        QtCore.QPointF(9, 9),
                        QtCore.QPointF(4, 6),
                    ]
                )
            )
            painter.drawLine(4, 6, 4, 12)
            painter.drawLine(14, 6, 14, 12)
            painter.drawLine(4, 12, 9, 15)
            painter.drawLine(9, 15, 14, 12)
        elif kind == "files":
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.drawRect(3, 4, 12, 10)
            painter.drawLine(6, 7, 12, 7)
            painter.drawLine(6, 10, 12, 10)
        elif kind == "activity":
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.drawPolyline(
                QtGui.QPolygonF(
                    [
                        QtCore.QPointF(3, 11),
                        QtCore.QPointF(6, 8),
                        QtCore.QPointF(9, 10),
                        QtCore.QPointF(12, 5),
                        QtCore.QPointF(15, 8),
                    ]
                )
            )
        elif kind == "preview":
            painter.setBrush(QtCore.Qt.NoBrush)
            for idx in range(3):
                painter.drawRoundedRect(QtCore.QRectF(3.5, 4.0 + (idx * 4.0), 11.0, 2.3), 0.9, 0.9)
        elif kind == "device":
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.drawRect(4, 4, 4, 4)
            painter.drawRect(10, 4, 4, 4)
            painter.drawRect(4, 10, 4, 4)
            painter.drawRect(10, 10, 4, 4)
        elif kind == "project":
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.drawRect(4, 5, 10, 9)
            painter.drawLine(6, 7, 12, 7)
            painter.drawLine(6, 10, 12, 10)
        elif kind == "calibration":
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.drawEllipse(QtCore.QPointF(9, 9), 3.5, 3.5)
            painter.drawLine(9, 2, 9, 4)
            painter.drawLine(9, 14, 9, 16)
            painter.drawLine(2, 9, 4, 9)
            painter.drawLine(14, 9, 16, 9)
        painter.end()
        return pm

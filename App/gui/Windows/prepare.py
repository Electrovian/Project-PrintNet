from PyQt5 import QtWidgets, QtCore

from ..viewer import Viewer3D
from ..settings_panel import SettingsPanel
from ..controls import TransformToolbar
from ..model_panel import ModelPanel
from ..popups import MovePopup, RotatePopup, ScalePopup, AutoOrientPopup, ArrangePopup
from ..theme import theme_css


class PrepareView(QtCore.QObject):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main = main_window
        self.viewer = Viewer3D(main_window)

        self._build_docks()
        self._build_toolbar()
        self._build_popups()
        self._build_action_panel()

        self.main.viewer = self.viewer

    def _build_docks(self):
        settings_panel = SettingsPanel(self.main)
        settings_dock = QtWidgets.QDockWidget("Printer", self.main)
        settings_dock.setWidget(settings_panel)
        settings_dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.main.addDockWidget(QtCore.Qt.RightDockWidgetArea, settings_dock)

        model_panel = ModelPanel(self.main)
        model_dock = QtWidgets.QDockWidget("Models", self.main)
        model_dock.setWidget(model_panel)
        model_dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.main.addDockWidget(QtCore.Qt.LeftDockWidgetArea, model_dock)

        self.settings_panel = settings_panel
        self.model_panel = model_panel
        self._settings_dock = settings_dock
        self._model_dock = model_dock

        self.main.settings_panel = settings_panel
        self.main.model_panel = model_panel
        self.main._settings_dock = settings_dock
        self.main._model_dock = model_dock

    def _build_toolbar(self):
        toolbar = TransformToolbar(self.main)
        self.main.addToolBar(QtCore.Qt.TopToolBarArea, toolbar)
        toolbar.setMovable(False)
        toolbar.addRequested.connect(self.main.open_stl_dialog)
        toolbar.moveRequested.connect(self.main._on_move_tool)
        toolbar.rotateRequested.connect(self.main._on_rotate_tool)
        toolbar.scaleRequested.connect(self.main._on_scale_tool)
        toolbar.autoOrientRequested.connect(self.main._on_auto_orient_tool)
        toolbar.autoArrangeRequested.connect(self.main._on_arrange_tool)
        toolbar.layOnFaceRequested.connect(self.main._lay_on_face)

        self.transform_toolbar = toolbar
        self.main.transform_toolbar = toolbar

    def _build_popups(self):
        self.main._popup_move = MovePopup(self.main)
        self.main._popup_rotate = RotatePopup(self.main)
        self.main._popup_scale = ScalePopup(self.main)
        self.main._popup_auto_orient = AutoOrientPopup(self.main)
        self.main._popup_arrange = ArrangePopup(self.main)
        for popup in (
            self.main._popup_move,
            self.main._popup_rotate,
            self.main._popup_scale,
            self.main._popup_auto_orient,
            self.main._popup_arrange,
        ):
            popup.hide()

        self.main._popup_move.position_changed.connect(self.main._on_transform_position_changed)
        self.main._popup_move.center_requested.connect(self.main._on_transform_center_requested)
        self.main._popup_rotate.rotation_changed.connect(self.main._on_transform_rotation_changed)
        self.main._popup_rotate.reset_requested.connect(self.main._on_transform_rotation_reset)
        self.main._popup_scale.scale_changed.connect(self.main._on_transform_scale_changed)
        self.main._popup_auto_orient.orient_requested.connect(self.main._on_auto_orient_requested)
        self.main._popup_auto_orient.reset_requested.connect(self.main._on_auto_orient_reset)
        self.main._popup_arrange.arrange_requested.connect(self.main._on_arrange_requested)
        self.main._popup_arrange.arrange_selected_requested.connect(self.main._on_arrange_selected_requested)
        self.main._popup_arrange.reset_requested.connect(self.main._on_arrange_reset)

    def _build_action_panel(self):
        self._action_panel = QtWidgets.QFrame(self.viewer)
        self._action_panel.setObjectName("ActionPanel")
        action_layout = QtWidgets.QVBoxLayout(self._action_panel)
        action_layout.setContentsMargins(10, 8, 10, 8)
        action_layout.setSpacing(6)

        self._slice_btn = QtWidgets.QPushButton("Slice plate", self._action_panel)
        self._slice_btn.clicked.connect(self.main.slice_current_model)
        action_layout.addWidget(self._slice_btn)

        self._print_btn = QtWidgets.QPushButton("Send print", self._action_panel)
        self._print_btn.clicked.connect(self.main._open_device_view)
        action_layout.addWidget(self._print_btn)

    def position_panels(self):
        margin = 16
        self._action_panel.adjustSize()
        x = max(0, self.viewer.width() - self._action_panel.width() - margin)
        y = max(0, self.viewer.height() - self._action_panel.height() - margin)
        self._action_panel.move(x, y)

    def show(self):
        for dock in (self._settings_dock, self._model_dock):
            dock.show()
        self.transform_toolbar.show()
        self._action_panel.show()
        self._action_panel.raise_()
        self.position_panels()

    def hide(self):
        for dock in (self._settings_dock, self._model_dock):
            dock.hide()
        self.transform_toolbar.hide()
        self._action_panel.hide()
        for popup in (
            self.main._popup_move,
            self.main._popup_rotate,
            self.main._popup_scale,
            self.main._popup_auto_orient,
            self.main._popup_arrange,
        ):
            popup.hide()

    def apply_theme(self):
        self.viewer.apply_theme()
        if hasattr(self, "settings_panel") and hasattr(self.settings_panel, "apply_theme"):
            self.settings_panel.apply_theme()
        action_border = theme_css("action_panel_border")
        action_bg = theme_css("action_panel_bg")
        self._action_panel.setStyleSheet(
            "QFrame#ActionPanel {"
            f"  background: {action_bg};"
            f"  border: 1px solid {action_border};"
            "  border-radius: 6px;"
            "}"
            "QPushButton {"
            f"  background: {theme_css('action_button_bg')};"
            f"  color: {theme_css('action_button_text')};"
            f"  border: 1px solid {action_border};"
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
        for popup in (
            self.main._popup_move,
            self.main._popup_rotate,
            self.main._popup_scale,
            self.main._popup_auto_orient,
            self.main._popup_arrange,
        ):
            popup.apply_theme()

from PyQt5 import QtWidgets, QtCore

from ..viewer_3d import Viewer3D
from ..settings_panel import SettingsPanel
from ..job_queue_panel import JobQueuePanel
from ..controls import TransformToolbar
from ..model_panel import ModelPanel
from ..popups import MovePopup, RotatePopup, ScalePopup, AutoOrientPopup, ArrangePopup


class PrepareView(QtCore.QObject):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main = main_window
        self.viewer = Viewer3D(main_window)

        self._build_docks()
        self._build_toolbar()
        self._build_popups()

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

        job_queue_panel = JobQueuePanel(self.main)
        job_dock = QtWidgets.QDockWidget("Job Queue", self.main)
        job_dock.setWidget(job_queue_panel)
        job_dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.main.addDockWidget(QtCore.Qt.RightDockWidgetArea, job_dock)

        self.settings_panel = settings_panel
        self.model_panel = model_panel
        self.job_queue_panel = job_queue_panel
        self._settings_dock = settings_dock
        self._model_dock = model_dock
        self._job_dock = job_dock

        self.main.settings_panel = settings_panel
        self.main.model_panel = model_panel
        self.main.job_queue_panel = job_queue_panel
        self.main._settings_dock = settings_dock
        self.main._model_dock = model_dock
        self.main._job_dock = job_dock

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

    def show(self):
        for dock in (self._settings_dock, self._model_dock, self._job_dock):
            dock.show()
        self.transform_toolbar.show()

    def hide(self):
        for dock in (self._settings_dock, self._model_dock, self._job_dock):
            dock.hide()
        self.transform_toolbar.hide()
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
        for popup in (
            self.main._popup_move,
            self.main._popup_rotate,
            self.main._popup_scale,
            self.main._popup_auto_orient,
            self.main._popup_arrange,
        ):
            popup.apply_theme()

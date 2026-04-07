import json

from PyQt5 import QtCore

from ...workers import Worker
from ...i18n import tr
from config.defaults import DEFAULTS
from config.runtime_printer_state import runtime_printer_state_from_defaults
from .activity_sync import ActivitySyncMixin
from .load import LoadMixin
from .print import PrintMixin
from .project import ProjectMixin
from .ui import UiMixin


class MainController(LoadMixin, PrintMixin, ProjectMixin, ActivitySyncMixin, UiMixin, QtCore.QObject):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main = main_window
        self.current_model_id = None
        self._current_project_path = None
        self._last_gcode_path = None
        self._last_slice_signature = None
        self._last_gcode_stats = None
        self._last_preview_key = None
        self._last_preview_data = None
        self._last_preview_text = None
        self._last_slice_meshes = None
        self._last_slicer_backend = None
        self._slice_in_progress = False
        self._labels_visible = True
        self._model_clipboard = []
        self._undo_stack = []
        self._redo_stack = []
        self._undo_stack_limit = 50
        self._undo_in_progress = False
        self._bed_warning_active = False
        self._undo_timer = QtCore.QTimer(self)
        self._undo_timer.setSingleShot(True)
        self._undo_timer.timeout.connect(self._finalize_undo_snapshot)
        self._pending_undo_snapshot = False
        self._device_status_timer = QtCore.QTimer(self)
        self._device_status_timer.setInterval(750)
        self._device_status_timer.timeout.connect(self._update_device_status)
        self._workers = set()
        self._ui_settings = QtCore.QSettings("EON", "OpenSlicer")
        self.runtime_printer_state = runtime_printer_state_from_defaults(DEFAULTS.get("printer", {}))

    def __getattr__(self, name):
        main = self.__dict__.get("main")
        if main is not None:
            if name in main.__dict__:
                return main.__dict__[name]
            if getattr(type(main), name, None) is not None:
                return object.__getattribute__(main, name)
        raise AttributeError(f"{type(self).__name__} has no attribute {name!r}")

    def initialize(self):
        self._apply_theme()
        self._connect_signals()
        self._init_activity_sync()
        self.viewer.set_snap(
            DEFAULTS["viewer"]["snap_enabled"],
            DEFAULTS["viewer"]["snap_step"],
        )

        self.current_model_id = None
        self._current_project_path = None
        self._last_gcode_path = None
        self._labels_visible = True
        self._model_clipboard = []
        self._undo_stack = []
        self._redo_stack = []
        self._undo_stack_limit = 50
        self._undo_in_progress = False
        self._bed_warning_active = False
        self._last_gcode_stats = None
        self._last_preview_key = None
        self._last_preview_data = None
        self._last_preview_text = None
        self._last_slice_meshes = None
        self._last_slicer_backend = None
        self._undo_timer = QtCore.QTimer(self)
        self._undo_timer.setSingleShot(True)
        self._undo_timer.timeout.connect(self._finalize_undo_snapshot)
        self._pending_undo_snapshot = False
        self.runtime_printer_state = runtime_printer_state_from_defaults(DEFAULTS.get("printer", {}))
        self._push_undo_state()
        self.viewer.set_labels_visible(self._labels_visible)
        if hasattr(self, "_update_prepare_action_state"):
            self._update_prepare_action_state()
        if hasattr(self, "_labels_action"):
            self._labels_action.setChecked(self._labels_visible)

        startup_mode = self._restore_persistent_ui_state()
        if hasattr(self, "_mode_tabs"):
            for btn in self._mode_tabs:
                mode_key = str(btn.property("mode_key") or "").strip().lower()
                if mode_key == startup_mode:
                    btn.setChecked(True)
                    break
        self._activate_mode(startup_mode)
        self.statusBar().showMessage(tr("app.status_ready", DEFAULTS["app"]["status_ready"]))
        if hasattr(self.viewer, "set_bed_limits"):
            self.viewer.set_bed_limits(self.runtime_printer_state.bed_size, self.runtime_printer_state.bed_z)
        active_printer = getattr(getattr(self, "printer_manager", None), "active_printer", None)
        if active_printer is not None and hasattr(self, "_apply_printer_profile"):
            self._apply_printer_profile(active_printer, source="initialize")
        if self._device_status_timer is not None:
            self._device_status_timer.start()

    def _connect_signals(self):
        self.model_panel.model_selected.connect(self._on_model_selected)
        self.model_panel.selection_changed.connect(self._on_model_selection_changed)
        self.model_panel.request_remove.connect(self._on_model_remove)
        self.model_panel.duplicate_requested.connect(self._on_duplicate_requested)
        if hasattr(self.model_panel, "select_all_requested"):
            self.model_panel.select_all_requested.connect(self._select_all_models)
        if hasattr(self.model_panel, "deselect_all_requested"):
            self.model_panel.deselect_all_requested.connect(self._deselect_all_models)
        self.viewer.modelPicked.connect(self._on_viewer_model_picked)
        self.viewer.modelMoved.connect(self._on_viewer_model_moved)
        self.viewer.modelRotated.connect(self._on_viewer_model_rotated)
        if hasattr(self.viewer, "selectionChanged"):
            self.viewer.selectionChanged.connect(self._on_viewer_selection_changed)
        if hasattr(self.viewer, "simplifyRequested"):
            self.viewer.simplifyRequested.connect(self._open_simplify_dialog)
        if hasattr(self.viewer, "sceneChanged"):
            self.viewer.sceneChanged.connect(self._on_viewer_scene_changed)
        if hasattr(self.viewer, "projectionModeChanged"):
            self.viewer.projectionModeChanged.connect(self._on_viewer_projection_mode_changed)
        if hasattr(self.viewer, "plateAutoOrientRequested"):
            self.viewer.plateAutoOrientRequested.connect(lambda: self._on_auto_orient_requested("default"))
        if hasattr(self.viewer, "plateArrangeRequested"):
            self.viewer.plateArrangeRequested.connect(self._on_arrange_requested)
        if hasattr(self.viewer, "plateRemoveRequested"):
            self.viewer.plateRemoveRequested.connect(self._on_plate_remove_requested)
        if hasattr(self.viewer, "plateLockChanged"):
            self.viewer.plateLockChanged.connect(self._on_plate_lock_changed)
        if hasattr(self.viewer, "plateNameChanged"):
            self.viewer.plateNameChanged.connect(self._on_plate_name_changed)
        if hasattr(self, "device_view") and hasattr(self.device_view, "printer_changed"):
            self.device_view.printer_changed.connect(
                lambda printer: self._apply_printer_profile(printer, source="device")
            )
        if hasattr(self, "device_view") and hasattr(self.device_view, "add_printer_requested"):
            self.device_view.add_printer_requested.connect(self._on_device_add_printer_requested)
        if hasattr(self, "device_view") and hasattr(self.device_view, "diagnostics_requested"):
            self.device_view.diagnostics_requested.connect(self._on_device_diagnostics_requested)
        if hasattr(self, "device_view") and hasattr(self.device_view, "download_installer_requested"):
            self.device_view.download_installer_requested.connect(self._on_device_download_installer_requested)
        if hasattr(self, "control_view") and hasattr(self.control_view, "printer_changed"):
            self.control_view.printer_changed.connect(
                lambda printer: self._apply_printer_profile(printer, source="control")
            )
        if hasattr(self, "preview_view") and hasattr(self.preview_view, "printer_changed"):
            self.preview_view.printer_changed.connect(
                lambda printer: self._apply_printer_profile(printer, source="preview")
            )
        if hasattr(self, "activity_view") and hasattr(self.activity_view, "state_changed"):
            self.activity_view.state_changed.connect(self._on_activity_view_state_changed)
        if hasattr(self, "activity_view") and hasattr(self.activity_view, "refresh_requested"):
            self.activity_view.refresh_requested.connect(self._on_activity_view_refresh_requested)

    def _start_worker(self, worker: Worker):
        self._workers.add(worker)

        def _cleanup(*_args):
            self._workers.discard(worker)

        worker.signals.finished.connect(_cleanup)
        worker.signals.error.connect(_cleanup)
        self.pool.start(worker)

    def _persist_active_mode(self, mode: str) -> None:
        if not hasattr(self, "_ui_settings") or self._ui_settings is None:
            return
        value = str(mode or "").strip().lower()
        if not value:
            return
        self._ui_settings.setValue("ui/active_mode", value)
        self._ui_settings.sync()

    def _on_activity_view_state_changed(self, state: dict) -> None:
        if not hasattr(self, "_ui_settings") or self._ui_settings is None:
            return
        payload = dict(state or {})
        try:
            encoded = json.dumps(payload, ensure_ascii=True)
        except Exception:
            return
        self._ui_settings.setValue("ui/activity_view_state", encoded)
        self._ui_settings.sync()

    def _restore_persistent_ui_state(self) -> str:
        settings = getattr(self, "_ui_settings", None)
        if settings is None:
            return "prepare"

        raw_state = settings.value("ui/activity_view_state", "")
        state_obj = None
        if isinstance(raw_state, dict):
            state_obj = raw_state
        else:
            state_text = str(raw_state or "").strip()
            if state_text:
                try:
                    parsed = json.loads(state_text)
                except Exception:
                    parsed = None
                if isinstance(parsed, dict):
                    state_obj = parsed
        if state_obj is not None and hasattr(self, "activity_view") and hasattr(self.activity_view, "restore_view_state"):
            self.activity_view.restore_view_state(state_obj)

        mode = str(settings.value("ui/active_mode", "prepare") or "prepare").strip().lower()
        allowed_modes = {"files", "activity", "prepare", "preview", "device", "control"}
        if mode not in allowed_modes:
            mode = "prepare"
        return mode


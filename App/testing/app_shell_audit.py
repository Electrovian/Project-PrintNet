from __future__ import annotations

import argparse
import json
import os
import sys
from contextlib import ExitStack
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping
from unittest import mock

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_OPENGL", "software")
os.environ.setdefault("EON_FLOATING_PREPARE_ACTIONS", "1")

REPO_ROOT = Path(__file__).resolve().parents[2]
APP_ROOT = REPO_ROOT / "App"


def _bootstrap_import_paths() -> None:
    for candidate in (APP_ROOT, REPO_ROOT):
        candidate_text = str(candidate)
        if candidate_text not in sys.path:
            sys.path.insert(0, candidate_text)


if __package__ in (None, ""):
    _bootstrap_import_paths()

from PyQt5 import QtCore, QtGui, QtTest, QtWidgets  # noqa: E402

try:  # pragma: no cover - import path depends on caller cwd / sys.path setup
    from gui.main_window import MainWindow  # type: ignore  # noqa: E402
    from gui.Windows.controller import MainController  # type: ignore  # noqa: E402
    from slicer_v2.legacy_gcode_preview import parse_gcode_preview  # type: ignore  # noqa: E402
except Exception:  # pragma: no cover
    _bootstrap_import_paths()
    from App.gui.main_window import MainWindow  # type: ignore  # noqa: E402
    from App.gui.Windows.controller import MainController  # type: ignore  # noqa: E402
    from App.slicer_v2.legacy_gcode_preview import parse_gcode_preview  # type: ignore  # noqa: E402

try:  # pragma: no cover - import path depends on caller cwd / sys.path setup
    import main as app_main  # type: ignore  # noqa: E402
except Exception:  # pragma: no cover
    _bootstrap_import_paths()
    from App import main as app_main  # type: ignore  # noqa: E402

try:  # pragma: no cover - import path depends on caller cwd / sys.path setup
    from testing import visual_audit as _visual_audit  # type: ignore  # noqa: E402
except Exception:  # pragma: no cover
    _bootstrap_import_paths()
    from App.testing import visual_audit as _visual_audit  # type: ignore  # noqa: E402


@dataclass(frozen=True)
class ScreenshotRecord:
    name: str
    path: str
    mode: str
    width: int
    height: int

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "path": self.path,
            "mode": self.mode,
            "width": int(self.width),
            "height": int(self.height),
        }


class ShellAuditError(RuntimeError):
    pass


class ActionLedger:
    def __init__(self) -> None:
        self.events: list[dict[str, object]] = []
        self.findings: list[dict[str, object]] = []

    def record(self, event: str, target: str, **payload: object) -> None:
        row: dict[str, object] = {
            "timestamp_utc": _utc_iso(),
            "event": str(event),
            "target": str(target),
        }
        for key, value in payload.items():
            row[str(key)] = value
        self.events.append(row)

    def finding(
        self,
        severity: str,
        code: str,
        message: str,
        *,
        target: str = "",
        details: dict[str, object] | None = None,
    ) -> None:
        row: dict[str, object] = {
            "timestamp_utc": _utc_iso(),
            "severity": str(severity).strip().lower(),
            "code": str(code).strip(),
            "message": str(message).strip(),
            "target": str(target or "").strip(),
        }
        if details:
            row["details"] = dict(details)
        self.findings.append(row)

    def write_jsonl(self, path: Path) -> Path:
        rows = []
        for event in self.events:
            rows.append({"kind": "event", **event})
        for finding in self.findings:
            rows.append({"kind": "finding", **finding})
        text = "\n".join(json.dumps(row, ensure_ascii=True) for row in rows)
        path.write_text(text + ("\n" if text else ""), encoding="utf-8")
        return path


def _utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _utc_token() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")


def _viewer_runtime_diagnostics(viewer: object, renderer_mode: str) -> dict[str, object]:
    fallback = {
        "renderer_mode": renderer_mode,
        "viewer_runtime_degraded": False,
        "viewer_runtime_error": "",
        "viewer_runtime_failure_count": 0,
    }
    if viewer is None or not hasattr(viewer, "runtime_diagnostics"):
        return fallback
    try:
        raw = viewer.runtime_diagnostics()  # type: ignore[call-arg]
    except Exception:
        return fallback
    if isinstance(raw, Mapping):
        return dict(raw)
    return fallback


def _ensure_app() -> QtWidgets.QApplication:
    renderer_mode = app_main.configure_opengl_mode()
    app = QtWidgets.QApplication.instance()
    if app is not None:
        app.setProperty("eon_opengl_mode", renderer_mode)
        return app
    app = QtWidgets.QApplication(["app-shell-audit"])
    app.setProperty("eon_opengl_mode", renderer_mode)
    return app


def _wait(app: QtWidgets.QApplication, *, visible: bool, ms: int = 40) -> None:
    app.processEvents()
    QtTest.QTest.qWait(max(ms, 140 if visible else ms))


def _capture_widget(widget: QtWidgets.QWidget, output_dir: Path, name: str, mode: str) -> ScreenshotRecord:
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{_utc_token()}_{name}.png"
    path = output_dir / filename
    pixmap = QtGui.QPixmap()
    if widget.isVisible():
        try:
            handle = widget.windowHandle()
            screen = handle.screen() if handle is not None else QtWidgets.QApplication.primaryScreen()
            if screen is not None:
                pixmap = screen.grabWindow(int(widget.winId()))
        except Exception:
            pixmap = QtGui.QPixmap()
    if pixmap.isNull():
        pixmap = widget.grab()
    if pixmap.isNull():
        raise ShellAuditError(f"APP_SHELL_CAPTURE_FAILED:{name}")
    if not pixmap.save(str(path), "PNG"):
        raise ShellAuditError(f"APP_SHELL_SAVE_FAILED:{name}")
    return ScreenshotRecord(
        name=name,
        path=str(path),
        mode=mode,
        width=int(pixmap.width()),
        height=int(pixmap.height()),
    )


def _write_json(path: Path, payload: dict[str, object]) -> Path:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def _cube_mesh(size: float = 18.0) -> tuple[list[list[float]], list[list[int]]]:
    half = float(size) * 0.5
    vertices = [
        [-half, -half, 0.0],
        [half, -half, 0.0],
        [half, half, 0.0],
        [-half, half, 0.0],
        [-half, -half, float(size)],
        [half, -half, float(size)],
        [half, half, float(size)],
        [-half, half, float(size)],
    ]
    faces = [
        [0, 1, 2],
        [0, 2, 3],
        [4, 5, 6],
        [4, 6, 7],
        [0, 1, 5],
        [0, 5, 4],
        [1, 2, 6],
        [1, 6, 5],
        [2, 3, 7],
        [2, 7, 6],
        [3, 0, 4],
        [3, 4, 7],
    ]
    return vertices, faces


def _clean_text(value: object) -> str:
    return str(value or "").replace("&", "").replace("\n", " ").strip()


def _widget_text(widget: QtCore.QObject) -> str:
    if isinstance(widget, QtWidgets.QAbstractButton):
        return _clean_text(widget.text())
    if isinstance(widget, QtWidgets.QLineEdit):
        return _clean_text(widget.placeholderText() or widget.text())
    if isinstance(widget, QtWidgets.QComboBox):
        return _clean_text(widget.currentText())
    if isinstance(widget, QtWidgets.QAbstractSpinBox):
        return _clean_text(widget.text())
    if isinstance(widget, QtWidgets.QSlider):
        return f"value={int(widget.value())}"
    return ""


def _object_path(widget: QtCore.QObject) -> str:
    parts: list[str] = []
    current: QtCore.QObject | None = widget
    while current is not None and len(parts) < 5:
        name = str(current.objectName() or "").strip()
        label = name or type(current).__name__
        parts.append(label)
        current = current.parent()
    return "/".join(reversed(parts))


def _control_id(control: object) -> str:
    if isinstance(control, QtWidgets.QAction):
        text = _clean_text(control.text()) or _clean_text(control.toolTip())
        parent = control.parent()
        parent_name = _clean_text(getattr(parent, "title", lambda: "")()) if isinstance(parent, QtWidgets.QMenu) else ""
        base = text or str(control.data() or "") or type(control).__name__
        if parent_name:
            return f"action:{parent_name}/{base}"
        return f"action:{base}"
    if isinstance(control, QtCore.QObject):
        text = _widget_text(control)
        name = str(control.objectName() or "").strip()
        path = _object_path(control)
        if name:
            suffix = name
        elif text and path:
            suffix = f"{path}|{text}"
        else:
            suffix = text or path or type(control).__name__
        return f"{type(control).__name__}:{suffix}"
    return f"control:{type(control).__name__}"


def _classification_for_control(control: object) -> str:
    if isinstance(control, QtWidgets.QAction):
        text = _clean_text(control.text()) or _clean_text(control.toolTip())
        data = _clean_text(control.data())
        parent = control.parent()
        if not text and not data and control.menu() is None:
            return "decorative"
        if isinstance(parent, QtWidgets.QMenu):
            parent_title = _clean_text(parent.title())
            if parent_title and text.lower() == parent_title.lower():
                return "decorative"
        if control.menu() is not None:
            return "decorative"
        if control.isSeparator():
            return "decorative"
        if not control.isEnabled():
            return "gated"
        return "state-changing" if control.isCheckable() else "command"
    if isinstance(control, QtWidgets.QAbstractButton):
        name = str(control.objectName() or "").strip().lower()
        text = _clean_text(control.text() or control.toolTip())
        path = _object_path(control).lower()
        if name == "logobutton":
            return "decorative"
        if name.startswith("qt_"):
            return "decorative"
        if not control.isVisible() and not text:
            return "decorative"
        if "qtablewidget/qabstractbutton" in path:
            return "decorative"
        if not control.isEnabled():
            return "gated"
        return "state-changing" if control.isCheckable() else "command"
    if isinstance(control, (QtWidgets.QComboBox, QtWidgets.QLineEdit, QtWidgets.QAbstractSpinBox, QtWidgets.QSlider)):
        if hasattr(control, "isEnabled") and not control.isEnabled():
            return "gated"
        return "state-changing"
    return "decorative"


class ShellAuditHarness:
    def __init__(self, *, output_dir: Path, visible: bool) -> None:
        self.output_dir = output_dir
        self.visible = bool(visible)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.desktop_dir = self.output_dir / "screenshots"
        self.logs_dir = self.output_dir / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.workspace = self.output_dir / "workspace"
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.ledger = ActionLedger()
        self.records: list[ScreenshotRecord] = []
        self.exercised_controls: set[str] = set()
        self.allowlisted_controls: dict[str, str] = {}
        self.dialog_counter = 0
        self.sample_stl_paths = self._write_sample_stls()
        self.sample_theme_path = self.workspace / "demo_theme.json"
        self.sample_theme_path.write_text(
            json.dumps({"theme": {"popup_bg": "#1f242b", "popup_text": "#f5f7fa"}}, indent=2),
            encoding="utf-8",
        )
        self.project_path = self.workspace / "demo_project.osproj"
        self.gcode_path = self.workspace / "demo_plate.gcode"
        self.calibration_path = self.workspace / "calibration_output.gcode"
        self.window: MainWindow | None = None

    def _write_sample_stls(self) -> list[Path]:
        paths: list[Path] = []
        for name in ("demo_part_a.stl", "demo_part_b.stl"):
            path = self.workspace / name
            path.write_text(
                "solid demo\n"
                "facet normal 0 0 1\n"
                "outer loop\n"
                "vertex 0 0 0\n"
                "vertex 20 0 0\n"
                "vertex 0 20 0\n"
                "endloop\n"
                "endfacet\n"
                "endsolid demo\n",
                encoding="utf-8",
            )
            paths.append(path)
        return paths

    def _mark_exercised(self, control: object, *, event: str = "exercise", **payload: object) -> None:
        identifier = _control_id(control)
        self.exercised_controls.add(identifier)
        self.ledger.record(event, identifier, **payload)

    def _allowlist(self, control: object, reason: str) -> None:
        self.allowlisted_controls[_control_id(control)] = str(reason)

    def _capture(self, widget: QtWidgets.QWidget, name: str, mode: str) -> None:
        self.records.append(_capture_widget(widget, self.desktop_dir, name, mode))

    def _show_menu_snapshot(self, menu: QtWidgets.QMenu, *, name: str, mode: str) -> None:
        if self.window is None:
            return
        anchor = self.window.mapToGlobal(QtCore.QPoint(60, 60))
        menu.popup(anchor)
        _wait(self.app, visible=self.visible, ms=60)
        self._capture(self.window, name, mode)
        menu.hide()
        _wait(self.app, visible=self.visible, ms=30)

    def _dialog_screenshot_name(self, title: str, klass: str) -> str:
        self.dialog_counter += 1
        base = _clean_text(title).lower().replace(" ", "_")
        if not base:
            base = str(klass or "dialog").lower()
        return f"dialog_{self.dialog_counter:02d}_{base}"

    def _patches(self) -> ExitStack:
        stack = ExitStack()
        harness = self

        def _mock_dialog_exec(dialog: QtWidgets.QDialog) -> int:
            dialog.show()
            QtWidgets.QApplication.processEvents()
            QtTest.QTest.qWait(30)
            try:
                harness._capture(
                    dialog,
                    harness._dialog_screenshot_name(dialog.windowTitle(), type(dialog).__name__),
                    "dialog",
                )
            except Exception as exc:
                harness.ledger.finding(
                    "warning",
                    "DIALOG_CAPTURE_FAILED",
                    str(exc),
                    target=_control_id(dialog),
                )
            harness.ledger.record("dialog_exec", _clean_text(dialog.windowTitle()) or type(dialog).__name__)
            QtWidgets.QDialog.accept(dialog)
            return int(QtWidgets.QDialog.Accepted)

        def _message_box(kind: str, *args: object, **_kwargs: object) -> int:
            title = _clean_text(args[1] if len(args) > 1 else kind)
            text = _clean_text(args[2] if len(args) > 2 else "")
            harness.ledger.record("message_box", title or kind, kind=kind, text=text)
            if kind in {"warning", "critical"}:
                harness.ledger.finding("warning", f"MESSAGE_BOX_{kind.upper()}", text or title, target=title or kind)
            return int(QtWidgets.QMessageBox.Yes if kind == "question" else QtWidgets.QMessageBox.Ok)

        def _get_item(*args: object, **_kwargs: object):
            title = _clean_text(args[1] if len(args) > 1 else "")
            items = list(args[3]) if len(args) > 3 and isinstance(args[3], (list, tuple)) else []
            value = str(items[0]) if items else "demo"
            harness.ledger.record("input_dialog_item", title or "item", value=value)
            return value, True

        def _get_text(*args: object, **_kwargs: object):
            title = _clean_text(args[1] if len(args) > 1 else "")
            value = "Emboss Demo"
            harness.ledger.record("input_dialog_text", title or "text", value=value)
            return value, True

        def _get_double(*args: object, **kwargs: object):
            title = _clean_text(args[1] if len(args) > 1 else "")
            value = float(kwargs.get("value", args[3] if len(args) > 3 else 1.0) or 1.0)
            harness.ledger.record("input_dialog_double", title or "double", value=value)
            return value, True

        def _get_multiline_text(*args: object, **_kwargs: object):
            title = _clean_text(args[1] if len(args) > 1 else "")
            value = "\n".join(str(path) for path in harness.sample_stl_paths)
            harness.ledger.record("input_dialog_multiline", title or "multiline", value=value)
            return value, True

        def _get_color(*_args: object, **_kwargs: object):
            color = QtGui.QColor("#4edc78")
            harness.ledger.record("color_dialog", "filament_color", value=color.name())
            return color

        def _safe_get_open_file_names(_controller: MainController, caption: str, _directory: str, file_filter: str):
            paths: list[str] = []
            if "stl" in str(caption or "").lower():
                paths = [str(path) for path in harness.sample_stl_paths]
            harness.ledger.record("file_dialog_open_many", caption, paths=paths)
            return paths, str(file_filter or "")

        def _safe_get_open_file_name(_controller: MainController, caption: str, _directory: str, file_filter: str):
            value = ""
            lower = str(caption or "").lower()
            if "open project" in lower and harness.project_path.exists():
                value = str(harness.project_path)
            elif "load theme" in lower:
                value = str(harness.sample_theme_path)
            harness.ledger.record("file_dialog_open_one", caption, path=value)
            return value, str(file_filter or "")

        def _safe_get_save_file_name(_controller: MainController, caption: str, directory: str, file_filter: str):
            lower = str(caption or "").lower()
            if "project" in lower:
                path = harness.project_path
            elif "calibration" in lower:
                path = harness.calibration_path
            elif "g-code" in lower or "gcode" in lower:
                base = Path(str(directory or "")).stem or "exported_plate"
                path = harness.workspace / f"{base}.gcode"
            else:
                path = harness.workspace / "audit_output.dat"
            harness.ledger.record("file_dialog_save", caption, path=str(path))
            return str(path), str(file_filter or "")

        def _mock_open_stl_dialog(controller: MainController) -> None:
            harness.ledger.record("controller_call", "open_stl_dialog")
            harness._add_demo_models(controller, source="open_stl_dialog")

        def _mock_slice_current_plate(controller: MainController) -> str:
            harness.ledger.record("controller_call", "slice_current_plate")
            harness._seed_preview(controller, source="slice_current_plate")
            return str(harness.gcode_path)

        def _mock_slice_current_model(controller: MainController) -> str:
            return _mock_slice_current_plate(controller)

        def _mock_export_gcode(controller: MainController) -> str:
            harness.ledger.record("controller_call", "export_gcode")
            harness._seed_preview(controller, source="export_gcode")
            return str(harness.gcode_path)

        def _mock_device_send(controller: MainController, printer: object) -> None:
            harness.ledger.record("controller_call", "device_send", printer=str(printer))
            controller.statusBar().showMessage("Mock send to printer completed")

        def _mock_device_save(controller: MainController) -> None:
            harness.ledger.record("controller_call", "device_save")
            _mock_export_gcode(controller)

        def _mock_simple_dialog(method_name: str):
            def _runner(controller: MainController, *args: object, **kwargs: object) -> None:
                dlg = QtWidgets.QDialog(controller.main)
                dlg.setWindowTitle(method_name.replace("_", " ").title())
                layout = QtWidgets.QVBoxLayout(dlg)
                layout.addWidget(QtWidgets.QLabel(f"Mocked audit dialog for {method_name}", dlg))
                buttons = QtWidgets.QDialogButtonBox(
                    QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
                    parent=dlg,
                )
                layout.addWidget(buttons)
                harness.ledger.record("controller_call", method_name, args=list(args), kwargs=dict(kwargs))
                dlg.exec_()
            return _runner

        def _mock_device_action(method_name: str):
            def _runner(controller: MainController, *args: object, **kwargs: object) -> None:
                harness.ledger.record("controller_call", method_name, args=list(args), kwargs=dict(kwargs))
                controller.statusBar().showMessage(f"Mocked {method_name}")
            return _runner

        def _mock_load_theme(controller: MainController) -> None:
            harness.ledger.record("controller_call", "load_theme_from_file", path=str(harness.sample_theme_path))
            controller.statusBar().showMessage("Mock theme loaded")

        def _mock_save_theme(controller: MainController) -> None:
            path = harness.workspace / "saved_theme.json"
            path.write_text(json.dumps({"theme": "saved"}, indent=2), encoding="utf-8")
            harness.ledger.record("controller_call", "save_theme_to_file", path=str(path))
            controller.statusBar().showMessage("Mock theme saved")

        def _mock_init_activity_sync(controller: MainController) -> None:
            harness.ledger.record("controller_call", "init_activity_sync")
            controller._activity_sync_client = None
            controller._compliance_blocked = False

        def _mock_update_device_status(controller: MainController) -> None:
            if hasattr(controller, "device_view"):
                controller.device_view.update_live_status(
                    head_pos=(110.0, 90.0, 12.0),
                    time_left_s=3220,
                    pla_remaining_m=2.8,
                    pla_low=False,
                )

        stack.enter_context(mock.patch.object(QtWidgets.QDialog, "exec_", _mock_dialog_exec))
        stack.enter_context(mock.patch.object(QtWidgets.QMessageBox, "question", lambda *a, **k: _message_box("question", *a, **k)))
        stack.enter_context(mock.patch.object(QtWidgets.QMessageBox, "warning", lambda *a, **k: _message_box("warning", *a, **k)))
        stack.enter_context(mock.patch.object(QtWidgets.QMessageBox, "critical", lambda *a, **k: _message_box("critical", *a, **k)))
        stack.enter_context(mock.patch.object(QtWidgets.QMessageBox, "information", lambda *a, **k: _message_box("information", *a, **k)))
        stack.enter_context(mock.patch.object(QtWidgets.QInputDialog, "getItem", _get_item))
        stack.enter_context(mock.patch.object(QtWidgets.QInputDialog, "getText", _get_text))
        stack.enter_context(mock.patch.object(QtWidgets.QInputDialog, "getDouble", _get_double))
        stack.enter_context(mock.patch.object(QtWidgets.QInputDialog, "getMultiLineText", _get_multiline_text))
        stack.enter_context(mock.patch.object(QtWidgets.QColorDialog, "getColor", _get_color))
        stack.enter_context(mock.patch.object(QtGui.QDesktopServices, "openUrl", lambda url: harness.ledger.record("desktop_open", str(url.toString() if hasattr(url, "toString") else url)) or True))

        stack.enter_context(mock.patch.object(MainController, "_safe_get_open_file_names", _safe_get_open_file_names))
        stack.enter_context(mock.patch.object(MainController, "_safe_get_open_file_name", _safe_get_open_file_name))
        stack.enter_context(mock.patch.object(MainController, "_safe_get_save_file_name", _safe_get_save_file_name))
        stack.enter_context(mock.patch.object(MainController, "open_stl_dialog", _mock_open_stl_dialog))
        stack.enter_context(mock.patch.object(MainController, "slice_current_plate", _mock_slice_current_plate))
        stack.enter_context(mock.patch.object(MainController, "slice_current_model", _mock_slice_current_model))
        stack.enter_context(mock.patch.object(MainController, "export_gcode", _mock_export_gcode))
        stack.enter_context(mock.patch.object(MainController, "_on_device_send_requested", _mock_device_send))
        stack.enter_context(mock.patch.object(MainController, "_on_device_save_requested", _mock_device_save))
        stack.enter_context(mock.patch.object(MainController, "_open_simplify_dialog", _mock_simple_dialog("_open_simplify_dialog")))
        stack.enter_context(mock.patch.object(MainController, "_open_boolean_dialog", _mock_simple_dialog("_open_boolean_dialog")))
        stack.enter_context(mock.patch.object(MainController, "_open_emboss_dialog", _mock_simple_dialog("_open_emboss_dialog")))
        stack.enter_context(mock.patch.object(MainController, "_load_theme_from_file", _mock_load_theme))
        stack.enter_context(mock.patch.object(MainController, "_save_theme_to_file", _mock_save_theme))
        stack.enter_context(mock.patch.object(MainController, "_on_device_add_printer_requested", _mock_device_action("_on_device_add_printer_requested")))
        stack.enter_context(mock.patch.object(MainController, "_on_device_diagnostics_requested", _mock_device_action("_on_device_diagnostics_requested")))
        stack.enter_context(mock.patch.object(MainController, "_on_device_download_installer_requested", _mock_device_action("_on_device_download_installer_requested")))
        stack.enter_context(mock.patch.object(MainController, "_on_activity_view_refresh_requested", _mock_device_action("_on_activity_view_refresh_requested")))
        stack.enter_context(mock.patch.object(MainController, "_init_activity_sync", _mock_init_activity_sync))
        stack.enter_context(mock.patch.object(MainController, "_auto_slice_prepare", lambda *_args, **_kwargs: None))
        stack.enter_context(mock.patch.object(MainController, "_update_device_status", _mock_update_device_status))
        return stack

    def _add_demo_models(self, controller: MainController, *, source: str) -> None:
        if not hasattr(controller, "viewer"):
            return
        viewer = controller.viewer
        existing = list(viewer.get_all_model_ids() if hasattr(viewer, "get_all_model_ids") else viewer.get_model_ids())
        if not existing:
            vertices, faces = _cube_mesh(18.0)
            first_id = viewer.add_model_from_data("demo_cube_a.stl", str(self.sample_stl_paths[0]), vertices, faces)
            second_id = viewer.add_model_from_data("demo_cube_b.stl", str(self.sample_stl_paths[1]), vertices, faces)
            viewer.set_model_transform(second_id, offset_xy=(28.0, 14.0))
            controller.current_model_id = int(first_id)
            viewer.set_selected_models([int(first_id), int(second_id)], emit_signal=False)
            if hasattr(controller.model_panel, "refresh_from_viewer"):
                controller.model_panel.refresh_from_viewer(viewer)
        controller._refresh_files_view()
        controller._sync_popups()
        controller._push_undo_state()
        controller.statusBar().showMessage(f"Seeded demo models via {source}")

    def _seed_preview(self, controller: MainController, *, source: str) -> None:
        self._add_demo_models(controller, source=source)
        self.gcode_path.write_text("\n".join(_visual_audit._build_preview_gcode()), encoding="utf-8")
        preview = parse_gcode_preview(_visual_audit._build_preview_gcode())
        controller._last_gcode_path = str(self.gcode_path)
        controller._last_gcode_stats = _visual_audit._build_preview_stats("tree")
        controller.preview_view.set_preview_data(preview)
        controller.preview_view.update_stats(_visual_audit._build_preview_stats("tree"))
        controller._activate_mode("preview")
        controller.statusBar().showMessage(f"Mock slice complete via {source}")

    def _seed_window_state(self, window: MainWindow) -> None:
        self._add_demo_models(window.controller, source="seed")
        me_rows, printer_rows = _visual_audit._build_activity_rows()
        window.activity_view.set_me_activity(me_rows)
        window.activity_view.set_printer_activity(printer_rows)
        window.activity_view.set_compliance_banner("Cloud sync is disabled during the audit.")
        window.activity_view.set_cache_banner("Cached activity replay loaded for shell audit.")
        window.device_view.update_live_status(
            head_pos=(101.0, 82.5, 12.0),
            time_left_s=4110,
            pla_remaining_m=4.2,
            pla_low=False,
        )
        _visual_audit._sync_printer_selection(window, "Demo Core")

    def _allowlist_equivalent_actions(self) -> None:
        assert self.window is not None
        covered_text = {
            "add",
            "auto orient",
            "arrange",
            "import stl(s)...",
            "export g-code...",
        }
        for action in self.window.findChildren(QtWidgets.QAction):
            text = _clean_text(action.text()).lower()
            if text in covered_text:
                self._allowlist(action, "covered_by_equivalent_control")

    def _exercise_actions(self, actions: list[QtWidgets.QAction]) -> None:
        for action in actions:
            if action is None or action.isSeparator():
                continue
            identifier = _control_id(action)
            text = _clean_text(action.text())
            lower = text.lower()
            if lower in {
                "quit",
                "new project",
                "delete selected",
                "delete all",
                "temperature tower",
                "flow rate test",
                "pressure advance",
                "retraction test",
                "tolerance test",
                "max flowrate test",
            }:
                self._allowlist(action, "destructive_or_heavy")
                continue
            if not action.isEnabled():
                self._allowlist(action, "disabled")
                continue
            action.trigger()
            _wait(self.app, visible=self.visible, ms=25)
            self._mark_exercised(action, text=text or identifier)

    def _exercise_buttons(self, buttons: list[QtWidgets.QAbstractButton]) -> None:
        for button in buttons:
            if button is None:
                continue
            if not button.isVisible() or not button.isEnabled():
                if not button.isEnabled():
                    self._allowlist(button, "disabled")
                continue
            identifier = _control_id(button)
            text = _clean_text(button.text() or button.toolTip())
            lower = text.lower()
            if lower in {"quit", "remove current plate (if not last one)", "remove selected"}:
                self._allowlist(button, "destructive")
                continue
            button.click()
            _wait(self.app, visible=self.visible, ms=25)
            self._mark_exercised(button, text=text or identifier)
            if button.isCheckable() and lower not in {"color show", "g-code"}:
                button.click()
                _wait(self.app, visible=self.visible, ms=15)
                self._mark_exercised(button, event="exercise_revert", text=text or identifier)

    def _exercise_combo(self, combo: QtWidgets.QComboBox) -> None:
        if not combo.isVisible() or not combo.isEnabled() or combo.count() <= 1:
            if not combo.isEnabled():
                self._allowlist(combo, "disabled")
            return
        current = combo.currentIndex()
        combo.setCurrentIndex((current + 1) % combo.count())
        _wait(self.app, visible=self.visible, ms=20)
        combo.setCurrentIndex(current)
        _wait(self.app, visible=self.visible, ms=20)
        self._mark_exercised(combo, text=combo.currentText())

    def _exercise_spin(self, spin: QtWidgets.QAbstractSpinBox) -> None:
        if not spin.isVisible() or not spin.isEnabled():
            if not spin.isEnabled():
                self._allowlist(spin, "disabled")
            return
        spin.stepBy(1)
        _wait(self.app, visible=self.visible, ms=15)
        self._mark_exercised(spin, text=_widget_text(spin))

    def _exercise_line_edit(self, line_edit: QtWidgets.QLineEdit, text: str) -> None:
        if not line_edit.isVisible() or not line_edit.isEnabled():
            if not line_edit.isEnabled():
                self._allowlist(line_edit, "disabled")
            return
        line_edit.clear()
        line_edit.setText(text)
        _wait(self.app, visible=self.visible, ms=15)
        self._mark_exercised(line_edit, text=text)

    def _exercise_slider(self, slider: QtWidgets.QSlider) -> None:
        if not slider.isVisible() or not slider.isEnabled():
            if not slider.isEnabled():
                self._allowlist(slider, "disabled")
            return
        value = slider.maximum() if slider.maximum() > slider.minimum() else slider.minimum()
        slider.setValue(value)
        _wait(self.app, visible=self.visible, ms=15)
        self._mark_exercised(slider, text=f"value={int(value)}")

    def _exercise_prepare(self) -> None:
        assert self.window is not None
        _visual_audit._activate_mode(self.window, "prepare")
        _wait(self.app, visible=self.visible, ms=60)
        self._capture(self.window, "prepare_default", "prepare")

        toolbar = self.window.transform_toolbar
        for action_id in ("move", "rotate", "scale", "auto_orient", "arrange"):
            action = toolbar.action_registry.get(action_id)
            if action is None:
                continue
            button = toolbar.widgetForAction(action)
            if button is not None:
                button.click()
                _wait(self.app, visible=self.visible, ms=30)
                self._mark_exercised(button, text=action_id)
                popup = {
                    "move": self.window._popup_move,
                    "rotate": self.window._popup_rotate,
                    "scale": self.window._popup_scale,
                    "auto_orient": self.window._popup_auto_orient,
                    "arrange": self.window._popup_arrange,
                }.get(action_id)
                if popup is not None and popup.isVisible():
                    self._capture(self.window, f"prepare_{action_id}_popup", "prepare")
        for action_id in (
            "add_plate",
            "add_instance",
            "split_objects",
            "split_parts",
            "variable_layer",
            "assembly_view",
            "cut",
            "mesh_boolean",
            "support_paint",
            "seam_paint",
            "fuzzy_paint",
            "emboss",
            "measure",
            "brim_ears",
        ):
            action = toolbar.action_registry.get(action_id)
            if action is not None and action.isEnabled():
                action.trigger()
                _wait(self.app, visible=self.visible, ms=25)
                self._mark_exercised(action, text=action_id)

        settings = self.window.settings_panel
        self._exercise_combo(settings._printer_combo)
        self._exercise_combo(settings._profile_combo)
        if hasattr(settings, "_filament_type_menu"):
            self._show_menu_snapshot(settings._filament_type_menu, name="settings_filament_menu", mode="prepare")
            self._exercise_actions(settings._filament_type_menu.actions())
            self._mark_exercised(settings._filament_button, text="filament_button")
        self._exercise_buttons(
            [
                settings._advanced_toggle,
                settings._filament_color_button,
                settings._scope_buttons["objects"],
                settings._scope_buttons["global"],
            ]
        )
        self._exercise_line_edit(settings._search_input, "support")
        for button in settings._nav_group.buttons():
            button.click()
            _wait(self.app, visible=self.visible, ms=20)
            self._mark_exercised(button, text=button.text())
            page = settings._pages_stack.currentWidget()
            if page is None:
                continue
            for check in page.findChildren(QtWidgets.QCheckBox):
                self._exercise_buttons([check])
            first_combo = next(iter(page.findChildren(QtWidgets.QComboBox)), None)
            if first_combo is not None:
                self._exercise_combo(first_combo)
            first_spin = next(iter(page.findChildren(QtWidgets.QAbstractSpinBox)), None)
            if first_spin is not None:
                self._exercise_spin(first_spin)
        settings._scope_buttons["objects"].click()
        _wait(self.app, visible=self.visible, ms=20)
        model_panel = settings.model_panel
        self._exercise_buttons([model_panel.select_all_btn, model_panel.duplicate_btn, model_panel.clear_selection_btn])
        self._allowlist(model_panel.remove_btn, "destructive")
        settings._scope_buttons["global"].click()
        _wait(self.app, visible=self.visible, ms=20)
        self._capture(self.window, "settings_panel", "prepare")

    def _exercise_preview(self) -> None:
        assert self.window is not None
        self.window.slice_current_plate()
        _wait(self.app, visible=self.visible, ms=80)
        _visual_audit._activate_mode(self.window, "preview")
        _wait(self.app, visible=self.visible, ms=50)
        preview = self.window.preview_view
        self._exercise_combo(preview._printer_combo)
        self._exercise_combo(preview._line_type_combo)
        self._exercise_buttons([preview._collapse_btn, preview._color_btn, preview._gcode_btn, preview._play_btn])
        self._exercise_buttons([preview._platform_check, preview._nozzle_check])
        self._exercise_spin(preview._steps_spin)
        self._exercise_spin(preview._play_speed_spin)
        self._exercise_slider(preview._steps_slider)
        self._exercise_slider(preview._layer_slider)
        self._capture(self.window, "preview_main", "preview")

    def _exercise_device(self) -> None:
        assert self.window is not None
        _visual_audit._activate_mode(self.window, "device")
        _wait(self.app, visible=self.visible, ms=50)
        device = self.window.device_view
        self._exercise_combo(device._printer_combo)
        self._exercise_buttons(
            [
                device._send_btn,
                device._save_btn,
                device._email_btn,
                device._add_printer_btn,
                device._diagnostics_btn,
                device._download_installer_btn,
            ]
        )
        self._capture(self.window, "device_main", "device")

    def _exercise_control(self) -> None:
        assert self.window is not None
        _visual_audit._activate_mode(self.window, "control")
        _wait(self.app, visible=self.visible, ms=50)
        control = self.window.control_view
        self._exercise_combo(control._printer_combo)
        self._exercise_combo(control._step_combo)
        self._exercise_buttons(control.findChildren(QtWidgets.QAbstractButton))
        for spin in control.findChildren(QtWidgets.QAbstractSpinBox):
            self._exercise_spin(spin)
        self._capture(self.window, "control_main", "control")

    def _exercise_files(self) -> None:
        assert self.window is not None
        self.window.files_view.set_models([])
        _visual_audit._activate_mode(self.window, "files")
        _wait(self.app, visible=self.visible, ms=40)
        self._capture(self.window, "files_empty", "files")
        self._exercise_buttons([self.window.files_view._add_btn])
        self.window.files_view.refresh_from_viewer(self.window.viewer)
        self._exercise_line_edit(self.window.files_view._search_input, "demo")
        self._exercise_line_edit(self.window.files_view._search_input, "")
        self._capture(self.window, "files_populated", "files")

    def _exercise_activity(self) -> None:
        assert self.window is not None
        _visual_audit._activate_mode(self.window, "activity")
        _wait(self.app, visible=self.visible, ms=40)
        activity = self.window.activity_view
        activity._me_btn.click()
        _wait(self.app, visible=self.visible, ms=15)
        self._mark_exercised(activity._me_btn, text="me")
        self._exercise_line_edit(activity._search_input, "demo")
        self._exercise_combo(activity._date_filter)
        self._exercise_buttons([activity._refresh_btn])
        self._capture(self.window, "activity_me", "activity")
        activity._printers_btn.click()
        _wait(self.app, visible=self.visible, ms=15)
        self._mark_exercised(activity._printers_btn, text="printers")
        self._capture(self.window, "activity_printers", "activity")

    def _exercise_topbar_and_menus(self) -> None:
        assert self.window is not None
        self._capture(self.window, "startup", "prepare")
        self._show_menu_snapshot(self.window._file_menu, name="topbar_file_menu", mode="menus")
        self._mark_exercised(self.window._file_btn, text="file")
        self._show_menu_snapshot(self.window._main_menu, name="topbar_main_menu", mode="menus")
        self._mark_exercised(self.window._file_caret_btn, text="menu")
        self._show_menu_snapshot(self.window._calib_menu, name="topbar_calibration_menu", mode="menus")
        self._mark_exercised(self.window._calib_btn, text="calibration")
        self._exercise_buttons(
            [
                self.window._save_btn,
                self.window._undo_btn,
                self.window._redo_btn,
                self.window._home_btn,
                self.window._topbar_slice_btn,
                self.window._topbar_print_btn,
            ]
        )
        self._exercise_buttons(self.window._mode_tabs)
        menus = [
            self.window._file_menu,
            self.window._edit_menu,
            self.window._view_menu,
            self.window._prefs_menu,
            self.window._calib_menu,
            self.window._help_menu,
            getattr(self.window, "_theme_menu", None),
        ]
        for menu in menus:
            if menu is None:
                continue
            self._exercise_actions(menu.actions())

    def _check_signal_receivers(self) -> None:
        assert self.window is not None
        device = self.window.device_view
        if int(device.receivers(device.email_requested)) <= 0:
            self.ledger.finding(
                "warning",
                "DEVICE_EMAIL_UNWIRED",
                "Device email action has no controller receiver.",
                target=_control_id(device._email_btn),
            )
        for button in self.window.control_view.findChildren(QtWidgets.QAbstractButton):
            menu = getattr(button, "menu", lambda: None)()
            if menu is not None:
                continue
            signal = button.toggled if button.isCheckable() else button.clicked
            try:
                receiver_count = int(button.receivers(signal))
            except Exception:
                receiver_count = 0
            if receiver_count <= 0:
                self.ledger.finding(
                    "info",
                    "CONTROL_BUTTON_NO_RECEIVER",
                    "Control button has no connected receiver.",
                    target=_control_id(button),
                    details={"text": _clean_text(button.text() or button.toolTip())},
                )

    def _collect_inventory(self) -> dict[str, object]:
        assert self.window is not None
        controls: list[dict[str, object]] = []
        unknown_controls: list[str] = []
        candidates: list[object] = []
        candidates.extend(self.window.findChildren(QtWidgets.QAbstractButton))
        candidates.extend(self.window.findChildren(QtWidgets.QComboBox))
        candidates.extend(self.window.findChildren(QtWidgets.QLineEdit))
        candidates.extend(self.window.findChildren(QtWidgets.QAbstractSpinBox))
        candidates.extend(self.window.findChildren(QtWidgets.QSlider))
        candidates.extend(self.window.findChildren(QtWidgets.QAction))
        seen: set[str] = set()
        for control in candidates:
            identifier = _control_id(control)
            if identifier in seen:
                continue
            seen.add(identifier)
            classification = _classification_for_control(control)
            if not classification:
                unknown_controls.append(identifier)
                classification = "unknown"
            enabled = bool(getattr(control, "isEnabled", lambda: True)())
            visible = bool(getattr(control, "isVisible", lambda: True)())
            entry = {
                "id": identifier,
                "type": type(control).__name__,
                "classification": classification,
                "enabled": enabled,
                "visible": visible,
                "text": _clean_text(getattr(control, "text", lambda: "")()),
                "tooltip": _clean_text(getattr(control, "toolTip", lambda: "")()),
                "object_name": str(getattr(control, "objectName", lambda: "")() or "").strip(),
                "path": _object_path(control) if isinstance(control, QtCore.QObject) else "",
                "exercised": identifier in self.exercised_controls,
                "allowlist_reason": self.allowlisted_controls.get(identifier, ""),
            }
            controls.append(entry)
            if (
                classification == "command"
                and enabled
                and visible
                and identifier not in self.exercised_controls
                and identifier not in self.allowlisted_controls
            ):
                self.ledger.finding(
                    "warning",
                    "COMMAND_NOT_EXERCISED",
                    "Enabled command control was not exercised during the audit.",
                    target=identifier,
                )
        controls.sort(key=lambda item: str(item["id"]))
        return {
            "controls": controls,
            "unknown_controls": unknown_controls,
            "control_count": len(controls),
        }

    def run(self) -> dict[str, object]:
        self.app = _ensure_app()
        with self._patches():
            self.window = MainWindow(_visual_audit._build_printers(), {})
            self.window.resize(1600, 1100)
            self.window.show()
            _wait(self.app, visible=self.visible, ms=120)
            self._seed_window_state(self.window)
            self._check_signal_receivers()
            self._exercise_topbar_and_menus()
            self._exercise_files()
            self._exercise_activity()
            self._exercise_prepare()
            self._exercise_preview()
            self._exercise_device()
            self._exercise_control()
            self._allowlist_equivalent_actions()
            viewer_diagnostics = _viewer_runtime_diagnostics(
                getattr(self.window, "viewer", None),
                str(self.app.property("eon_opengl_mode") or "software"),
            )
            if bool(viewer_diagnostics.get("viewer_runtime_degraded")):
                self.ledger.finding(
                    "warning",
                    "VIEWER_RUNTIME_DEGRADED",
                    "Viewer entered degraded runtime mode during the shell audit.",
                    target="viewer",
                    details={
                        "renderer_mode": str(viewer_diagnostics.get("renderer_mode") or ""),
                        "viewer_runtime_error": str(viewer_diagnostics.get("viewer_runtime_error") or ""),
                    },
                )
            inventory = self._collect_inventory()
            self.window.close()
            _wait(self.app, visible=self.visible, ms=40)

        manifest_path = self.output_dir / "app_shell_audit_manifest.json"
        inventory_path = self.output_dir / "control_inventory.json"
        ledger_path = self.logs_dir / "action_ledger.jsonl"
        self.ledger.write_jsonl(ledger_path)
        _write_json(inventory_path, inventory)
        payload = {
            "ok": True,
            "scenario": "full-shell",
            "visible": bool(self.visible),
            "generated_at_utc": _utc_iso(),
            "output_dir": str(self.output_dir),
            "screenshot_count": len(self.records),
            "screenshots": [record.to_dict() for record in self.records],
            "action_count": len(self.ledger.events),
            "finding_count": len(self.ledger.findings),
            "findings": list(self.ledger.findings),
            "action_ledger_path": str(ledger_path),
            "control_inventory_path": str(inventory_path),
            "unknown_controls": list(inventory["unknown_controls"]),
            "renderer_mode": str(viewer_diagnostics.get("renderer_mode") or self.app.property("eon_opengl_mode") or "software"),
            "viewer_runtime_degraded": bool(viewer_diagnostics.get("viewer_runtime_degraded")),
            "viewer_runtime_error": str(viewer_diagnostics.get("viewer_runtime_error") or ""),
            "viewer_runtime_failure_count": int(viewer_diagnostics.get("viewer_runtime_failure_count") or 0),
        }
        _write_json(manifest_path, payload)
        payload["manifest_path"] = str(manifest_path)
        return payload


def run_full_shell_audit(*, output_dir: str | Path | None = None, visible: bool = False) -> dict[str, object]:
    output_path = Path(output_dir).expanduser().resolve() if output_dir is not None else (
        REPO_ROOT / "App" / "testing" / "app_shell_audit_output" / _utc_token()
    )
    output_path.mkdir(parents=True, exist_ok=True)
    return ShellAuditHarness(output_dir=output_path, visible=bool(visible)).run()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a full desktop app shell interaction audit.")
    parser.add_argument("--scenario", default="full-shell", help="Audit scenario to run.")
    parser.add_argument("--output-dir", default="", help="Optional directory for screenshots and reports.")
    parser.add_argument("--visible", action="store_true", help="Run the audit in a visible desktop window.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    scenario = str(args.scenario or "").strip().lower()
    if scenario != "full-shell":
        print(json.dumps({"ok": False, "error": f"UNSUPPORTED_SCENARIO:{scenario}"}))
        return 2
    try:
        if bool(args.visible):
            os.environ.pop("QT_QPA_PLATFORM", None)
        payload = run_full_shell_audit(output_dir=(args.output_dir or None), visible=bool(args.visible))
        print(json.dumps(payload, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"ok": False, "scenario": scenario, "error": str(exc)}, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

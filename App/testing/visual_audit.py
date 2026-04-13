from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

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
except Exception:  # pragma: no cover
    _bootstrap_import_paths()
    from App.gui.main_window import MainWindow  # type: ignore  # noqa: E402

try:  # pragma: no cover - import path depends on caller cwd / sys.path setup
    import main as app_main  # type: ignore  # noqa: E402
except Exception:  # pragma: no cover
    _bootstrap_import_paths()
    from App import main as app_main  # type: ignore  # noqa: E402

try:  # pragma: no cover - import path depends on caller cwd / sys.path setup
    from slicer_v2.legacy_gcode_preview import parse_gcode_preview  # type: ignore  # noqa: E402
except Exception:  # pragma: no cover
    _bootstrap_import_paths()
    from App.slicer_v2.legacy_gcode_preview import parse_gcode_preview  # type: ignore  # noqa: E402

try:  # pragma: no cover - import path depends on caller cwd / sys.path setup
    from testing.qt_cleanup import dispose_created_top_levels, snapshot_top_level_widgets  # type: ignore  # noqa: E402
except Exception:  # pragma: no cover
    _bootstrap_import_paths()
    from App.testing.qt_cleanup import dispose_created_top_levels, snapshot_top_level_widgets  # type: ignore  # noqa: E402


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


class VisualAuditError(RuntimeError):
    pass


def _utc_token() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")


def _utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


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
    argv = ["visual-audit"]
    app = QtWidgets.QApplication(argv)
    app.setProperty("eon_opengl_mode", renderer_mode)
    return app


def _build_printers() -> list[dict[str, object]]:
    return [
        {
            "name": "Demo Core",
            "bed_x": 256,
            "bed_y": 256,
            "bed_z": 256,
            "connector_type": "bambu_lan",
            "octoprint_url": "http://demo-core.local",
        },
        {
            "name": "Workhorse",
            "bed_x": 220,
            "bed_y": 220,
            "bed_z": 250,
            "connector_type": "local_file",
        },
    ]


def _build_activity_rows() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    me_entries = [
        {
            "job": "Demo Benchy",
            "status": "printing",
            "duration": "00:42:10",
            "material": "PLA",
            "when": "2026-04-05T10:00:00Z",
            "user": "Elect",
            "printer": "Demo Core",
        },
        {
            "job": "Support Tower",
            "status": "completed",
            "duration": "00:19:54",
            "material": "PETG",
            "when": "2026-04-04T15:20:00Z",
            "user": "Elect",
            "printer": "Workhorse",
        },
    ]
    printer_entries = [
        {
            "job": "Calibration Sheet",
            "status": "queued",
            "duration": "00:00:00",
            "material": "PLA",
            "when": "2026-04-05T08:30:00Z",
            "user": "Lab",
            "printer": "Demo Core",
        },
        {
            "job": "Bridge Stress Test",
            "status": "failed",
            "duration": "00:09:12",
            "material": "ABS",
            "when": "2026-04-03T12:10:00Z",
            "user": "Lab",
            "printer": "Workhorse",
        },
    ]
    return me_entries, printer_entries


def _build_preview_stats(style: str) -> dict[str, object]:
    support_style = "organic" if style == "organic" else "tree"
    return {
        "length": "18.42 m",
        "weight": "62.8 g",
        "cost": "$1.84",
        "time": "1h12m",
        "ai_warnings": ["Thin overhang detected"],
        "ai_suggestions": ["Confirm support reach before export"],
        "support_diagnostics": {
            "status": "warnings" if style == "organic" else "ok",
            "diagnostics_source": "supports_stage",
            "support_type": "tree",
            "support_style": support_style,
            "support_build_plate_only": True,
            "support_critical_regions_only": False,
            "support_remove_small_overhang": True,
            "support_interface_bottom_layers_effective": 2,
            "tree_support_strict_parity_mode": style == "tree",
            "support_region_count": 4,
            "support_path_count": 18,
            "support_path_length_mm_total": 1243.58,
            "support_interface_path_count_total": 6,
            "unsupported_island_count_total": 1,
            "tree_branch_count_total": 8,
            "tree_trunk_count_total": 3,
            "tree_merge_count_total": 2,
            "tree_collision_avoid_count_total": 5,
            "tree_pruned_branch_count_total": 1,
            "tree_parent_assignment_count_total": 7,
            "tree_branch_trunk_assignment_counts": {"branch": 6, "trunk": 2},
            "warnings": [
                "support_planning:tree_style=organic" if style == "organic" else "support_planning:tree_style=tree",
                "layer_4:tree_collision_avoided=2",
            ],
        },
    }


def _build_preview_gcode() -> list[str]:
    return [
        ";LAYER:0",
        ";TYPE:Outer wall",
        "G1 X0 Y0 Z0.2 F1200",
        "G1 X20 Y0 E0.8 F1200",
        ";TYPE:Support",
        "G1 X20 Y10 E0.4 F1200",
        ";TYPE:Travel",
        "G0 X30 Y15",
        ";LAYER:1",
        ";TYPE:Inner wall",
        "G1 X1 Y1 Z0.4 F1200",
        "G1 X12 Y1 E0.5 F1200",
    ]


def _write_sample_models(workspace: Path) -> list[dict[str, object]]:
    paths = []
    for name, content in (
        ("demo_part_a.stl", "solid demo_a\nendsolid demo_a\n"),
        ("demo_part_b.stl", "solid demo_b\nendsolid demo_b\n"),
    ):
        path = workspace / name
        path.write_text(content, encoding="utf-8")
        paths.append(path)
    return [
        {
            "id": 1,
            "name": "demo_part_a.stl",
            "path": str(paths[0]),
            "plate": "01",
        },
        {
            "id": 2,
            "name": "demo_part_b.stl",
            "path": str(paths[1]),
            "plate": "01",
        },
    ]


def _find_mode_button(window: MainWindow, mode_key: str):
    for button in getattr(window, "_mode_tabs", []) or []:
        if str(button.property("mode_key") or "").strip().lower() == str(mode_key).strip().lower():
            return button
    return None


def _activate_mode(window: MainWindow, mode_key: str) -> None:
    button = _find_mode_button(window, mode_key)
    if button is not None:
        button.click()
    else:
        window._activate_mode(mode_key)


def _sync_printer_selection(window: MainWindow, printer_name: str) -> None:
    for view_name in ("device_view", "control_view", "preview_view"):
        view = getattr(window, view_name, None)
        if view is not None and hasattr(view, "select_printer_by_name"):
            try:
                view.select_printer_by_name(printer_name, emit=False)
            except Exception:
                continue


def _capture_widget(window: MainWindow, output_dir: Path, name: str, mode: str) -> ScreenshotRecord:
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{_utc_token()}_{name}.png"
    path = output_dir / filename
    pixmap = window.grab()
    if pixmap.isNull():
        raise VisualAuditError(f"VISUAL_AUDIT_CAPTURE_FAILED:{name}")
    if not pixmap.save(str(path), "PNG"):
        raise VisualAuditError(f"VISUAL_AUDIT_SAVE_FAILED:{name}")
    return ScreenshotRecord(
        name=name,
        path=str(path),
        mode=mode,
        width=int(pixmap.width()),
        height=int(pixmap.height()),
    )


def _capture_rect(widget: QtWidgets.QWidget, rect: QtCore.QRect, output_dir: Path, name: str, mode: str) -> ScreenshotRecord:
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{_utc_token()}_{name}.png"
    path = output_dir / filename
    pixmap = widget.grab(rect)
    if pixmap.isNull():
        raise VisualAuditError(f"VISUAL_AUDIT_CAPTURE_FAILED:{name}")
    if not pixmap.save(str(path), "PNG"):
        raise VisualAuditError(f"VISUAL_AUDIT_SAVE_FAILED:{name}")
    return ScreenshotRecord(
        name=name,
        path=str(path),
        mode=mode,
        width=int(pixmap.width()),
        height=int(pixmap.height()),
    )


def _capture_navigator_closeup(window: MainWindow, output_dir: Path, name: str, mode: str) -> ScreenshotRecord:
    viewer = getattr(window, "viewer", None)
    overlay = getattr(viewer, "_view_cube", None) if viewer is not None else None
    if viewer is None or overlay is None:
        raise VisualAuditError(f"VISUAL_AUDIT_NAVIGATOR_UNAVAILABLE:{name}")
    return _capture_rect(overlay, overlay.rect(), output_dir, name, mode)


def _write_manifest(output_dir: Path, payload: dict[str, object]) -> Path:
    manifest = output_dir / "visual_audit_manifest.json"
    manifest.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return manifest


def run_demo_audit(*, output_dir: str | Path | None = None) -> dict[str, object]:
    app = _ensure_app()
    baseline_widget_ids = snapshot_top_level_widgets(app)
    output_path = Path(output_dir).expanduser().resolve() if output_dir is not None else (
        REPO_ROOT / "App" / "testing" / "visual_audit_output" / _utc_token()
    )
    output_path.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="visual_audit_demo_") as scratch:
        scratch_dir = Path(scratch)
        printers = _build_printers()
        window = None
        try:
            window = MainWindow(printers, {})
            window.resize(1600, 1100)
            window.show()
            app.processEvents()
            QtTest.QTest.qWait(100)

            records: list[ScreenshotRecord] = []
            records.append(_capture_widget(window, output_path, "startup", "prepare"))

            sample_models = _write_sample_models(scratch_dir)
            me_entries, printer_entries = _build_activity_rows()

            # Empty files state.
            window.files_view.set_models([])
            _activate_mode(window, "files")
            app.processEvents()
            QtTest.QTest.qWait(60)
            records.append(_capture_widget(window, output_path, "files_empty", "files"))

            # Populated files state.
            window.files_view.set_models(sample_models)
            app.processEvents()
            QtTest.QTest.qWait(60)
            records.append(_capture_widget(window, output_path, "files_populated", "files"))

            # Activity state with banners.
            window.activity_view.set_me_activity(me_entries)
            window.activity_view.set_printer_activity(printer_entries)
            window.activity_view.set_compliance_banner("Cloud sync is disabled for the demo window.")
            window.activity_view.set_cache_banner("Cached entries loaded from local replay state.")
            _activate_mode(window, "activity")
            app.processEvents()
            QtTest.QTest.qWait(60)
            if hasattr(window.activity_view, "_printers_btn"):
                window.activity_view._printers_btn.click()
                app.processEvents()
                QtTest.QTest.qWait(40)
            records.append(_capture_widget(window, output_path, "activity_banners", "activity"))

            # Prepare default state.
            _sync_printer_selection(window, "Demo Core")
            _activate_mode(window, "prepare")
            app.processEvents()
            QtTest.QTest.qWait(60)
            records.append(_capture_widget(window, output_path, "prepare_default", "prepare"))
            records.append(_capture_navigator_closeup(window, output_path, "prepare_navigator_closeup", "prepare"))

            # Preview after slice with support diagnostics.
            preview = parse_gcode_preview(_build_preview_gcode())
            _activate_mode(window, "preview")
            _sync_printer_selection(window, "Demo Core")
            if hasattr(window.preview_view, "set_preview_data"):
                window.preview_view.set_preview_data(preview)
            window.preview_view.update_stats(_build_preview_stats("tree"))
            app.processEvents()
            QtTest.QTest.qWait(80)
            records.append(_capture_widget(window, output_path, "preview_tree_support", "preview"))
            records.append(_capture_navigator_closeup(window, output_path, "preview_navigator_closeup", "preview"))

            window.preview_view.update_stats(_build_preview_stats("organic"))
            app.processEvents()
            QtTest.QTest.qWait(80)
            records.append(_capture_widget(window, output_path, "preview_organic_support", "preview"))

            # Device live status.
            _activate_mode(window, "device")
            window.device_view.update_live_status(
                head_pos=(123.456, 78.9, 12.345),
                time_left_s=4891,
                pla_remaining_m=3.14,
                pla_low=False,
            )
            app.processEvents()
            QtTest.QTest.qWait(60)
            records.append(_capture_widget(window, output_path, "device_live_status", "device"))

            # Control / calibration route.
            _activate_mode(window, "control")
            _sync_printer_selection(window, "Demo Core")
            app.processEvents()
            QtTest.QTest.qWait(60)
            records.append(_capture_widget(window, output_path, "control_calibration", "control"))

            diagnostics = _viewer_runtime_diagnostics(
                getattr(window, "viewer", None),
                str(app.property("eon_opengl_mode") or "software"),
            )
        finally:
            dispose_created_top_levels(app, baseline_widget_ids, window)

    payload = {
        "ok": True,
        "scenario": "demo",
        "generated_at_utc": _utc_iso(),
        "output_dir": str(output_path),
        "screenshot_count": len(records),
        "screenshots": [record.to_dict() for record in records],
        "renderer_mode": str(diagnostics.get("renderer_mode") or app.property("eon_opengl_mode") or "software"),
        "viewer_runtime_degraded": bool(diagnostics.get("viewer_runtime_degraded")),
        "viewer_runtime_error": str(diagnostics.get("viewer_runtime_error") or ""),
        "viewer_runtime_failure_count": int(diagnostics.get("viewer_runtime_failure_count") or 0),
    }
    _write_manifest(output_path, payload)
    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a timestamped GUI visual audit pack.")
    parser.add_argument("--scenario", default="demo", help="Visual audit scenario to run.")
    parser.add_argument(
        "--output-dir",
        default="",
        help="Optional directory for screenshots and the manifest JSON.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    scenario = str(args.scenario or "").strip().lower()
    if scenario != "demo":
        print(json.dumps({"ok": False, "error": f"UNSUPPORTED_SCENARIO:{scenario}"}))
        return 2
    try:
        payload = run_demo_audit(output_dir=(args.output_dir or None))
        print(json.dumps(payload, indent=2))
        return 0
    except Exception as exc:
        payload = {"ok": False, "error": str(exc), "scenario": scenario}
        print(json.dumps(payload, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

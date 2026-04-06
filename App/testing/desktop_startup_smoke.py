from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator, Mapping

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_OPENGL", "software")

REPO_ROOT = Path(__file__).resolve().parents[2]
APP_ROOT = REPO_ROOT / "App"


def _bootstrap_import_paths() -> None:
    for candidate in (APP_ROOT, REPO_ROOT):
        candidate_text = str(candidate)
        if candidate_text not in sys.path:
            sys.path.insert(0, candidate_text)


if __package__ in (None, ""):
    _bootstrap_import_paths()

from PyQt5 import QtWidgets  # noqa: E402

try:  # pragma: no cover - import path varies by caller cwd
    import main as app_main  # type: ignore  # noqa: E402
    from config.bootstrap import bootstrap_defaults, mark_setup_completed, save_bootstrap_config  # type: ignore  # noqa: E402
except Exception:  # pragma: no cover
    _bootstrap_import_paths()
    from App import main as app_main  # type: ignore  # noqa: E402
    from App.config.bootstrap import bootstrap_defaults, mark_setup_completed, save_bootstrap_config  # type: ignore  # noqa: E402


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


@contextmanager
def _isolated_runtime_environment() -> Iterator[Path]:
    with tempfile.TemporaryDirectory(prefix="desktop_startup_smoke_") as tmp:
        root = Path(tmp)
        config_root = root / "config"
        cache_root = root / "cache"
        config_root.mkdir(parents=True, exist_ok=True)
        cache_root.mkdir(parents=True, exist_ok=True)

        overrides = {
            "APPDATA": str(config_root),
            "LOCALAPPDATA": str(root / "localappdata"),
            "XDG_CONFIG_HOME": str(config_root),
            "XDG_CACHE_HOME": str(cache_root),
        }
        previous = {key: os.environ.get(key) for key in overrides}
        try:
            os.environ.update(overrides)
            yield root
        finally:
            for key, old_value in previous.items():
                if old_value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = old_value


def run_startup_smoke() -> dict[str, object]:
    started = time.perf_counter()
    with _isolated_runtime_environment() as runtime_root:
        renderer_mode = app_main.configure_opengl_mode()
        bootstrap_config = mark_setup_completed(bootstrap_defaults())
        save_bootstrap_config(bootstrap_config)

        app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(["desktop-startup-smoke"])
        app.setApplicationName("EON-OpenSlicer")
        app.setQuitOnLastWindowClosed(False)
        app.setProperty("eon_opengl_mode", renderer_mode)

        ensured_bootstrap = app_main._ensure_bootstrap_configuration(app)
        ui_language = str(ensured_bootstrap.get("ui_language", "en")).strip() or "en"
        region_code = str(ensured_bootstrap.get("region_code", "")).strip().upper()
        os.environ["EON_UI_LANG"] = ui_language
        if region_code:
            os.environ["EON_REGION_CODE"] = region_code

        activity_logger = app_main.ActivityLogger()
        activity_logger.install(app)
        crash_reporter = app_main.CrashReporter(activity_logger=activity_logger)
        crash_reporter.install()
        crash_reporter.install_faulthandler()
        crash_reporter.install_watchdog(app)

        splash = app_main.SplashScreen()
        splash.show()
        splash.start_progress(50)
        app.processEvents()
        app_main._run_preset_startup_validation(app, splash)

        printers, airtable_cfg = app_main.load_printer_config()
        window = app_main.MainWindow(printers=printers, airtable_cfg=airtable_cfg)
        window.activity_logger = activity_logger
        window.crash_reporter = crash_reporter
        activity_logger.track_widget_tree(window)
        window.showMaximized()
        if hasattr(window, "apply_titlebar_theme"):
            window.apply_titlebar_theme()
        app.processEvents()

        window_title = str(window.windowTitle() or "").strip()
        duration_s = max(0.0, time.perf_counter() - started)
        viewer = getattr(window, "viewer", None)
        diagnostics = _viewer_runtime_diagnostics(viewer, renderer_mode)
        report = {
            "ok": True,
            "started_at_utc": _utc_iso(),
            "duration_s": round(duration_s, 3),
            "bootstrap_language": ui_language,
            "bootstrap_region": region_code,
            "printer_count": len(printers),
            "window_title": window_title,
            "window_visible": bool(window.isVisible()),
            "window_maximized": bool(window.isMaximized()),
            "runtime_root": str(runtime_root),
            "renderer_mode": str(diagnostics.get("renderer_mode") or renderer_mode),
            "viewer_runtime_degraded": bool(diagnostics.get("viewer_runtime_degraded")),
            "viewer_runtime_error": str(diagnostics.get("viewer_runtime_error") or ""),
            "viewer_runtime_failure_count": int(diagnostics.get("viewer_runtime_failure_count") or 0),
        }

        splash.close()
        window.close()
        app.processEvents()
        return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--report",
        default="",
        help="Optional path to write the JSON startup smoke report.",
    )
    args = parser.parse_args(argv)

    try:
        report = run_startup_smoke()
    except Exception as exc:
        failure = {
            "ok": False,
            "started_at_utc": _utc_iso(),
            "error": f"{type(exc).__name__}: {exc}",
        }
        if args.report:
            Path(args.report).write_text(json.dumps(failure, indent=2, sort_keys=True), encoding="utf-8")
        print(json.dumps(failure, indent=2, sort_keys=True))
        return 1

    if args.report:
        Path(args.report).write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

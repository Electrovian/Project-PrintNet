import sys
import os
from pathlib import Path
from PyQt5 import QtWidgets, QtCore
from gui.main_window import MainWindow
from gui.bootstrap_wizard import BootstrapSetupDialog
from gui.Windows.splash import SplashScreen
from config.bootstrap import load_bootstrap_config, mark_setup_completed, save_bootstrap_config, setup_completed
from config.printer_config import load_printer_config
from gui.activity_logger import ActivityLogger
from gui.crash_reporter import CrashReporter
from printer_presets import PresetValidationError, validate_preset_python_files


_QT_DLL_DIRECTORY_HANDLES: list[object] = []
_QT_DLL_DIRECTORY_PATHS: set[str] = set()


def _qt_platform_name() -> str:
    return str(os.environ.get("QT_QPA_PLATFORM", "")).strip().lower()


def _default_opengl_mode() -> str:
    platform_name = _qt_platform_name()
    if platform_name in {"offscreen", "minimal", "minimalegl", "headless"}:
        return "software"
    return "desktop" if os.name == "nt" else "software"


def _qt_library_bin_dir() -> Path | None:
    library_info = getattr(QtCore, "QLibraryInfo", None)
    if library_info is None:
        return None
    binaries_path = getattr(library_info, "BinariesPath", None)
    if binaries_path is None:
        return None
    raw_path = ""
    try:
        if hasattr(library_info, "path"):
            raw_path = str(library_info.path(binaries_path) or "")
        elif hasattr(library_info, "location"):
            raw_path = str(library_info.location(binaries_path) or "")
    except Exception:
        return None
    candidate = Path(raw_path).expanduser() if raw_path else None
    if candidate is None or not candidate.is_dir():
        return None
    return candidate


def ensure_qt_runtime_path() -> str:
    qt_bin_dir = _qt_library_bin_dir()
    if qt_bin_dir is None:
        return ""

    qt_bin_text = str(qt_bin_dir)
    path_key = qt_bin_text.lower()
    current_path = os.environ.get("PATH", "")
    path_entries = {entry.strip().lower() for entry in current_path.split(os.pathsep) if entry.strip()}
    if path_key not in path_entries:
        os.environ["PATH"] = qt_bin_text if not current_path else f"{qt_bin_text}{os.pathsep}{current_path}"

    if os.name == "nt" and hasattr(os, "add_dll_directory") and path_key not in _QT_DLL_DIRECTORY_PATHS:
        try:
            handle = os.add_dll_directory(qt_bin_text)
        except (FileNotFoundError, OSError):
            handle = None
        if handle is not None:
            _QT_DLL_DIRECTORY_HANDLES.append(handle)
            _QT_DLL_DIRECTORY_PATHS.add(path_key)
    return qt_bin_text


def normalize_opengl_mode(value: object | None) -> str:
    normalized = str(value or "").strip().lower()
    if normalized in {"software", "desktop"}:
        return normalized
    return _default_opengl_mode()


def configure_opengl_mode(mode: object | None = None) -> str:
    ensure_qt_runtime_path()
    source_mode = mode
    if source_mode is None:
        source_mode = os.environ.get("EON_OPENGL_MODE")
    if source_mode is None or not str(source_mode).strip():
        source_mode = os.environ.get("QT_OPENGL")
    normalized = normalize_opengl_mode(source_mode)
    os.environ["EON_OPENGL_MODE"] = normalized
    os.environ["QT_OPENGL"] = "desktop" if normalized == "desktop" else "software"

    app_instance = QtWidgets.QApplication.instance()
    if app_instance is None:
        software_attr = getattr(QtCore.Qt, "AA_UseSoftwareOpenGL", None)
        desktop_attr = getattr(QtCore.Qt, "AA_UseDesktopOpenGL", None)
        if software_attr is not None:
            QtCore.QCoreApplication.setAttribute(software_attr, normalized == "software")
        if desktop_attr is not None:
            QtCore.QCoreApplication.setAttribute(desktop_attr, normalized == "desktop")
    else:
        app_instance.setProperty("eon_opengl_mode", normalized)
    return normalized


def _run_preset_startup_validation(app: QtWidgets.QApplication, splash: SplashScreen) -> None:
    splash.set_message("Validating preset modules...")
    splash.set_progress(0)
    app.processEvents()

    last_percent = -1
    update_every: int | None = None

    def _on_progress(index: int, total: int, path: str) -> None:
        nonlocal last_percent, update_every
        if total <= 0:
            return
        if update_every is None:
            # Limit expensive UI refreshes while still showing actively checked files.
            update_every = max(1, total // 120)

        should_refresh = index == 1 or index == total or index % update_every == 0
        if not should_refresh:
            return

        percent = int((index * 100) / total)
        if percent != last_percent:
            last_percent = percent
            splash.set_progress(percent)
        file_name = Path(path).name if path else "unknown"
        if len(file_name) > 72:
            file_name = f"{file_name[:69]}..."
        splash.set_message(f"Validating preset modules... ({index}/{total}) {file_name}")
        app.processEvents()

    report = validate_preset_python_files(on_progress=_on_progress)
    splash.set_progress(100)
    splash.set_message(f"Validated {report.checked_count} preset modules.")
    app.processEvents()


def _ensure_bootstrap_configuration(app: QtWidgets.QApplication) -> dict:
    config = load_bootstrap_config()
    if not setup_completed(config):
        dialog = BootstrapSetupDialog(initial=config)
        result = dialog.exec_()
        if result != QtWidgets.QDialog.Accepted:
            raise RuntimeError("SETUP_ABORTED")
        merged = dict(config)
        merged.update(dialog.result_config())
        config = mark_setup_completed(merged)
        save_bootstrap_config(config)
    language = str(config.get("ui_language", "en")).strip() or "en"
    region = str(config.get("region_code", "")).strip()
    app.setProperty("bootstrap_config", dict(config))
    app.setProperty("bootstrap_language", language)
    app.setProperty("bootstrap_region", region)
    return dict(config)


def main() -> int:
    renderer_mode = configure_opengl_mode()
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("EON-OpenSlicer")
    app.setProperty("eon_opengl_mode", renderer_mode)
    try:
        bootstrap_config = _ensure_bootstrap_configuration(app)
    except RuntimeError as exc:
        if str(exc) == "SETUP_ABORTED":
            return 1
        raise
    ui_language = str(bootstrap_config.get("ui_language", "en")).strip() or "en"
    region_code = str(bootstrap_config.get("region_code", "")).strip().upper()
    if ui_language:
        # Main window reads this at construction time.
        os.environ["EON_UI_LANG"] = ui_language
    if region_code:
        os.environ["EON_REGION_CODE"] = region_code

    activity_logger = ActivityLogger()
    activity_logger.install(app)
    crash_reporter = CrashReporter(activity_logger=activity_logger)
    crash_reporter.install()
    crash_reporter.install_faulthandler()
    crash_reporter.install_watchdog(app)

    splash = SplashScreen()
    screen = app.primaryScreen()
    if screen is not None:
        geom = screen.availableGeometry()
        splash.move(
            geom.center().x() - splash.width() // 2,
            geom.center().y() - splash.height() // 2,
        )
    splash.show()
    splash.start_progress(3000)
    app.processEvents()
    try:
        _run_preset_startup_validation(app, splash)
    except PresetValidationError as exc:
        details = "\n".join(f"{item.path} -> {item.reason}" for item in exc.failures[:20])
        if len(exc.failures) > 20:
            details += f"\n... {len(exc.failures) - 20} more failures"
        QtWidgets.QMessageBox.critical(
            None,
            "Preset Validation Failed",
            f"Startup validation failed.\n\n{exc}\n\n{details}",
        )
        return 1

    timer = QtCore.QElapsedTimer()
    timer.start()
    printers, airtable_cfg = load_printer_config()
    window = MainWindow(printers=printers, airtable_cfg=airtable_cfg)
    window.activity_logger = activity_logger
    window.crash_reporter = crash_reporter
    activity_logger.track_widget_tree(window)

    remaining = 3000 - int(timer.elapsed())
    if remaining > 0:
        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(remaining, loop.quit)
        loop.exec_()
    splash.close()

    window.showMaximized()
    if hasattr(window, "apply_titlebar_theme"):
        window.apply_titlebar_theme()
    return app.exec_()

if __name__ == "__main__":
    raise SystemExit(main())

import sys
from pathlib import Path
from PyQt5 import QtWidgets, QtCore
from gui.main_window import MainWindow
from gui.Windows.splash import SplashScreen
from config.printer_config import load_printer_config
from gui.activity_logger import ActivityLogger
from gui.crash_reporter import CrashReporter
from printer_presets import PresetValidationError, validate_preset_python_files


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


def main() -> int:
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("EON-OpenSlicer")

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

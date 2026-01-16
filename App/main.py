import sys
from PyQt5 import QtWidgets, QtCore
from gui.main_window import MainWindow
from gui.Windows.splash import SplashScreen
from config.printer_config import load_printer_config
from gui.activity_logger import ActivityLogger
from gui.crash_reporter import CrashReporter

def main():
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
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

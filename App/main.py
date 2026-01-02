import sys
from PyQt5 import QtWidgets
from gui.main_window import MainWindow
from gui.Windows.splash import SplashScreen
from config.printer_config import load_printer_config

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("OpenSlicer")

    splash = SplashScreen()
    screen = app.primaryScreen()
    if screen is not None:
        geom = screen.availableGeometry()
        splash.move(
            geom.center().x() - splash.width() // 2,
            geom.center().y() - splash.height() // 2,
        )
    splash.show()
    app.processEvents()

    printers, airtable_cfg = load_printer_config()
    window = MainWindow(printers=printers, airtable_cfg=airtable_cfg)
    window.show()
    splash.close()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

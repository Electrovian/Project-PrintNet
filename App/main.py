import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from config.printer_config import load_printer_config

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("OpenSlicer")

    printers, airtable_cfg = load_printer_config()
    window = MainWindow(printers=printers, airtable_cfg=airtable_cfg)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

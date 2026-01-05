from PyQt5 import QtWidgets, QtCore

from ..theme import theme_css


class DeviceView(QtWidgets.QWidget):
    send_requested = QtCore.pyqtSignal(object)
    save_requested = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._printers = []
        self._build_ui()

    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QtWidgets.QLabel("Device")
        title.setObjectName("DeviceTitle")
        layout.addWidget(title)

        select_row = QtWidgets.QHBoxLayout()
        select_label = QtWidgets.QLabel("Select printer:")
        select_row.addWidget(select_label)
        self._printer_combo = QtWidgets.QComboBox(self)
        select_row.addWidget(self._printer_combo, 1)
        layout.addLayout(select_row)

        self._printer_details = QtWidgets.QLabel("")
        self._printer_details.setObjectName("DeviceDetails")
        self._printer_details.setWordWrap(True)
        layout.addWidget(self._printer_details)

        status_frame = QtWidgets.QFrame(self)
        status_frame.setObjectName("DeviceStatus")
        status_layout = QtWidgets.QVBoxLayout(status_frame)
        status_layout.setContentsMargins(12, 10, 12, 10)
        status_layout.setSpacing(8)

        status_title = QtWidgets.QLabel("Live status", status_frame)
        status_title.setObjectName("DeviceStatusTitle")
        status_layout.addWidget(status_title)

        grid = QtWidgets.QGridLayout()
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(6)

        head_label = QtWidgets.QLabel("Head position", status_frame)
        head_label.setObjectName("DeviceStatusLabel")
        self._head_pos_value = QtWidgets.QLabel("n/a", status_frame)
        self._head_pos_value.setObjectName("DeviceStatusValue")
        grid.addWidget(head_label, 0, 0)
        grid.addWidget(self._head_pos_value, 0, 1)

        time_label = QtWidgets.QLabel("Time left", status_frame)
        time_label.setObjectName("DeviceStatusLabel")
        self._time_left_value = QtWidgets.QLabel("n/a", status_frame)
        self._time_left_value.setObjectName("DeviceStatusValue")
        grid.addWidget(time_label, 1, 0)
        grid.addWidget(self._time_left_value, 1, 1)

        pla_label = QtWidgets.QLabel("PLA status", status_frame)
        pla_label.setObjectName("DeviceStatusLabel")
        self._pla_status_value = QtWidgets.QLabel("n/a", status_frame)
        self._pla_status_value.setObjectName("DeviceStatusValue")
        grid.addWidget(pla_label, 2, 0)
        grid.addWidget(self._pla_status_value, 2, 1)

        status_layout.addLayout(grid)
        layout.addWidget(status_frame)

        btn_row = QtWidgets.QHBoxLayout()
        self._send_btn = QtWidgets.QPushButton("Send to printer")
        self._save_btn = QtWidgets.QPushButton("Save G-code")
        btn_row.addWidget(self._send_btn)
        btn_row.addWidget(self._save_btn)
        layout.addLayout(btn_row)
        layout.addStretch(1)

        self._printer_combo.currentIndexChanged.connect(self._update_details)
        self._send_btn.clicked.connect(self._emit_send)
        self._save_btn.clicked.connect(self.save_requested.emit)

        self.apply_theme()

    def set_printers(self, printers):
        self._printers = list(printers or [])
        self._printer_combo.clear()
        if not self._printers:
            self._printer_combo.addItem("No printers configured")
            self._printer_combo.setEnabled(False)
        else:
            self._printer_combo.setEnabled(True)
            for printer in self._printers:
                self._printer_combo.addItem(printer.get("name", "Printer"))
        self._update_details()

    def current_printer(self):
        if not self._printers:
            return None
        index = self._printer_combo.currentIndex()
        if index < 0 or index >= len(self._printers):
            return None
        return self._printers[index]

    def _update_details(self):
        printer = self.current_printer()
        if not printer:
            self._printer_details.setText("No printer selected.")
            self._send_btn.setEnabled(False)
            return
        desc = [
            f"Name: {printer.get('name', 'Printer')}",
            f"Bed: {printer.get('bed_x', 'n/a')} x {printer.get('bed_y', 'n/a')} x {printer.get('bed_z', 'n/a')}",
        ]
        url = printer.get("octoprint_url")
        if url:
            desc.append(f"OctoPrint: {url}")
        self._printer_details.setText("\n".join(desc))
        self._send_btn.setEnabled(True)

    def _emit_send(self):
        printer = self.current_printer()
        if printer is None:
            return
        self.send_requested.emit(printer)

    def update_live_status(
        self,
        head_pos: tuple[float, float, float] | None = None,
        time_left_s: float | None = None,
        pla_remaining_m: float | None = None,
        pla_low: bool | None = None,
    ):
        if hasattr(self, "_head_pos_value"):
            if head_pos is None:
                self._head_pos_value.setText("n/a")
            else:
                x, y, z = head_pos
                self._head_pos_value.setText(f"X: {x:.2f}  Y: {y:.2f}  Z: {z:.2f}")
        if hasattr(self, "_time_left_value"):
            if time_left_s is None:
                self._time_left_value.setText("n/a")
            else:
                self._time_left_value.setText(self._format_duration(time_left_s))
        if hasattr(self, "_pla_status_value"):
            if pla_remaining_m is None or pla_low is None:
                self._pla_status_value.setText("n/a")
            else:
                remaining = max(0.0, float(pla_remaining_m))
                state = "LOW" if pla_low else "OK"
                self._pla_status_value.setText(f"{state} ({remaining:.2f} m left)")
        self._apply_pla_style(pla_low)

    def _apply_pla_style(self, pla_low: bool | None):
        if not hasattr(self, "_pla_status_value"):
            return
        if pla_low is True:
            color = theme_css("axis_x")
            weight = "600"
        elif pla_low is False:
            color = theme_css("topbar_accent")
            weight = "600"
        else:
            color = theme_css("popup_muted_text")
            weight = "400"
        self._pla_status_value.setStyleSheet(f"color: {color}; font-weight: {weight};")

    def _format_duration(self, seconds: float) -> str:
        seconds = max(0, int(round(seconds)))
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        if hours:
            return f"{hours}h{mins:02d}m"
        return f"{mins}m{secs:02d}s"

    def apply_theme(self):
        self.setStyleSheet(
            "QWidget {"
            f"  background: {theme_css('popup_bg')};"
            f"  color: {theme_css('popup_text')};"
            "}"
            "QLabel#DeviceTitle {"
            "  font-size: 18px;"
            "  font-weight: 600;"
            "}"
            "QFrame#DeviceStatus {"
            f"  border: 1px solid {theme_css('action_panel_border')};"
            f"  background: {theme_css('action_panel_bg')};"
            "  border-radius: 8px;"
            "}"
            "QLabel#DeviceStatusTitle {"
            "  font-size: 13px;"
            "  font-weight: 600;"
            "}"
            "QLabel#DeviceStatusLabel {"
            f"  color: {theme_css('popup_muted_text')};"
            "}"
            "QLabel#DeviceStatusValue {"
            "  font-weight: 600;"
            "}"
            "QPushButton {"
            f"  background: {theme_css('action_button_bg')};"
            f"  color: {theme_css('action_button_text')};"
            f"  border: 1px solid {theme_css('action_panel_border')};"
            "  border-radius: 6px;"
            "  padding: 6px 14px;"
            "}"
            "QPushButton:hover {"
            f"  background: {theme_css('action_button_hover_bg')};"
            "}"
            "QPushButton:pressed {"
            f"  background: {theme_css('action_button_active_bg')};"
            "}"
            "QComboBox {"
            f"  background: {theme_css('popup_input_bg')};"
            f"  color: {theme_css('popup_input_text')};"
            f"  border: 1px solid {theme_css('popup_input_border')};"
            "  padding: 3px 8px;"
            "  border-radius: 4px;"
            "}"
        )
        self._apply_pla_style(None)

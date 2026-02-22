from PyQt5 import QtWidgets, QtCore

from ..theme import theme_css
from config.defaults import DEFAULTS


class DeviceView(QtWidgets.QWidget):
    send_requested = QtCore.pyqtSignal(object)
    save_requested = QtCore.pyqtSignal()
    email_requested = QtCore.pyqtSignal()
    printer_changed = QtCore.pyqtSignal(object)

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
        select_label = QtWidgets.QLabel("Search printer:")
        select_row.addWidget(select_label)
        self._printer_combo = QtWidgets.QComboBox(self)
        self._printer_combo.setObjectName("DeviceCombo")
        self._printer_combo.setEditable(True)
        self._printer_combo.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        completer = QtWidgets.QCompleter(self._printer_combo.model(), self)
        completer.setFilterMode(QtCore.Qt.MatchContains)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self._printer_combo.setCompleter(completer)
        if self._printer_combo.lineEdit() is not None:
            self._printer_combo.lineEdit().setPlaceholderText("Search connected printers")
        select_row.addWidget(self._printer_combo, 1)
        layout.addLayout(select_row)

        self._printer_details = QtWidgets.QLabel("")
        self._printer_details.setObjectName("DeviceDetails")
        self._printer_details.setWordWrap(True)
        layout.addWidget(self._printer_details)

        content_row = QtWidgets.QHBoxLayout()
        content_row.setSpacing(16)

        left_col = QtWidgets.QVBoxLayout()
        left_col.setSpacing(16)

        camera_frame = QtWidgets.QFrame(self)
        camera_frame.setObjectName("DeviceCamera")
        camera_layout = QtWidgets.QVBoxLayout(camera_frame)
        camera_layout.setContentsMargins(12, 12, 12, 12)
        camera_layout.setSpacing(8)
        camera_title = QtWidgets.QLabel("Live preview", camera_frame)
        camera_title.setObjectName("DeviceSectionTitle")
        camera_layout.addWidget(camera_title)
        camera_placeholder = QtWidgets.QLabel("Camera feed not connected", camera_frame)
        camera_placeholder.setObjectName("DeviceCameraPlaceholder")
        camera_placeholder.setAlignment(QtCore.Qt.AlignCenter)
        camera_layout.addWidget(camera_placeholder, 1)
        left_col.addWidget(camera_frame, 1)

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
        left_col.addWidget(status_frame)

        btn_row = QtWidgets.QHBoxLayout()
        self._send_btn = QtWidgets.QPushButton("Send to printer")
        self._save_btn = QtWidgets.QPushButton("Save G-code")
        self._email_btn = QtWidgets.QPushButton("Send email")
        btn_row.addWidget(self._send_btn)
        btn_row.addWidget(self._save_btn)
        btn_row.addWidget(self._email_btn)
        left_col.addLayout(btn_row)
        left_col.addStretch(1)

        content_row.addLayout(left_col, 3)

        queue_frame = QtWidgets.QFrame(self)
        queue_frame.setObjectName("DeviceQueue")
        queue_layout = QtWidgets.QVBoxLayout(queue_frame)
        queue_layout.setContentsMargins(12, 12, 12, 12)
        queue_layout.setSpacing(8)
        queue_title = QtWidgets.QLabel("Queue", queue_frame)
        queue_title.setObjectName("DeviceSectionTitle")
        queue_layout.addWidget(queue_title)
        queue_placeholder = QtWidgets.QLabel("No queued jobs yet.", queue_frame)
        queue_placeholder.setObjectName("DeviceQueuePlaceholder")
        queue_placeholder.setAlignment(QtCore.Qt.AlignCenter)
        queue_layout.addWidget(queue_placeholder, 1)
        right_col = QtWidgets.QVBoxLayout()
        right_col.setSpacing(16)
        right_col.addWidget(queue_frame, 2)

        connected_frame = QtWidgets.QFrame(self)
        connected_frame.setObjectName("DeviceConnected")
        connected_layout = QtWidgets.QVBoxLayout(connected_frame)
        connected_layout.setContentsMargins(12, 12, 12, 12)
        connected_layout.setSpacing(8)
        self._connected_title = QtWidgets.QLabel("Connected printers", connected_frame)
        self._connected_title.setObjectName("DeviceSectionTitle")
        connected_layout.addWidget(self._connected_title)
        self._connected_scroll = QtWidgets.QScrollArea(connected_frame)
        self._connected_scroll.setObjectName("DeviceConnectedScroll")
        self._connected_scroll.setWidgetResizable(True)
        connected_container = QtWidgets.QWidget(self._connected_scroll)
        connected_container.setObjectName("DeviceConnectedList")
        self._connected_list = QtWidgets.QVBoxLayout(connected_container)
        self._connected_list.setContentsMargins(0, 0, 0, 0)
        self._connected_list.setSpacing(6)
        self._connected_scroll.setWidget(connected_container)
        connected_layout.addWidget(self._connected_scroll, 1)
        right_col.addWidget(connected_frame, 1)
        content_row.addLayout(right_col, 2)

        layout.addLayout(content_row, 1)
        layout.addStretch(1)

        self._printer_combo.currentIndexChanged.connect(lambda _idx: self._update_details())
        self._send_btn.clicked.connect(self._emit_send)
        self._save_btn.clicked.connect(self.save_requested.emit)
        self._email_btn.clicked.connect(self.email_requested.emit)

        self.apply_theme()

    def set_printers(self, printers):
        raw_printers = list(printers or [])
        self._printers = [
            printer
            for printer in raw_printers
            if not (isinstance(printer, dict) and printer.get("catalog_only"))
        ]
        self._printer_combo.clear()
        if not self._printers:
            self._printer_combo.addItem("No connected printers")
            self._printer_combo.setEnabled(False)
        else:
            self._printer_combo.setEnabled(True)
            default_name = ""
            main = self.parent()
            runtime_state = getattr(main, "runtime_printer_state", None) if main is not None else None
            if runtime_state is not None:
                default_name = str(getattr(runtime_state, "name", "")).strip().lower()
            if not default_name:
                default_name = str(DEFAULTS.get("printer", {}).get("name", "")).strip().lower()
            default_index = None
            for idx, printer in enumerate(self._printers):
                name = printer.get("name", "Printer")
                self._printer_combo.addItem(name)
                if default_name and str(name or "").strip().lower() == default_name:
                    default_index = idx
            if default_index is not None:
                self._printer_combo.setCurrentIndex(default_index)
        self._populate_connected_list()
        self._update_details()

    def current_printer(self):
        if not self._printers:
            return None
        index = self._printer_combo.currentIndex()
        if index < 0 or index >= len(self._printers):
            return None
        return self._printers[index]

    def select_printer_by_name(self, name: str, emit: bool = True):
        target = str(name or "").strip().lower()
        if not target:
            return
        idx = None
        for row in range(self._printer_combo.count()):
            if self._printer_combo.itemText(row).strip().lower() == target:
                idx = row
                break
        if idx is None:
            return
        block = self._printer_combo.blockSignals(True)
        self._printer_combo.setCurrentIndex(idx)
        self._printer_combo.blockSignals(block)
        self._update_details(emit_signal=emit)

    def _update_details(self, emit_signal: bool = True):
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
        if emit_signal:
            self.printer_changed.emit(printer)

    def _populate_connected_list(self):
        if not hasattr(self, "_connected_list"):
            return

        def _clear_layout(layout):
            while layout.count():
                item = layout.takeAt(0)
                if item is None:
                    continue
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                    continue
                nested = item.layout()
                if nested is not None:
                    _clear_layout(nested)

        _clear_layout(self._connected_list)

        if hasattr(self, "_connected_title"):
            if self._printers:
                self._connected_title.setText(f"Connected printers ({len(self._printers)})")
            else:
                self._connected_title.setText("Connected printers")

        if not self._printers:
            placeholder = QtWidgets.QLabel("No connected printers.")
            placeholder.setObjectName("DeviceQueuePlaceholder")
            placeholder.setAlignment(QtCore.Qt.AlignCenter)
            self._connected_list.addWidget(placeholder)
            return

        for printer in self._printers:
            name = printer.get("name", "Printer")
            bed = f"{printer.get('bed_x', 'n/a')} x {printer.get('bed_y', 'n/a')} x {printer.get('bed_z', 'n/a')}"
            row = QtWidgets.QFrame(self)
            row.setObjectName("DevicePrinterItem")
            row_layout = QtWidgets.QVBoxLayout(row)
            row_layout.setContentsMargins(10, 6, 10, 6)
            row_layout.setSpacing(2)
            name_label = QtWidgets.QLabel(str(name), row)
            name_label.setObjectName("DevicePrinterName")
            bed_label = QtWidgets.QLabel(f"Bed: {bed}", row)
            bed_label.setObjectName("DevicePrinterMeta")
            row_layout.addWidget(name_label)
            row_layout.addWidget(bed_label)
            self._connected_list.addWidget(row)
        self._connected_list.addStretch(1)

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
            "QFrame#DeviceCamera, QFrame#DeviceQueue {"
            f"  border: 1px solid {theme_css('action_panel_border')};"
            f"  background: {theme_css('action_panel_bg')};"
            "  border-radius: 8px;"
            "}"
            "QFrame#DeviceConnected {"
            f"  border: 1px solid {theme_css('action_panel_border')};"
            f"  background: {theme_css('action_panel_bg')};"
            "  border-radius: 8px;"
            "}"
            "QLabel#DeviceSectionTitle {"
            "  font-size: 13px;"
            "  font-weight: 600;"
            "}"
            "QLabel#DeviceCameraPlaceholder, QLabel#DeviceQueuePlaceholder {"
            f"  color: {theme_css('popup_muted_text')};"
            "  background: #0b0c0e;"
            "  border-radius: 6px;"
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
            "QFrame#DevicePrinterItem {"
            f"  background: {theme_css('popup_bg')};"
            f"  border: 1px solid {theme_css('action_panel_border')};"
            "  border-radius: 6px;"
            "}"
            "QScrollArea#DeviceConnectedScroll {"
            "  border: none;"
            "  background: transparent;"
            "}"
            "QWidget#DeviceConnectedList {"
            "  background: transparent;"
            "}"
            "QLabel#DevicePrinterName {"
            "  font-weight: 600;"
            "}"
            "QLabel#DevicePrinterMeta {"
            f"  color: {theme_css('popup_muted_text')};"
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
            "QComboBox#DeviceCombo {"
            f"  background: {theme_css('popup_input_bg')};"
            f"  color: {theme_css('popup_input_text')};"
            f"  border: 1px solid {theme_css('popup_input_border')};"
            "  padding: 3px 8px;"
            "  border-radius: 4px;"
            "}"
        )
        self._apply_pla_style(None)

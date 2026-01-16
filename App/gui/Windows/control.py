from PyQt5 import QtWidgets, QtCore

from ..theme import theme_css
from config.defaults import DEFAULTS


class ControlView(QtWidgets.QWidget):
    printer_changed = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._printers = []
        self._build_ui()

    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QtWidgets.QLabel("Control", self)
        title.setObjectName("ControlTitle")
        layout.addWidget(title)

        select_row = QtWidgets.QHBoxLayout()
        select_label = QtWidgets.QLabel("Select printer:", self)
        select_row.addWidget(select_label)
        self._printer_combo = QtWidgets.QComboBox(self)
        select_row.addWidget(self._printer_combo, 1)
        layout.addLayout(select_row)

        self._printer_details = QtWidgets.QLabel("", self)
        self._printer_details.setObjectName("ControlDetails")
        self._printer_details.setWordWrap(True)
        layout.addWidget(self._printer_details)

        content = QtWidgets.QHBoxLayout()
        content.setSpacing(16)

        left_col = QtWidgets.QVBoxLayout()
        left_col.setSpacing(16)
        camera_frame = QtWidgets.QFrame(self)
        camera_frame.setObjectName("ControlCamera")
        camera_layout = QtWidgets.QVBoxLayout(camera_frame)
        camera_layout.setContentsMargins(12, 12, 12, 12)
        camera_layout.setSpacing(8)
        camera_title = QtWidgets.QLabel("Live preview", camera_frame)
        camera_title.setObjectName("ControlSectionTitle")
        camera_layout.addWidget(camera_title)
        camera_placeholder = QtWidgets.QLabel("Camera feed not connected", camera_frame)
        camera_placeholder.setObjectName("ControlCameraPlaceholder")
        camera_placeholder.setAlignment(QtCore.Qt.AlignCenter)
        camera_layout.addWidget(camera_placeholder, 1)
        left_col.addWidget(camera_frame, 1)

        hint = QtWidgets.QLabel("Manual controls are enabled when the printer is idle.", self)
        hint.setObjectName("ControlHint")
        left_col.addWidget(hint)

        content.addLayout(left_col, 3)

        control_panel = QtWidgets.QFrame(self)
        control_panel.setObjectName("ControlPanel")
        panel_layout = QtWidgets.QVBoxLayout(control_panel)
        panel_layout.setContentsMargins(12, 12, 12, 12)
        panel_layout.setSpacing(12)

        tabs_row = QtWidgets.QHBoxLayout()
        tabs_group = QtWidgets.QButtonGroup(self)
        tabs_group.setExclusive(True)
        self._control_tab = self._make_tab_button("Control", checked=True)
        self._parts_tab = self._make_tab_button("Printer Parts")
        self._options_tab = self._make_tab_button("Print Options")
        self._safety_tab = self._make_tab_button("Safety Options")
        self._calib_tab = self._make_tab_button("Calibration")
        for btn in (self._control_tab, self._parts_tab, self._options_tab, self._safety_tab, self._calib_tab):
            tabs_group.addButton(btn)
            tabs_row.addWidget(btn)
        tabs_row.addStretch(1)
        panel_layout.addLayout(tabs_row)

        temp_card, temp_body = self._make_card("Temperature")
        temp_layout = QtWidgets.QGridLayout(temp_body)
        temp_layout.setContentsMargins(12, 12, 12, 12)
        temp_layout.setHorizontalSpacing(8)
        temp_layout.setVerticalSpacing(8)
        temp_layout.addWidget(QtWidgets.QLabel("Nozzle", temp_card), 0, 0)
        self._nozzle_temp = QtWidgets.QLabel("-- / -- C", temp_card)
        self._nozzle_temp.setObjectName("ControlValue")
        temp_layout.addWidget(self._nozzle_temp, 0, 1)
        self._nozzle_target = self._make_spinbox(temp_card, 0, 320, " C")
        temp_layout.addWidget(self._nozzle_target, 0, 2)
        temp_layout.addWidget(self._make_action_button("Set"), 0, 3)
        temp_layout.addWidget(QtWidgets.QLabel("Bed", temp_card), 1, 0)
        self._bed_temp = QtWidgets.QLabel("-- / -- C", temp_card)
        self._bed_temp.setObjectName("ControlValue")
        temp_layout.addWidget(self._bed_temp, 1, 1)
        self._bed_target = self._make_spinbox(temp_card, 0, 130, " C")
        temp_layout.addWidget(self._bed_target, 1, 2)
        temp_layout.addWidget(self._make_action_button("Set"), 1, 3)
        panel_layout.addWidget(temp_card)

        move_card, move_body = self._make_card("Movement")
        move_layout = QtWidgets.QVBoxLayout(move_body)
        move_layout.setContentsMargins(12, 12, 12, 12)
        move_layout.setSpacing(10)
        step_row = QtWidgets.QHBoxLayout()
        step_row.addWidget(QtWidgets.QLabel("Step", move_card))
        self._step_combo = QtWidgets.QComboBox(move_card)
        self._step_combo.setObjectName("ControlCombo")
        self._step_combo.addItems(["0.1 mm", "1 mm", "10 mm", "100 mm"])
        step_row.addWidget(self._step_combo)
        step_row.addStretch(1)
        move_layout.addLayout(step_row)

        jog_row = QtWidgets.QHBoxLayout()
        jog_row.setSpacing(10)

        jog_pad = QtWidgets.QFrame(move_card)
        jog_pad.setObjectName("ControlJogPad")
        jog_pad.setFixedSize(180, 180)
        jog_layout = QtWidgets.QGridLayout(jog_pad)
        jog_layout.setContentsMargins(18, 18, 18, 18)
        jog_layout.setHorizontalSpacing(8)
        jog_layout.setVerticalSpacing(8)
        jog_layout.addWidget(self._make_jog_button("Y+"), 0, 1)
        jog_layout.addWidget(self._make_jog_button("X-"), 1, 0)
        jog_layout.addWidget(self._make_jog_button("Home", center=True), 1, 1)
        jog_layout.addWidget(self._make_jog_button("X+"), 1, 2)
        jog_layout.addWidget(self._make_jog_button("Y-"), 2, 1)
        jog_row.addWidget(jog_pad)

        axis_col = QtWidgets.QVBoxLayout()
        axis_col.setSpacing(8)
        axis_col.addWidget(self._make_move_button("Z+"))
        axis_col.addWidget(self._make_move_button("Z-"))
        axis_col.addSpacing(6)
        axis_col.addWidget(self._make_move_button("E+"))
        axis_col.addWidget(self._make_move_button("E-"))
        axis_col.addStretch(1)
        jog_row.addLayout(axis_col)
        jog_row.addStretch(1)
        move_layout.addLayout(jog_row)
        panel_layout.addWidget(move_card)

        aux_card, aux_body = self._make_card("Auxiliary")
        aux_layout = QtWidgets.QGridLayout(aux_body)
        aux_layout.setContentsMargins(12, 12, 12, 12)
        aux_layout.setHorizontalSpacing(8)
        aux_layout.setVerticalSpacing(8)
        self._fan_toggle = QtWidgets.QCheckBox("Fan", aux_card)
        self._lamp_toggle = QtWidgets.QCheckBox("Lamp", aux_card)
        self._motors_toggle = QtWidgets.QCheckBox("Motors enabled", aux_card)
        aux_layout.addWidget(self._fan_toggle, 0, 0)
        aux_layout.addWidget(self._lamp_toggle, 0, 1)
        aux_layout.addWidget(self._motors_toggle, 1, 0, 1, 2)
        panel_layout.addWidget(aux_card)
        panel_layout.addStretch(1)

        content.addWidget(control_panel, 2)
        layout.addLayout(content, 1)

        self._printer_combo.currentIndexChanged.connect(lambda _idx: self._update_details())
        self.apply_theme()

    def _make_tab_button(self, label: str, checked: bool = False):
        btn = QtWidgets.QToolButton(self)
        btn.setText(label)
        btn.setCheckable(True)
        btn.setChecked(checked)
        btn.setObjectName("ControlTab")
        return btn

    def _make_card(self, title: str):
        frame = QtWidgets.QFrame(self)
        frame.setObjectName("ControlCard")
        layout = QtWidgets.QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        header = QtWidgets.QLabel(title, frame)
        header.setObjectName("ControlCardTitle")
        layout.addWidget(header)
        body = QtWidgets.QWidget(frame)
        body.setObjectName("ControlCardBody")
        layout.addWidget(body)
        return frame, body

    def _make_move_button(self, label: str):
        btn = QtWidgets.QToolButton(self)
        btn.setText(label)
        btn.setObjectName("ControlMoveButton")
        btn.setCursor(QtCore.Qt.PointingHandCursor)
        return btn

    def _make_jog_button(self, label: str, center: bool = False):
        btn = QtWidgets.QToolButton(self)
        btn.setText(label)
        btn.setObjectName("ControlJogButton" if not center else "ControlJogHome")
        btn.setCursor(QtCore.Qt.PointingHandCursor)
        btn.setFixedSize(54, 38 if not center else 44)
        return btn

    def _make_action_button(self, label: str):
        btn = QtWidgets.QPushButton(label, self)
        btn.setObjectName("ControlActionButton")
        return btn

    def _make_spinbox(self, parent, min_val: int, max_val: int, suffix: str):
        spin = QtWidgets.QSpinBox(parent)
        spin.setObjectName("ControlSpin")
        spin.setRange(min_val, max_val)
        spin.setSuffix(suffix)
        return spin

    def set_printers(self, printers):
        self._printers = list(printers or [])
        self._printer_combo.clear()
        if not self._printers:
            self._printer_combo.addItem("No printers configured")
            self._printer_combo.setEnabled(False)
            return
        self._printer_combo.setEnabled(True)
        default_name = str(DEFAULTS.get("printer", {}).get("name", "")).strip().lower()
        default_index = None
        for idx, printer in enumerate(self._printers):
            name = printer.get("name") if isinstance(printer, dict) else None
            self._printer_combo.addItem(name or "Printer")
            if default_name and str(name or "").strip().lower() == default_name:
                default_index = idx
        if default_index is not None:
            self._printer_combo.setCurrentIndex(default_index)
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
            return
        desc = [
            f"Name: {printer.get('name', 'Printer')}",
            f"Bed: {printer.get('bed_x', 'n/a')} x {printer.get('bed_y', 'n/a')} x {printer.get('bed_z', 'n/a')}",
        ]
        url = printer.get("octoprint_url")
        if url:
            desc.append(f"OctoPrint: {url}")
        self._printer_details.setText("\n".join(desc))
        if emit_signal:
            self.printer_changed.emit(printer)

    def apply_theme(self):
        self.setStyleSheet(
            "QWidget {"
            f"  background: {theme_css('popup_bg')};"
            f"  color: {theme_css('popup_text')};"
            "}"
            "QLabel#ControlTitle {"
            "  font-size: 18px;"
            "  font-weight: 600;"
            "}"
            "QLabel#ControlSectionTitle {"
            "  font-size: 13px;"
            "  font-weight: 600;"
            "}"
            "QLabel#ControlHint {"
            f"  color: {theme_css('popup_muted_text')};"
            "}"
            "QLabel#ControlDetails {"
            f"  color: {theme_css('popup_muted_text')};"
            "}"
            "QFrame#ControlCamera, QFrame#ControlPanel, QFrame#ControlCard {"
            f"  border: 1px solid {theme_css('action_panel_border')};"
            f"  background: {theme_css('action_panel_bg')};"
            "  border-radius: 8px;"
            "}"
            "QLabel#ControlCameraPlaceholder {"
            f"  color: {theme_css('popup_muted_text')};"
            "  background: #0b0c0e;"
            "  border-radius: 6px;"
            "}"
            "QLabel#ControlCardTitle {"
            "  padding: 0 0 6px 0;"
            "  font-weight: 600;"
            "}"
            "QLabel#ControlValue {"
            "  font-weight: 600;"
            "}"
            "QToolButton#ControlTab {"
            "  padding: 6px 10px;"
            "  border-radius: 6px;"
            "  border: 1px solid transparent;"
            "}"
            "QToolButton#ControlTab:checked {"
            f"  background: {theme_css('topbar_accent')};"
            f"  color: {theme_css('popup_text')};"
            "  font-weight: 600;"
            "}"
            "QToolButton#ControlMoveButton {"
            f"  background: {theme_css('action_button_bg')};"
            f"  border: 1px solid {theme_css('action_panel_border')};"
            "  border-radius: 6px;"
            "  padding: 6px 10px;"
            "}"
            "QFrame#ControlJogPad {"
            f"  background: {theme_css('action_button_bg')};"
            f"  border: 1px solid {theme_css('action_panel_border')};"
            "  border-radius: 90px;"
            "}"
            "QToolButton#ControlJogButton {"
            f"  background: {theme_css('action_button_bg')};"
            f"  border: 1px solid {theme_css('action_panel_border')};"
            "  border-radius: 10px;"
            "  padding: 4px 6px;"
            "}"
            "QToolButton#ControlJogHome {"
            f"  background: {theme_css('topbar_accent')};"
            f"  color: {theme_css('popup_text')};"
            "  border: 1px solid transparent;"
            "  border-radius: 14px;"
            "  font-weight: 600;"
            "}"
            "QToolButton#ControlMoveButton:hover {"
            f"  background: {theme_css('action_button_hover_bg')};"
            "}"
            "QToolButton#ControlJogButton:hover {"
            f"  background: {theme_css('action_button_hover_bg')};"
            "}"
            "QToolButton#ControlMoveButton:pressed {"
            f"  background: {theme_css('action_button_active_bg')};"
            "}"
            "QToolButton#ControlJogButton:pressed, QToolButton#ControlJogHome:pressed {"
            f"  background: {theme_css('action_button_active_bg')};"
            "}"
            "QPushButton#ControlActionButton {"
            f"  background: {theme_css('action_button_bg')};"
            f"  color: {theme_css('action_button_text')};"
            f"  border: 1px solid {theme_css('action_panel_border')};"
            "  border-radius: 6px;"
            "  padding: 4px 10px;"
            "}"
            "QPushButton#ControlActionButton:hover {"
            f"  background: {theme_css('action_button_hover_bg')};"
            "}"
            "QPushButton#ControlActionButton:pressed {"
            f"  background: {theme_css('action_button_active_bg')};"
            "}"
            "QComboBox#ControlCombo, QSpinBox#ControlSpin {"
            f"  background: {theme_css('popup_input_bg')};"
            f"  color: {theme_css('popup_input_text')};"
            f"  border: 1px solid {theme_css('popup_input_border')};"
            "  padding: 3px 8px;"
            "  border-radius: 4px;"
            "}"
        )

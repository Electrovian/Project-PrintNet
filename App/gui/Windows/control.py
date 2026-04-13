from PyQt5 import QtCore, QtWidgets

from ..i18n import tr
from ..printer_selection import connector_endpoint, connector_name
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
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        header_row = QtWidgets.QHBoxLayout()
        header_row.setSpacing(12)

        title_col = QtWidgets.QVBoxLayout()
        title_col.setSpacing(1)
        title = QtWidgets.QLabel(tr("control.title"), self)
        title.setObjectName("ControlTitle")
        subtitle = QtWidgets.QLabel(tr("control.subtitle"), self)
        subtitle.setObjectName("ControlSubtitle")
        title_col.addWidget(title)
        title_col.addWidget(subtitle)
        header_row.addLayout(title_col, 1)

        selector = QtWidgets.QFrame(self)
        selector.setObjectName("ControlSelector")
        selector_layout = QtWidgets.QHBoxLayout(selector)
        selector_layout.setContentsMargins(10, 8, 10, 8)
        selector_layout.setSpacing(8)
        selector_layout.addWidget(QtWidgets.QLabel(tr("control.selector.printer"), selector))
        self._printer_combo = QtWidgets.QComboBox(selector)
        self._printer_combo.setObjectName("ControlCombo")
        selector_layout.addWidget(self._printer_combo, 1)
        header_row.addWidget(selector, 2)
        layout.addLayout(header_row)

        self._printer_details = QtWidgets.QLabel("", self)
        self._printer_details.setObjectName("ControlDetails")
        self._printer_details.setWordWrap(True)
        layout.addWidget(self._printer_details)

        top_row = QtWidgets.QHBoxLayout()
        top_row.setSpacing(12)

        quick_frame = QtWidgets.QFrame(self)
        quick_frame.setObjectName("ControlQuickFrame")
        quick_layout = QtWidgets.QHBoxLayout(quick_frame)
        quick_layout.setContentsMargins(10, 8, 10, 8)
        quick_layout.setSpacing(8)
        quick_group = QtWidgets.QButtonGroup(self)
        quick_group.setExclusive(True)
        self._jog_mode_btn = self._make_quick_button(tr("control.quick.jog"), checked=True)
        self._extruder_mode_btn = self._make_quick_button(tr("control.quick.extruders"))
        quick_group.addButton(self._jog_mode_btn)
        quick_group.addButton(self._extruder_mode_btn)
        quick_layout.addWidget(self._jog_mode_btn)
        quick_layout.addWidget(self._extruder_mode_btn)
        self._restart_btn = QtWidgets.QPushButton(tr("control.quick.restart"), quick_frame)
        self._restart_btn.setObjectName("ControlDangerButton")
        quick_layout.addWidget(self._restart_btn)
        quick_layout.addStretch(1)
        top_row.addWidget(quick_frame, 2)

        telemetry = QtWidgets.QFrame(self)
        telemetry.setObjectName("ControlTelemetry")
        telemetry_layout = QtWidgets.QGridLayout(telemetry)
        telemetry_layout.setContentsMargins(10, 8, 10, 8)
        telemetry_layout.setHorizontalSpacing(16)
        telemetry_layout.setVerticalSpacing(4)
        self._axis_x = QtWidgets.QLabel(tr("control.telemetry.axis_x"), telemetry)
        self._axis_y = QtWidgets.QLabel(tr("control.telemetry.axis_y"), telemetry)
        self._axis_z = QtWidgets.QLabel(tr("control.telemetry.axis_z"), telemetry)
        self._axis_e = QtWidgets.QLabel(tr("control.telemetry.axis_e"), telemetry)
        self._telemetry_nozzle = QtWidgets.QLabel(tr("control.telemetry.extruder"), telemetry)
        self._telemetry_bed = QtWidgets.QLabel(tr("control.telemetry.heatbed"), telemetry)
        for widget in (
            self._axis_x,
            self._axis_y,
            self._axis_z,
            self._axis_e,
            self._telemetry_nozzle,
            self._telemetry_bed,
        ):
            widget.setObjectName("ControlTelemetryValue")
        telemetry_layout.addWidget(self._axis_x, 0, 0)
        telemetry_layout.addWidget(self._axis_z, 0, 1)
        telemetry_layout.addWidget(self._telemetry_nozzle, 0, 2)
        telemetry_layout.addWidget(self._axis_y, 1, 0)
        telemetry_layout.addWidget(self._axis_e, 1, 1)
        telemetry_layout.addWidget(self._telemetry_bed, 1, 2)
        telemetry_layout.setColumnStretch(2, 1)
        top_row.addWidget(telemetry, 3)

        layout.addLayout(top_row)

        body_row = QtWidgets.QHBoxLayout()
        body_row.setSpacing(12)

        left_col = QtWidgets.QVBoxLayout()
        left_col.setSpacing(12)

        speed_card, speed_body = self._make_card(tr("control.card.movement_speed"))
        speed_layout = QtWidgets.QGridLayout(speed_body)
        speed_layout.setContentsMargins(12, 10, 12, 12)
        speed_layout.setHorizontalSpacing(8)
        speed_layout.setVerticalSpacing(8)
        speed_layout.addWidget(QtWidgets.QLabel(tr("control.field.speed_xy"), speed_card), 0, 0)
        self._speed_xy_spin = self._make_spinbox(speed_card, 1, 10000, " mm/s")
        self._speed_xy_spin.setValue(2000)
        speed_layout.addWidget(self._speed_xy_spin, 0, 1)
        speed_layout.addWidget(QtWidgets.QLabel(tr("control.field.speed_z"), speed_card), 0, 2)
        self._speed_z_spin = self._make_spinbox(speed_card, 1, 5000, " mm/s")
        self._speed_z_spin.setValue(300)
        speed_layout.addWidget(self._speed_z_spin, 0, 3)
        speed_layout.setColumnStretch(1, 1)
        speed_layout.setColumnStretch(3, 1)
        left_col.addWidget(speed_card)

        move_card, move_body = self._make_card(tr("control.card.movement"))
        move_layout = QtWidgets.QVBoxLayout(move_body)
        move_layout.setContentsMargins(12, 10, 12, 12)
        move_layout.setSpacing(10)
        step_row = QtWidgets.QHBoxLayout()
        step_row.addWidget(QtWidgets.QLabel(tr("control.field.step"), move_card))
        self._step_combo = QtWidgets.QComboBox(move_card)
        self._step_combo.setObjectName("ControlCombo")
        self._step_combo.addItems(
            [
                tr("control.step.0_1"),
                tr("control.step.1"),
                tr("control.step.10"),
                tr("control.step.100"),
            ]
        )
        step_row.addWidget(self._step_combo)
        step_row.addStretch(1)
        move_layout.addLayout(step_row)

        jog_row = QtWidgets.QHBoxLayout()
        jog_row.setSpacing(10)
        jog_pad = QtWidgets.QFrame(move_card)
        jog_pad.setObjectName("ControlJogPad")
        jog_pad.setFixedSize(190, 190)
        jog_layout = QtWidgets.QGridLayout(jog_pad)
        jog_layout.setContentsMargins(18, 18, 18, 18)
        jog_layout.setHorizontalSpacing(8)
        jog_layout.setVerticalSpacing(8)
        jog_layout.addWidget(self._make_jog_button("Y+"), 0, 1)
        jog_layout.addWidget(self._make_jog_button("X-"), 1, 0)
        jog_layout.addWidget(self._make_jog_button(tr("control.button.home_xy"), center=True), 1, 1)
        jog_layout.addWidget(self._make_jog_button("X+"), 1, 2)
        jog_layout.addWidget(self._make_jog_button("Y-"), 2, 1)
        jog_row.addWidget(jog_pad)

        axis_col = QtWidgets.QVBoxLayout()
        axis_col.setSpacing(7)
        axis_col.addWidget(self._make_move_button("Z+"))
        axis_col.addWidget(self._make_move_button("Z-"))
        axis_col.addSpacing(8)
        axis_col.addWidget(self._make_move_button("E+"))
        axis_col.addWidget(self._make_move_button("E-"))
        axis_col.addStretch(1)
        jog_row.addLayout(axis_col)
        jog_row.addStretch(1)
        move_layout.addLayout(jog_row)
        left_col.addWidget(move_card)

        temp_card, temp_body = self._make_card(tr("control.card.extruder_heatbed"))
        temp_layout = QtWidgets.QGridLayout(temp_body)
        temp_layout.setContentsMargins(12, 10, 12, 12)
        temp_layout.setHorizontalSpacing(8)
        temp_layout.setVerticalSpacing(8)
        temp_layout.addWidget(QtWidgets.QLabel(tr("control.field.extruder"), temp_card), 0, 0)
        self._nozzle_temp = QtWidgets.QLabel("-- / -- C", temp_card)
        self._nozzle_temp.setObjectName("ControlValue")
        temp_layout.addWidget(self._nozzle_temp, 0, 1)
        self._nozzle_target = self._make_spinbox(temp_card, 0, 320, " C")
        temp_layout.addWidget(self._nozzle_target, 0, 2)
        temp_layout.addWidget(self._make_action_button(tr("control.button.set")), 0, 3)

        temp_layout.addWidget(QtWidgets.QLabel(tr("control.field.heatbed"), temp_card), 1, 0)
        self._bed_temp = QtWidgets.QLabel("-- / -- C", temp_card)
        self._bed_temp.setObjectName("ControlValue")
        temp_layout.addWidget(self._bed_temp, 1, 1)
        self._bed_target = self._make_spinbox(temp_card, 0, 130, " C")
        temp_layout.addWidget(self._bed_target, 1, 2)
        temp_layout.addWidget(self._make_action_button(tr("control.button.set")), 1, 3)

        temp_layout.addWidget(QtWidgets.QLabel(tr("control.field.extrude"), temp_card), 2, 0)
        temp_layout.addWidget(self._make_action_button(tr("control.button.extrude")), 2, 1)
        temp_layout.addWidget(self._make_action_button(tr("control.button.retract")), 2, 2)

        self._fan_toggle = QtWidgets.QCheckBox(tr("control.toggle.fan"), temp_card)
        self._lamp_toggle = QtWidgets.QCheckBox(tr("control.toggle.lamp"), temp_card)
        self._motors_toggle = QtWidgets.QCheckBox(tr("control.toggle.motors_enabled"), temp_card)
        temp_layout.addWidget(self._fan_toggle, 3, 0)
        temp_layout.addWidget(self._lamp_toggle, 3, 1)
        temp_layout.addWidget(self._motors_toggle, 3, 2, 1, 2)
        left_col.addWidget(temp_card)

        left_col.addStretch(1)
        body_row.addLayout(left_col, 3)

        right_col = QtWidgets.QVBoxLayout()
        right_col.setSpacing(12)
        camera_frame = QtWidgets.QFrame(self)
        camera_frame.setObjectName("ControlCamera")
        camera_layout = QtWidgets.QVBoxLayout(camera_frame)
        camera_layout.setContentsMargins(12, 10, 12, 12)
        camera_layout.setSpacing(8)
        camera_title = QtWidgets.QLabel(tr("control.card.live_preview"), camera_frame)
        camera_title.setObjectName("ControlSectionTitle")
        camera_layout.addWidget(camera_title)
        camera_placeholder = QtWidgets.QLabel(tr("control.card.preview_placeholder"), camera_frame)
        camera_placeholder.setObjectName("ControlCameraPlaceholder")
        camera_placeholder.setAlignment(QtCore.Qt.AlignCenter)
        camera_layout.addWidget(camera_placeholder, 1)
        right_col.addWidget(camera_frame, 1)
        body_row.addLayout(right_col, 2)

        layout.addLayout(body_row, 1)

        hint = QtWidgets.QLabel(tr("control.hint.manual_idle"), self)
        hint.setObjectName("ControlHint")
        layout.addWidget(hint)

        self._printer_combo.currentIndexChanged.connect(lambda _idx: self._update_details())
        self.apply_theme()

    def _make_quick_button(self, label: str, checked: bool = False):
        btn = QtWidgets.QToolButton(self)
        btn.setText(label)
        btn.setCheckable(True)
        btn.setChecked(checked)
        btn.setObjectName("ControlQuickButton")
        btn.setCursor(QtCore.Qt.PointingHandCursor)
        return btn

    def _make_card(self, title: str):
        frame = QtWidgets.QFrame(self)
        frame.setObjectName("ControlCard")
        card_layout = QtWidgets.QVBoxLayout(frame)
        card_layout.setContentsMargins(10, 8, 10, 10)
        card_layout.setSpacing(0)
        header = QtWidgets.QLabel(title, frame)
        header.setObjectName("ControlCardTitle")
        card_layout.addWidget(header)
        body = QtWidgets.QWidget(frame)
        body.setObjectName("ControlCardBody")
        card_layout.addWidget(body)
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
        btn.setFixedSize(56, 40 if not center else 48)
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
        block = self._printer_combo.blockSignals(True)
        try:
            self._printer_combo.clear()
            if not self._printers:
                self._printer_combo.addItem(tr("control.printer.none_configured"))
                self._printer_combo.setEnabled(False)
                self._printer_details.setText(tr("control.printer.none_selected"))
                return
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
                name = printer.get("name") if isinstance(printer, dict) else None
                self._printer_combo.addItem(name or tr("control.printer.default_name"))
                if default_name and str(name or "").strip().lower() == default_name:
                    default_index = idx
            if default_index is not None:
                self._printer_combo.setCurrentIndex(default_index)
        finally:
            self._printer_combo.blockSignals(block)
        self._update_details(emit_signal=False)

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
            self._printer_details.setText(tr("control.printer.none_selected"))
            return
        desc = [
            tr("control.printer.name", name=printer.get("name", tr("control.printer.default_name"))),
            tr(
                "control.printer.bed",
                x=printer.get("bed_x", "n/a"),
                y=printer.get("bed_y", "n/a"),
                z=printer.get("bed_z", "n/a"),
            ),
        ]
        connector = connector_name(printer)
        if connector:
            desc.append(tr("control.printer.connector", "Connector: {connector}", connector=connector))
        endpoint = connector_endpoint(printer)
        if endpoint:
            desc.append(tr("control.printer.endpoint", "Endpoint: {endpoint}", endpoint=endpoint))
        self._printer_details.setText(" | ".join(desc))
        if emit_signal:
            self.printer_changed.emit(printer)

    def apply_theme(self):
        self.setStyleSheet(
            "QWidget {"
            f"  background: {theme_css('popup_bg')};"
            f"  color: {theme_css('popup_text')};"
            "}"
            "QLabel#ControlTitle {"
            "  font-size: 20px;"
            "  font-weight: 700;"
            "}"
            "QLabel#ControlSubtitle {"
            f"  color: {theme_css('popup_muted_text')};"
            "  font-size: 12px;"
            "}"
            "QLabel#ControlSectionTitle {"
            "  font-size: 13px;"
            "  font-weight: 600;"
            "}"
            "QLabel#ControlHint, QLabel#ControlDetails {"
            f"  color: {theme_css('popup_muted_text')};"
            "}"
            "QFrame#ControlSelector, QFrame#ControlQuickFrame, QFrame#ControlTelemetry, QFrame#ControlCamera, QFrame#ControlCard {"
            f"  border: 1px solid {theme_css('action_panel_border')};"
            f"  background: {theme_css('action_panel_bg')};"
            "  border-radius: 10px;"
            "}"
            "QLabel#ControlTelemetryValue {"
            "  font-weight: 600;"
            f"  color: {theme_css('popup_text')};"
            "}"
            "QLabel#ControlCameraPlaceholder {"
            f"  color: {theme_css('popup_muted_text')};"
            f"  background: {theme_css('popup_input_bg')};"
            "  border-radius: 8px;"
            "}"
            "QLabel#ControlCardTitle {"
            "  padding: 0 0 6px 0;"
            "  font-weight: 700;"
            "}"
            "QLabel#ControlValue {"
            "  font-weight: 700;"
            "}"
            "QToolButton#ControlQuickButton {"
            f"  background: {theme_css('action_button_bg')};"
            f"  color: {theme_css('popup_text')};"
            f"  border: 1px solid {theme_css('action_panel_border')};"
            "  border-radius: 8px;"
            "  padding: 6px 12px;"
            "  font-weight: 600;"
            "}"
            "QToolButton#ControlQuickButton:checked {"
            f"  background: {theme_css('topbar_accent')};"
            "  border: 1px solid transparent;"
            "}"
            "QPushButton#ControlDangerButton {"
            f"  background: {theme_css('rotate_reset')};"
            f"  color: {theme_css('popup_text')};"
            "  border: 1px solid transparent;"
            "  border-radius: 8px;"
            "  padding: 6px 12px;"
            "  font-weight: 700;"
            "}"
            "QPushButton#ControlDangerButton:pressed {"
            f"  background: {theme_css('action_button_active_bg')};"
            "}"
            "QToolButton#ControlMoveButton {"
            f"  background: {theme_css('action_button_bg')};"
            f"  border: 1px solid {theme_css('action_panel_border')};"
            "  border-radius: 8px;"
            "  padding: 6px 12px;"
            "}"
            "QFrame#ControlJogPad {"
            f"  background: {theme_css('action_button_bg')};"
            f"  border: 1px solid {theme_css('action_panel_border')};"
            "  border-radius: 95px;"
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
            "  border-radius: 12px;"
            "  font-weight: 700;"
            "}"
            "QToolButton#ControlMoveButton:hover, QToolButton#ControlJogButton:hover {"
            f"  background: {theme_css('action_button_hover_bg')};"
            "}"
            "QToolButton#ControlMoveButton:pressed, QToolButton#ControlJogButton:pressed, QToolButton#ControlJogHome:pressed {"
            f"  background: {theme_css('action_button_active_bg')};"
            "}"
            "QPushButton#ControlActionButton {"
            f"  background: {theme_css('action_button_bg')};"
            f"  color: {theme_css('action_button_text')};"
            f"  border: 1px solid {theme_css('action_panel_border')};"
            "  border-radius: 8px;"
            "  padding: 4px 10px;"
            "  font-weight: 600;"
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
            "  padding: 4px 8px;"
            "  border-radius: 6px;"
            "  min-height: 24px;"
            "}"
            "QCheckBox {"
            "  spacing: 6px;"
            "}"
        )

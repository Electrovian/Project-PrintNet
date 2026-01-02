from PyQt5 import QtWidgets, QtCore

from ..theme import theme_css


class PreviewView(QtCore.QObject):
    def __init__(self, main_window, viewer):
        super().__init__(main_window)
        self.main = main_window
        self.viewer = viewer
        self._build_panels()
        self.hide()

    def _build_panels(self):
        self._preview_panel = QtWidgets.QFrame(self.viewer)
        self._preview_panel.setObjectName("PreviewPanel")
        panel_layout = QtWidgets.QVBoxLayout(self._preview_panel)
        panel_layout.setContentsMargins(12, 12, 12, 12)
        panel_layout.setSpacing(10)

        printer_row = QtWidgets.QHBoxLayout()
        printer_label = QtWidgets.QLabel("Printer")
        printer_label.setObjectName("PreviewHeader")
        printer_row.addWidget(printer_label)
        printer_row.addStretch(1)
        self._printer_combo = QtWidgets.QComboBox(self._preview_panel)
        self._printer_combo.setObjectName("PreviewCombo")
        printer_row.addWidget(self._printer_combo)
        panel_layout.addLayout(printer_row)

        tabs_row = QtWidgets.QHBoxLayout()
        self._global_btn = QtWidgets.QToolButton(self._preview_panel)
        self._global_btn.setText("Global")
        self._global_btn.setCheckable(True)
        self._global_btn.setChecked(True)
        self._global_btn.setObjectName("PreviewTab")
        self._objects_btn = QtWidgets.QToolButton(self._preview_panel)
        self._objects_btn.setText("Objects")
        self._objects_btn.setCheckable(True)
        self._objects_btn.setObjectName("PreviewTab")
        tabs_group = QtWidgets.QButtonGroup(self._preview_panel)
        tabs_group.setExclusive(True)
        tabs_group.addButton(self._global_btn)
        tabs_group.addButton(self._objects_btn)
        tabs_row.addWidget(self._global_btn)
        tabs_row.addWidget(self._objects_btn)
        tabs_row.addStretch(1)
        panel_layout.addLayout(tabs_row)

        gcode_title = QtWidgets.QLabel("G-code Preview")
        gcode_title.setObjectName("PreviewHeader")
        panel_layout.addWidget(gcode_title)

        stats_grid = QtWidgets.QGridLayout()
        stats_grid.setHorizontalSpacing(12)
        stats_grid.setVerticalSpacing(4)
        stats_grid.addWidget(QtWidgets.QLabel("Printing Time:"), 0, 0)
        stats_grid.addWidget(QtWidgets.QLabel("Filament Wt:"), 0, 2)
        stats_grid.addWidget(QtWidgets.QLabel("Filament Length:"), 1, 0)
        stats_grid.addWidget(QtWidgets.QLabel("Filament Cost:"), 1, 2)

        self._time_value = QtWidgets.QLabel("n/a")
        self._weight_value = QtWidgets.QLabel("n/a")
        self._length_value = QtWidgets.QLabel("n/a")
        self._cost_value = QtWidgets.QLabel("n/a")

        stats_grid.addWidget(self._time_value, 0, 1)
        stats_grid.addWidget(self._weight_value, 0, 3)
        stats_grid.addWidget(self._length_value, 1, 1)
        stats_grid.addWidget(self._cost_value, 1, 3)
        panel_layout.addLayout(stats_grid)

        show_row = QtWidgets.QHBoxLayout()
        show_row.addWidget(QtWidgets.QLabel("Show in Preview"))
        show_row.addStretch(1)
        self._platform_check = QtWidgets.QCheckBox("Print Platform")
        self._platform_check.setChecked(True)
        self._nozzle_check = QtWidgets.QCheckBox("Nozzle")
        self._nozzle_check.setChecked(True)
        show_row.addWidget(self._platform_check)
        show_row.addWidget(self._nozzle_check)
        panel_layout.addLayout(show_row)

        toggle_row = QtWidgets.QHBoxLayout()
        self._color_btn = QtWidgets.QToolButton(self._preview_panel)
        self._color_btn.setText("Color Show")
        self._color_btn.setCheckable(True)
        self._color_btn.setChecked(True)
        self._color_btn.setObjectName("PreviewToggle")
        self._gcode_btn = QtWidgets.QToolButton(self._preview_panel)
        self._gcode_btn.setText("G-code")
        self._gcode_btn.setCheckable(True)
        self._gcode_btn.setObjectName("PreviewToggle")
        toggle_group = QtWidgets.QButtonGroup(self._preview_panel)
        toggle_group.setExclusive(True)
        toggle_group.addButton(self._color_btn)
        toggle_group.addButton(self._gcode_btn)
        toggle_row.addWidget(self._color_btn)
        toggle_row.addWidget(self._gcode_btn)
        toggle_row.addStretch(1)
        panel_layout.addLayout(toggle_row)

        options_row = QtWidgets.QHBoxLayout()
        self._line_type_combo = QtWidgets.QComboBox(self._preview_panel)
        self._line_type_combo.addItems(
            [
                "Line Type",
                "Filament",
                "Speed",
                "Layer Height",
                "Line Width",
                "Flow",
                "Layer Time",
                "Layer Time (log)",
                "Fan Speed",
                "Temperature",
                "Acceleration",
            ]
        )
        self._line_type_combo.setObjectName("PreviewCombo")
        options_row.addWidget(self._line_type_combo)
        options_row.addStretch(1)
        self._lite_mode_check = QtWidgets.QCheckBox("Lite Mode")
        options_row.addWidget(self._lite_mode_check)
        panel_layout.addLayout(options_row)

        self._stack = QtWidgets.QStackedWidget(self._preview_panel)
        panel_layout.addWidget(self._stack, 1)

        self._line_table = QtWidgets.QTableWidget(0, 3, self._preview_panel)
        self._line_table.setHorizontalHeaderLabels(["Line Type", "Time", "Percent"])
        self._line_table.verticalHeader().setVisible(False)
        self._line_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self._line_table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self._line_table.horizontalHeader().setStretchLastSection(True)
        self._stack.addWidget(self._line_table)

        self._gcode_text = QtWidgets.QPlainTextEdit(self._preview_panel)
        self._gcode_text.setReadOnly(True)
        self._gcode_text.setObjectName("PreviewGCode")
        self._gcode_text.setPlaceholderText("Slice to generate a preview...")
        self._stack.addWidget(self._gcode_text)

        self._action_panel = QtWidgets.QFrame(self.viewer)
        self._action_panel.setObjectName("ActionPanel")
        action_layout = QtWidgets.QVBoxLayout(self._action_panel)
        action_layout.setContentsMargins(10, 8, 10, 8)
        action_layout.setSpacing(6)

        self._slice_btn = QtWidgets.QPushButton("Slice plate", self._action_panel)
        self._slice_btn.clicked.connect(self.main.slice_current_model)
        action_layout.addWidget(self._slice_btn)

        self._print_btn = QtWidgets.QPushButton("Send print", self._action_panel)
        self._print_btn.clicked.connect(self.main._open_device_view)
        action_layout.addWidget(self._print_btn)

        self._timeline_panel = QtWidgets.QFrame(self.viewer)
        self._timeline_panel.setObjectName("PreviewTimeline")
        timeline_layout = QtWidgets.QHBoxLayout(self._timeline_panel)
        timeline_layout.setContentsMargins(10, 8, 10, 8)
        timeline_layout.setSpacing(8)

        self._play_btn = QtWidgets.QToolButton(self._timeline_panel)
        self._play_btn.setText("Play")
        self._play_btn.setObjectName("PreviewButton")
        timeline_layout.addWidget(self._play_btn)

        timeline_layout.addWidget(QtWidgets.QLabel("Steps"))
        self._steps_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self._timeline_panel)
        self._steps_slider.setRange(0, 0)
        timeline_layout.addWidget(self._steps_slider, 1)
        self._steps_spin = QtWidgets.QSpinBox(self._timeline_panel)
        self._steps_spin.setRange(0, 0)
        self._steps_spin.setFixedWidth(70)
        timeline_layout.addWidget(self._steps_spin)

        self._layer_panel = QtWidgets.QFrame(self.viewer)
        self._layer_panel.setObjectName("PreviewLayer")
        layer_layout = QtWidgets.QVBoxLayout(self._layer_panel)
        layer_layout.setContentsMargins(6, 8, 6, 8)
        layer_layout.setSpacing(6)
        self._layer_top = QtWidgets.QLabel("0")
        self._layer_top.setAlignment(QtCore.Qt.AlignCenter)
        self._layer_slider = QtWidgets.QSlider(QtCore.Qt.Vertical, self._layer_panel)
        self._layer_slider.setRange(0, 0)
        self._layer_bottom = QtWidgets.QLabel("0")
        self._layer_bottom.setAlignment(QtCore.Qt.AlignCenter)
        layer_layout.addWidget(self._layer_top)
        layer_layout.addWidget(self._layer_slider, 1)
        layer_layout.addWidget(self._layer_bottom)

        self._populate_line_types()
        self._wire_toggles()
        self._populate_printers()

    def _populate_printers(self):
        self._printer_combo.clear()
        printers = getattr(self.main, "printers", []) or []
        if not printers:
            self._printer_combo.addItem("No printers configured")
            self._printer_combo.setEnabled(False)
            return
        self._printer_combo.setEnabled(True)
        for printer in printers:
            name = printer.get("name") if isinstance(printer, dict) else None
            self._printer_combo.addItem(name or "Printer")

    def _populate_line_types(self):
        line_types = [
            "Inner wall",
            "Outer wall",
            "Sparse infill",
            "Internal solid infill",
            "Top surface",
            "Bottom surface",
            "Internal Bridge",
            "Gap infill",
            "Travel",
            "Retract",
        ]
        self._line_table.setRowCount(len(line_types))
        for row, label in enumerate(line_types):
            item = QtWidgets.QTableWidgetItem(label)
            item.setCheckState(QtCore.Qt.Checked)
            self._line_table.setItem(row, 0, item)
            self._line_table.setItem(row, 1, QtWidgets.QTableWidgetItem("n/a"))
            self._line_table.setItem(row, 2, QtWidgets.QTableWidgetItem("n/a"))

    def _wire_toggles(self):
        self._color_btn.toggled.connect(self._sync_toggle_stack)
        self._gcode_btn.toggled.connect(self._sync_toggle_stack)
        self._sync_toggle_stack()

    def _sync_toggle_stack(self):
        if self._color_btn.isChecked():
            self._stack.setCurrentIndex(0)
        else:
            self._stack.setCurrentIndex(1)

    def apply_theme(self):
        panel_bg = theme_css("popup_bg")
        panel_border = theme_css("popup_border")
        panel_text = theme_css("popup_text")
        muted_text = theme_css("popup_muted_text")
        action_border = theme_css("action_panel_border")
        action_bg = theme_css("action_panel_bg")

        self._preview_panel.setStyleSheet(
            "QFrame#PreviewPanel {"
            f"  background: {panel_bg};"
            f"  border: 1px solid {panel_border};"
            "  border-radius: 10px;"
            "}"
            "QLabel {"
            f"  color: {panel_text};"
            "}"
            "QLabel#PreviewHeader {"
            "  font-weight: 600;"
            "}"
            "QToolButton#PreviewToggle {"
            f"  background: {theme_css('action_button_bg')};"
            f"  color: {panel_text};"
            f"  border: 1px solid {action_border};"
            "  border-radius: 10px;"
            "  padding: 4px 12px;"
            "}"
            "QToolButton#PreviewToggle:checked {"
            f"  background: {theme_css('topbar_accent')};"
            f"  color: {theme_css('popup_text')};"
            "  font-weight: 600;"
            "}"
            "QToolButton#PreviewTab {"
            f"  background: {theme_css('menu_hover_bg')};"
            f"  color: {panel_text};"
            f"  border: 1px solid {action_border};"
            "  border-radius: 10px;"
            "  padding: 3px 10px;"
            "}"
            "QToolButton#PreviewTab:checked {"
            f"  background: {theme_css('topbar_accent')};"
            f"  color: {theme_css('popup_text')};"
            "  font-weight: 600;"
            "}"
            "QComboBox#PreviewCombo {"
            f"  background: {theme_css('popup_input_bg')};"
            f"  color: {panel_text};"
            f"  border: 1px solid {panel_border};"
            "  padding: 2px 6px;"
            "  border-radius: 6px;"
            "}"
            "QCheckBox {"
            f"  color: {panel_text};"
            "}"
            "QTableWidget {"
            f"  background: {theme_css('popup_input_bg')};"
            f"  color: {panel_text};"
            f"  border: 1px solid {panel_border};"
            "}"
            "QHeaderView::section {"
            f"  background: {theme_css('popup_header_bg')};"
            f"  color: {panel_text};"
            f"  border: 1px solid {panel_border};"
            "}"
            "QPlainTextEdit#PreviewGCode {"
            f"  background: {theme_css('popup_input_bg')};"
            f"  color: {panel_text};"
            f"  border: 1px solid {panel_border};"
            "}"
            "QScrollBar:vertical {"
            f"  background: {panel_bg};"
            "}"
            f"QLabel[muted='true'] {{ color: {muted_text}; }}"
        )

        self._action_panel.setStyleSheet(
            "QFrame#ActionPanel {"
            f"  background: {action_bg};"
            f"  border: 1px solid {action_border};"
            "  border-radius: 6px;"
            "}"
            "QPushButton {"
            f"  background: {theme_css('action_button_bg')};"
            f"  color: {theme_css('action_button_text')};"
            f"  border: 1px solid {action_border};"
            "  border-radius: 4px;"
            "  padding: 6px 16px;"
            "}"
            "QPushButton:hover {"
            f"  background: {theme_css('action_button_hover_bg')};"
            "}"
            "QPushButton:pressed {"
            f"  background: {theme_css('action_button_active_bg')};"
            "}"
        )

        self._timeline_panel.setStyleSheet(
            "QFrame#PreviewTimeline {"
            f"  background: {panel_bg};"
            f"  border: 1px solid {panel_border};"
            "  border-radius: 10px;"
            "}"
            "QLabel, QToolButton {"
            f"  color: {panel_text};"
            "}"
        )

        self._layer_panel.setStyleSheet(
            "QFrame#PreviewLayer {"
            f"  background: {panel_bg};"
            f"  border: 1px solid {panel_border};"
            "  border-radius: 10px;"
            "}"
            "QLabel {"
            f"  color: {panel_text};"
            "}"
        )

    def position_panels(self):
        margin = 16
        self._preview_panel.adjustSize()
        self._preview_panel.move(margin, margin + 6)

        self._action_panel.adjustSize()
        x = max(0, self.viewer.width() - self._action_panel.width() - margin)
        y = max(0, self.viewer.height() - self._action_panel.height() - margin)
        self._action_panel.move(x, y)

        self._timeline_panel.adjustSize()
        t_x = max(0, (self.viewer.width() - self._timeline_panel.width()) // 2)
        t_y = max(0, self.viewer.height() - self._timeline_panel.height() - margin)
        self._timeline_panel.move(t_x, t_y)

        self._layer_panel.adjustSize()
        l_x = max(0, self.viewer.width() - self._layer_panel.width() - margin)
        l_y = max(0, (self.viewer.height() - self._layer_panel.height()) // 2)
        self._layer_panel.move(l_x, l_y)

    def update_stats(self, stats):
        if not stats:
            self._time_value.setText("n/a")
            self._weight_value.setText("n/a")
            self._length_value.setText("n/a")
            self._cost_value.setText("n/a")
            return
        self._time_value.setText(stats.get("time", "n/a"))
        self._weight_value.setText(stats.get("weight", "n/a"))
        self._length_value.setText(stats.get("length", "n/a"))
        self._cost_value.setText(stats.get("cost", "n/a"))

    def set_gcode_text(self, text: str):
        self._gcode_text.setPlainText(text or "")

    def set_steps_count(self, count: int):
        count = max(0, int(count))
        self._steps_slider.setRange(0, count)
        self._steps_spin.setRange(0, count)
        self._layer_slider.setRange(0, max(0, count))
        self._layer_top.setText(str(count))
        self._layer_bottom.setText("0")

    def show(self):
        self._preview_panel.show()
        self._action_panel.show()
        self._timeline_panel.show()
        self._layer_panel.show()
        self.position_panels()

    def hide(self):
        self._preview_panel.hide()
        self._action_panel.hide()
        self._timeline_panel.hide()
        self._layer_panel.hide()

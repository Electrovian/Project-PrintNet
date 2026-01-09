import math
from PyQt5 import QtWidgets, QtCore, QtGui

from ..theme import theme_css, theme_qcolor
from ..preview_utils import play_interval_ms


class PreviewView(QtCore.QObject):
    def __init__(self, main_window, viewer):
        super().__init__(main_window)
        self.main = main_window
        self.viewer = viewer
        self._preview_data = None
        self._play_timer = QtCore.QTimer(self.main)
        self._play_timer.timeout.connect(self._on_play_tick)
        self._play_base_interval_ms = 30
        self._play_speed = 1.0
        self._play_timer.setInterval(self._play_base_interval_ms)
        self._is_playing = False
        self._line_type_updating = False
        self._line_type_map = []
        self._build_panels()
        self.hide()

    def _build_panels(self):
        self._preview_panel = QtWidgets.QFrame(self.viewer)
        self._preview_panel.setObjectName("PreviewPanel")
        self._preview_panel.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Expanding,
        )
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
        self._line_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self._line_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self._line_table.setWordWrap(False)
        self._stack.addWidget(self._line_table)

        self._gcode_text = QtWidgets.QPlainTextEdit(self._preview_panel)
        self._gcode_text.setReadOnly(True)
        self._gcode_text.setObjectName("PreviewGCode")
        self._gcode_text.setPlaceholderText("Slice to generate a preview...")
        self._gcode_text.setLineWrapMode(QtWidgets.QPlainTextEdit.WidgetWidth)
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
        timeline_layout = QtWidgets.QVBoxLayout(self._timeline_panel)
        timeline_layout.setContentsMargins(10, 8, 10, 8)
        timeline_layout.setSpacing(6)

        info_row = QtWidgets.QHBoxLayout()
        self._nozzle_info = QtWidgets.QLabel("X: --  Y: --  Z: --  Speed: --")
        self._nozzle_info.setObjectName("PreviewNozzleInfo")
        info_row.addWidget(self._nozzle_info)
        info_row.addStretch(1)
        timeline_layout.addLayout(info_row)

        controls_row = QtWidgets.QHBoxLayout()
        self._play_btn = QtWidgets.QToolButton(self._timeline_panel)
        self._play_btn.setObjectName("PreviewPlayButton")
        self._play_btn.setCheckable(True)
        self._play_btn.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self._play_btn.setFixedSize(48, 32)
        self._play_btn.setIconSize(QtCore.QSize(18, 18))
        self._play_btn.setCursor(QtCore.Qt.PointingHandCursor)
        controls_row.addWidget(self._play_btn)

        controls_row.addWidget(QtWidgets.QLabel("Speed"))
        self._play_speed_spin = QtWidgets.QDoubleSpinBox(self._timeline_panel)
        self._play_speed_spin.setRange(0.25, 4.0)
        self._play_speed_spin.setSingleStep(0.25)
        self._play_speed_spin.setDecimals(2)
        self._play_speed_spin.setValue(self._play_speed)
        self._play_speed_spin.setSuffix("x")
        self._play_speed_spin.setFixedWidth(70)
        self._play_speed_spin.setToolTip("Playback speed")
        controls_row.addWidget(self._play_speed_spin)

        controls_row.addWidget(QtWidgets.QLabel("Steps"))
        self._steps_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self._timeline_panel)
        self._steps_slider.setRange(0, 0)
        controls_row.addWidget(self._steps_slider, 1)
        self._steps_spin = QtWidgets.QSpinBox(self._timeline_panel)
        self._steps_spin.setRange(0, 0)
        self._steps_spin.setFixedWidth(70)
        controls_row.addWidget(self._steps_spin)
        timeline_layout.addLayout(controls_row)

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

        self._refresh_play_icons()
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
        dummy_index = None
        for idx, printer in enumerate(printers):
            name = printer.get("name") if isinstance(printer, dict) else None
            self._printer_combo.addItem(name or "Printer")
            if str(name or "").strip().lower() == "dummy printer":
                dummy_index = idx
        if dummy_index is not None:
            self._printer_combo.setCurrentIndex(dummy_index)

    def _populate_line_types(self):
        self._line_type_map = [
            ("Inner wall", "inner_wall"),
            ("Outer wall", "outer_wall"),
            ("Sparse infill", "sparse_infill"),
            ("Internal solid infill", "solid_infill"),
            ("Top surface", "top_surface"),
            ("Bottom surface", "bottom_surface"),
            ("Internal Bridge", "bridge"),
            ("Gap infill", "gap_infill"),
            ("Travel", "travel"),
            ("Retract", "retract"),
        ]
        self._line_type_updating = True
        self._line_table.setRowCount(len(self._line_type_map))
        for row, (label, key) in enumerate(self._line_type_map):
            item = QtWidgets.QTableWidgetItem(label)
            item.setCheckState(QtCore.Qt.Checked)
            item.setData(QtCore.Qt.UserRole, key)
            self._line_table.setItem(row, 0, item)
            self._line_table.setItem(row, 1, QtWidgets.QTableWidgetItem("n/a"))
            self._line_table.setItem(row, 2, QtWidgets.QTableWidgetItem("n/a"))
        self._line_type_updating = False

    def _wire_toggles(self):
        self._color_btn.toggled.connect(self._sync_toggle_stack)
        self._gcode_btn.toggled.connect(self._sync_toggle_stack)
        self._sync_toggle_stack()
        self._layer_slider.valueChanged.connect(self._on_layer_changed)
        self._steps_slider.valueChanged.connect(self._on_step_changed)
        self._steps_spin.valueChanged.connect(self._on_step_spin_changed)
        self._line_type_combo.currentTextChanged.connect(self._on_color_mode_changed)
        self._play_btn.toggled.connect(self._on_play_toggled)
        self._play_speed_spin.valueChanged.connect(self._on_play_speed_changed)
        self._line_table.itemChanged.connect(self._on_line_type_changed)
        self._platform_check.toggled.connect(self._on_platform_toggled)
        self._nozzle_check.toggled.connect(self._on_nozzle_toggled)
        self._on_platform_toggled(self._platform_check.isChecked())
        self._on_nozzle_toggled(self._nozzle_check.isChecked())

    def _sync_toggle_stack(self):
        if self._color_btn.isChecked():
            self._stack.setCurrentIndex(0)
        else:
            self._stack.setCurrentIndex(1)

    def apply_theme(self):
        panel_bg_color = theme_qcolor("popup_bg")
        panel_bg_color.setAlpha(210)
        panel_bg = (f"rgba({panel_bg_color.red()}, {panel_bg_color.green()}, "
                    f"{panel_bg_color.blue()}, {panel_bg_color.alpha()})")
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
            "QToolButton#PreviewPlayButton {"
            f"  background: {theme_css('rotate_reset')};"
            f"  border: 1px solid {theme_qcolor('rotate_reset').darker(115).name()};"
            "  border-radius: 10px;"
            "  padding: 2px 10px;"
            "}"
            "QToolButton#PreviewPlayButton:hover {"
            f"  background: {theme_qcolor('rotate_reset').lighter(108).name()};"
            "}"
            "QToolButton#PreviewPlayButton:pressed {"
            f"  background: {theme_qcolor('rotate_reset').darker(120).name()};"
            "}"
            "QLabel#PreviewNozzleInfo {"
            f"  color: {panel_text};"
            "  font-weight: 600;"
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
        self._autosize_panel()
        self._refresh_play_icons()

    def position_panels(self):
        margin = 16
        self._autosize_panel()
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
        self._autosize_panel()

    def _autosize_panel(self):
        if self._preview_panel is None:
            return
        margin = 16
        available = max(240, self.viewer.width() - margin * 2)
        max_width = min(380, available)
        target = min(self._preview_panel.sizeHint().width(), max_width)
        target = max(260, int(target))
        self._preview_panel.setFixedWidth(target)

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
        self._steps_slider.setValue(count)
        self._steps_spin.setValue(count)

    def set_layer_count(self, count: int):
        count = max(0, int(count))
        top = max(0, count - 1)
        self._layer_slider.setRange(0, top)
        self._layer_slider.setValue(top)
        self._update_layer_label(top)
        self._layer_bottom.setText("0")
        if count > 0:
            self._update_steps_for_layer(top)

    def _update_layer_label(self, value: int | None = None):
        if self._layer_slider is None or self._layer_top is None:
            return
        max_index = int(self._layer_slider.maximum())
        if value is None:
            current = int(self._layer_slider.value())
        else:
            current = int(value)
        current = max(0, min(current, max_index))
        self._layer_top.setText(str(current))
        if max_index > 0:
            self._layer_top.setToolTip(f"Layer {current} / {max_index}")
        else:
            self._layer_top.setToolTip("Layer 0")

    def show(self):
        self._preview_panel.show()
        self._action_panel.show()
        self._timeline_panel.show()
        self._layer_panel.show()
        if self._play_btn.isChecked():
            self._play_btn.setChecked(False)
        for panel in (self._preview_panel, self._action_panel, self._timeline_panel, self._layer_panel):
            panel.raise_()
        self.position_panels()
        self._update_nozzle_info()

    def hide(self):
        self._preview_panel.hide()
        self._action_panel.hide()
        self._timeline_panel.hide()
        self._layer_panel.hide()

    def _on_layer_changed(self, value: int):
        if hasattr(self.viewer, "set_preview_layer_index"):
            self.viewer.set_preview_layer_index(int(value))
        self._update_steps_for_layer(int(value))
        self._update_layer_label(int(value))
        self._update_nozzle_info()

    def _on_step_changed(self, value: int):
        if hasattr(self.viewer, "set_preview_step_index"):
            self.viewer.set_preview_step_index(int(value))
        if self._steps_spin.value() != value:
            self._steps_spin.setValue(int(value))
        self._update_nozzle_info()

    def _on_step_spin_changed(self, value: int):
        if self._steps_slider.value() != value:
            self._steps_slider.setValue(int(value))

    def _on_play_toggled(self, checked: bool):
        if self._preview_data is None or not getattr(self._preview_data, "layers", None):
            if checked:
                self._play_btn.setChecked(False)
            self._is_playing = False
            self._play_timer.stop()
            self._update_play_button_state(False)
            return
        if checked:
            if self._steps_slider.value() >= self._steps_slider.maximum():
                self._steps_slider.setValue(0)
            self._is_playing = True
            self._update_play_timer_interval()
            self._play_timer.start()
        else:
            self._is_playing = False
            self._play_timer.stop()
        self._update_play_button_state(checked)

    def _on_play_tick(self):
        if self._steps_slider.maximum() <= 0:
            self._play_btn.setChecked(False)
            return
        next_value = self._steps_slider.value() + 1
        if next_value > self._steps_slider.maximum():
            self._play_btn.setChecked(False)
            return
        self._steps_slider.setValue(next_value)
        self._update_nozzle_info()

    def set_preview_data(self, preview):
        self._preview_data = preview
        if preview is None or not getattr(preview, "layers", None):
            self.set_layer_count(0)
            self.set_steps_count(0)
            self._update_line_type_stats()
            self._sync_feature_filter()
            self._update_nozzle_info()
            return
        self.set_layer_count(len(preview.layers))
        self._update_line_type_stats()
        self._sync_feature_filter()
        self._update_nozzle_info()

    def _update_steps_for_layer(self, layer_index: int):
        count = 0
        if self._preview_data is not None and getattr(self._preview_data, "layers", None):
            idx = max(0, min(layer_index, len(self._preview_data.layers) - 1))
            count = len(self._preview_data.layers[idx].segments)
        self.set_steps_count(count)
        self._update_nozzle_info()

    def _on_line_type_changed(self, item):
        if self._line_type_updating:
            return
        if item is None or item.column() != 0:
            return
        self._sync_feature_filter()

    def _sync_feature_filter(self):
        if not hasattr(self.viewer, "set_preview_feature_filter"):
            return
        total_rows = self._line_table.rowCount()
        if total_rows == 0:
            self.viewer.set_preview_feature_filter(None)
            return
        checked = []
        checked_count = 0
        for row in range(total_rows):
            item = self._line_table.item(row, 0)
            if item is None:
                continue
            if item.checkState() == QtCore.Qt.Checked:
                checked_count += 1
                key = item.data(QtCore.Qt.UserRole) or item.text().strip().lower().replace(" ", "_")
                checked.append(key)
        if checked_count == total_rows:
            self.viewer.set_preview_feature_filter(None)
        else:
            self.viewer.set_preview_feature_filter(checked)

    def _format_duration(self, seconds: float) -> str:
        seconds = max(0, int(round(seconds)))
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        if hours:
            return f"{hours}h{mins:02d}m"
        return f"{mins}m{secs:02d}s"

    def _update_line_type_stats(self):
        totals = {}
        total_time = 0.0
        if self._preview_data is not None and getattr(self._preview_data, "layers", None):
            for layer in self._preview_data.layers:
                for seg in layer.segments:
                    dist = math.dist(seg.start, seg.end)
                    if seg.speed > 0:
                        t = dist / seg.speed
                    else:
                        t = 0.0
                    totals[seg.feature] = totals.get(seg.feature, 0.0) + t
                    total_time += t
        for row in range(self._line_table.rowCount()):
            item = self._line_table.item(row, 0)
            if item is None:
                continue
            key = item.data(QtCore.Qt.UserRole)
            seconds = totals.get(key, 0.0)
            time_str = self._format_duration(seconds) if seconds > 0 else "n/a"
            percent = (seconds / total_time * 100.0) if total_time > 0 else 0.0
            self._line_table.setItem(row, 1, QtWidgets.QTableWidgetItem(time_str))
            self._line_table.setItem(row, 2, QtWidgets.QTableWidgetItem(f"{percent:.1f}%"))

    def _on_color_mode_changed(self, value: str):
        mode = (value or "").strip().lower()
        if mode == "speed":
            selected = "speed"
        elif mode in ("flow", "filament"):
            selected = "flow"
        elif mode in ("line width", "width"):
            selected = "width"
        else:
            selected = "feature"
        if hasattr(self.viewer, "set_preview_color_mode"):
            self.viewer.set_preview_color_mode(selected)

    def _on_platform_toggled(self, checked: bool):
        if hasattr(self.viewer, "set_platform_visible"):
            self.viewer.set_platform_visible(bool(checked))

    def _on_nozzle_toggled(self, checked: bool):
        if hasattr(self.viewer, "set_nozzle_visible"):
            self.viewer.set_nozzle_visible(bool(checked))

    def sync_preview_toggles(self):
        self._on_platform_toggled(self._platform_check.isChecked())
        self._on_nozzle_toggled(self._nozzle_check.isChecked())
        self._update_nozzle_info()

    def _update_nozzle_info(self):
        if not hasattr(self, "_nozzle_info") or self._nozzle_info is None:
            return
        if not hasattr(self.viewer, "get_preview_nozzle_state"):
            self._nozzle_info.setText("X: --  Y: --  Z: --  Speed: --")
            return
        state = self.viewer.get_preview_nozzle_state()
        if not state:
            self._nozzle_info.setText("X: --  Y: --  Z: --  Speed: --")
            return
        pos, speed, is_extrude = state
        speed_text = f"{speed:.0f}" if speed > 0 else "n/a"
        mode = "Print" if is_extrude else "Travel"
        self._nozzle_info.setText(
            f"X: {pos[0]:.3f}  Y: {pos[1]:.3f}  Z: {pos[2]:.3f}  Speed: {speed_text} ({mode})"
        )

    def _play_icon_pixmap(self, color: QtGui.QColor) -> QtGui.QPixmap:
        size = 18
        pm = QtGui.QPixmap(size, size)
        pm.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pm)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QBrush(color))
        margin = 3
        points = [
            QtCore.QPointF(margin, margin),
            QtCore.QPointF(margin, size - margin),
            QtCore.QPointF(size - margin, size / 2),
        ]
        painter.drawPolygon(QtGui.QPolygonF(points))
        painter.end()
        return pm

    def _pause_icon_pixmap(self, color: QtGui.QColor) -> QtGui.QPixmap:
        size = 18
        pm = QtGui.QPixmap(size, size)
        pm.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pm)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QBrush(color))
        bar_width = 4
        gap = 4
        left = (size - (bar_width * 2 + gap)) // 2
        top = 3
        height = size - 6
        painter.drawRoundedRect(left, top, bar_width, height, 1.5, 1.5)
        painter.drawRoundedRect(left + bar_width + gap, top, bar_width, height, 1.5, 1.5)
        painter.end()
        return pm

    def _refresh_play_icons(self):
        color = QtGui.QColor(20, 20, 20)
        self._play_icon = QtGui.QIcon(self._play_icon_pixmap(color))
        self._pause_icon = QtGui.QIcon(self._pause_icon_pixmap(color))
        self._update_play_button_state(self._is_playing)

    def _update_play_button_state(self, playing: bool):
        if not hasattr(self, "_play_btn") or self._play_btn is None:
            return
        if playing:
            self._play_btn.setIcon(self._pause_icon)
            self._play_btn.setToolTip("Pause preview")
        else:
            self._play_btn.setIcon(self._play_icon)
            self._play_btn.setToolTip("Play preview")

    def _update_play_timer_interval(self):
        interval = play_interval_ms(self._play_base_interval_ms, self._play_speed)
        self._play_timer.setInterval(interval)

    def _on_play_speed_changed(self, value: float):
        try:
            self._play_speed = float(value)
        except (TypeError, ValueError):
            self._play_speed = 1.0
        self._update_play_timer_interval()

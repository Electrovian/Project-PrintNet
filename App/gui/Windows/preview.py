import bisect
import math
from PyQt5 import QtWidgets, QtCore, QtGui

from ..theme import theme_css, theme_qcolor
from ..preview_utils import play_interval_ms
from config.defaults import DEFAULTS


BASE_LINE_TYPE_MAP = [
    ("Inner wall", "inner_wall"),
    ("Outer wall", "outer_wall"),
    ("Sparse infill", "sparse_infill"),
    ("Internal solid infill", "solid_infill"),
    ("Top surface", "top_surface"),
    ("Bottom surface", "bottom_surface"),
    ("Bridge", "bridge"),
    ("Gap infill", "gap_infill"),
    ("Thin wall", "thin_wall"),
    ("Ironing", "ironing"),
    ("Support", "support"),
    ("Skirt", "skirt"),
    ("Brim", "brim"),
    ("Raft", "raft"),
    ("Travel", "travel"),
    ("Retract", "retract"),
    ("Unretract", "unretract"),
    ("Wipe", "wipe"),
    ("Seams", "seams"),
    ("Other", "other"),
]

FEATURE_LABEL_OVERRIDES = {
    "inner_wall": "Inner wall",
    "outer_wall": "Outer wall",
    "sparse_infill": "Sparse infill",
    "solid_infill": "Internal solid infill",
    "top_surface": "Top surface",
    "bottom_surface": "Bottom surface",
    "bridge": "Bridge",
    "gap_infill": "Gap infill",
    "thin_wall": "Thin wall",
    "support": "Support",
    "support_interface": "Support interface",
    "ironing": "Ironing",
    "skirt": "Skirt",
    "brim": "Brim",
    "raft": "Raft",
    "travel": "Travel",
    "retract": "Retract",
    "unretract": "Unretract",
    "wipe": "Wipe",
    "seams": "Seams",
    "other": "Other",
}


class PreviewView(QtCore.QObject):
    printer_changed = QtCore.pyqtSignal(object)
    def __init__(self, main_window, viewer):
        super().__init__(main_window)
        self.main = main_window
        self.viewer = viewer
        self._preview_data = None
        self._layer_offsets = []
        self._total_steps = 0
        self._play_timer = QtCore.QTimer(self.main)
        self._play_timer.timeout.connect(self._on_play_tick)
        self._play_base_interval_ms = 30
        self._play_speed = 1.0
        self._play_timer.setInterval(self._play_base_interval_ms)
        self._is_playing = False
        self._line_type_updating = False
        self._line_type_map = []
        self._preview_settings = None
        self._preview_stats = {}
        self._mode_pages = {}
        self._legend_tables = {}
        self._options_tables = {}
        self._feature_display_state = {}
        self._feature_display_items = {}
        self._feature_state_updating = False
        self._panel_collapsed = False
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
        panel_layout.setSpacing(8)

        self._printer_row = QtWidgets.QFrame(self._preview_panel)
        self._printer_row.setObjectName("PreviewPrinterRow")
        printer_row = QtWidgets.QHBoxLayout(self._printer_row)
        printer_row.setContentsMargins(0, 0, 0, 0)
        printer_row.setSpacing(6)
        printer_label = QtWidgets.QLabel("Printer")
        printer_label.setObjectName("PreviewHeader")
        printer_row.addWidget(printer_label)
        printer_row.addStretch(1)
        self._printer_combo = QtWidgets.QComboBox(self._preview_panel)
        self._printer_combo.setObjectName("PreviewCombo")
        printer_row.addWidget(self._printer_combo)
        self._printer_row.setVisible(False)
        panel_layout.addWidget(self._printer_row)

        header_row = QtWidgets.QHBoxLayout()
        header_label = QtWidgets.QLabel("Slicing Result")
        header_label.setObjectName("PreviewHeader")
        header_row.addWidget(header_label)
        header_row.addStretch(1)
        self._collapse_btn = QtWidgets.QToolButton(self._preview_panel)
        self._collapse_btn.setObjectName("PreviewCollapse")
        self._collapse_btn.setText("v")
        self._collapse_btn.setVisible(True)
        header_row.addWidget(self._collapse_btn)
        panel_layout.addLayout(header_row)

        options_row = QtWidgets.QHBoxLayout()
        scheme_label = QtWidgets.QLabel("Color Scheme")
        scheme_label.setObjectName("PreviewLabel")
        options_row.addWidget(scheme_label)
        self._line_type_combo = QtWidgets.QComboBox(self._preview_panel)
        self._line_type_combo.addItems(
            [
                "Line Type",
                "Filament",
                "Speed",
                "Flow",
                "Line Width",
                "Layer Height",
                "Layer Time",
                "Fan Speed",
                "Temperature",
            ]
        )
        self._line_type_combo.setObjectName("PreviewCombo")
        self._line_type_combo.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed,
        )
        options_row.addWidget(self._line_type_combo)
        options_row.addStretch(1)
        panel_layout.addLayout(options_row)

        self._color_btn = QtWidgets.QToolButton(self._preview_panel)
        self._color_btn.setText("Color Show")
        self._color_btn.setCheckable(True)
        self._color_btn.setChecked(True)
        self._color_btn.setObjectName("PreviewToggle")
        self._color_btn.setVisible(False)
        self._gcode_btn = QtWidgets.QToolButton(self._preview_panel)
        self._gcode_btn.setText("G-code")
        self._gcode_btn.setCheckable(True)
        self._gcode_btn.setObjectName("PreviewToggle")
        self._gcode_btn.setVisible(False)
        toggle_group = QtWidgets.QButtonGroup(self._preview_panel)
        toggle_group.setExclusive(True)
        toggle_group.addButton(self._color_btn)
        toggle_group.addButton(self._gcode_btn)

        self._stack = QtWidgets.QStackedWidget(self._preview_panel)
        panel_layout.addWidget(self._stack, 1)
        self._build_preview_pages()

        self._platform_check = QtWidgets.QCheckBox("Print Platform")
        self._platform_check.setChecked(True)
        self._platform_check.setVisible(False)
        self._nozzle_check = QtWidgets.QCheckBox("Nozzle")
        self._nozzle_check.setChecked(True)
        self._nozzle_check.setVisible(False)

        self._action_panel = QtWidgets.QFrame(self.viewer)
        self._action_panel.setObjectName("ActionPanel")
        action_layout = QtWidgets.QVBoxLayout(self._action_panel)
        action_layout.setContentsMargins(10, 8, 10, 8)
        action_layout.setSpacing(6)

        self._slice_btn = QtWidgets.QPushButton("Slice plate", self._action_panel)
        slice_handler = getattr(self.main, "slice_current_plate", None)
        if not callable(slice_handler):
            slice_handler = getattr(self.main, "slice_current_model", None)
        if callable(slice_handler):
            self._slice_btn.clicked.connect(slice_handler)
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

    def _build_preview_pages(self):
        self._stack.setUpdatesEnabled(False)
        self._mode_pages.clear()
        self._legend_tables.clear()
        self._options_tables.clear()
        self._feature_display_items.clear()

        line_page = self._build_line_type_page()
        self._stack.addWidget(line_page)
        self._mode_pages["line_type"] = line_page

        filament_page = self._build_filament_page()
        self._stack.addWidget(filament_page)
        self._mode_pages["filament"] = filament_page

        legend_specs = [
            ("speed", "Speed (mm/s)"),
            ("flow", "Volumetric flow rate (mm^3/s)"),
            ("line_width", "Line Width (mm)"),
            ("layer_height", "Layer Height (mm)"),
            ("layer_time", "Layer Time"),
            ("fan", "Fan Speed (%)"),
            ("temperature", "Temperature (C)"),
        ]
        for key, title in legend_specs:
            page = self._build_legend_page(title, key)
            self._stack.addWidget(page)
            self._mode_pages[key] = page

        self._gcode_page = self._build_gcode_page()
        self._stack.addWidget(self._gcode_page)

        self._set_mode_page("line_type")
        self._stack.setUpdatesEnabled(True)

    def _build_line_type_page(self):
        page = QtWidgets.QWidget(self._stack)
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self._line_table = QtWidgets.QTableWidget(0, 5, page)
        self._line_table.setHorizontalHeaderLabels(
            ["Line Type", "Time", "Percent", "Used filament", "Display"]
        )
        self._line_table.verticalHeader().setVisible(False)
        self._line_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self._line_table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self._line_table.setAlternatingRowColors(False)
        self._line_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self._line_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self._line_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self._line_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self._line_table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self._line_table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self._line_table.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        self._line_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self._line_table.setWordWrap(False)
        self._line_table.verticalHeader().setDefaultSectionSize(22)
        self._line_table.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed,
        )
        self._line_table.setIconSize(QtCore.QSize(12, 12))
        layout.addWidget(self._line_table)

        layout.addWidget(self._make_separator())

        total_label = QtWidgets.QLabel("Total Estimation")
        total_label.setObjectName("PreviewHeader")
        layout.addWidget(total_label)

        totals_grid = QtWidgets.QGridLayout()
        totals_grid.setHorizontalSpacing(12)
        totals_grid.setVerticalSpacing(4)
        totals_labels = [
            "Total Filament:",
            "Model Filament:",
            "Cost:",
            "Prepare and timelapse time:",
            "Model printing time:",
            "Total time:",
        ]
        for row, text in enumerate(totals_labels):
            label = QtWidgets.QLabel(text)
            label.setObjectName("PreviewLabel")
            totals_grid.addWidget(label, row, 0)

        self._total_filament_value = QtWidgets.QLabel("n/a")
        self._model_filament_value = QtWidgets.QLabel("n/a")
        self._cost_value = QtWidgets.QLabel("n/a")
        self._prepare_time_value = QtWidgets.QLabel("n/a")
        self._model_time_value = QtWidgets.QLabel("n/a")
        self._total_time_value = QtWidgets.QLabel("n/a")

        for label in (
            self._total_filament_value,
            self._model_filament_value,
            self._cost_value,
            self._prepare_time_value,
            self._model_time_value,
            self._total_time_value,
        ):
            label.setObjectName("PreviewValue")

        totals_grid.addWidget(self._total_filament_value, 0, 1)
        totals_grid.addWidget(self._model_filament_value, 1, 1)
        totals_grid.addWidget(self._cost_value, 2, 1)
        totals_grid.addWidget(self._prepare_time_value, 3, 1)
        totals_grid.addWidget(self._model_time_value, 4, 1)
        totals_grid.addWidget(self._total_time_value, 5, 1)
        layout.addLayout(totals_grid)

        layout.addWidget(self._make_separator())

        ai_label = QtWidgets.QLabel("AI Checks")
        ai_label.setObjectName("PreviewHeader")
        layout.addWidget(ai_label)

        self._ai_checks_value = QtWidgets.QLabel("All checks passed.")
        self._ai_checks_value.setObjectName("PreviewValue")
        self._ai_checks_value.setWordWrap(True)
        layout.addWidget(self._ai_checks_value)

        return page

    def _build_filament_page(self):
        page = QtWidgets.QWidget(self._stack)
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        header = QtWidgets.QLabel("Filament")
        header.setObjectName("PreviewHeader")
        layout.addWidget(header)

        self._filament_table = QtWidgets.QTableWidget(0, 2, page)
        self._filament_table.setHorizontalHeaderLabels(["Filament", "Model"])
        self._filament_table.verticalHeader().setVisible(False)
        self._filament_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self._filament_table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self._filament_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self._filament_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self._filament_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self._filament_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self._filament_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self._filament_table.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self._filament_table.verticalHeader().setDefaultSectionSize(22)
        self._filament_table.setIconSize(QtCore.QSize(12, 12))
        layout.addWidget(self._filament_table)

        self._filament_change_label = QtWidgets.QLabel("Filament change times: n/a")
        self._filament_change_label.setObjectName("PreviewLabel")
        layout.addWidget(self._filament_change_label)
        self._filament_cost_label = QtWidgets.QLabel("Cost: n/a")
        self._filament_cost_label.setObjectName("PreviewLabel")
        layout.addWidget(self._filament_cost_label)

        layout.addWidget(self._make_separator())

        time_label = QtWidgets.QLabel("Time Estimation")
        time_label.setObjectName("PreviewHeader")
        layout.addWidget(time_label)

        time_grid = QtWidgets.QGridLayout()
        time_grid.setHorizontalSpacing(12)
        time_grid.setVerticalSpacing(4)
        time_rows = [
            "Prepare and timelapse time:",
            "Model printing time:",
            "Total time:",
        ]
        for row, text in enumerate(time_rows):
            label = QtWidgets.QLabel(text)
            label.setObjectName("PreviewLabel")
            time_grid.addWidget(label, row, 0)
        self._filament_prepare_value = QtWidgets.QLabel("n/a")
        self._filament_model_time_value = QtWidgets.QLabel("n/a")
        self._filament_total_time_value = QtWidgets.QLabel("n/a")
        for label in (
            self._filament_prepare_value,
            self._filament_model_time_value,
            self._filament_total_time_value,
        ):
            label.setObjectName("PreviewValue")
        time_grid.addWidget(self._filament_prepare_value, 0, 1)
        time_grid.addWidget(self._filament_model_time_value, 1, 1)
        time_grid.addWidget(self._filament_total_time_value, 2, 1)
        layout.addLayout(time_grid)

        layout.addWidget(self._make_separator())

        options_label = QtWidgets.QLabel("Options")
        options_label.setObjectName("PreviewHeader")
        layout.addWidget(options_label)
        options_table = self._build_options_table(page)
        layout.addWidget(options_table)
        self._options_tables["filament"] = options_table

        return page

    def _build_legend_page(self, title: str, mode_key: str):
        page = QtWidgets.QWidget(self._stack)
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        header = QtWidgets.QLabel(title)
        header.setObjectName("PreviewHeader")
        layout.addWidget(header)

        table = QtWidgets.QTableWidget(0, 1, page)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setVisible(False)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        table.setShowGrid(False)
        table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        table.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        table.verticalHeader().setDefaultSectionSize(22)
        table.setIconSize(QtCore.QSize(12, 12))
        layout.addWidget(table)
        self._legend_tables[mode_key] = table

        layout.addWidget(self._make_separator())

        options_label = QtWidgets.QLabel("Options")
        options_label.setObjectName("PreviewHeader")
        layout.addWidget(options_label)
        options_table = self._build_options_table(page)
        layout.addWidget(options_table)
        self._options_tables[mode_key] = options_table

        return page

    def _build_gcode_page(self):
        page = QtWidgets.QWidget(self._stack)
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        self._gcode_text = QtWidgets.QPlainTextEdit(page)
        self._gcode_text.setReadOnly(True)
        self._gcode_text.setObjectName("PreviewGCode")
        self._gcode_text.setPlaceholderText("Slice to generate a preview...")
        self._gcode_text.setLineWrapMode(QtWidgets.QPlainTextEdit.WidgetWidth)
        layout.addWidget(self._gcode_text)
        return page

    def _build_options_table(self, parent):
        features = [
            ("Travel", "travel"),
            ("Retract", "retract"),
            ("Unretract", "unretract"),
            ("Wipe", "wipe"),
            ("Seams", "seams"),
        ]
        table = QtWidgets.QTableWidget(len(features), 2, parent)
        table.setHorizontalHeaderLabels(["Options", "Display"])
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        table.setAlternatingRowColors(False)
        table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        table.verticalHeader().setDefaultSectionSize(22)
        for row, (label, key) in enumerate(features):
            name_item = QtWidgets.QTableWidgetItem(label)
            table.setItem(row, 0, name_item)
            display_item = QtWidgets.QTableWidgetItem("")
            display_item.setFlags(display_item.flags() | QtCore.Qt.ItemIsUserCheckable)
            display_item.setData(QtCore.Qt.UserRole, key)
            display_item.setCheckState(
                QtCore.Qt.Checked if self._default_feature_state(key) else QtCore.Qt.Unchecked
            )
            display_item.setTextAlignment(QtCore.Qt.AlignCenter)
            table.setItem(row, 1, display_item)
            self._register_feature_display_item(key, display_item)
        table.itemChanged.connect(self._on_feature_display_item_changed)
        self._autosize_table(table)
        return table

    def _make_separator(self):
        line = QtWidgets.QFrame(self._preview_panel)
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        line.setObjectName("PreviewSeparator")
        return line

    def _autosize_table(self, table: QtWidgets.QTableWidget):
        if table is None:
            return
        table.resizeRowsToContents()
        header_height = table.horizontalHeader().height() if table.horizontalHeader().isVisible() else 0
        rows_height = sum(table.rowHeight(row) for row in range(table.rowCount()))
        frame = table.frameWidth() * 2
        if table.rowCount() == 0:
            total = header_height + frame + 6
        else:
            total = header_height + rows_height + frame + 2
        table.setFixedHeight(total)

    def _autosize_preview_tables(self):
        if hasattr(self, "_line_table"):
            self._autosize_table(self._line_table)
        if hasattr(self, "_filament_table"):
            self._autosize_table(self._filament_table)
        for table in self._legend_tables.values():
            self._autosize_table(table)
        for table in self._options_tables.values():
            self._autosize_table(table)
        if hasattr(self, "_preview_panel") and self._preview_panel is not None:
            self._preview_panel.adjustSize()

    def _register_feature_display_item(self, key: str, item: QtWidgets.QTableWidgetItem):
        if key not in self._feature_display_state:
            self._feature_display_state[key] = self._default_feature_state(key)
        self._feature_display_items.setdefault(key, []).append(item)

    def _default_feature_state(self, key: str) -> bool:
        return key not in ("travel",)

    def _set_mode_page(self, key: str):
        page = self._mode_pages.get(key)
        if page is not None:
            self._stack.setCurrentWidget(page)

    def _toggle_collapsed(self):
        self._panel_collapsed = not self._panel_collapsed
        self._stack.setVisible(not self._panel_collapsed)
        self._collapse_btn.setText("^" if self._panel_collapsed else "v")
        self._preview_panel.adjustSize()
        self._autosize_panel()

    def _set_feature_display_state(self, key: str, checked: bool):
        self._feature_display_state[key] = bool(checked)
        self._feature_state_updating = True
        for item in self._feature_display_items.get(key, []):
            item.setCheckState(QtCore.Qt.Checked if checked else QtCore.Qt.Unchecked)
        self._feature_state_updating = False
        self._sync_feature_filter_from_state()

    def _sync_feature_filter_from_state(self):
        if not hasattr(self.viewer, "set_preview_feature_filter"):
            return
        checked = [key for key, enabled in self._feature_display_state.items() if enabled]
        if not checked:
            self.viewer.set_preview_feature_filter([])
            return
        if len(checked) == len(self._feature_display_state):
            self.viewer.set_preview_feature_filter(None)
        else:
            self.viewer.set_preview_feature_filter(checked)

    def _on_feature_display_item_changed(self, item):
        if self._feature_state_updating or self._line_type_updating:
            return
        if item is None:
            return
        if not item.flags() & QtCore.Qt.ItemIsUserCheckable:
            return
        key = item.data(QtCore.Qt.UserRole)
        if not key:
            return
        checked = item.checkState() == QtCore.Qt.Checked
        self._set_feature_display_state(str(key), checked)

    def _populate_printers(self):
        self._printer_combo.clear()
        printers = getattr(self.main, "printers", []) or []
        if not printers:
            self._printer_combo.addItem("No printers configured")
            self._printer_combo.setEnabled(False)
            return
        self._printer_combo.setEnabled(True)
        default_name = ""
        runtime_state = getattr(self.main, "runtime_printer_state", None)
        if runtime_state is not None:
            default_name = str(getattr(runtime_state, "name", "")).strip().lower()
        if not default_name:
            default_name = str(DEFAULTS.get("printer", {}).get("name", "")).strip().lower()
        default_index = None
        for idx, printer in enumerate(printers):
            name = printer.get("name") if isinstance(printer, dict) else None
            self._printer_combo.addItem(name or "Printer")
            if default_name and str(name or "").strip().lower() == default_name:
                default_index = idx
        if default_index is not None:
            self._printer_combo.setCurrentIndex(default_index)
        self._printer_combo.currentIndexChanged.connect(self._emit_printer_changed)

    def set_preview_settings(self, settings):
        self._preview_settings = settings
        self._update_line_type_stats()
        self._update_filament_view()

    def _line_type_color(self, key: str) -> QtGui.QColor:
        color = None
        if hasattr(self.viewer, "_preview_feature_color"):
            try:
                color = self.viewer._preview_feature_color(key)
            except Exception:
                color = None
        if color is None:
            color = (0.7, 0.7, 0.7, 1.0)
        if isinstance(color, QtGui.QColor):
            return color
        values = list(color) if isinstance(color, (list, tuple)) else [0.7, 0.7, 0.7, 1.0]
        if len(values) < 3:
            values = [0.7, 0.7, 0.7, 1.0]
        if len(values) == 3:
            values.append(1.0)
        if max(values[:3]) <= 1.0:
            values = [float(v) * 255.0 for v in values]

        def _channel(value: object, fallback: int) -> int:
            try:
                numeric = float(value)
            except (TypeError, ValueError):
                numeric = float(fallback)
            if numeric < 0.0:
                return 0
            if numeric > 255.0:
                return 255
            return int(round(numeric))

        red = _channel(values[0], 179)
        green = _channel(values[1], 179)
        blue = _channel(values[2], 179)
        alpha = _channel(values[3], 255)
        return QtGui.QColor(red, green, blue, alpha)

    def _line_type_icon(self, key: str) -> QtGui.QIcon:
        color = self._line_type_color(key)
        pix = QtGui.QPixmap(10, 10)
        pix.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pix)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QBrush(color))
        painter.drawRoundedRect(0, 0, 10, 10, 2, 2)
        painter.end()
        return QtGui.QIcon(pix)

    def _color_square_icon(self, color) -> QtGui.QIcon:
        qcolor = QtGui.QColor(color) if color else QtGui.QColor(180, 180, 180)
        pix = QtGui.QPixmap(10, 10)
        pix.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pix)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QBrush(qcolor))
        painter.drawRoundedRect(0, 0, 10, 10, 2, 2)
        painter.end()
        return QtGui.QIcon(pix)

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
        if emit:
            self._emit_printer_changed(idx)

    def _emit_printer_changed(self, _index: int):
        printers = getattr(self.main, "printers", []) or []
        if not printers:
            return
        idx = self._printer_combo.currentIndex()
        if idx < 0 or idx >= len(printers):
            return
        printer = printers[idx]
        if isinstance(printer, dict):
            self.printer_changed.emit(printer)

    def _feature_label(self, key: str) -> str:
        text = str(key or "").strip()
        if not text:
            return "Other"
        known = FEATURE_LABEL_OVERRIDES.get(text)
        if known:
            return known
        normalized = text.replace("-", "_").replace(" ", "_")
        return normalized.replace("_", " ").strip().title() or "Other"

    def _line_type_keys_for_preview(self, preview) -> list[str]:
        keys = [key for _label, key in BASE_LINE_TYPE_MAP]
        if preview is None or not getattr(preview, "layers", None):
            return keys

        seen = set(keys)
        for layer in preview.layers:
            for seg in getattr(layer, "segments", []):
                feature = str(getattr(seg, "feature", "") or "").strip()
                if not feature or feature in seen:
                    continue
                keys.append(feature)
                seen.add(feature)
        return keys

    def _populate_line_types(self, preview=None):
        feature_keys = self._line_type_keys_for_preview(preview)
        allowed_keys = set(feature_keys)
        for key in list(self._feature_display_state.keys()):
            if key not in allowed_keys:
                self._feature_display_state.pop(key, None)
        self._line_type_map = [(self._feature_label(key), key) for key in feature_keys]
        updated_items = {}
        for key, items in self._feature_display_items.items():
            kept = [item for item in items if item.tableWidget() is not self._line_table]
            if kept:
                updated_items[key] = kept
        self._feature_display_items = updated_items
        self._line_type_updating = True
        self._line_table.setRowCount(len(self._line_type_map))
        for row, (label, key) in enumerate(self._line_type_map):
            item = QtWidgets.QTableWidgetItem(label)
            item.setData(QtCore.Qt.UserRole, key)
            item.setIcon(self._line_type_icon(key))
            self._line_table.setItem(row, 0, item)
            self._line_table.setItem(row, 1, QtWidgets.QTableWidgetItem("n/a"))
            self._line_table.setItem(row, 2, QtWidgets.QTableWidgetItem("n/a"))
            self._line_table.setItem(row, 3, QtWidgets.QTableWidgetItem("n/a"))
            display_item = QtWidgets.QTableWidgetItem("")
            display_item.setFlags(display_item.flags() | QtCore.Qt.ItemIsUserCheckable)
            self._register_feature_display_item(key, display_item)
            display_item.setCheckState(
                QtCore.Qt.Checked if self._feature_display_state.get(key, True) else QtCore.Qt.Unchecked
            )
            display_item.setData(QtCore.Qt.UserRole, key)
            display_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self._line_table.setItem(row, 4, display_item)
        self._line_type_updating = False
        self._autosize_line_table()

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
        self._line_table.itemChanged.connect(self._on_feature_display_item_changed)
        self._platform_check.toggled.connect(self._on_platform_toggled)
        self._nozzle_check.toggled.connect(self._on_nozzle_toggled)
        self._collapse_btn.clicked.connect(self._toggle_collapsed)
        self._on_platform_toggled(self._platform_check.isChecked())
        self._on_nozzle_toggled(self._nozzle_check.isChecked())

    def _autosize_line_table(self):
        self._autosize_preview_tables()

    def _sync_toggle_stack(self):
        if self._gcode_btn.isChecked() and hasattr(self, "_gcode_page"):
            self._stack.setCurrentWidget(self._gcode_page)

    def apply_theme(self):
        panel_bg_color = theme_qcolor("popup_bg")
        if panel_bg_color.lightness() > 160:
            panel_bg_color = QtGui.QColor("#2f3137")
        panel_bg_color.setAlpha(180)
        panel_bg = (f"rgba({panel_bg_color.red()}, {panel_bg_color.green()}, "
                    f"{panel_bg_color.blue()}, {panel_bg_color.alpha()})")
        inner_bg = panel_bg
        header_bg_color = theme_qcolor("popup_header_bg")
        if header_bg_color.alpha() == 255:
            header_bg_color.setAlpha(panel_bg_color.alpha())
        header_bg = (f"rgba({header_bg_color.red()}, {header_bg_color.green()}, "
                     f"{header_bg_color.blue()}, {header_bg_color.alpha()})")
        panel_border = theme_css("popup_border")
        panel_text = "#f8f9fb"
        muted_text = panel_text
        action_border = theme_css("action_panel_border")
        action_bg = panel_bg

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
            "QToolButton#PreviewCollapse {"
            f"  color: {panel_text};"
            "  background: transparent;"
            "  border: none;"
            "  font-weight: 600;"
            "}"
            "QLabel#PreviewLabel {"
            f"  color: {muted_text};"
            "}"
            "QLabel#PreviewValue {"
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
            f"  background: {inner_bg};"
            f"  color: {panel_text};"
            f"  border: 1px solid {panel_border};"
            "  padding: 2px 6px;"
            "  border-radius: 6px;"
            "}"
            "QComboBox#PreviewCombo QAbstractItemView {"
            f"  background: {inner_bg};"
            f"  color: {panel_text};"
            f"  selection-background-color: {theme_css('menu_hover_bg')};"
            "}"
            "QCheckBox {"
            f"  color: {panel_text};"
            "}"
            "QTableWidget {"
            f"  background: {inner_bg};"
            f"  color: {panel_text};"
            f"  border: 1px solid {panel_border};"
            f"  gridline-color: rgba(255, 255, 255, 35);"
            "}"
            "QTableWidget QAbstractScrollArea::viewport {"
            f"  background: {inner_bg};"
            "}"
            "QTableWidget::item {"
            "  background: transparent;"
            "  padding: 2px 6px;"
            "}"
            "QTableWidget::item:selected {"
            "  background: rgba(255, 255, 255, 25);"
            f"  color: {panel_text};"
            "}"
            "QTableWidget::indicator {"
            "  width: 12px;"
            "  height: 12px;"
            "}"
            "QTableWidget::indicator:checked {"
            f"  background: {theme_css('topbar_accent')};"
            f"  border: 1px solid {theme_css('topbar_accent')};"
            "}"
            "QTableWidget::indicator:unchecked {"
            f"  background: transparent;"
            f"  border: 1px solid {panel_border};"
            "}"
            "QHeaderView::section {"
            f"  background: {header_bg};"
            f"  color: {panel_text};"
            f"  border: 1px solid {panel_border};"
            "  padding: 4px 6px;"
            "}"
            "QTableCornerButton::section {"
            f"  background: {header_bg};"
            f"  border: 1px solid {panel_border};"
            "}"
            "QStackedWidget {"
            "  background: transparent;"
            "}"
            "QFrame#PreviewSeparator {"
            f"  background: {panel_border};"
            "  max-height: 1px;"
            "}"
            "QPlainTextEdit#PreviewGCode {"
            f"  background: {inner_bg};"
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
        self._autosize_preview_tables()
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
        max_width = min(560, available)
        target = min(self._preview_panel.sizeHint().width(), max_width)
        target = max(380, int(target))
        self._preview_panel.setFixedWidth(target)

    def update_stats(self, stats):
        self._preview_stats = stats or {}
        if not stats:
            self._total_filament_value.setText("n/a")
            self._model_filament_value.setText("n/a")
            self._cost_value.setText("n/a")
            self._prepare_time_value.setText("n/a")
            self._model_time_value.setText("n/a")
            self._total_time_value.setText("n/a")
            if hasattr(self, "_ai_checks_value"):
                self._ai_checks_value.setText("All checks passed.")
            self._update_filament_view()
            return
        length = stats.get("length", "n/a")
        weight = stats.get("weight", "n/a")
        total_filament = f"{length}   {weight}" if length != "n/a" and weight != "n/a" else "n/a"
        self._total_filament_value.setText(total_filament)
        self._model_filament_value.setText(total_filament)
        self._cost_value.setText(stats.get("cost", "n/a"))
        self._prepare_time_value.setText("n/a")
        time_val = stats.get("time", "n/a")
        self._model_time_value.setText(time_val)
        self._total_time_value.setText(time_val)
        if hasattr(self, "_ai_checks_value"):
            warnings = stats.get("ai_warnings") or []
            suggestions = stats.get("ai_suggestions") or []
            lines = []
            if warnings:
                lines.append("Warnings: " + " | ".join(warnings))
            if suggestions:
                lines.append("Suggestions: " + " | ".join(suggestions))
            self._ai_checks_value.setText("All checks passed." if not lines else "\n".join(lines))
        self._update_filament_view()

    def _update_filament_view(self):
        stats = self._preview_stats or {}
        length = stats.get("length", "n/a")
        weight = stats.get("weight", "n/a")
        cost = stats.get("cost", "n/a")
        model_value = (
            f"{length}   {weight}" if length != "n/a" and weight != "n/a" else "n/a"
        )
        if hasattr(self, "_filament_table"):
            if model_value == "n/a":
                self._filament_table.setRowCount(0)
            else:
                self._filament_table.setRowCount(1)
                item = QtWidgets.QTableWidgetItem("1")
                filament_color = None
                if self._preview_settings is not None:
                    filament_color = getattr(self._preview_settings, "filament_color", None)
                item.setIcon(self._color_square_icon(filament_color))
                self._filament_table.setItem(0, 0, item)
                self._filament_table.setItem(0, 1, QtWidgets.QTableWidgetItem(model_value))
        if hasattr(self, "_filament_change_label"):
            change_val = "1" if model_value != "n/a" else "n/a"
            self._filament_change_label.setText(f"Filament change times: {change_val}")
        if hasattr(self, "_filament_cost_label"):
            self._filament_cost_label.setText(f"Cost: {cost}")
        time_val = stats.get("time", "n/a")
        if hasattr(self, "_filament_prepare_value"):
            self._filament_prepare_value.setText("n/a")
        if hasattr(self, "_filament_model_time_value"):
            self._filament_model_time_value.setText(time_val)
        if hasattr(self, "_filament_total_time_value"):
            self._filament_total_time_value.setText(time_val)
        self._autosize_preview_tables()

    def _legend_values(self, min_val: float, max_val: float, steps: int = 9):
        if max_val <= 0:
            return []
        if max_val <= min_val:
            return [max_val]
        if steps <= 1:
            return [max_val]
        step = (max_val - min_val) / float(steps - 1)
        return [max_val - step * i for i in range(steps)]

    def _populate_legend_table(self, mode_key: str, values, min_val: float, max_val: float, fmt: str):
        table = self._legend_tables.get(mode_key)
        if table is None:
            return
        table.setRowCount(len(values))
        for row, value in enumerate(values):
            if hasattr(self.viewer, "_preview_color_from_scalar"):
                color = self.viewer._preview_color_from_scalar(value, min_val, max_val)
            else:
                color = (0.4, 0.8, 0.9, 1.0)
            pix = QtGui.QPixmap(10, 10)
            pix.fill(QtCore.Qt.transparent)
            painter = QtGui.QPainter(pix)
            painter.fillRect(pix.rect(), QtGui.QColor.fromRgbF(*color))
            painter.end()
            item = QtWidgets.QTableWidgetItem(fmt.format(value))
            item.setIcon(QtGui.QIcon(pix))
            table.setItem(row, 0, item)
        self._autosize_table(table)

    def _update_legend_tables(self):
        preview = self._preview_data
        if preview is None:
            for table in self._legend_tables.values():
                table.setRowCount(0)
            self._autosize_preview_tables()
            return
        self._populate_legend_table(
            "speed",
            self._legend_values(preview.min_speed, preview.max_speed),
            preview.min_speed,
            preview.max_speed,
            "{:.0f}",
        )
        self._populate_legend_table(
            "flow",
            self._legend_values(preview.min_flow, preview.max_flow),
            preview.min_flow,
            preview.max_flow,
            "{:.2f}",
        )
        self._populate_legend_table(
            "line_width",
            self._legend_values(preview.min_width, preview.max_width),
            preview.min_width,
            preview.max_width,
            "{:.2f}",
        )
        self._populate_legend_table(
            "layer_height",
            self._legend_values(preview.min_layer_height, preview.max_layer_height),
            preview.min_layer_height,
            preview.max_layer_height,
            "{:.2f}",
        )
        self._populate_legend_table(
            "layer_time",
            self._legend_values(preview.min_layer_time, preview.max_layer_time),
            preview.min_layer_time,
            preview.max_layer_time,
            "{:.1f}",
        )
        fan_values = self._legend_values(preview.min_fan, preview.max_fan)
        fan_display = [val / 255.0 * 100.0 for val in fan_values]
        table = self._legend_tables.get("fan")
        if table is not None:
            table.setRowCount(len(fan_values))
            for row, raw in enumerate(fan_values):
                if hasattr(self.viewer, "_preview_color_from_scalar"):
                    color = self.viewer._preview_color_from_scalar(raw, preview.min_fan, preview.max_fan)
                else:
                    color = (0.4, 0.8, 0.9, 1.0)
                pix = QtGui.QPixmap(10, 10)
                pix.fill(QtCore.Qt.transparent)
                painter = QtGui.QPainter(pix)
                painter.fillRect(pix.rect(), QtGui.QColor.fromRgbF(*color))
                painter.end()
                item = QtWidgets.QTableWidgetItem(f"{fan_display[row]:.0f}")
                item.setIcon(QtGui.QIcon(pix))
                table.setItem(row, 0, item)
            self._autosize_table(table)
        self._populate_legend_table(
            "temperature",
            self._legend_values(preview.min_temp, preview.max_temp),
            preview.min_temp,
            preview.max_temp,
            "{:.0f}",
        )
        self._autosize_preview_tables()

    def set_gcode_text(self, text: str):
        self._gcode_text.setPlainText(text or "")

    def set_steps_count(self, count: int):
        count = max(0, int(count))
        self._steps_slider.setRange(0, count)
        self._steps_spin.setRange(0, count)
        self._set_steps_value(count)

    def set_layer_count(self, count: int):
        count = max(0, int(count))
        top = max(0, count - 1)
        self._layer_slider.setRange(0, top)
        self._set_layer_value(top)
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
        step_value = self._step_value_for_layer(int(value))
        if hasattr(self.viewer, "set_preview_step_index"):
            self.viewer.set_preview_step_index(int(step_value))
        self._set_steps_value(step_value)
        self._update_layer_label(int(value))
        self._update_nozzle_info()

    def _on_step_changed(self, value: int):
        if hasattr(self.viewer, "set_preview_step_index"):
            self.viewer.set_preview_step_index(int(value))
        if self._steps_spin.value() != value:
            block = self._steps_spin.blockSignals(True)
            self._steps_spin.setValue(int(value))
            self._steps_spin.blockSignals(block)
        layer_index = self._layer_for_step(int(value))
        self._set_layer_value(layer_index)
        self._update_layer_label(layer_index)
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
        self._layer_offsets = []
        self._total_steps = 0
        self._populate_line_types(preview)
        if preview is None or not getattr(preview, "layers", None):
            self.set_layer_count(0)
            self.set_steps_count(0)
            self._update_line_type_stats()
            self._sync_feature_filter()
            self._update_nozzle_info()
            self._update_legend_tables()
            return
        total = 0
        for layer in preview.layers:
            self._layer_offsets.append(total)
            total += len(layer.segments)
        self._total_steps = total
        self.set_layer_count(len(preview.layers))
        self.set_steps_count(total)
        self._update_line_type_stats()
        self._sync_feature_filter()
        self._update_legend_tables()
        self._update_nozzle_info()

    def _update_steps_for_layer(self, layer_index: int):
        step_value = self._step_value_for_layer(layer_index)
        self._set_steps_value(step_value)
        self._update_nozzle_info()

    def _step_value_for_layer(self, layer_index: int) -> int:
        if self._preview_data is None or not getattr(self._preview_data, "layers", None):
            return 0
        layers = self._preview_data.layers
        idx = max(0, min(int(layer_index), len(layers) - 1))
        if not self._layer_offsets:
            total = 0
            for layer in layers:
                self._layer_offsets.append(total)
                total += len(layer.segments)
            self._total_steps = total
        return self._layer_offsets[idx] + len(layers[idx].segments)

    def _layer_for_step(self, step_value: int) -> int:
        if self._preview_data is None or not getattr(self._preview_data, "layers", None):
            return 0
        layers = self._preview_data.layers
        if not layers:
            return 0
        if not self._layer_offsets:
            total = 0
            for layer in layers:
                self._layer_offsets.append(total)
                total += len(layer.segments)
            self._total_steps = total
        step_value = max(0, min(int(step_value), int(self._total_steps)))
        layer_index = bisect.bisect_right(self._layer_offsets, step_value) - 1
        return max(0, min(layer_index, len(layers) - 1))

    def _set_steps_value(self, value: int):
        block_slider = self._steps_slider.blockSignals(True)
        block_spin = self._steps_spin.blockSignals(True)
        self._steps_slider.setValue(int(value))
        self._steps_spin.setValue(int(value))
        self._steps_slider.blockSignals(block_slider)
        self._steps_spin.blockSignals(block_spin)

    def _set_layer_value(self, value: int):
        block = self._layer_slider.blockSignals(True)
        self._layer_slider.setValue(int(value))
        self._layer_slider.blockSignals(block)

    def _on_line_type_changed(self, item):
        self._on_feature_display_item_changed(item)

    def _sync_feature_filter(self):
        self._sync_feature_filter_from_state()

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
        total_extrude = 0.0
        if self._preview_data is not None and getattr(self._preview_data, "layers", None):
            for layer in self._preview_data.layers:
                for seg in layer.segments:
                    dist = math.dist(seg.start, seg.end)
                    if seg.speed > 0:
                        t = dist / seg.speed
                    else:
                        t = 0.0
                    entry = totals.setdefault(seg.feature, {"time": 0.0, "extrude": 0.0})
                    entry["time"] += t
                    total_time += t
                    if seg.is_extrude and seg.extrusion > 0.0:
                        entry["extrude"] += float(seg.extrusion)
                        total_extrude += float(seg.extrusion)
        area = None
        density = None
        settings = self._preview_settings
        if settings is not None:
            try:
                filament_diameter = float(settings.filament_diameter or 1.75)
                area = math.pi * (filament_diameter / 2.0) ** 2
                density = float(settings.filament_density)
            except (TypeError, ValueError):
                area = None
                density = None
        for row in range(self._line_table.rowCount()):
            item = self._line_table.item(row, 0)
            if item is None:
                continue
            key = item.data(QtCore.Qt.UserRole)
            entry = totals.get(key, {"time": 0.0, "extrude": 0.0})
            seconds = float(entry.get("time", 0.0) or 0.0)
            time_str = self._format_duration(seconds) if seconds > 0 else "n/a"
            percent = (seconds / total_time * 100.0) if total_time > 0 else 0.0
            self._line_table.setItem(row, 1, QtWidgets.QTableWidgetItem(time_str))
            self._line_table.setItem(row, 2, QtWidgets.QTableWidgetItem(f"{percent:.1f}%"))
            extrude_len = float(entry.get("extrude", 0.0) or 0.0)
            used_str = "n/a"
            if extrude_len > 0.0:
                length_m = extrude_len / 1000.0
                if area is not None and density is not None and area > 0.0 and density > 0.0:
                    volume_mm3 = area * extrude_len
                    weight_g = (volume_mm3 / 1000.0) * density
                    used_str = f"{length_m:.2f} m   {weight_g:.2f} g"
                else:
                    used_str = f"{length_m:.2f} m"
            self._line_table.setItem(row, 3, QtWidgets.QTableWidgetItem(used_str))
        self._autosize_preview_tables()

    def _on_color_mode_changed(self, value: str):
        label = (value or "").strip()
        scheme_map = {
            "Line Type": ("line_type", "feature"),
            "Filament": ("filament", "filament"),
            "Speed": ("speed", "speed"),
            "Flow": ("flow", "flow"),
            "Line Width": ("line_width", "width"),
            "Layer Height": ("layer_height", "layer_height"),
            "Layer Time": ("layer_time", "layer_time"),
            "Fan Speed": ("fan", "fan"),
            "Temperature": ("temperature", "temperature"),
        }
        mode_key, selected = scheme_map.get(label, ("line_type", "feature"))
        self._set_mode_page(mode_key)
        self._autosize_preview_tables()
        self._preview_panel.adjustSize()
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

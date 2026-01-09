from __future__ import annotations

from dataclasses import asdict
from typing import Dict, List, Tuple

from PyQt5 import QtCore, QtGui, QtWidgets

from slicer.gcode import SliceSettings
from config.defaults import DEFAULTS
from .theme import theme_css


class SettingsTooltip(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent, QtCore.Qt.ToolTip)
        self.setObjectName("SettingsTooltip")
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint, True)
        self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, False)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(6)
        layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        self._title = QtWidgets.QLabel(self)
        self._title.setObjectName("SettingsTooltipTitle")
        layout.addWidget(self._title)

        self._body = QtWidgets.QLabel(self)
        self._body.setObjectName("SettingsTooltipBody")
        self._body.setWordWrap(True)
        layout.addWidget(self._body)

        self._param = QtWidgets.QLabel(self)
        self._param.setObjectName("SettingsTooltipParam")
        self._param.setWordWrap(True)
        layout.addWidget(self._param)

        self._image = QtWidgets.QLabel(self)
        self._image.setObjectName("SettingsTooltipImage")
        self._image.setAlignment(QtCore.Qt.AlignCenter)
        self._image.setFixedSize(220, 130)
        layout.addWidget(self._image)

    def set_content(self, title: str, body: str, param: str, image_key: str, accent: QtGui.QColor):
        self._title.setText(title)
        self._body.setText(body)
        self._param.setText("")
        self._param.setVisible(False)
        self._image.setPixmap(self._render_image(image_key, accent))

    def apply_theme(self, bg: str, border: str, text: str, muted: str):
        self.setStyleSheet(
            "QFrame#SettingsTooltip {"
            f"  background: {bg};"
            f"  border: 1px solid {border};"
            "  border-radius: 8px;"
            "}"
            "QLabel#SettingsTooltipTitle {"
            f"  color: {text};"
            "  font-weight: 600;"
            "}"
            "QLabel#SettingsTooltipBody {"
            f"  color: {text};"
            "}"
            "QLabel#SettingsTooltipParam {"
            f"  color: {muted};"
            "}"
        )

    def _render_image(self, key: str, accent: QtGui.QColor) -> QtGui.QPixmap:
        width = self._image.width()
        height = self._image.height()
        pix = QtGui.QPixmap(width, height)
        bg = QtGui.QColor("#3a3d44")
        pix.fill(bg)

        painter = QtGui.QPainter(pix)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        base = QtGui.QColor("#5b5f67")
        dark = QtGui.QColor("#2a2d33")

        def draw_stack(highlight_top: bool, highlight_bottom: bool):
            painter.setPen(QtGui.QPen(base, 2))
            for idx in range(6):
                y = height - 30 - idx * 12
                painter.drawRoundedRect(24, y, 130, 8, 3, 3)
            if highlight_top:
                painter.setPen(QtGui.QPen(accent, 3))
                painter.drawLine(24, height - 30 - 5 * 12, 154, height - 30 - 5 * 12)
            if highlight_bottom:
                painter.setPen(QtGui.QPen(accent, 3))
                painter.drawLine(24, height - 30, 154, height - 30)

        if key == "layer_height":
            draw_stack(True, False)
            painter.setPen(QtGui.QPen(accent, 2))
            painter.drawLine(178, height - 30, 178, height - 30 - 5 * 12)
            painter.drawLine(172, height - 30 - 5 * 12 + 6, 178, height - 30 - 5 * 12)
            painter.drawLine(184, height - 30 - 5 * 12 + 6, 178, height - 30 - 5 * 12)
        elif key == "first_layer_height":
            draw_stack(False, True)
            painter.setPen(QtGui.QPen(accent, 2))
            painter.drawLine(178, height - 30, 178, height - 42)
            painter.drawLine(172, height - 36, 178, height - 42)
            painter.drawLine(184, height - 36, 178, height - 42)
        elif key == "seam_position":
            painter.setPen(QtGui.QPen(base, 6))
            for idx in range(4):
                y = 32 + idx * 16
                painter.drawLine(24, y, 180, y)
            painter.setPen(QtGui.QPen(accent, 6))
            painter.drawPoint(70, 32)
            painter.setPen(QtGui.QPen(accent, 2))
            painter.drawLine(70, 18, 100, 18)
            painter.drawLine(96, 14, 100, 18)
            painter.drawLine(96, 22, 100, 18)
        elif key == "precise_wall":
            painter.setPen(QtGui.QPen(base, 3))
            painter.drawRoundedRect(34, 26, 140, 90, 6, 6)
            painter.setPen(QtGui.QPen(accent, 2))
            painter.drawRoundedRect(46, 38, 116, 66, 5, 5)
        elif key == "filament_color":
            swatch = QtCore.QRect(40, 35, 90, 60)
            painter.fillRect(swatch, accent)
            painter.setPen(QtGui.QPen(QtGui.QColor("#ffffff"), 2))
            painter.drawRect(swatch)
        elif key == "one_wall_top":
            draw_stack(True, False)
            painter.setPen(QtGui.QPen(accent, 2))
            painter.drawLine(170, 30, 190, 30)
            painter.drawLine(186, 26, 190, 30)
            painter.drawLine(186, 34, 190, 30)
        elif key == "one_wall_first":
            draw_stack(False, True)
            painter.setPen(QtGui.QPen(accent, 2))
            painter.drawLine(170, height - 30, 190, height - 30)
            painter.drawLine(186, height - 34, 190, height - 30)
            painter.drawLine(186, height - 26, 190, height - 30)
        elif key == "filament_type":
            painter.setPen(QtGui.QPen(base, 3))
            painter.drawEllipse(50, 30, 90, 90)
            painter.setPen(QtGui.QPen(dark, 3))
            painter.drawEllipse(70, 50, 50, 50)
            painter.setPen(QtGui.QPen(accent, 3))
            painter.drawLine(110, 20, 170, 20)
            painter.drawLine(166, 16, 170, 20)
            painter.drawLine(166, 24, 170, 20)
            painter.setPen(QtGui.QPen(QtGui.QColor("#ffffff"), 1))
            painter.drawText(60, 120, "PLA")
        elif key == "line_width":
            nozzle_x = width - 80
            painter.setPen(QtGui.QPen(base, 2))
            painter.setBrush(base)
            painter.drawRect(nozzle_x, 28, 24, 38)
            tip = QtGui.QPolygon(
                [
                    QtCore.QPoint(nozzle_x - 6, 66),
                    QtCore.QPoint(nozzle_x + 12, 92),
                    QtCore.QPoint(nozzle_x + 30, 66),
                ]
            )
            painter.drawPolygon(tip)
            painter.setPen(QtGui.QPen(accent, 3))
            painter.drawLine(30, 92, nozzle_x - 10, 92)
            painter.drawLine(30, 86, 30, 98)
            painter.drawLine(nozzle_x - 10, 86, nozzle_x - 10, 98)
        elif key == "precision":
            painter.setPen(QtGui.QPen(base, 2))
            painter.drawRoundedRect(28, 24, 150, 88, 6, 6)
            painter.setPen(QtGui.QPen(accent, 2))
            painter.drawLine(44, 68, 162, 68)
            painter.drawLine(44, 54, 44, 82)
            painter.drawLine(162, 54, 162, 82)
            painter.setPen(QtGui.QPen(dark, 1))
            for x in range(40, 160, 12):
                painter.drawLine(x, 34, x, 100)
        elif key == "ironing_type":
            painter.setPen(QtGui.QPen(base, 2))
            painter.drawRoundedRect(36, 60, 130, 40, 6, 6)
            painter.setPen(QtGui.QPen(accent, 2))
            for idx in range(6):
                y = 66 + idx * 5
                painter.drawLine(42, y, 160, y)
            painter.setPen(QtGui.QPen(base, 2))
            painter.drawLine(170, 45, 190, 45)
            painter.drawLine(188, 41, 190, 45)
            painter.drawLine(188, 49, 190, 45)
        elif key == "wall_generator":
            painter.setPen(QtGui.QPen(base, 2))
            painter.drawRoundedRect(30, 24, 70, 90, 6, 6)
            painter.drawRoundedRect(40, 34, 50, 70, 5, 5)
            painter.setPen(QtGui.QPen(accent, 2))
            painter.drawRoundedRect(112, 24, 70, 90, 6, 6)
            painter.drawLine(122, 34, 172, 84)
            painter.drawLine(122, 84, 172, 34)
        elif key == "wall_sequence":
            painter.setPen(QtGui.QPen(base, 2))
            painter.drawRoundedRect(32, 30, 70, 70, 6, 6)
            painter.drawRoundedRect(46, 44, 42, 42, 5, 5)
            painter.setPen(QtGui.QPen(accent, 2))
            painter.drawLine(120, 50, 180, 50)
            painter.drawLine(176, 46, 180, 50)
            painter.drawLine(176, 54, 180, 50)
            painter.setPen(QtGui.QPen(base, 2))
            painter.drawRoundedRect(120, 60, 60, 40, 6, 6)
        elif key == "bridge_flow":
            painter.setPen(QtGui.QPen(base, 3))
            painter.drawRect(40, 70, 25, 30)
            painter.drawRect(150, 70, 25, 30)
            painter.setPen(QtGui.QPen(accent, 3))
            for idx in range(5):
                y = 70 + idx * 4
                painter.drawLine(65, y, 150, y)
        elif key == "overhang":
            painter.setPen(QtGui.QPen(base, 2))
            painter.drawLine(40, 96, 160, 96)
            painter.setPen(QtGui.QPen(accent, 3))
            painter.drawLine(70, 90, 150, 60)
            painter.drawLine(70, 90, 70, 60)
            painter.drawLine(70, 60, 150, 60)
        else:
            painter.setPen(QtGui.QPen(dark, 2))
            painter.drawRect(20, 20, width - 40, height - 40)

        painter.end()
        return pix


class SettingsPanel(QtWidgets.QWidget):
    """Print settings panel with process scopes and grouped sections."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("SettingsPanel")
        self._defaults = SliceSettings()
        self._search_rows: Dict[str, List[Tuple[QtWidgets.QFrame, QtWidgets.QWidget, str]]] = {}
        self._page_keys: List[str] = []
        self._page_widgets: Dict[str, QtWidgets.QScrollArea] = {}
        self._filament_color = QtGui.QColor("#42d94a")
        self._tooltip = SettingsTooltip()
        self._tooltip_hide_timer = QtCore.QTimer(self)
        self._tooltip_hide_timer.setSingleShot(True)
        self._tooltip_hide_timer.timeout.connect(self._hide_tooltip)
        self._hover_tooltips: Dict[QtCore.QObject, dict] = {}
        self._advanced_rows: set[QtWidgets.QWidget] = set()
        self._tooltip_defs = self._build_tooltip_defs()
        self._build_ui()
        self.apply_theme()
        self.set_printers(getattr(self.parent(), "printers", []) or [])

    def _build_ui(self):
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(8, 8, 8, 8)
        root.setSpacing(8)

        self._build_printer_row(root)
        self._build_header(root)
        self._build_process_row(root)
        self._build_profile_row(root)
        self._build_content(root)

    def _build_header(self, root: QtWidgets.QVBoxLayout):
        header = QtWidgets.QFrame(self)
        header.setObjectName("SettingsHeader")
        header_layout = QtWidgets.QHBoxLayout(header)
        header_layout.setContentsMargins(10, 6, 10, 6)
        header_layout.setSpacing(6)

        title = QtWidgets.QLabel("Filament", header)
        title.setObjectName("SettingsHeaderTitle")
        header_layout.addWidget(title)
        header_layout.addStretch(1)

        for label in ("Save", "Import", "+", "-", "Gear"):
            btn = QtWidgets.QToolButton(header)
            btn.setText(label)
            btn.setObjectName("SettingsHeaderButton")
            btn.setCursor(QtCore.Qt.PointingHandCursor)
            header_layout.addWidget(btn)

        root.addWidget(header)

        filament_row = QtWidgets.QFrame(self)
        filament_row.setObjectName("FilamentRow")
        filament_layout = QtWidgets.QHBoxLayout(filament_row)
        filament_layout.setContentsMargins(4, 0, 4, 0)
        filament_layout.setSpacing(8)

        self._filament_slot_label = QtWidgets.QLabel("1", filament_row)
        self._filament_slot_label.setObjectName("FilamentSlot")
        filament_layout.addWidget(self._filament_slot_label)

        self._filament_color_button = QtWidgets.QToolButton(filament_row)
        self._filament_color_button.setObjectName("FilamentColorButton")
        self._filament_color_button.setFixedSize(26, 26)
        self._filament_color_button.setCursor(QtCore.Qt.PointingHandCursor)
        self._filament_color_button.clicked.connect(self._choose_filament_color)
        filament_layout.addWidget(self._filament_color_button)

        self._filament_type_menu = QtWidgets.QMenu(self)
        for name in ("Hyper PLA", "PLA", "PETG", "ABS", "TPU"):
            action = self._filament_type_menu.addAction(name)
            action.triggered.connect(lambda _checked=False, n=name: self._on_filament_type_selected(n))

        self._filament_button = QtWidgets.QToolButton(filament_row)
        self._filament_button.setText(self._defaults.filament_name)
        self._filament_button.setObjectName("FilamentButton")
        self._filament_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self._filament_button.setCursor(QtCore.Qt.PointingHandCursor)
        self._filament_button.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self._filament_button.setMenu(self._filament_type_menu)
        filament_layout.addWidget(self._filament_button, 1)

        self._register_hover_tooltip(self._filament_color_button, "filament_color")
        self._register_hover_tooltip(self._filament_button, "filament_type")

        root.addWidget(filament_row)

    def _build_printer_row(self, root: QtWidgets.QVBoxLayout):
        row = QtWidgets.QFrame(self)
        row.setObjectName("PrinterRow")
        layout = QtWidgets.QHBoxLayout(row)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(6)

        label = QtWidgets.QLabel("Printer", row)
        label.setObjectName("PrinterLabel")
        layout.addWidget(label)

        self._printer_combo = QtWidgets.QComboBox(row)
        self._printer_combo.setObjectName("PrinterCombo")
        self._printer_combo.currentIndexChanged.connect(self._on_printer_changed)
        layout.addWidget(self._printer_combo, 1)

        root.addWidget(row)

    def _build_process_row(self, root: QtWidgets.QVBoxLayout):
        process_row = QtWidgets.QFrame(self)
        process_row.setObjectName("ProcessRow")
        process_layout = QtWidgets.QHBoxLayout(process_row)
        process_layout.setContentsMargins(6, 4, 6, 4)
        process_layout.setSpacing(6)

        label = QtWidgets.QLabel("Process", process_row)
        label.setObjectName("ProcessLabel")
        process_layout.addWidget(label)

        self._scope_group = QtWidgets.QButtonGroup(process_row)
        self._scope_group.setExclusive(True)
        self._scope_buttons = {}
        for name in ("Global", "Objects"):
            btn = QtWidgets.QToolButton(process_row)
            btn.setText(name)
            btn.setCheckable(True)
            btn.setObjectName("SettingsChip")
            btn.setCursor(QtCore.Qt.PointingHandCursor)
            self._scope_group.addButton(btn)
            self._scope_buttons[name.lower()] = btn
            process_layout.addWidget(btn)
        self._scope_buttons["global"].setChecked(True)

        process_layout.addStretch(1)

        advanced_label = QtWidgets.QLabel("Advanced", process_row)
        advanced_label.setObjectName("AdvancedLabel")
        process_layout.addWidget(advanced_label)

        self._advanced_toggle = QtWidgets.QCheckBox(process_row)
        self._advanced_toggle.setObjectName("SettingsToggle")
        self._advanced_toggle.setCursor(QtCore.Qt.PointingHandCursor)
        self._advanced_toggle.setText("")
        self._advanced_toggle.setChecked(True)
        self._advanced_toggle.toggled.connect(self._on_advanced_toggled)
        process_layout.addWidget(self._advanced_toggle)

        root.addWidget(process_row)

    def _build_profile_row(self, root: QtWidgets.QVBoxLayout):
        row = QtWidgets.QFrame(self)
        row.setObjectName("ProfileRow")
        layout = QtWidgets.QHBoxLayout(row)
        layout.setContentsMargins(6, 4, 6, 4)
        layout.setSpacing(6)

        self._profile_combo = QtWidgets.QComboBox(row)
        self._profile_combo.setObjectName("ProfileCombo")
        self._profile_combo.addItem("0.20mm Standard @K1 Max 0.4 nozzle")
        layout.addWidget(self._profile_combo, 1)

        for label in ("Save", "Search"):
            btn = QtWidgets.QToolButton(row)
            btn.setText(label)
            btn.setObjectName("ProfileButton")
            btn.setCursor(QtCore.Qt.PointingHandCursor)
            layout.addWidget(btn)

        self._search_input = QtWidgets.QLineEdit(row)
        self._search_input.setObjectName("SettingsSearch")
        self._search_input.setPlaceholderText("Search settings")
        self._search_input.textChanged.connect(self._apply_search_filter)
        layout.addWidget(self._search_input, 1)

        root.addWidget(row)

    def _build_content(self, root: QtWidgets.QVBoxLayout):
        content = QtWidgets.QHBoxLayout()
        content.setSpacing(6)

        nav = QtWidgets.QFrame(self)
        nav.setObjectName("SettingsNav")
        nav_layout = QtWidgets.QVBoxLayout(nav)
        nav_layout.setContentsMargins(4, 4, 4, 4)
        nav_layout.setSpacing(4)

        self._nav_group = QtWidgets.QButtonGroup(nav)
        self._nav_group.setExclusive(True)
        self._nav_group.buttonClicked.connect(self._on_nav_changed)

        pages = [
            ("quality", "Quality"),
            ("strength", "Strength"),
            ("support", "Support"),
            ("multifilament", "Multifilament"),
            ("others", "Others"),
        ]
        for idx, (key, label) in enumerate(pages):
            btn = QtWidgets.QToolButton(nav)
            btn.setText(label)
            btn.setCheckable(True)
            btn.setObjectName("SettingsNavButton")
            btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
            btn.setCursor(QtCore.Qt.PointingHandCursor)
            self._nav_group.addButton(btn, idx)
            nav_layout.addWidget(btn)
            if idx == 0:
                btn.setChecked(True)

        nav_layout.addStretch(1)
        content.addWidget(nav, 0)

        self._pages_stack = QtWidgets.QStackedWidget(self)
        self._pages_stack.setObjectName("SettingsPages")
        content.addWidget(self._pages_stack, 1)

        self._build_quality_page()
        self._build_strength_page()
        self._build_support_page()
        self._build_multifilament_page()
        self._build_other_page()

        root.addLayout(content, 1)

    def _build_tooltip_defs(self) -> Dict[str, dict]:
        return {
            "filament_color": {
                "title": "Filament color",
                "body": "Pick the color used for previews and filament presets.",
                "param": "Parameter name: filament_color",
                "image": "filament_color",
            },
            "filament_type": {
                "title": "Filament type",
                "body": "Select the material preset (PLA, PETG, ABS, etc.).",
                "param": "Parameter name: filament_name",
                "image": "filament_type",
            },
            "layer_height": {
                "title": "Layer height",
                "body": ("This is the height for each layer. Smaller layer heights give "
                         "greater accuracy but longer printing time."),
                "param": "Parameter name: layer_height",
                "image": "layer_height",
            },
            "first_layer_height": {
                "title": "First layer height",
                "body": ("This is the height of the first layer. Making the first layer "
                         "height thicker can improve build plate adhesion."),
                "param": "Parameter name: first_layer_height",
                "image": "first_layer_height",
            },
            "seam_position": {
                "title": "Seam position",
                "body": ("This is the starting position for each part of the outer wall."),
                "param": "Parameter name: seam_position",
                "image": "seam_position",
            },
            "line_width_default": {
                "title": "Default",
                "body": ("Default line width if other line widths are set to 0."),
                "param": "Parameter name: line_width",
                "image": "line_width",
            },
            "line_width_first_layer": {
                "title": "First layer",
                "body": ("Line width for initial layer."),
                "param": "Parameter name: initial_layer_line_width",
                "image": "line_width",
            },
            "line_width_outer_wall": {
                "title": "Outer wall",
                "body": ("Line width for outer wall."),
                "param": "Parameter name: outer_wall_line_width",
                "image": "line_width",
            },
            "line_width_inner_wall": {
                "title": "Inner wall",
                "body": ("Line width for inner wall."),
                "param": "Parameter name: inner_wall_line_width",
                "image": "line_width",
            },
            "line_width_top_surface": {
                "title": "Top surface",
                "body": ("Line width for top surfaces."),
                "param": "Parameter name: top_surface_line_width",
                "image": "line_width",
            },
            "line_width_sparse_infill": {
                "title": "Sparse infill",
                "body": ("Line width for sparse infill."),
                "param": "Parameter name: sparse_infill_line_width",
                "image": "line_width",
            },
            "line_width_internal_solid": {
                "title": "Internal solid infill",
                "body": ("Line width for internal solid infill."),
                "param": "Parameter name: internal_solid_infill_line_width",
                "image": "line_width",
            },
            "line_width_support": {
                "title": "Support",
                "body": ("Line width for support."),
                "param": "Parameter name: support_line_width",
                "image": "line_width",
            },
            "staggered_inner_seams": {
                "title": "Staggered inner seams",
                "body": ("Offset inner seams to reduce alignment artifacts."),
                "param": "Parameter name: staggered_inner_seams",
                "image": "seam_position",
            },
            "seam_gap": {
                "title": "Seam gap",
                "body": ("Skip a small portion of the seam to reduce visibility."),
                "param": "Parameter name: seam_gap",
                "image": "seam_position",
            },
            "scarf_joint_seam": {
                "title": "Scarf joint seam (beta)",
                "body": ("Use scarf joint to minimize seam visibility."),
                "param": "Parameter name: seam_slope_type",
                "image": "seam_position",
            },
            "wipe_use_base_speed": {
                "title": "Use base wipe speed",
                "body": ("Use the base print speed for wipe moves."),
                "param": "Parameter name: wipe_use_base_speed",
                "image": "seam_position",
            },
            "wipe_speed": {
                "title": "Wipe speed",
                "body": ("Wipe speed as a percentage of the base speed."),
                "param": "Parameter name: wipe_speed",
                "image": "seam_position",
            },
            "wipe_on_loops": {
                "title": "Wipe on loops",
                "body": ("Add a short wipe before leaving closed loops."),
                "param": "Parameter name: wipe_on_loops",
                "image": "seam_position",
            },
            "wipe_before_external_loop": {
                "title": "Wipe before external loop",
                "body": ("Wipe before starting outer walls."),
                "param": "Parameter name: wipe_before_external_loop",
                "image": "seam_position",
            },
            "slice_gap_closing_radius": {
                "title": "Slice gap closing radius",
                "body": ("Close tiny gaps in sliced contours."),
                "param": "Parameter name: slice_gap_closing_radius",
                "image": "precision",
            },
            "resolution": {
                "title": "Resolution",
                "body": ("Simplification tolerance for slice polygons."),
                "param": "Parameter name: resolution",
                "image": "precision",
            },
            "arc_fitting": {
                "title": "Arc fitting",
                "body": ("Enable arcs for supported firmware."),
                "param": "Parameter name: enable_arc_fitting",
                "image": "precision",
            },
            "xy_hole_compensation": {
                "title": "X-Y hole compensation",
                "body": ("Adjust holes to improve fit."),
                "param": "Parameter name: xy_hole_compensation",
                "image": "precision",
            },
            "xy_contour_compensation": {
                "title": "X-Y contour compensation",
                "body": ("Adjust outer contours to tweak dimensions."),
                "param": "Parameter name: xy_contour_compensation",
                "image": "precision",
            },
            "elephant_foot_compensation": {
                "title": "Elephant foot compensation",
                "body": ("Shrink lower layers to reduce bulging."),
                "param": "Parameter name: elephant_foot_compensation",
                "image": "precision",
            },
            "elephant_foot_layers": {
                "title": "Elephant foot compensation layers",
                "body": ("Number of layers to apply elephant foot compensation."),
                "param": "Parameter name: elephant_foot_compensation_layers",
                "image": "precision",
            },
            "convert_holes_to_polyholes": {
                "title": "Convert holes to polyholes",
                "body": ("Approximate circular holes with polygons."),
                "param": "Parameter name: hole_to_polyhole",
                "image": "precision",
            },
            "precise_z_height": {
                "title": "Precise Z height",
                "body": ("Adjust final layers to match model height."),
                "param": "Parameter name: precise_z_height",
                "image": "precision",
            },
            "ironing_type": {
                "title": "Ironing type",
                "body": ("Control which layers are ironed."),
                "param": "Parameter name: ironing_type",
                "image": "ironing_type",
            },
            "wall_generator": {
                "title": "Wall generator",
                "body": ("Select the wall generation method."),
                "param": "Parameter name: wall_generator",
                "image": "wall_generator",
            },
            "wall_transition_angle": {
                "title": "Wall transitioning threshold angle",
                "body": ("Angle threshold for wall transitions."),
                "param": "Parameter name: wall_transition_angle",
                "image": "wall_generator",
            },
            "wall_transition_filter_margin": {
                "title": "Wall transitioning filter margin",
                "body": ("Filter margin for wall transitions."),
                "param": "Parameter name: wall_transition_filter_deviation",
                "image": "wall_generator",
            },
            "wall_transition_length": {
                "title": "Wall transition length",
                "body": ("Transition length percentage."),
                "param": "Parameter name: wall_transition_length",
                "image": "wall_generator",
            },
            "wall_distribution_count": {
                "title": "Wall distribution count",
                "body": ("Number of walls used for width distribution."),
                "param": "Parameter name: wall_distribution_count",
                "image": "wall_generator",
            },
            "first_layer_min_wall_width": {
                "title": "First layer minimum wall width",
                "body": ("Minimum wall width for the first layer."),
                "param": "Parameter name: initial_layer_min_bead_width",
                "image": "wall_generator",
            },
            "min_wall_width": {
                "title": "Minimum wall width",
                "body": ("Minimum wall width for thin features."),
                "param": "Parameter name: min_bead_width",
                "image": "wall_generator",
            },
            "min_feature_size": {
                "title": "Minimum feature size",
                "body": ("Minimum feature size percentage."),
                "param": "Parameter name: min_feature_size",
                "image": "wall_generator",
            },
            "min_wall_length": {
                "title": "Minimum wall length",
                "body": ("Discard walls shorter than this."),
                "param": "Parameter name: min_wall_length",
                "image": "wall_generator",
            },
            "wall_printing_order": {
                "title": "Walls printing order",
                "body": ("Order for printing wall perimeters."),
                "param": "Parameter name: wall_sequence",
                "image": "wall_sequence",
            },
            "print_infill_first": {
                "title": "Print infill first",
                "body": ("Print infill before walls."),
                "param": "Parameter name: is_infill_first",
                "image": "wall_sequence",
            },
            "wall_loop_direction": {
                "title": "Wall loop direction",
                "body": ("Direction for perimeter loops."),
                "param": "Parameter name: wall_direction",
                "image": "wall_sequence",
            },
            "top_surface_flow_ratio": {
                "title": "Top surface flow ratio",
                "body": ("Extrusion multiplier for top surfaces."),
                "param": "Parameter name: top_solid_infill_flow_ratio",
                "image": "wall_sequence",
            },
            "bottom_surface_flow_ratio": {
                "title": "Bottom surface flow ratio",
                "body": ("Extrusion multiplier for bottom surfaces."),
                "param": "Parameter name: bottom_solid_infill_flow_ratio",
                "image": "wall_sequence",
            },
            "one_wall_threshold": {
                "title": "One wall threshold",
                "body": ("Threshold for using a single wall on small surfaces."),
                "param": "Parameter name: min_width_top_surface",
                "image": "wall_sequence",
            },
            "avoid_crossing_walls": {
                "title": "Avoid crossing walls",
                "body": ("Keep travel moves inside perimeters when possible."),
                "param": "Parameter name: reduce_crossing_wall",
                "image": "wall_sequence",
            },
            "small_area_flow_compensation": {
                "title": "Small area flow compensation (beta)",
                "body": ("Reduce flow on tiny segments."),
                "param": "Parameter name: small_area_infill_flow_compensation",
                "image": "wall_sequence",
            },
            "smooth_wall_speed_z": {
                "title": "Smoothing wall speed along Z (experimental)",
                "body": ("Smooth wall speeds across variable layer heights."),
                "param": "Parameter name: z_direction_outwall_speed_continuous",
                "image": "wall_sequence",
            },
            "bridge_flow_ratio": {
                "title": "Bridge flow ratio",
                "body": ("Extrusion multiplier for bridge lines."),
                "param": "Parameter name: bridge_flow",
                "image": "bridge_flow",
            },
            "internal_bridge_flow_ratio": {
                "title": "Internal bridge flow ratio",
                "body": ("Extrusion multiplier for internal bridges."),
                "param": "Parameter name: internal_bridge_flow",
                "image": "bridge_flow",
            },
            "bridge_density": {
                "title": "Bridge density",
                "body": ("Density of bridge infill."),
                "param": "Parameter name: bridge_density",
                "image": "bridge_flow",
            },
            "thick_bridges": {
                "title": "Thick bridges",
                "body": ("Use thicker extrusion for bridges."),
                "param": "Parameter name: thick_bridges",
                "image": "bridge_flow",
            },
            "thick_internal_bridges": {
                "title": "Thick internal bridges",
                "body": ("Use thicker extrusion for internal bridges."),
                "param": "Parameter name: thick_internal_bridges",
                "image": "bridge_flow",
            },
            "bridge_filter_mode": {
                "title": "Don't filter out small internal bridges (beta)",
                "body": ("Control filtering for small internal bridges."),
                "param": "Parameter name: dont_filter_internal_bridges",
                "image": "bridge_flow",
            },
            "bridge_counterbore_holes": {
                "title": "Bridge counterbore holes",
                "body": ("Create bridges for counterbore holes."),
                "param": "Parameter name: counterbore_hole_bridging",
                "image": "bridge_flow",
            },
            "detect_overhang_walls": {
                "title": "Detect overhang walls",
                "body": ("Detect walls that exceed the overhang angle."),
                "param": "Parameter name: detect_overhang_wall",
                "image": "overhang",
            },
            "make_overhangs_printable": {
                "title": "Make overhangs printable",
                "body": ("Adjust slicing to improve overhang printability."),
                "param": "Parameter name: make_overhang_printable",
                "image": "overhang",
            },
            "extra_perimeters_on_overhangs": {
                "title": "Extra perimeters on overhangs",
                "body": ("Add extra perimeters on overhang layers."),
                "param": "Parameter name: extra_perimeters_on_overhangs",
                "image": "overhang",
            },
            "reverse_overhang_on_odd": {
                "title": "Reverse on odd",
                "body": ("Reverse wall direction on odd overhang layers."),
                "param": "Parameter name: overhang_reverse",
                "image": "overhang",
            },
            "overhang_optimization": {
                "title": "Overhang optimization (beta)",
                "body": ("Use adaptive settings for overhangs."),
                "param": "Parameter name: overhang_optimization",
                "image": "overhang",
            },
            "precise_wall": {
                "title": "Precise wall",
                "body": ("Improve shell precision by adjusting outer wall spacing. This also "
                         "improves layer consistency. Note: This setting will only take "
                         "effect if the wall sequence is configured to Inner-Outer."),
                "param": "Parameter name: precise_wall",
                "image": "precise_wall",
            },
            "only_one_wall_top": {
                "title": "Only one wall on top surfaces",
                "body": ("Use only one wall on flat top surfaces, to give more space "
                         "to the top infill pattern."),
                "param": "Parameter name: only_one_wall_top",
                "image": "one_wall_top",
            },
            "only_one_wall_first": {
                "title": "Only one wall on first layer",
                "body": ("Use only one wall on first layer, to give more space "
                         "to the bottom infill pattern."),
                "param": "Parameter name: only_one_wall_first_layer",
                "image": "one_wall_first",
            },
        }

    def _register_hover_tooltip(self, widget: QtWidgets.QWidget, key: str):
        data = self._tooltip_defs.get(key)
        if data is None:
            return
        widget.installEventFilter(self)
        self._hover_tooltips[widget] = data

    def eventFilter(self, a0: QtCore.QObject, a1: QtCore.QEvent):
        if a0 in self._hover_tooltips:
            if a1.type() == QtCore.QEvent.Enter:
                self._tooltip_hide_timer.stop()
                self._show_tooltip(a0, self._hover_tooltips[a0])
            elif a1.type() == QtCore.QEvent.Leave:
                self._tooltip_hide_timer.start(120)
        return super().eventFilter(a0, a1)

    def _show_tooltip(self, obj: QtCore.QObject, data: dict):
        if not isinstance(obj, QtWidgets.QWidget):
            return
        accent = QtGui.QColor(theme_css("topbar_accent"))
        if data.get("image") == "filament_color":
            accent = QtGui.QColor(self._filament_color)
        self._tooltip.set_content(
            data.get("title", ""),
            data.get("body", ""),
            data.get("param", ""),
            data.get("image", ""),
            accent,
        )
        if self._tooltip.layout() is not None:
            self._tooltip.layout().activate()
        tip_size = self._tooltip.sizeHint()
        self._tooltip.resize(tip_size)

        anchor = obj.mapToGlobal(QtCore.QPoint(0, obj.height() // 2))
        panel_pos = self.mapToGlobal(QtCore.QPoint(0, 0))
        margin = 12

        screen = QtGui.QGuiApplication.screenAt(anchor)
        if screen is None:
            screen = QtGui.QGuiApplication.primaryScreen()
        geom = screen.availableGeometry() if screen is not None else QtCore.QRect(0, 0, 1920, 1080)

        tip_size = self._tooltip.size()
        x_left = panel_pos.x() - tip_size.width() - margin
        x_right = panel_pos.x() + self.width() + margin
        if x_left >= geom.left() + margin:
            x = x_left
        else:
            x = min(x_right, geom.right() - tip_size.width() - margin)

        y = anchor.y() - tip_size.height() // 2
        y = max(geom.top() + margin, min(y, geom.bottom() - tip_size.height() - margin))

        self._tooltip.move(int(x), int(y))
        self._tooltip.show()
        self._tooltip.raise_()

    def _hide_tooltip(self):
        if self._tooltip.isVisible():
            self._tooltip.hide()

    def _build_page(self, key: str) -> QtWidgets.QVBoxLayout:
        scroll = QtWidgets.QScrollArea(self)
        scroll.setObjectName("SettingsScroll")
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        container = QtWidgets.QWidget(scroll)
        container.setObjectName("SettingsPage")
        layout = QtWidgets.QVBoxLayout(container)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(10)
        layout.addStretch(1)
        scroll.setWidget(container)

        self._page_keys.append(key)
        self._page_widgets[key] = scroll
        self._search_rows[key] = []
        self._pages_stack.addWidget(scroll)
        return layout

    def _section(self, title: str, advanced: bool = False) -> Tuple[QtWidgets.QFrame, QtWidgets.QVBoxLayout]:
        section = QtWidgets.QFrame(self)
        section.setObjectName("SettingsSection")
        section.setProperty("advanced", bool(advanced))
        layout = QtWidgets.QVBoxLayout(section)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(6)

        header_row = QtWidgets.QHBoxLayout()
        header_row.setSpacing(6)
        title_label = QtWidgets.QLabel(title, section)
        title_label.setObjectName("SettingsSectionTitle")
        header_row.addWidget(title_label)
        header_row.addStretch(1)
        header_line = QtWidgets.QFrame(section)
        header_line.setFrameShape(QtWidgets.QFrame.HLine)
        header_line.setObjectName("SettingsSectionLine")
        header_row.addWidget(header_line)
        layout.addLayout(header_row)

        return section, layout

    def _add_row(self,
                 page_key: str,
                 section: QtWidgets.QFrame,
                 layout: QtWidgets.QVBoxLayout,
                 label_text: str,
                 control: QtWidgets.QWidget,
                 tooltip: str | None = None,
                 use_native_tooltip: bool = True,
                 advanced: bool | None = None):
        row = QtWidgets.QWidget(section)
        row_layout = QtWidgets.QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(6)

        label = QtWidgets.QLabel(label_text, row)
        label.setObjectName("SettingsLabel")
        if tooltip and use_native_tooltip:
            label.setToolTip(tooltip)
        row_layout.addWidget(label, 1)
        row_layout.addStretch(1)
        row_layout.addWidget(control, 0)
        layout.addWidget(row)

        is_advanced = bool(advanced) if advanced is not None else bool(section.property("advanced"))
        if is_advanced:
            self._advanced_rows.add(row)

        search_text = f"{label_text} {tooltip or ''}".strip().lower()
        self._search_rows[page_key].append((section, row, search_text))
        return label

    def _make_double_spin(self, value: float, minimum: float, maximum: float,
                          step: float, suffix: str = "") -> QtWidgets.QDoubleSpinBox:
        spin = QtWidgets.QDoubleSpinBox(self)
        spin.setRange(minimum, maximum)
        spin.setSingleStep(step)
        spin.setValue(value)
        spin.setDecimals(3)
        if suffix:
            spin.setSuffix(f" {suffix}")
        spin.setObjectName("SettingsSpin")
        spin.setFixedWidth(110)
        return spin

    def _make_int_spin(self, value: int, minimum: int, maximum: int,
                       step: int = 1, suffix: str = "") -> QtWidgets.QSpinBox:
        spin = QtWidgets.QSpinBox(self)
        spin.setRange(minimum, maximum)
        spin.setSingleStep(step)
        spin.setValue(value)
        if suffix:
            spin.setSuffix(f" {suffix}")
        spin.setObjectName("SettingsSpin")
        spin.setFixedWidth(110)
        return spin

    def _make_combo(self, items: List[Tuple[str, str]]) -> QtWidgets.QComboBox:
        combo = QtWidgets.QComboBox(self)
        combo.setObjectName("SettingsCombo")
        for label, value in items:
            combo.addItem(label, value)
        combo.setFixedWidth(150)
        return combo

    def _build_quality_page(self):
        layout = self._build_page("quality")

        section, section_layout = self._section("Layer height")
        self.layer_height_spin = self._make_double_spin(
            self._defaults.layer_height, 0.05, 1.0, 0.01, "mm"
        )
        self._label_layer_height = self._add_row(
            "quality",
            section,
            section_layout,
            "Layer height",
            self.layer_height_spin,
            "Height of each layer.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_layer_height, "layer_height")
        self._register_hover_tooltip(self.layer_height_spin, "layer_height")
        self.first_layer_height_spin = self._make_double_spin(
            self._defaults.first_layer_height, 0.05, 1.0, 0.01, "mm"
        )
        self._label_first_layer_height = self._add_row(
            "quality",
            section,
            section_layout,
            "First layer height",
            self.first_layer_height_spin,
            "Height of the first layer.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_first_layer_height, "first_layer_height")
        self._register_hover_tooltip(self.first_layer_height_spin, "first_layer_height")
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Line width")
        self.line_width_default_spin = self._make_double_spin(
            self._defaults.extrusion_width, 0.1, 2.0, 0.01, "mm"
        )
        self._label_line_width_default = self._add_row(
            "quality", section, section_layout, "Default",
            self.line_width_default_spin, "Default extrusion width.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_line_width_default, "line_width_default")
        self._register_hover_tooltip(self.line_width_default_spin, "line_width_default")
        self.line_width_first_layer_spin = self._make_double_spin(
            self._defaults.first_layer_line_width, 0.1, 3.0, 0.01, "mm"
        )
        self._label_line_width_first_layer = self._add_row(
            "quality", section, section_layout, "First layer",
            self.line_width_first_layer_spin, "Extrusion width on the first layer.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_line_width_first_layer, "line_width_first_layer")
        self._register_hover_tooltip(self.line_width_first_layer_spin, "line_width_first_layer")
        self.line_width_outer_wall_spin = self._make_double_spin(
            self._defaults.outer_wall_line_width, 0.1, 2.0, 0.01, "mm"
        )
        self._label_line_width_outer_wall = self._add_row(
            "quality", section, section_layout, "Outer wall",
            self.line_width_outer_wall_spin, "Extrusion width for outer walls.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_line_width_outer_wall, "line_width_outer_wall")
        self._register_hover_tooltip(self.line_width_outer_wall_spin, "line_width_outer_wall")
        self.line_width_inner_wall_spin = self._make_double_spin(
            self._defaults.inner_wall_line_width, 0.1, 2.0, 0.01, "mm"
        )
        self._label_line_width_inner_wall = self._add_row(
            "quality", section, section_layout, "Inner wall",
            self.line_width_inner_wall_spin, "Extrusion width for inner walls.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_line_width_inner_wall, "line_width_inner_wall")
        self._register_hover_tooltip(self.line_width_inner_wall_spin, "line_width_inner_wall")
        self.line_width_top_surface_spin = self._make_double_spin(
            self._defaults.top_surface_line_width, 0.1, 2.0, 0.01, "mm"
        )
        self._label_line_width_top_surface = self._add_row(
            "quality", section, section_layout, "Top surface",
            self.line_width_top_surface_spin, "Extrusion width for top surfaces.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_line_width_top_surface, "line_width_top_surface")
        self._register_hover_tooltip(self.line_width_top_surface_spin, "line_width_top_surface")
        self.line_width_sparse_infill_spin = self._make_double_spin(
            self._defaults.sparse_infill_line_width, 0.1, 2.0, 0.01, "mm"
        )
        self._label_line_width_sparse_infill = self._add_row(
            "quality", section, section_layout, "Sparse infill",
            self.line_width_sparse_infill_spin, "Extrusion width for sparse infill.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_line_width_sparse_infill, "line_width_sparse_infill")
        self._register_hover_tooltip(self.line_width_sparse_infill_spin, "line_width_sparse_infill")
        self.line_width_internal_solid_spin = self._make_double_spin(
            self._defaults.internal_solid_infill_line_width, 0.1, 2.0, 0.01, "mm"
        )
        self._label_line_width_internal_solid = self._add_row(
            "quality", section, section_layout, "Internal solid infill",
            self.line_width_internal_solid_spin, "Extrusion width for internal solid infill.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_line_width_internal_solid,
                                     "line_width_internal_solid")
        self._register_hover_tooltip(self.line_width_internal_solid_spin,
                                     "line_width_internal_solid")
        self.line_width_support_spin = self._make_double_spin(
            self._defaults.support_line_width, 0.1, 2.0, 0.01, "mm"
        )
        self._label_line_width_support = self._add_row(
            "quality", section, section_layout, "Support",
            self.line_width_support_spin, "Extrusion width for supports.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_line_width_support, "line_width_support")
        self._register_hover_tooltip(self.line_width_support_spin, "line_width_support")
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Seam", advanced=True)
        self.seam_position_combo = self._make_combo(
            [
                ("Nearest", "nearest"),
                ("Aligned", "aligned"),
                ("Back", "back"),
                ("Random", "random"),
                ("Assemble", "assemble"),
            ]
        )
        self._set_combo_value(self.seam_position_combo, self._defaults.seam_position)
        self._label_seam_position = self._add_row(
            "quality",
            section,
            section_layout,
            "Seam position",
            self.seam_position_combo,
            "Starting position for each outer wall loop.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_seam_position, "seam_position")
        self._register_hover_tooltip(self.seam_position_combo, "seam_position")
        self.staggered_inner_seams_check = QtWidgets.QCheckBox(section)
        self.staggered_inner_seams_check.setObjectName("SettingsCheck")
        self.staggered_inner_seams_check.setChecked(bool(self._defaults.staggered_inner_seams))
        self._label_staggered_inner_seams = self._add_row(
            "quality", section, section_layout, "Staggered inner seams",
            self.staggered_inner_seams_check, "Offset inner seams to reduce alignment.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_staggered_inner_seams, "staggered_inner_seams")
        self._register_hover_tooltip(self.staggered_inner_seams_check, "staggered_inner_seams")
        self.seam_gap_spin = self._make_double_spin(self._defaults.seam_gap, 0.0, 100.0, 1.0, "%")
        self._label_seam_gap = self._add_row(
            "quality", section, section_layout, "Seam gap",
            self.seam_gap_spin, "Skip a small percentage of the seam to reduce blobs.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_seam_gap, "seam_gap")
        self._register_hover_tooltip(self.seam_gap_spin, "seam_gap")
        self.scarf_joint_seam_combo = self._make_combo(
            [
                ("None", "none"),
                ("Contour", "contour"),
                ("Contour and hole", "contour_hole"),
            ]
        )
        self._set_combo_value(self.scarf_joint_seam_combo, self._defaults.scarf_joint_seam)
        self._label_scarf_joint_seam = self._add_row(
            "quality", section, section_layout, "Scarf joint seam (beta)",
            self.scarf_joint_seam_combo, "Apply seam shaping on contours/holes.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_scarf_joint_seam, "scarf_joint_seam")
        self._register_hover_tooltip(self.scarf_joint_seam_combo, "scarf_joint_seam")
        self.wipe_use_base_speed_check = QtWidgets.QCheckBox(section)
        self.wipe_use_base_speed_check.setObjectName("SettingsCheck")
        self.wipe_use_base_speed_check.setChecked(bool(self._defaults.wipe_use_base_speed))
        self._label_wipe_use_base_speed = self._add_row(
            "quality", section, section_layout, "Use base wipe speed",
            self.wipe_use_base_speed_check, "Use the base print speed for wipe moves.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_wipe_use_base_speed, "wipe_use_base_speed")
        self._register_hover_tooltip(self.wipe_use_base_speed_check, "wipe_use_base_speed")
        self.wipe_speed_spin = self._make_double_spin(
            self._defaults.wipe_speed_percent, 0.0, 200.0, 5.0, "%"
        )
        self._label_wipe_speed = self._add_row(
            "quality", section, section_layout, "Wipe speed",
            self.wipe_speed_spin, "Wipe speed as a percent of the base speed.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_wipe_speed, "wipe_speed")
        self._register_hover_tooltip(self.wipe_speed_spin, "wipe_speed")
        self.wipe_on_loops_check = QtWidgets.QCheckBox(section)
        self.wipe_on_loops_check.setObjectName("SettingsCheck")
        self.wipe_on_loops_check.setChecked(bool(self._defaults.wipe_on_loops))
        self._label_wipe_on_loops = self._add_row(
            "quality", section, section_layout, "Wipe on loops",
            self.wipe_on_loops_check, "Add a short wipe at loop ends.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_wipe_on_loops, "wipe_on_loops")
        self._register_hover_tooltip(self.wipe_on_loops_check, "wipe_on_loops")
        self.wipe_before_external_loop_check = QtWidgets.QCheckBox(section)
        self.wipe_before_external_loop_check.setObjectName("SettingsCheck")
        self.wipe_before_external_loop_check.setChecked(bool(self._defaults.wipe_before_external_loop))
        self._label_wipe_before_external = self._add_row(
            "quality", section, section_layout, "Wipe before external loop",
            self.wipe_before_external_loop_check,
            "Wipe before starting the outer wall.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_wipe_before_external, "wipe_before_external_loop")
        self._register_hover_tooltip(self.wipe_before_external_loop_check,
                                     "wipe_before_external_loop")
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Precision", advanced=True)
        self.precise_wall_check = QtWidgets.QCheckBox(section)
        self.precise_wall_check.setObjectName("SettingsCheck")
        self.precise_wall_check.setChecked(bool(self._defaults.precise_wall))
        self._label_precise_wall = self._add_row(
            "quality",
            section,
            section_layout,
            "Precise wall",
            self.precise_wall_check,
            "Adjust outer wall spacing for better accuracy.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_precise_wall, "precise_wall")
        self._register_hover_tooltip(self.precise_wall_check, "precise_wall")
        self.slice_gap_closing_radius_spin = self._make_double_spin(
            self._defaults.slice_gap_closing_radius, 0.0, 1.0, 0.001, "mm"
        )
        self._label_slice_gap_closing = self._add_row(
            "quality", section, section_layout, "Slice gap closing radius",
            self.slice_gap_closing_radius_spin,
            "Close tiny gaps during slicing.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_slice_gap_closing, "slice_gap_closing_radius")
        self._register_hover_tooltip(self.slice_gap_closing_radius_spin,
                                     "slice_gap_closing_radius")
        self.resolution_spin = self._make_double_spin(
            self._defaults.resolution, 0.0, 1.0, 0.001, "mm"
        )
        self._label_resolution = self._add_row(
            "quality", section, section_layout, "Resolution",
            self.resolution_spin,
            "Simplification tolerance for sliced polygons.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_resolution, "resolution")
        self._register_hover_tooltip(self.resolution_spin, "resolution")
        self.arc_fitting_check = QtWidgets.QCheckBox(section)
        self.arc_fitting_check.setObjectName("SettingsCheck")
        self.arc_fitting_check.setChecked(bool(self._defaults.arc_fitting))
        self._label_arc_fitting = self._add_row(
            "quality", section, section_layout, "Arc fitting",
            self.arc_fitting_check, "Use arcs for compatible loops.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_arc_fitting, "arc_fitting")
        self._register_hover_tooltip(self.arc_fitting_check, "arc_fitting")
        self.xy_hole_compensation_spin = self._make_double_spin(
            self._defaults.xy_hole_compensation, -1.0, 1.0, 0.01, "mm"
        )
        self._label_xy_hole_comp = self._add_row(
            "quality", section, section_layout, "X-Y hole compensation",
            self.xy_hole_compensation_spin,
            "Offset circular holes to improve fit.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_xy_hole_comp, "xy_hole_compensation")
        self._register_hover_tooltip(self.xy_hole_compensation_spin, "xy_hole_compensation")
        self.xy_contour_compensation_spin = self._make_double_spin(
            self._defaults.xy_contour_compensation, -1.0, 1.0, 0.01, "mm"
        )
        self._label_xy_contour_comp = self._add_row(
            "quality", section, section_layout, "X-Y contour compensation",
            self.xy_contour_compensation_spin,
            "Offset model contours to tweak dimensions.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_xy_contour_comp, "xy_contour_compensation")
        self._register_hover_tooltip(self.xy_contour_compensation_spin,
                                     "xy_contour_compensation")
        self.elephant_foot_compensation_spin = self._make_double_spin(
            self._defaults.elephant_foot_compensation, 0.0, 2.0, 0.01, "mm"
        )
        self._label_elephant_foot = self._add_row(
            "quality", section, section_layout, "Elephant foot compensation",
            self.elephant_foot_compensation_spin,
            "Shrink lower layers to reduce bulging.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_elephant_foot, "elephant_foot_compensation")
        self._register_hover_tooltip(self.elephant_foot_compensation_spin,
                                     "elephant_foot_compensation")
        self.elephant_foot_layers_spin = self._make_int_spin(
            self._defaults.elephant_foot_compensation_layers, 0, 10, suffix="layers"
        )
        self._label_elephant_foot_layers = self._add_row(
            "quality", section, section_layout, "Elephant foot compensation layers",
            self.elephant_foot_layers_spin,
            "Number of layers to apply elephant foot compensation.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_elephant_foot_layers, "elephant_foot_layers")
        self._register_hover_tooltip(self.elephant_foot_layers_spin, "elephant_foot_layers")
        self.convert_holes_to_polyholes_check = QtWidgets.QCheckBox(section)
        self.convert_holes_to_polyholes_check.setObjectName("SettingsCheck")
        self.convert_holes_to_polyholes_check.setChecked(bool(self._defaults.convert_holes_to_polyholes))
        self._label_convert_holes = self._add_row(
            "quality", section, section_layout, "Convert holes to polyholes",
            self.convert_holes_to_polyholes_check,
            "Approximate circular holes with polygons.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_convert_holes, "convert_holes_to_polyholes")
        self._register_hover_tooltip(self.convert_holes_to_polyholes_check,
                                     "convert_holes_to_polyholes")
        self.precise_z_height_check = QtWidgets.QCheckBox(section)
        self.precise_z_height_check.setObjectName("SettingsCheck")
        self.precise_z_height_check.setChecked(bool(self._defaults.precise_z_height))
        self._label_precise_z_height = self._add_row(
            "quality", section, section_layout, "Precise Z height",
            self.precise_z_height_check,
            "Adjust final layers to match the exact model height.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_precise_z_height, "precise_z_height")
        self._register_hover_tooltip(self.precise_z_height_check, "precise_z_height")
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Ironing", advanced=True)
        self.ironing_type_combo = self._make_combo(
            [
                ("No ironing", "no_ironing"),
                ("All top surfaces", "all_top_surfaces"),
                ("Topmost surface only", "topmost_surface_only"),
                ("All solid layers", "all_solid_layers"),
            ]
        )
        self._set_combo_value(self.ironing_type_combo, self._defaults.ironing_type)
        self._label_ironing_type = self._add_row(
            "quality", section, section_layout, "Ironing type",
            self.ironing_type_combo, "Control which layers are ironed.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_ironing_type, "ironing_type")
        self._register_hover_tooltip(self.ironing_type_combo, "ironing_type")
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Wall generator", advanced=True)
        self.wall_generator_combo = self._make_combo(
            [
                ("Classic", "classic"),
                ("Arachne", "arachne"),
            ]
        )
        self._set_combo_value(self.wall_generator_combo, self._defaults.wall_generator)
        self._label_wall_generator = self._add_row(
            "quality", section, section_layout, "Wall generator",
            self.wall_generator_combo, "Select the wall generation method.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_wall_generator, "wall_generator")
        self._register_hover_tooltip(self.wall_generator_combo, "wall_generator")
        self.wall_transition_angle_spin = self._make_double_spin(
            self._defaults.wall_transition_angle, 0.0, 90.0, 1.0, "deg"
        )
        self._label_wall_transition_angle = self._add_row(
            "quality", section, section_layout, "Wall transitioning threshold angle",
            self.wall_transition_angle_spin, "Angle threshold for wall transitions.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_wall_transition_angle, "wall_transition_angle")
        self._register_hover_tooltip(self.wall_transition_angle_spin, "wall_transition_angle")
        self.wall_transition_filter_margin_spin = self._make_double_spin(
            self._defaults.wall_transition_filter_margin, 0.0, 200.0, 1.0, "%"
        )
        self._label_wall_transition_filter = self._add_row(
            "quality", section, section_layout, "Wall transitioning filter margin",
            self.wall_transition_filter_margin_spin, "Filter margin for wall transitions.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_wall_transition_filter,
                                     "wall_transition_filter_margin")
        self._register_hover_tooltip(self.wall_transition_filter_margin_spin,
                                     "wall_transition_filter_margin")
        self.wall_transition_length_spin = self._make_double_spin(
            self._defaults.wall_transition_length, 0.0, 500.0, 1.0, "%"
        )
        self._label_wall_transition_length = self._add_row(
            "quality", section, section_layout, "Wall transition length",
            self.wall_transition_length_spin, "Transition length percentage.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_wall_transition_length, "wall_transition_length")
        self._register_hover_tooltip(self.wall_transition_length_spin, "wall_transition_length")
        self.wall_distribution_count_spin = self._make_int_spin(
            self._defaults.wall_distribution_count, 1, 10
        )
        self._label_wall_distribution_count = self._add_row(
            "quality", section, section_layout, "Wall distribution count",
            self.wall_distribution_count_spin, "Number of walls for distribution.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_wall_distribution_count, "wall_distribution_count")
        self._register_hover_tooltip(self.wall_distribution_count_spin, "wall_distribution_count")
        self.first_layer_min_wall_width_spin = self._make_double_spin(
            self._defaults.first_layer_min_wall_width, 10.0, 400.0, 1.0, "%"
        )
        self._label_first_layer_min_wall = self._add_row(
            "quality", section, section_layout, "First layer minimum wall width",
            self.first_layer_min_wall_width_spin, "Minimum wall width on the first layer.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_first_layer_min_wall,
                                     "first_layer_min_wall_width")
        self._register_hover_tooltip(self.first_layer_min_wall_width_spin,
                                     "first_layer_min_wall_width")
        self.min_wall_width_spin = self._make_double_spin(
            self._defaults.min_wall_width, 10.0, 400.0, 1.0, "%"
        )
        self._label_min_wall_width = self._add_row(
            "quality", section, section_layout, "Minimum wall width",
            self.min_wall_width_spin, "Minimum wall width for thin features.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_min_wall_width, "min_wall_width")
        self._register_hover_tooltip(self.min_wall_width_spin, "min_wall_width")
        self.min_feature_size_spin = self._make_double_spin(
            self._defaults.min_feature_size, 10.0, 400.0, 1.0, "%"
        )
        self._label_min_feature_size = self._add_row(
            "quality", section, section_layout, "Minimum feature size",
            self.min_feature_size_spin, "Minimum feature size percentage.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_min_feature_size, "min_feature_size")
        self._register_hover_tooltip(self.min_feature_size_spin, "min_feature_size")
        self.min_wall_length_spin = self._make_double_spin(
            self._defaults.min_wall_length, 0.0, 5.0, 0.1, "mm"
        )
        self._label_min_wall_length = self._add_row(
            "quality", section, section_layout, "Minimum wall length",
            self.min_wall_length_spin, "Discard walls shorter than this.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_min_wall_length, "min_wall_length")
        self._register_hover_tooltip(self.min_wall_length_spin, "min_wall_length")
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Walls and surfaces", advanced=True)
        self.wall_printing_order_combo = self._make_combo(
            [
                ("Inner/Outer", "inner_outer"),
                ("Outer/Inner", "outer_inner"),
                ("Inner/Outer/Inner", "inner_outer_inner"),
                ("Adaptive Outer/Inner (experimental)", "adaptive_outer_inner"),
            ]
        )
        self._set_combo_value(self.wall_printing_order_combo, self._defaults.wall_printing_order)
        self._label_wall_printing_order = self._add_row(
            "quality", section, section_layout, "Walls printing order",
            self.wall_printing_order_combo, "Order for printing wall perimeters.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_wall_printing_order, "wall_printing_order")
        self._register_hover_tooltip(self.wall_printing_order_combo, "wall_printing_order")
        self.print_infill_first_check = QtWidgets.QCheckBox(section)
        self.print_infill_first_check.setObjectName("SettingsCheck")
        self.print_infill_first_check.setChecked(bool(self._defaults.print_infill_first))
        self._label_print_infill_first = self._add_row(
            "quality", section, section_layout, "Print infill first",
            self.print_infill_first_check, "Print infill before walls.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_print_infill_first, "print_infill_first")
        self._register_hover_tooltip(self.print_infill_first_check, "print_infill_first")
        self.wall_loop_direction_combo = self._make_combo(
            [
                ("Auto", "auto"),
                ("Counter clockwise", "counter_clockwise"),
                ("Clockwise", "clockwise"),
            ]
        )
        self._set_combo_value(self.wall_loop_direction_combo, self._defaults.wall_loop_direction)
        self._label_wall_loop_direction = self._add_row(
            "quality", section, section_layout, "Wall loop direction",
            self.wall_loop_direction_combo, "Direction for perimeter loops.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_wall_loop_direction, "wall_loop_direction")
        self._register_hover_tooltip(self.wall_loop_direction_combo, "wall_loop_direction")
        self.top_surface_flow_ratio_spin = self._make_double_spin(
            self._defaults.top_surface_flow_ratio, 0.5, 2.0, 0.05
        )
        self._label_top_surface_flow_ratio = self._add_row(
            "quality", section, section_layout, "Top surface flow ratio",
            self.top_surface_flow_ratio_spin, "Extrusion multiplier for top surfaces.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_top_surface_flow_ratio, "top_surface_flow_ratio")
        self._register_hover_tooltip(self.top_surface_flow_ratio_spin, "top_surface_flow_ratio")
        self.bottom_surface_flow_ratio_spin = self._make_double_spin(
            self._defaults.bottom_surface_flow_ratio, 0.5, 2.0, 0.05
        )
        self._label_bottom_surface_flow_ratio = self._add_row(
            "quality", section, section_layout, "Bottom surface flow ratio",
            self.bottom_surface_flow_ratio_spin, "Extrusion multiplier for bottom surfaces.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_bottom_surface_flow_ratio, "bottom_surface_flow_ratio")
        self._register_hover_tooltip(self.bottom_surface_flow_ratio_spin, "bottom_surface_flow_ratio")
        self.only_one_wall_top_check = QtWidgets.QCheckBox(section)
        self.only_one_wall_top_check.setObjectName("SettingsCheck")
        self.only_one_wall_top_check.setChecked(bool(self._defaults.only_one_wall_top))
        self._label_one_wall_top = self._add_row(
            "quality",
            section,
            section_layout,
            "Only one wall on top surfaces",
            self.only_one_wall_top_check,
            "Use a single wall for top surfaces.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_one_wall_top, "only_one_wall_top")
        self._register_hover_tooltip(self.only_one_wall_top_check, "only_one_wall_top")
        self.one_wall_threshold_spin = self._make_double_spin(
            self._defaults.one_wall_threshold, 0.0, 500.0, 5.0, "%"
        )
        self._label_one_wall_threshold = self._add_row(
            "quality", section, section_layout, "One wall threshold",
            self.one_wall_threshold_spin,
            "Threshold for using a single wall on small surfaces.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_one_wall_threshold, "one_wall_threshold")
        self._register_hover_tooltip(self.one_wall_threshold_spin, "one_wall_threshold")
        self.only_one_wall_first_layer_check = QtWidgets.QCheckBox(section)
        self.only_one_wall_first_layer_check.setObjectName("SettingsCheck")
        self.only_one_wall_first_layer_check.setChecked(bool(self._defaults.only_one_wall_first_layer))
        self._label_one_wall_first = self._add_row(
            "quality",
            section,
            section_layout,
            "Only one wall on first layer",
            self.only_one_wall_first_layer_check,
            "Use a single wall for the first layer.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_one_wall_first, "only_one_wall_first")
        self._register_hover_tooltip(self.only_one_wall_first_layer_check, "only_one_wall_first")
        self.avoid_crossing_walls_check = QtWidgets.QCheckBox(section)
        self.avoid_crossing_walls_check.setObjectName("SettingsCheck")
        self.avoid_crossing_walls_check.setChecked(bool(self._defaults.avoid_crossing_walls))
        self._label_avoid_crossing_walls = self._add_row(
            "quality", section, section_layout, "Avoid crossing walls",
            self.avoid_crossing_walls_check,
            "Keep travel moves inside perimeters when possible.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_avoid_crossing_walls, "avoid_crossing_walls")
        self._register_hover_tooltip(self.avoid_crossing_walls_check, "avoid_crossing_walls")
        self.small_area_flow_compensation_check = QtWidgets.QCheckBox(section)
        self.small_area_flow_compensation_check.setObjectName("SettingsCheck")
        self.small_area_flow_compensation_check.setChecked(bool(self._defaults.small_area_flow_compensation))
        self._label_small_area_flow_comp = self._add_row(
            "quality", section, section_layout, "Small area flow compensation (beta)",
            self.small_area_flow_compensation_check,
            "Reduce flow on tiny segments.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_small_area_flow_comp,
                                     "small_area_flow_compensation")
        self._register_hover_tooltip(self.small_area_flow_compensation_check,
                                     "small_area_flow_compensation")
        self.smooth_wall_speed_z_check = QtWidgets.QCheckBox(section)
        self.smooth_wall_speed_z_check.setObjectName("SettingsCheck")
        self.smooth_wall_speed_z_check.setChecked(bool(self._defaults.smooth_wall_speed_z))
        self._label_smooth_wall_speed_z = self._add_row(
            "quality", section, section_layout, "Smoothing wall speed along Z (experimental)",
            self.smooth_wall_speed_z_check,
            "Smooth wall speeds across variable layer heights.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_smooth_wall_speed_z, "smooth_wall_speed_z")
        self._register_hover_tooltip(self.smooth_wall_speed_z_check, "smooth_wall_speed_z")
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Bridging", advanced=True)
        self.bridge_flow_ratio_spin = self._make_double_spin(
            self._defaults.bridge_flow_ratio, 0.1, 2.0, 0.05
        )
        self._label_bridge_flow_ratio = self._add_row(
            "quality", section, section_layout, "Bridge flow ratio",
            self.bridge_flow_ratio_spin, "Extrusion multiplier for bridge lines.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_bridge_flow_ratio, "bridge_flow_ratio")
        self._register_hover_tooltip(self.bridge_flow_ratio_spin, "bridge_flow_ratio")
        self.internal_bridge_flow_ratio_spin = self._make_double_spin(
            self._defaults.internal_bridge_flow_ratio, 0.1, 2.0, 0.05
        )
        self._label_internal_bridge_flow_ratio = self._add_row(
            "quality", section, section_layout, "Internal bridge flow ratio",
            self.internal_bridge_flow_ratio_spin,
            "Extrusion multiplier for internal bridges.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_internal_bridge_flow_ratio,
                                     "internal_bridge_flow_ratio")
        self._register_hover_tooltip(self.internal_bridge_flow_ratio_spin,
                                     "internal_bridge_flow_ratio")
        self.bridge_density_spin = self._make_double_spin(
            self._defaults.bridge_density, 0.0, 100.0, 1.0, "%"
        )
        self._label_bridge_density = self._add_row(
            "quality", section, section_layout, "Bridge density",
            self.bridge_density_spin, "Density of bridge infill.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_bridge_density, "bridge_density")
        self._register_hover_tooltip(self.bridge_density_spin, "bridge_density")
        self.thick_bridges_check = QtWidgets.QCheckBox(section)
        self.thick_bridges_check.setObjectName("SettingsCheck")
        self.thick_bridges_check.setChecked(bool(self._defaults.thick_bridges))
        self._label_thick_bridges = self._add_row(
            "quality", section, section_layout, "Thick bridges",
            self.thick_bridges_check, "Use thicker extrusion for bridges.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_thick_bridges, "thick_bridges")
        self._register_hover_tooltip(self.thick_bridges_check, "thick_bridges")
        self.thick_internal_bridges_check = QtWidgets.QCheckBox(section)
        self.thick_internal_bridges_check.setObjectName("SettingsCheck")
        self.thick_internal_bridges_check.setChecked(bool(self._defaults.thick_internal_bridges))
        self._label_thick_internal_bridges = self._add_row(
            "quality", section, section_layout, "Thick internal bridges",
            self.thick_internal_bridges_check,
            "Use thicker extrusion for internal bridges.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_thick_internal_bridges, "thick_internal_bridges")
        self._register_hover_tooltip(self.thick_internal_bridges_check,
                                     "thick_internal_bridges")
        self.bridge_filter_mode_combo = self._make_combo(
            [
                ("Disabled", "disabled"),
                ("Limited filtering", "limited"),
                ("No filtering", "none"),
            ]
        )
        self._set_combo_value(self.bridge_filter_mode_combo, self._defaults.bridge_filter_mode)
        self._label_bridge_filter_mode = self._add_row(
            "quality", section, section_layout, "Don't filter out small internal bridges (beta)",
            self.bridge_filter_mode_combo,
            "Control filtering for small internal bridges.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_bridge_filter_mode, "bridge_filter_mode")
        self._register_hover_tooltip(self.bridge_filter_mode_combo, "bridge_filter_mode")
        self.bridge_counterbore_combo = self._make_combo(
            [
                ("None", "none"),
                ("Partially bridged", "partial"),
                ("Sacrificial layer", "sacrificial"),
            ]
        )
        self._set_combo_value(self.bridge_counterbore_combo, self._defaults.bridge_counterbore_holes)
        self._label_bridge_counterbore = self._add_row(
            "quality", section, section_layout, "Bridge counterbore holes",
            self.bridge_counterbore_combo,
            "Create bridges for counterbore holes.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_bridge_counterbore, "bridge_counterbore_holes")
        self._register_hover_tooltip(self.bridge_counterbore_combo, "bridge_counterbore_holes")
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Overhangs", advanced=True)
        self.detect_overhang_walls_check = QtWidgets.QCheckBox(section)
        self.detect_overhang_walls_check.setObjectName("SettingsCheck")
        self.detect_overhang_walls_check.setChecked(bool(self._defaults.detect_overhang_walls))
        self._label_detect_overhang_walls = self._add_row(
            "quality", section, section_layout, "Detect overhang walls",
            self.detect_overhang_walls_check,
            "Detect walls that exceed the overhang angle.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_detect_overhang_walls, "detect_overhang_walls")
        self._register_hover_tooltip(self.detect_overhang_walls_check, "detect_overhang_walls")
        self.make_overhangs_printable_check = QtWidgets.QCheckBox(section)
        self.make_overhangs_printable_check.setObjectName("SettingsCheck")
        self.make_overhangs_printable_check.setChecked(bool(self._defaults.make_overhangs_printable))
        self._label_make_overhangs_printable = self._add_row(
            "quality", section, section_layout, "Make overhangs printable",
            self.make_overhangs_printable_check,
            "Adjust slicing to improve overhang printability.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_make_overhangs_printable,
                                     "make_overhangs_printable")
        self._register_hover_tooltip(self.make_overhangs_printable_check,
                                     "make_overhangs_printable")
        self.extra_perimeters_on_overhangs_check = QtWidgets.QCheckBox(section)
        self.extra_perimeters_on_overhangs_check.setObjectName("SettingsCheck")
        self.extra_perimeters_on_overhangs_check.setChecked(bool(self._defaults.extra_perimeters_on_overhangs))
        self._label_extra_perimeters = self._add_row(
            "quality", section, section_layout, "Extra perimeters on overhangs",
            self.extra_perimeters_on_overhangs_check,
            "Add extra perimeters on overhang layers.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_extra_perimeters,
                                     "extra_perimeters_on_overhangs")
        self._register_hover_tooltip(self.extra_perimeters_on_overhangs_check,
                                     "extra_perimeters_on_overhangs")
        self.reverse_overhang_on_odd_check = QtWidgets.QCheckBox(section)
        self.reverse_overhang_on_odd_check.setObjectName("SettingsCheck")
        self.reverse_overhang_on_odd_check.setChecked(bool(self._defaults.reverse_overhang_on_odd))
        self._label_reverse_overhang = self._add_row(
            "quality", section, section_layout, "Reverse on odd",
            self.reverse_overhang_on_odd_check,
            "Reverse wall direction on odd overhang layers.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_reverse_overhang, "reverse_overhang_on_odd")
        self._register_hover_tooltip(self.reverse_overhang_on_odd_check,
                                     "reverse_overhang_on_odd")
        self.overhang_optimization_check = QtWidgets.QCheckBox(section)
        self.overhang_optimization_check.setObjectName("SettingsCheck")
        self.overhang_optimization_check.setChecked(bool(self._defaults.overhang_optimization))
        self._label_overhang_optimization = self._add_row(
            "quality", section, section_layout, "Overhang optimization (beta)",
            self.overhang_optimization_check,
            "Use adaptive settings for overhangs.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_overhang_optimization, "overhang_optimization")
        self._register_hover_tooltip(self.overhang_optimization_check, "overhang_optimization")
        layout.insertWidget(layout.count() - 1, section)

    def _build_strength_page(self):
        layout = self._build_page("strength")

        section, section_layout = self._section("Walls")
        self.wall_loops_spin = self._make_int_spin(self._defaults.perimeter_count, 1, 10)
        self._add_row("strength", section, section_layout, "Wall loops", self.wall_loops_spin,
                      "Number of perimeter walls.")
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Top/bottom shells")
        self.top_shell_layers_spin = self._make_int_spin(self._defaults.top_layers, 0, 20, suffix="layers")
        self._add_row("strength", section, section_layout, "Top shell layers", self.top_shell_layers_spin,
                      "Number of top layers.")
        self.bottom_shell_layers_spin = self._make_int_spin(self._defaults.bottom_layers, 0, 20, suffix="layers")
        self._add_row("strength", section, section_layout, "Bottom shell layers", self.bottom_shell_layers_spin,
                      "Number of bottom layers.")
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Infill")
        self.infill_density_spin = self._make_int_spin(int(self._defaults.infill_percent), 0, 100, suffix="%")
        self._add_row("strength", section, section_layout, "Sparse infill density", self.infill_density_spin,
                      "Density of sparse infill.")
        self.infill_pattern_combo = self._make_combo(
            [
                ("Grid", "grid"),
                ("Rectilinear", "rectilinear"),
                ("Triangle", "triangle"),
            ]
        )
        self._set_combo_value(self.infill_pattern_combo, self._defaults.infill_pattern)
        self._add_row("strength", section, section_layout, "Sparse infill pattern", self.infill_pattern_combo,
                      "Infill pattern for non-solid regions.")
        layout.insertWidget(layout.count() - 1, section)

    def _build_support_page(self):
        layout = self._build_page("support")

        section, section_layout = self._section("Support")
        self.support_enable_check = QtWidgets.QCheckBox(section)
        self.support_enable_check.setObjectName("SettingsCheck")
        self.support_enable_check.setChecked(bool(self._defaults.support_enabled))
        self._add_row("support", section, section_layout, "Enable support", self.support_enable_check,
                      "Generate support structures.")

        self.support_type_combo = self._make_combo(
            [
                ("Normal (auto)", "normal"),
                ("Tree", "tree"),
            ]
        )
        self._set_combo_value(self.support_type_combo, self._defaults.support_type)
        self._add_row("support", section, section_layout, "Type", self.support_type_combo)

        self.support_style_combo = self._make_combo(
            [
                ("Default", "pillars"),
                ("Pillars", "pillars"),
                ("Tree", "tree"),
            ]
        )
        self._set_combo_value(self.support_style_combo, self._defaults.support_style)
        self._add_row("support", section, section_layout, "Style", self.support_style_combo)

        self.support_angle_spin = self._make_double_spin(self._defaults.overhang_angle, 0, 90, 1, "deg")
        self._add_row("support", section, section_layout, "Threshold angle", self.support_angle_spin,
                      "Overhang angle that triggers support.")

        self.support_build_plate_check = QtWidgets.QCheckBox(section)
        self.support_build_plate_check.setObjectName("SettingsCheck")
        self.support_build_plate_check.setChecked(bool(self._defaults.support_build_plate_only))
        self._add_row("support", section, section_layout, "On build plate only",
                      self.support_build_plate_check)
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Filament for supports")
        self.support_base_combo = self._make_combo(
            [
                ("Default", "default"),
                ("Support", "support"),
            ]
        )
        self._set_combo_value(self.support_base_combo, self._defaults.support_filament_base)
        self._add_row("support", section, section_layout, "Support/raft base", self.support_base_combo)

        self.support_interface_combo = self._make_combo(
            [
                ("Default", "default"),
                ("Support", "support"),
            ]
        )
        self._set_combo_value(self.support_interface_combo, self._defaults.support_filament_interface)
        self._add_row("support", section, section_layout, "Support/raft interface",
                      self.support_interface_combo)
        layout.insertWidget(layout.count() - 1, section)

        self.support_enable_check.toggled.connect(self._update_support_controls)
        self._update_support_controls(self.support_enable_check.isChecked())

    def _build_multifilament_page(self):
        layout = self._build_page("multifilament")

        section, section_layout = self._section("Prime tower")
        self.prime_tower_enable_check = QtWidgets.QCheckBox(section)
        self.prime_tower_enable_check.setObjectName("SettingsCheck")
        self.prime_tower_enable_check.setChecked(bool(self._defaults.prime_tower_enabled))
        self._add_row("multifilament", section, section_layout, "Enable", self.prime_tower_enable_check)

        self.prime_tower_width_spin = self._make_double_spin(
            self._defaults.prime_tower_width, 5.0, 100.0, 1.0, "mm"
        )
        self._add_row("multifilament", section, section_layout, "Width", self.prime_tower_width_spin)

        self.prime_tower_square_check = QtWidgets.QCheckBox(section)
        self.prime_tower_square_check.setObjectName("SettingsCheck")
        self.prime_tower_square_check.setChecked(bool(self._defaults.prime_tower_square))
        self._add_row("multifilament", section, section_layout, "Square prime tower",
                      self.prime_tower_square_check)

        self.prime_tower_volume_spin = self._make_double_spin(
            self._defaults.prime_tower_volume, 1.0, 200.0, 1.0, "mm3"
        )
        self._add_row("multifilament", section, section_layout, "Prime volume",
                      self.prime_tower_volume_spin)
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Flush options")
        self.flush_into_infill_check = QtWidgets.QCheckBox(section)
        self.flush_into_infill_check.setObjectName("SettingsCheck")
        self.flush_into_infill_check.setChecked(bool(self._defaults.flush_into_infill))
        self._add_row("multifilament", section, section_layout, "Flush into objects' infill",
                      self.flush_into_infill_check)

        self.flush_into_support_check = QtWidgets.QCheckBox(section)
        self.flush_into_support_check.setObjectName("SettingsCheck")
        self.flush_into_support_check.setChecked(bool(self._defaults.flush_into_support))
        self._add_row("multifilament", section, section_layout, "Flush into objects' support",
                      self.flush_into_support_check)
        layout.insertWidget(layout.count() - 1, section)

        self.prime_tower_enable_check.toggled.connect(self._update_prime_controls)
        self._update_prime_controls(self.prime_tower_enable_check.isChecked())

    def _build_other_page(self):
        layout = self._build_page("others")

        section, section_layout = self._section("Skirt")
        self.skirt_loops_spin = self._make_int_spin(self._defaults.skirt_loops, 0, 10, suffix="loops")
        self._add_row("others", section, section_layout, "Skirt loops", self.skirt_loops_spin)

        self.skirt_height_spin = self._make_int_spin(self._defaults.skirt_height, 0, 20, suffix="layers")
        self._add_row("others", section, section_layout, "Skirt height", self.skirt_height_spin)
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Brim")
        self.brim_type_combo = self._make_combo(
            [
                ("Auto", "auto"),
                ("Outer", "outer"),
                ("Inner", "inner"),
                ("Both", "both"),
            ]
        )
        self._set_combo_value(self.brim_type_combo, self._defaults.brim_type)
        self._add_row("others", section, section_layout, "Brim type", self.brim_type_combo)
        self.brim_width_spin = self._make_double_spin(self._defaults.brim_width, 0.0, 50.0, 0.5, "mm")
        self._add_row("others", section, section_layout, "Brim width", self.brim_width_spin)
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Special mode")
        self.print_sequence_combo = self._make_combo(
            [
                ("By layer", "by_layer"),
                ("By object", "by_object"),
            ]
        )
        self._set_combo_value(self.print_sequence_combo, self._defaults.print_sequence)
        self._add_row("others", section, section_layout, "Print sequence", self.print_sequence_combo)

        self.spiral_vase_check = QtWidgets.QCheckBox(section)
        self.spiral_vase_check.setObjectName("SettingsCheck")
        self.spiral_vase_check.setChecked(bool(self._defaults.spiral_vase))
        self._add_row("others", section, section_layout, "Spiral vase", self.spiral_vase_check)

        self.ignore_inner_color_check = QtWidgets.QCheckBox(section)
        self.ignore_inner_color_check.setObjectName("SettingsCheck")
        self.ignore_inner_color_check.setChecked(bool(self._defaults.ignore_inner_color))
        self._add_row("others", section, section_layout, "Ignore inner color", self.ignore_inner_color_check)

        self.timelapse_combo = self._make_combo(
            [
                ("Traditional", "traditional"),
                ("Smooth", "smooth"),
            ]
        )
        self._set_combo_value(self.timelapse_combo, self._defaults.timelapse_mode)
        self._add_row("others", section, section_layout, "Timelapse", self.timelapse_combo)

        self.fuzzy_skin_combo = self._make_combo(
            [
                ("None", "none"),
                ("Light", "light"),
                ("Normal", "normal"),
                ("Heavy", "heavy"),
            ]
        )
        self._set_combo_value(self.fuzzy_skin_combo, self._defaults.fuzzy_skin)
        self._add_row("others", section, section_layout, "Fuzzy skin", self.fuzzy_skin_combo)
        layout.insertWidget(layout.count() - 1, section)

    def _choose_filament_color(self):
        color = QtWidgets.QColorDialog.getColor(self._filament_color, self)
        if color.isValid():
            self._filament_color = color
            self._update_filament_button_style()

    def set_printers(self, printers):
        self._printers = list(printers or [])
        if not hasattr(self, "_printer_combo"):
            return
        self._printer_combo.clear()
        if not self._printers:
            self._printer_combo.addItem("No printers configured")
            self._printer_combo.setEnabled(False)
            return
        self._printer_combo.setEnabled(True)
        dummy_index = None
        for idx, printer in enumerate(self._printers):
            name = printer.get("name") if isinstance(printer, dict) else None
            self._printer_combo.addItem(name or "Printer")
            if str(name or "").strip().lower() == "dummy printer":
                dummy_index = idx
        if dummy_index is not None:
            self._printer_combo.setCurrentIndex(dummy_index)
        self._on_printer_changed(self._printer_combo.currentIndex())

    def current_printer(self):
        if not getattr(self, "_printers", None):
            return None
        idx = self._printer_combo.currentIndex()
        if idx < 0 or idx >= len(self._printers):
            return None
        return self._printers[idx]

    def _on_printer_changed(self, _index: int):
        printer = self.current_printer()
        if printer is None:
            return
        main = self.parent()
        if hasattr(main, "printer_manager"):
            main.printer_manager.set_active_printer(printer)
        defaults = DEFAULTS.get("printer", {})
        bed_defaults = defaults.get("bed_size", (200, 200))

        def _float_or(value, fallback):
            try:
                return float(value)
            except (TypeError, ValueError):
                return float(fallback)

        bed_x = _float_or(printer.get("bed_x"), bed_defaults[0] if bed_defaults else 200)
        bed_y = _float_or(printer.get("bed_y"), bed_defaults[1] if len(bed_defaults) > 1 else 200)
        bed_z = _float_or(printer.get("bed_z"), defaults.get("max_height", 200))
        DEFAULTS.setdefault("printer", {})["bed_size"] = (bed_x, bed_y)
        DEFAULTS["printer"]["max_height"] = bed_z
        viewer = getattr(main, "viewer", None)
        if viewer is not None and hasattr(viewer, "set_bed_limits"):
            viewer.set_bed_limits((bed_x, bed_y), bed_z)
        if viewer is not None and hasattr(main, "_update_bed_warnings"):
            main._update_bed_warnings()

    def _on_filament_type_selected(self, name: str):
        name = (name or "").strip()
        if name:
            self._filament_button.setText(name)

    def _update_filament_button_style(self):
        accent = self._filament_color.name()
        self._filament_button.setStyleSheet(
            "QToolButton#FilamentButton {"
            f"  background: {accent};"
            "  color: #000000;"
            "  border-radius: 6px;"
            "  padding: 6px 8px;"
            "}"
        )
        if getattr(self, "_filament_color_button", None) is not None:
            self._filament_color_button.setStyleSheet(
                "QToolButton#FilamentColorButton {"
                f"  background: {accent};"
                "  border-radius: 6px;"
                "  border: 1px solid #1d1f23;"
                "}"
            )

    def _update_support_controls(self, enabled: bool):
        for control in (
            self.support_type_combo,
            self.support_style_combo,
            self.support_angle_spin,
            self.support_build_plate_check,
            self.support_base_combo,
            self.support_interface_combo,
        ):
            control.setEnabled(bool(enabled))

    def _update_prime_controls(self, enabled: bool):
        for control in (
            self.prime_tower_width_spin,
            self.prime_tower_square_check,
            self.prime_tower_volume_spin,
            self.flush_into_infill_check,
            self.flush_into_support_check,
        ):
            control.setEnabled(bool(enabled))

    def _on_nav_changed(self, button):
        idx = self._nav_group.id(button)
        if idx < 0:
            return
        self._pages_stack.setCurrentIndex(idx)
        self._apply_search_filter(self._search_input.text())

    def _on_advanced_toggled(self, _checked: bool):
        self._apply_search_filter(self._search_input.text())

    def _apply_search_filter(self, text: str):
        query = (text or "").strip().lower()
        page_index = int(self._pages_stack.currentIndex())
        if page_index < 0 or page_index >= len(self._page_keys):
            return
        key = self._page_keys[page_index]
        rows = self._search_rows.get(key, [])
        show_advanced = True
        if hasattr(self, "_advanced_toggle"):
            show_advanced = bool(self._advanced_toggle.isChecked())
        section_visible: Dict[QtWidgets.QFrame, bool] = {}
        for section, row, label in rows:
            is_advanced = row in self._advanced_rows
            if not show_advanced and is_advanced:
                match = False
            elif not query:
                match = True
                if is_advanced and not show_advanced:
                    match = False
            else:
                match = query in label
            row.setVisible(match)
            section_visible[section] = section_visible.get(section, False) or match
        for section, visible in section_visible.items():
            section.setVisible(visible)

    def _set_combo_value(self, combo: QtWidgets.QComboBox, value: str | None):
        if value is None:
            return
        value = str(value).strip().lower()
        for idx in range(combo.count()):
            data = combo.itemData(idx)
            if data is None:
                continue
            if str(data).strip().lower() == value:
                combo.setCurrentIndex(idx)
                return

    def _combo_value(self, combo: QtWidgets.QComboBox, default: str) -> str:
        data = combo.currentData()
        if data is None:
            text = combo.currentText().strip().lower().replace(" ", "_")
            return text or default
        return str(data).strip().lower() or default

    def apply_theme(self):
        panel_bg = theme_css("popup_bg")
        panel_border = theme_css("popup_border")
        panel_text = theme_css("popup_text")
        muted_text = theme_css("popup_muted_text")
        accent = theme_css("topbar_accent")
        input_bg = theme_css("popup_input_bg")

        self.setStyleSheet(
            "QWidget#SettingsPanel {"
            f"  background: {panel_bg};"
            "}"
            "QFrame#SettingsHeader {"
            f"  background: {panel_bg};"
            "}"
            "QLabel#SettingsHeaderTitle {"
            f"  color: {panel_text};"
            "  font-weight: 600;"
            "  font-size: 13px;"
            "}"
            "QToolButton#SettingsHeaderButton {"
            f"  color: {muted_text};"
            f"  background: {panel_bg};"
            "  border: none;"
            "  padding: 2px 6px;"
            "}"
            "QLabel#FilamentSlot {"
            f"  color: {panel_text};"
            "  padding: 4px 6px;"
            "}"
            "QToolButton#FilamentButton {"
            "  border: none;"
            "}"
            "QToolButton#FilamentColorButton {"
            "  border: none;"
            "}"
            "QFrame#ProcessRow, QFrame#ProfileRow, QFrame#PrinterRow {"
            f"  background: {panel_bg};"
            f"  border: 1px solid {panel_border};"
            "  border-radius: 8px;"
            "}"
            "QLabel#PrinterLabel {"
            f"  color: {panel_text};"
            "  font-weight: 600;"
            "}"
            "QLabel#ProcessLabel {"
            f"  color: {panel_text};"
            "  font-weight: 600;"
            "}"
            "QLabel#AdvancedLabel {"
            f"  color: {panel_text};"
            "  font-weight: 600;"
            "}"
            "QToolButton#SettingsChip {"
            f"  background: {input_bg};"
            f"  color: {panel_text};"
            f"  border: 1px solid {panel_border};"
            "  border-radius: 10px;"
            "  padding: 3px 10px;"
            "}"
            "QToolButton#SettingsChip:checked {"
            f"  background: {accent};"
            "  color: #ffffff;"
            "  font-weight: 600;"
            "}"
            "QCheckBox#SettingsToggle::indicator {"
            "  width: 36px;"
            "  height: 18px;"
            "}"
            "QCheckBox#SettingsToggle::indicator:unchecked {"
            f"  background: {input_bg};"
            f"  border: 1px solid {panel_border};"
            "  border-radius: 9px;"
            "}"
            "QCheckBox#SettingsToggle::indicator:checked {"
            f"  background: {accent};"
            "  border-radius: 9px;"
            "}"
            "QComboBox#ProfileCombo, QComboBox#PrinterCombo, QLineEdit#SettingsSearch {"
            f"  background: {input_bg};"
            f"  color: {panel_text};"
            f"  border: 1px solid {panel_border};"
            "  border-radius: 6px;"
            "  padding: 3px 6px;"
            "}"
            "QToolButton#ProfileButton {"
            f"  background: {input_bg};"
            f"  color: {panel_text};"
            f"  border: 1px solid {panel_border};"
            "  border-radius: 6px;"
            "  padding: 2px 8px;"
            "}"
            "QFrame#SettingsNav {"
            f"  background: {panel_bg};"
            f"  border: 1px solid {panel_border};"
            "  border-radius: 8px;"
            "}"
            "QToolButton#SettingsNavButton {"
            f"  color: {panel_text};"
            "  padding: 6px 6px;"
            "  border-radius: 6px;"
            "}"
            "QToolButton#SettingsNavButton:checked {"
            f"  background: {accent};"
            "  color: #ffffff;"
            "  font-weight: 600;"
            "}"
            "QFrame#SettingsSection {"
            f"  background: {panel_bg};"
            f"  border: 1px solid {panel_border};"
            "  border-radius: 8px;"
            "}"
            "QLabel#SettingsSectionTitle {"
            f"  color: {panel_text};"
            "  font-weight: 600;"
            "}"
            "QFrame#SettingsSectionLine {"
            f"  color: {panel_border};"
            "}"
            "QLabel#SettingsLabel {"
            f"  color: {panel_text};"
            "}"
            "QComboBox#SettingsCombo, QSpinBox#SettingsSpin, QDoubleSpinBox#SettingsSpin {"
            f"  background: {input_bg};"
            f"  color: {panel_text};"
            f"  border: 1px solid {panel_border};"
            "  border-radius: 6px;"
            "  padding: 2px 6px;"
            "}"
            "QCheckBox#SettingsCheck::indicator {"
            "  width: 18px;"
            "  height: 18px;"
            "}"
            "QCheckBox#SettingsCheck::indicator:unchecked {"
            f"  border: 1px solid {panel_border};"
            f"  background: {input_bg};"
            "  border-radius: 3px;"
            "}"
            "QCheckBox#SettingsCheck::indicator:checked {"
            f"  background: {accent};"
            "  border-radius: 3px;"
            "}"
        )
        self._update_filament_button_style()
        self._tooltip.apply_theme(panel_bg, panel_border, panel_text, muted_text)

    def to_settings(self) -> SliceSettings:
        return SliceSettings(
            layer_height=float(self.layer_height_spin.value()),
            first_layer_height=float(self.first_layer_height_spin.value()),
            seam_position=self._combo_value(self.seam_position_combo, "aligned"),
            staggered_inner_seams=bool(self.staggered_inner_seams_check.isChecked()),
            seam_gap=float(self.seam_gap_spin.value()),
            scarf_joint_seam=self._combo_value(self.scarf_joint_seam_combo, "none"),
            wipe_use_base_speed=bool(self.wipe_use_base_speed_check.isChecked()),
            wipe_speed_percent=float(self.wipe_speed_spin.value()),
            wipe_on_loops=bool(self.wipe_on_loops_check.isChecked()),
            wipe_before_external_loop=bool(self.wipe_before_external_loop_check.isChecked()),
            precise_wall=bool(self.precise_wall_check.isChecked()),
            slice_gap_closing_radius=float(self.slice_gap_closing_radius_spin.value()),
            resolution=float(self.resolution_spin.value()),
            arc_fitting=bool(self.arc_fitting_check.isChecked()),
            xy_hole_compensation=float(self.xy_hole_compensation_spin.value()),
            xy_contour_compensation=float(self.xy_contour_compensation_spin.value()),
            elephant_foot_compensation=float(self.elephant_foot_compensation_spin.value()),
            elephant_foot_compensation_layers=int(self.elephant_foot_layers_spin.value()),
            convert_holes_to_polyholes=bool(self.convert_holes_to_polyholes_check.isChecked()),
            precise_z_height=bool(self.precise_z_height_check.isChecked()),
            only_one_wall_top=bool(self.only_one_wall_top_check.isChecked()),
            only_one_wall_first_layer=bool(self.only_one_wall_first_layer_check.isChecked()),
            extrusion_width=float(self.line_width_default_spin.value()),
            first_layer_line_width=float(self.line_width_first_layer_spin.value()),
            outer_wall_line_width=float(self.line_width_outer_wall_spin.value()),
            inner_wall_line_width=float(self.line_width_inner_wall_spin.value()),
            top_surface_line_width=float(self.line_width_top_surface_spin.value()),
            sparse_infill_line_width=float(self.line_width_sparse_infill_spin.value()),
            internal_solid_infill_line_width=float(self.line_width_internal_solid_spin.value()),
            support_line_width=float(self.line_width_support_spin.value()),
            ironing_type=self._combo_value(self.ironing_type_combo, "no_ironing"),
            wall_generator=self._combo_value(self.wall_generator_combo, "classic"),
            wall_transition_angle=float(self.wall_transition_angle_spin.value()),
            wall_transition_filter_margin=float(self.wall_transition_filter_margin_spin.value()),
            wall_transition_length=float(self.wall_transition_length_spin.value()),
            wall_distribution_count=int(self.wall_distribution_count_spin.value()),
            first_layer_min_wall_width=float(self.first_layer_min_wall_width_spin.value()),
            min_wall_width=float(self.min_wall_width_spin.value()),
            min_feature_size=float(self.min_feature_size_spin.value()),
            min_wall_length=float(self.min_wall_length_spin.value()),
            wall_printing_order=self._combo_value(self.wall_printing_order_combo, "inner_outer"),
            print_infill_first=bool(self.print_infill_first_check.isChecked()),
            wall_loop_direction=self._combo_value(self.wall_loop_direction_combo, "auto"),
            top_surface_flow_ratio=float(self.top_surface_flow_ratio_spin.value()),
            bottom_surface_flow_ratio=float(self.bottom_surface_flow_ratio_spin.value()),
            one_wall_threshold=float(self.one_wall_threshold_spin.value()),
            avoid_crossing_walls=bool(self.avoid_crossing_walls_check.isChecked()),
            small_area_flow_compensation=bool(self.small_area_flow_compensation_check.isChecked()),
            smooth_wall_speed_z=bool(self.smooth_wall_speed_z_check.isChecked()),
            bridge_flow_ratio=float(self.bridge_flow_ratio_spin.value()),
            internal_bridge_flow_ratio=float(self.internal_bridge_flow_ratio_spin.value()),
            bridge_density=float(self.bridge_density_spin.value()),
            thick_bridges=bool(self.thick_bridges_check.isChecked()),
            thick_internal_bridges=bool(self.thick_internal_bridges_check.isChecked()),
            bridge_filter_mode=self._combo_value(self.bridge_filter_mode_combo, "disabled"),
            bridge_counterbore_holes=self._combo_value(self.bridge_counterbore_combo, "none"),
            detect_overhang_walls=bool(self.detect_overhang_walls_check.isChecked()),
            make_overhangs_printable=bool(self.make_overhangs_printable_check.isChecked()),
            extra_perimeters_on_overhangs=bool(self.extra_perimeters_on_overhangs_check.isChecked()),
            reverse_overhang_on_odd=bool(self.reverse_overhang_on_odd_check.isChecked()),
            overhang_optimization=bool(self.overhang_optimization_check.isChecked()),
            perimeter_count=int(self.wall_loops_spin.value()),
            top_layers=int(self.top_shell_layers_spin.value()),
            bottom_layers=int(self.bottom_shell_layers_spin.value()),
            infill_percent=float(self.infill_density_spin.value()),
            infill_pattern=self._combo_value(self.infill_pattern_combo, "rectilinear"),
            support_enabled=bool(self.support_enable_check.isChecked()),
            support_type=self._combo_value(self.support_type_combo, "normal"),
            support_style=self._combo_value(self.support_style_combo, "pillars"),
            overhang_angle=float(self.support_angle_spin.value()),
            support_build_plate_only=bool(self.support_build_plate_check.isChecked()),
            support_filament_base=self._combo_value(self.support_base_combo, "default"),
            support_filament_interface=self._combo_value(self.support_interface_combo, "default"),
            prime_tower_enabled=bool(self.prime_tower_enable_check.isChecked()),
            prime_tower_width=float(self.prime_tower_width_spin.value()),
            prime_tower_square=bool(self.prime_tower_square_check.isChecked()),
            prime_tower_volume=float(self.prime_tower_volume_spin.value()),
            flush_into_infill=bool(self.flush_into_infill_check.isChecked()),
            flush_into_support=bool(self.flush_into_support_check.isChecked()),
            skirt_loops=int(self.skirt_loops_spin.value()),
            skirt_height=int(self.skirt_height_spin.value()),
            brim_type=self._combo_value(self.brim_type_combo, "auto"),
            brim_width=float(self.brim_width_spin.value()),
            print_sequence=self._combo_value(self.print_sequence_combo, "by_layer"),
            spiral_vase=bool(self.spiral_vase_check.isChecked()),
            ignore_inner_color=bool(self.ignore_inner_color_check.isChecked()),
            timelapse_mode=self._combo_value(self.timelapse_combo, "traditional"),
            fuzzy_skin=self._combo_value(self.fuzzy_skin_combo, "none"),
            filament_name=self._filament_button.text().strip() or self._defaults.filament_name,
            filament_color=self._filament_color.name(),
        )

    def apply_settings(self, settings):
        data = {}
        if isinstance(settings, SliceSettings):
            data = asdict(settings)
        elif isinstance(settings, dict):
            data = settings

        if "layer_height" in data:
            self.layer_height_spin.setValue(float(data["layer_height"]))
        if "first_layer_height" in data:
            self.first_layer_height_spin.setValue(float(data["first_layer_height"]))
        if "seam_position" in data:
            self._set_combo_value(self.seam_position_combo, data["seam_position"])
        if "staggered_inner_seams" in data:
            self.staggered_inner_seams_check.setChecked(bool(data["staggered_inner_seams"]))
        if "seam_gap" in data:
            self.seam_gap_spin.setValue(float(data["seam_gap"]))
        if "scarf_joint_seam" in data:
            self._set_combo_value(self.scarf_joint_seam_combo, data["scarf_joint_seam"])
        if "wipe_use_base_speed" in data:
            self.wipe_use_base_speed_check.setChecked(bool(data["wipe_use_base_speed"]))
        if "wipe_speed_percent" in data:
            self.wipe_speed_spin.setValue(float(data["wipe_speed_percent"]))
        if "wipe_on_loops" in data:
            self.wipe_on_loops_check.setChecked(bool(data["wipe_on_loops"]))
        if "wipe_before_external_loop" in data:
            self.wipe_before_external_loop_check.setChecked(bool(data["wipe_before_external_loop"]))
        if "precise_wall" in data:
            self.precise_wall_check.setChecked(bool(data["precise_wall"]))
        if "slice_gap_closing_radius" in data:
            self.slice_gap_closing_radius_spin.setValue(float(data["slice_gap_closing_radius"]))
        if "resolution" in data:
            self.resolution_spin.setValue(float(data["resolution"]))
        if "arc_fitting" in data:
            self.arc_fitting_check.setChecked(bool(data["arc_fitting"]))
        if "xy_hole_compensation" in data:
            self.xy_hole_compensation_spin.setValue(float(data["xy_hole_compensation"]))
        if "xy_contour_compensation" in data:
            self.xy_contour_compensation_spin.setValue(float(data["xy_contour_compensation"]))
        if "elephant_foot_compensation" in data:
            self.elephant_foot_compensation_spin.setValue(float(data["elephant_foot_compensation"]))
        if "elephant_foot_compensation_layers" in data:
            self.elephant_foot_layers_spin.setValue(int(data["elephant_foot_compensation_layers"]))
        if "convert_holes_to_polyholes" in data:
            self.convert_holes_to_polyholes_check.setChecked(bool(data["convert_holes_to_polyholes"]))
        if "precise_z_height" in data:
            self.precise_z_height_check.setChecked(bool(data["precise_z_height"]))
        if "only_one_wall_top" in data:
            self.only_one_wall_top_check.setChecked(bool(data["only_one_wall_top"]))
        if "only_one_wall_first_layer" in data:
            self.only_one_wall_first_layer_check.setChecked(bool(data["only_one_wall_first_layer"]))
        if "extrusion_width" in data:
            self.line_width_default_spin.setValue(float(data["extrusion_width"]))
        if "first_layer_line_width" in data:
            self.line_width_first_layer_spin.setValue(float(data["first_layer_line_width"]))
        if "outer_wall_line_width" in data:
            self.line_width_outer_wall_spin.setValue(float(data["outer_wall_line_width"]))
        if "inner_wall_line_width" in data:
            self.line_width_inner_wall_spin.setValue(float(data["inner_wall_line_width"]))
        if "top_surface_line_width" in data:
            self.line_width_top_surface_spin.setValue(float(data["top_surface_line_width"]))
        if "sparse_infill_line_width" in data:
            self.line_width_sparse_infill_spin.setValue(float(data["sparse_infill_line_width"]))
        if "internal_solid_infill_line_width" in data:
            self.line_width_internal_solid_spin.setValue(float(data["internal_solid_infill_line_width"]))
        if "support_line_width" in data:
            self.line_width_support_spin.setValue(float(data["support_line_width"]))
        if "ironing_type" in data:
            self._set_combo_value(self.ironing_type_combo, data["ironing_type"])
        if "wall_generator" in data:
            self._set_combo_value(self.wall_generator_combo, data["wall_generator"])
        if "wall_transition_angle" in data:
            self.wall_transition_angle_spin.setValue(float(data["wall_transition_angle"]))
        if "wall_transition_filter_margin" in data:
            self.wall_transition_filter_margin_spin.setValue(float(data["wall_transition_filter_margin"]))
        if "wall_transition_length" in data:
            self.wall_transition_length_spin.setValue(float(data["wall_transition_length"]))
        if "wall_distribution_count" in data:
            self.wall_distribution_count_spin.setValue(int(data["wall_distribution_count"]))
        if "first_layer_min_wall_width" in data:
            self.first_layer_min_wall_width_spin.setValue(float(data["first_layer_min_wall_width"]))
        if "min_wall_width" in data:
            self.min_wall_width_spin.setValue(float(data["min_wall_width"]))
        if "min_feature_size" in data:
            self.min_feature_size_spin.setValue(float(data["min_feature_size"]))
        if "min_wall_length" in data:
            self.min_wall_length_spin.setValue(float(data["min_wall_length"]))
        if "wall_printing_order" in data:
            self._set_combo_value(self.wall_printing_order_combo, data["wall_printing_order"])
        if "print_infill_first" in data:
            self.print_infill_first_check.setChecked(bool(data["print_infill_first"]))
        if "wall_loop_direction" in data:
            self._set_combo_value(self.wall_loop_direction_combo, data["wall_loop_direction"])
        if "top_surface_flow_ratio" in data:
            self.top_surface_flow_ratio_spin.setValue(float(data["top_surface_flow_ratio"]))
        if "bottom_surface_flow_ratio" in data:
            self.bottom_surface_flow_ratio_spin.setValue(float(data["bottom_surface_flow_ratio"]))
        if "one_wall_threshold" in data:
            self.one_wall_threshold_spin.setValue(float(data["one_wall_threshold"]))
        if "avoid_crossing_walls" in data:
            self.avoid_crossing_walls_check.setChecked(bool(data["avoid_crossing_walls"]))
        if "small_area_flow_compensation" in data:
            self.small_area_flow_compensation_check.setChecked(bool(data["small_area_flow_compensation"]))
        if "smooth_wall_speed_z" in data:
            self.smooth_wall_speed_z_check.setChecked(bool(data["smooth_wall_speed_z"]))
        if "bridge_flow_ratio" in data:
            self.bridge_flow_ratio_spin.setValue(float(data["bridge_flow_ratio"]))
        if "internal_bridge_flow_ratio" in data:
            self.internal_bridge_flow_ratio_spin.setValue(float(data["internal_bridge_flow_ratio"]))
        if "bridge_density" in data:
            self.bridge_density_spin.setValue(float(data["bridge_density"]))
        if "thick_bridges" in data:
            self.thick_bridges_check.setChecked(bool(data["thick_bridges"]))
        if "thick_internal_bridges" in data:
            self.thick_internal_bridges_check.setChecked(bool(data["thick_internal_bridges"]))
        if "bridge_filter_mode" in data:
            self._set_combo_value(self.bridge_filter_mode_combo, data["bridge_filter_mode"])
        if "bridge_counterbore_holes" in data:
            self._set_combo_value(self.bridge_counterbore_combo, data["bridge_counterbore_holes"])
        if "detect_overhang_walls" in data:
            self.detect_overhang_walls_check.setChecked(bool(data["detect_overhang_walls"]))
        if "make_overhangs_printable" in data:
            self.make_overhangs_printable_check.setChecked(bool(data["make_overhangs_printable"]))
        if "extra_perimeters_on_overhangs" in data:
            self.extra_perimeters_on_overhangs_check.setChecked(
                bool(data["extra_perimeters_on_overhangs"])
            )
        if "reverse_overhang_on_odd" in data:
            self.reverse_overhang_on_odd_check.setChecked(bool(data["reverse_overhang_on_odd"]))
        if "overhang_optimization" in data:
            self.overhang_optimization_check.setChecked(bool(data["overhang_optimization"]))
        if "perimeter_count" in data:
            self.wall_loops_spin.setValue(int(data["perimeter_count"]))
        if "top_layers" in data:
            self.top_shell_layers_spin.setValue(int(data["top_layers"]))
        if "bottom_layers" in data:
            self.bottom_shell_layers_spin.setValue(int(data["bottom_layers"]))
        if "infill_percent" in data:
            self.infill_density_spin.setValue(int(float(data["infill_percent"])))
        if "infill_pattern" in data:
            self._set_combo_value(self.infill_pattern_combo, data["infill_pattern"])
        if "support_enabled" in data:
            self.support_enable_check.setChecked(bool(data["support_enabled"]))
        if "support_type" in data:
            self._set_combo_value(self.support_type_combo, data["support_type"])
        if "support_style" in data:
            self._set_combo_value(self.support_style_combo, data["support_style"])
        if "overhang_angle" in data:
            self.support_angle_spin.setValue(float(data["overhang_angle"]))
        if "support_build_plate_only" in data:
            self.support_build_plate_check.setChecked(bool(data["support_build_plate_only"]))
        if "support_filament_base" in data:
            self._set_combo_value(self.support_base_combo, data["support_filament_base"])
        if "support_filament_interface" in data:
            self._set_combo_value(self.support_interface_combo, data["support_filament_interface"])
        if "prime_tower_enabled" in data:
            self.prime_tower_enable_check.setChecked(bool(data["prime_tower_enabled"]))
        if "prime_tower_width" in data:
            self.prime_tower_width_spin.setValue(float(data["prime_tower_width"]))
        if "prime_tower_square" in data:
            self.prime_tower_square_check.setChecked(bool(data["prime_tower_square"]))
        if "prime_tower_volume" in data:
            self.prime_tower_volume_spin.setValue(float(data["prime_tower_volume"]))
        if "flush_into_infill" in data:
            self.flush_into_infill_check.setChecked(bool(data["flush_into_infill"]))
        if "flush_into_support" in data:
            self.flush_into_support_check.setChecked(bool(data["flush_into_support"]))
        if "skirt_loops" in data:
            self.skirt_loops_spin.setValue(int(data["skirt_loops"]))
        if "skirt_height" in data:
            self.skirt_height_spin.setValue(int(data["skirt_height"]))
        if "brim_type" in data:
            self._set_combo_value(self.brim_type_combo, data["brim_type"])
        if "brim_width" in data:
            self.brim_width_spin.setValue(float(data["brim_width"]))
        if "print_sequence" in data:
            self._set_combo_value(self.print_sequence_combo, data["print_sequence"])
        if "spiral_vase" in data:
            self.spiral_vase_check.setChecked(bool(data["spiral_vase"]))
        if "ignore_inner_color" in data:
            self.ignore_inner_color_check.setChecked(bool(data["ignore_inner_color"]))
        if "timelapse_mode" in data:
            self._set_combo_value(self.timelapse_combo, data["timelapse_mode"])
        if "fuzzy_skin" in data:
            self._set_combo_value(self.fuzzy_skin_combo, data["fuzzy_skin"])
        if "filament_name" in data:
            name = str(data["filament_name"]).strip()
            if name:
                self._filament_button.setText(name)
        if "filament_color" in data:
            color = QtGui.QColor(str(data["filament_color"]))
            if color.isValid():
                self._filament_color = color
                self._update_filament_button_style()

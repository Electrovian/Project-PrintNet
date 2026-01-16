from __future__ import annotations

from dataclasses import asdict
from typing import Dict, List, Tuple, TYPE_CHECKING, cast

from PyQt5 import QtCore, QtGui, QtWidgets

from slicer.gcode.writer import SliceSettings
from config.defaults import DEFAULTS
from ..theme import theme_css
from .multifilament import MultifilamentSectionMixin
from .others import OtherSectionMixin
from .quality import QualitySectionMixin
from .strength import StrengthSectionMixin
from .support import SupportSectionMixin

if TYPE_CHECKING:
    from ..main_window import MainWindow


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


class SettingsPanel(
    QualitySectionMixin,
    StrengthSectionMixin,
    SupportSectionMixin,
    MultifilamentSectionMixin,
    OtherSectionMixin,
    QtWidgets.QWidget,
):
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
        self._apply_search_filter(self._search_input.text())
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
        self._advanced_toggle.setChecked(False)
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


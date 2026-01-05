from __future__ import annotations

from dataclasses import asdict
from typing import Dict, List, Tuple

from PyQt5 import QtCore, QtGui, QtWidgets

from slicer.gcode import SliceSettings
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
        self._param.setText(param)
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
        for name in ("Global", "Objects", "Advanced"):
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

        self._advanced_toggle = QtWidgets.QCheckBox(process_row)
        self._advanced_toggle.setObjectName("SettingsToggle")
        self._advanced_toggle.setCursor(QtCore.Qt.PointingHandCursor)
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
        self._profile_combo.addItem("0.20mm Standard @Creality K1 Max...")
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
                "body": ("This is the starting position for each part of the outer wall.\n"
                         "https://wiki.creality.com/en/software/update-released/"
                         "toolbar-introduction/seam"),
                "param": "Parameter name: seam_position",
                "image": "seam_position",
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
        self._tooltip.adjustSize()

        anchor = obj.mapToGlobal(QtCore.QPoint(0, obj.height() // 2))
        panel_pos = self.mapToGlobal(QtCore.QPoint(0, 0))
        margin = 12

        screen = QtGui.QGuiApplication.screenAt(anchor)
        if screen is None:
            screen = QtGui.QGuiApplication.primaryScreen()
        geom = screen.availableGeometry() if screen is not None else QtCore.QRect(0, 0, 1920, 1080)

        tip_size = self._tooltip.sizeHint()
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

    def _section(self, title: str) -> Tuple[QtWidgets.QFrame, QtWidgets.QVBoxLayout]:
        section = QtWidgets.QFrame(self)
        section.setObjectName("SettingsSection")
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
                 use_native_tooltip: bool = True):
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

        section, section_layout = self._section("Seam")
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
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Precision")
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
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Walls and surfaces")
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
        for printer in self._printers:
            name = printer.get("name") if isinstance(printer, dict) else None
            self._printer_combo.addItem(name or "Printer")

    def current_printer(self):
        if not getattr(self, "_printers", None):
            return None
        idx = self._printer_combo.currentIndex()
        if idx < 0 or idx >= len(self._printers):
            return None
        return self._printers[idx]

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

    def _apply_search_filter(self, text: str):
        query = (text or "").strip().lower()
        page_index = int(self._pages_stack.currentIndex())
        if page_index < 0 or page_index >= len(self._page_keys):
            return
        key = self._page_keys[page_index]
        rows = self._search_rows.get(key, [])
        if not query:
            for section, row, _ in rows:
                section.setVisible(True)
                row.setVisible(True)
            return
        section_visible: Dict[QtWidgets.QFrame, bool] = {}
        for section, row, label in rows:
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
            precise_wall=bool(self.precise_wall_check.isChecked()),
            only_one_wall_top=bool(self.only_one_wall_top_check.isChecked()),
            only_one_wall_first_layer=bool(self.only_one_wall_first_layer_check.isChecked()),
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
        if "precise_wall" in data:
            self.precise_wall_check.setChecked(bool(data["precise_wall"]))
        if "only_one_wall_top" in data:
            self.only_one_wall_top_check.setChecked(bool(data["only_one_wall_top"]))
        if "only_one_wall_first_layer" in data:
            self.only_one_wall_first_layer_check.setChecked(bool(data["only_one_wall_first_layer"]))
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

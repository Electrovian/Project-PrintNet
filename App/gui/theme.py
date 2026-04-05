from PyQt5 import QtGui

_BASE_THEME = {
    "popup_bg": "#171b23",
    "popup_border": "#2c3443",
    "popup_header_bg": "#1e2531",
    "popup_text": "#ebeff7",
    "popup_muted_text": "#97a2b7",
    "popup_input_bg": "#0f141d",
    "popup_input_border": "#2f3a4c",
    "popup_input_text": "#ebeff7",
    "popup_button_bg": "#202938",
    "popup_button_border": "#31415e",
    "popup_button_text": "#e8edf8",
    "popup_button_hover_bg": "#273246",
    "popup_button_active_bg": "#2e3d56",
    "topbar_bg": "#121722",
    "topbar_border": "#202a3a",
    "topbar_text": "#ebeff7",
    "topbar_icon": "#8da0bd",
    "topbar_accent": "#3a74ff",
    "menu_bg": "#0f141d",
    "menu_text": "#ebeff7",
    "menu_border": "#2b3446",
    "menu_hover_bg": "#1d2533",
    "menu_disabled_text": "#5f6e88",
    "menu_sep": "#2a3344",
    "action_panel_bg": "#141b28",
    "action_panel_border": "#2b3446",
    "action_button_bg": "#1e2839",
    "action_button_text": "#e8edf8",
    "action_button_hover_bg": "#273246",
    "action_button_active_bg": "#2f3d55",
    "warning_bg": "#3a2415",
    "warning_border": "#8e5a2f",
    "warning_text": "#ffd39a",
    "rotate_reset": "#ff9933",
    "axis_x": "#ff6b6b",
    "axis_y": "#4cd964",
    "axis_z": "#4aa3ff",
    "cube_panel": (18, 24, 34),
    "cube_face": (50, 60, 79),
    "cube_border": (122, 141, 178),
    "cube_text": (247, 249, 253),
    "cube_accent": (70, 123, 255),
    "cube_hover": (98, 149, 255),
    "cube_active": (122, 171, 255),
    "view_bg": (16, 21, 30),
    "grid_color": (58, 70, 92, 255),
    "mesh_color": (0.96, 0.9, 0.56, 1.0),
    "mesh_edge_color": (0.62, 0.64, 0.68, 0.72),
    "mesh_warning": (1.0, 0.25, 0.2, 1.0),
    "gizmo_x": (1.0, 0.2, 0.2, 1.0),
    "gizmo_y": (0.2, 1.0, 0.3, 1.0),
    "gizmo_z": (0.2, 0.5, 1.0, 1.0),
    "gizmo_tick": (0.9, 0.9, 0.9, 1.0),
}

THEMES = {
    "DEFAULT": {**_BASE_THEME, "topbar_accent": "#3a74ff", "cube_accent": (58, 116, 255)},
    "professional": {**_BASE_THEME, "popup_bg": "#5f6166", "topbar_accent": "#22c46b"},
    "dark": _BASE_THEME.copy(),
    "summer": {**_BASE_THEME, "popup_bg": "#f1f0e6", "popup_text": "#2f2f2f"},
    "custom": _BASE_THEME.copy(),
}

_CURRENT_THEME_NAME = "dark"


def set_theme(name: str):
    global _CURRENT_THEME_NAME
    if name in THEMES:
        _CURRENT_THEME_NAME = name
    return THEMES[_CURRENT_THEME_NAME]


def register_theme(name: str, overrides: dict):
    if not isinstance(name, str) or not name:
        return None
    if not isinstance(overrides, dict):
        return None
    theme = dict(_BASE_THEME)
    theme.update(overrides)
    THEMES[name] = theme
    return theme


def get_theme_name():
    return _CURRENT_THEME_NAME


def export_theme(name: str | None = None):
    theme_name = name or _CURRENT_THEME_NAME
    theme = THEMES.get(theme_name)
    if theme is None:
        return None
    return dict(theme)


def get_theme():
    return THEMES[_CURRENT_THEME_NAME]


def theme_value(key: str, default=None):
    return get_theme().get(key, default)


def theme_qcolor(key: str):
    value = theme_value(key)
    if isinstance(value, QtGui.QColor):
        return value
    if isinstance(value, str):
        return QtGui.QColor(value)
    if isinstance(value, (tuple, list)):
        return QtGui.QColor(*value)
    return QtGui.QColor()


def theme_css(key: str):
    value = theme_value(key)
    if isinstance(value, str):
        return value
    if isinstance(value, QtGui.QColor):
        return value.name()
    if isinstance(value, (tuple, list)) and len(value) >= 3:
        r, g, b = int(value[0]), int(value[1]), int(value[2])
        return f"#{r:02x}{g:02x}{b:02x}"
    return "#000000"

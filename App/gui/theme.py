from PyQt5 import QtGui

_BASE_THEME = {
    "popup_bg": "#2f3137",
    "popup_border": "#4b4e57",
    "popup_header_bg": "#3a3d44",
    "popup_text": "#e6e6e6",
    "popup_muted_text": "#b8bcc3",
    "popup_input_bg": "#23252a",
    "popup_input_border": "#4b4e57",
    "popup_input_text": "#e6e6e6",
    "popup_button_bg": "#2e3036",
    "popup_button_border": "#4b4e57",
    "popup_button_text": "#e6e6e6",
    "popup_button_hover_bg": "#3a3d44",
    "popup_button_active_bg": "#454851",
    "topbar_bg": "#0d0e10",
    "topbar_border": "#24262b",
    "topbar_text": "#e6e6e6",
    "topbar_icon": "#b8bcc3",
    "topbar_accent": "#1dbb61",
    "menu_bg": "#23252a",
    "menu_text": "#e6e6e6",
    "menu_border": "#3a3d44",
    "menu_hover_bg": "#2e3036",
    "menu_disabled_text": "#6e7279",
    "menu_sep": "#3f4248",
    "action_panel_bg": "#23252a",
    "action_panel_border": "#3a3d44",
    "action_button_bg": "#2e3036",
    "action_button_text": "#e6e6e6",
    "action_button_hover_bg": "#3a3d44",
    "action_button_active_bg": "#454851",
    "rotate_reset": "#ff9933",
    "axis_x": "#ff6b6b",
    "axis_y": "#4cd964",
    "axis_z": "#4aa3ff",
    "cube_panel": (15, 16, 18),
    "cube_face": (22, 24, 28),
    "cube_border": (120, 124, 132),
    "cube_text": (245, 245, 245),
    "cube_accent": (0, 170, 255),
    "cube_hover": (70, 200, 120),
    "cube_active": (90, 150, 255),
    "view_bg": (15, 16, 18),
    "grid_color": (60, 63, 68, 255),
    "mesh_color": (0.0, 0.9, 0.6, 0.9),
    "gizmo_x": (1.0, 0.2, 0.2, 1.0),
    "gizmo_y": (0.2, 1.0, 0.3, 1.0),
    "gizmo_z": (0.2, 0.5, 1.0, 1.0),
    "gizmo_tick": (0.9, 0.9, 0.9, 1.0),
}

THEMES = {
    "DEFAULT": {**_BASE_THEME, "topbar_accent": "#19c15b", "cube_accent": (38, 140, 255)},
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

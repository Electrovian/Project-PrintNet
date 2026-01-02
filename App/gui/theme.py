from PyQt5 import QtGui

THEMES = {
    "DEFAULT": {
        "popup_bg": "#4b4d52",
        "popup_border": "#6c6f75",
        "popup_header_bg": "#5b5d63",
        "popup_text": "#f2f2f2",
        "popup_muted_text": "#cfd1d4",
        "popup_input_bg": "#3b3d42",
        "popup_input_border": "#6c6f75",
        "popup_input_text": "#f2f2f2",
        "popup_button_bg": "#4a4c51",
        "popup_button_border": "#6c6f75",
        "popup_button_text": "#f2f2f2",
        "popup_button_hover_bg": "#5b5d63",
        "popup_button_active_bg": "#6a6c72",
        "topbar_bg": "#0f0f10",
        "topbar_border": "#2a2c2f",
        "topbar_text": "#f0f0f0",
        "topbar_icon": "#cfd2d6",
        "topbar_accent": "#19c15b",
        "menu_bg": "#2b2d31",
        "menu_text": "#f0f0f0",
        "menu_border": "#3a3d41",
        "menu_hover_bg": "#3f4247",
        "menu_disabled_text": "#7c8086",
        "menu_sep": "#45484d",
        "action_panel_bg": "#2b2d31",
        "action_panel_border": "#3a3d41",
        "action_button_bg": "#3a3c40",
        "action_button_text": "#f0f0f0",
        "action_button_hover_bg": "#4a4d52",
        "action_button_active_bg": "#5a5d63",
        "rotate_reset": "#ff8a2a",
        "axis_x": "#e34b4b",
        "axis_y": "#35c36a",
        "axis_z": "#4b6fe3",
        "cube_panel": (18, 20, 24),
        "cube_face": (28, 31, 36),
        "cube_border": (160, 165, 170),
        "cube_text": (255, 255, 255),
        "cube_accent": (38, 140, 255),
        "cube_hover": (46, 204, 113),
        "cube_active": (58, 135, 255),
        "view_bg": (20, 22, 26),
        "grid_color": (80, 80, 80, 255),
        "mesh_color": (0.0, 0.9, 0.4, 0.9),
        "gizmo_x": (1.0, 0.1, 0.1, 1.0),
        "gizmo_y": (0.1, 1.0, 0.1, 1.0),
        "gizmo_z": (0.1, 0.4, 1.0, 1.0),
        "gizmo_tick": (1.0, 1.0, 1.0, 1.0),
    },
    "professional": {
        "popup_bg": "#5f6166",
        "popup_border": "#7a7d83",
        "popup_header_bg": "#6a6c71",
        "popup_text": "#f4f4f4",
        "popup_muted_text": "#d7d9dc",
        "popup_input_bg": "#4c4e53",
        "popup_input_border": "#7a7d83",
        "popup_input_text": "#f4f4f4",
        "popup_button_bg": "#585a60",
        "popup_button_border": "#7a7d83",
        "popup_button_text": "#f4f4f4",
        "popup_button_hover_bg": "#6a6c71",
        "popup_button_active_bg": "#76797f",
        "topbar_bg": "#1b1d20",
        "topbar_border": "#32353a",
        "topbar_text": "#f4f4f4",
        "topbar_icon": "#d7d9dc",
        "topbar_accent": "#22c46b",
        "menu_bg": "#35383d",
        "menu_text": "#f4f4f4",
        "menu_border": "#4a4d52",
        "menu_hover_bg": "#404449",
        "menu_disabled_text": "#8a8f96",
        "menu_sep": "#50545a",
        "action_panel_bg": "#35383d",
        "action_panel_border": "#4a4d52",
        "action_button_bg": "#44474d",
        "action_button_text": "#f4f4f4",
        "action_button_hover_bg": "#50545a",
        "action_button_active_bg": "#5b5f66",
        "rotate_reset": "#ff8a2a",
        "axis_x": "#e34b4b",
        "axis_y": "#35c36a",
        "axis_z": "#4b6fe3",
        "cube_panel": (26, 28, 32),
        "cube_face": (38, 40, 45),
        "cube_border": (170, 174, 179),
        "cube_text": (250, 250, 250),
        "cube_accent": (44, 174, 89),
        "cube_hover": (80, 220, 130),
        "cube_active": (58, 135, 255),
        "view_bg": (28, 30, 34),
        "grid_color": (90, 94, 98, 255),
        "mesh_color": (0.2, 0.8, 0.3, 0.9),
        "gizmo_x": (0.95, 0.15, 0.15, 1.0),
        "gizmo_y": (0.15, 0.95, 0.25, 1.0),
        "gizmo_z": (0.15, 0.45, 0.95, 1.0),
        "gizmo_tick": (1.0, 1.0, 1.0, 1.0),
    },
    "dark": {
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
    },
    "summer": {
        "popup_bg": "#f1f0e6",
        "popup_border": "#c5c0a9",
        "popup_header_bg": "#e0ddc8",
        "popup_text": "#2f2f2f",
        "popup_muted_text": "#4f4f4f",
        "popup_input_bg": "#ffffff",
        "popup_input_border": "#c5c0a9",
        "popup_input_text": "#2f2f2f",
        "popup_button_bg": "#e7e3cf",
        "popup_button_border": "#c5c0a9",
        "popup_button_text": "#2f2f2f",
        "popup_button_hover_bg": "#d8d4be",
        "popup_button_active_bg": "#cfcab5",
        "topbar_bg": "#f1f0e6",
        "topbar_border": "#c5c0a9",
        "topbar_text": "#2f2f2f",
        "topbar_icon": "#4f4f4f",
        "topbar_accent": "#2ea44f",
        "menu_bg": "#ffffff",
        "menu_text": "#2f2f2f",
        "menu_border": "#c5c0a9",
        "menu_hover_bg": "#ebe6d3",
        "menu_disabled_text": "#8a8570",
        "menu_sep": "#cfcab5",
        "action_panel_bg": "#f1f0e6",
        "action_panel_border": "#c5c0a9",
        "action_button_bg": "#e7e3cf",
        "action_button_text": "#2f2f2f",
        "action_button_hover_bg": "#d8d4be",
        "action_button_active_bg": "#cfcab5",
        "rotate_reset": "#cc6a21",
        "axis_x": "#d64a3a",
        "axis_y": "#2ea44f",
        "axis_z": "#2f6df6",
        "cube_panel": (236, 232, 216),
        "cube_face": (220, 214, 195),
        "cube_border": (140, 130, 110),
        "cube_text": (30, 30, 30),
        "cube_accent": (46, 164, 79),
        "cube_hover": (88, 200, 120),
        "cube_active": (58, 135, 255),
        "view_bg": (230, 225, 210),
        "grid_color": (170, 165, 150, 255),
        "mesh_color": (0.15, 0.7, 0.3, 0.9),
        "gizmo_x": (0.9, 0.25, 0.25, 1.0),
        "gizmo_y": (0.2, 0.8, 0.3, 1.0),
        "gizmo_z": (0.2, 0.45, 0.95, 1.0),
        "gizmo_tick": (0.3, 0.3, 0.3, 1.0),
    },
}

_CURRENT_THEME_NAME = "DEFAULT"


def set_theme(name: str):
    global _CURRENT_THEME_NAME
    if name in THEMES:
        _CURRENT_THEME_NAME = name
    return THEMES[_CURRENT_THEME_NAME]


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

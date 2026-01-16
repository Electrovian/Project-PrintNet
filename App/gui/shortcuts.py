from dataclasses import dataclass
from typing import Dict, List, Sequence


@dataclass(frozen=True)
class ShortcutDef:
    id: str
    label: str
    keys: str
    category: str


SHORTCUT_CATEGORIES = (
    "Global",
    "Prepare",
    "Toolbar",
    "Objects list",
    "Preview",
)

SHORTCUTS = [
    ShortcutDef("new_project", "New Project", "Ctrl+N", "Global"),
    ShortcutDef("open_project", "Open Project...", "Ctrl+O", "Global"),
    ShortcutDef("save_project", "Save Project", "Ctrl+S", "Global"),
    ShortcutDef("save_project_as", "Save Project as...", "Ctrl+Shift+S", "Global"),
    ShortcutDef("import_geometry", "Import geometry data from STL/STEP/3MF/OBJ/AMF files", "Ctrl+I", "Global"),
    ShortcutDef("export_gcode", "Export G-code", "Ctrl+G", "Global"),
    ShortcutDef("slice_plate", "Slice plate", "Ctrl+R", "Global"),
    ShortcutDef("print_plate", "Print plate", "Ctrl+Shift+G", "Global"),
    ShortcutDef("global_cut", "Cut", "Ctrl+X", "Global"),
    ShortcutDef("global_copy", "Copy to clipboard", "Ctrl+C", "Global"),
    ShortcutDef("global_paste", "Paste from clipboard", "Ctrl+V", "Global"),
    ShortcutDef("preferences", "Printer Preferences", "Ctrl+P", "Global"),
    ShortcutDef("show_3dconnexion", "Show/Hide 3Dconnexion devices settings dialog", "Ctrl+M", "Global"),
    ShortcutDef("switch_table_page", "Switch table page", "Ctrl+Tab", "Global"),
    ShortcutDef("global_delete_selected", "Delete Selected", "Del", "Global"),
    ShortcutDef("show_shortcuts", "Show keyboard shortcuts list", "?", "Global"),
    ShortcutDef("view_default", "Default View", "Ctrl+0", "Prepare"),
    ShortcutDef("view_top", "Top", "Ctrl+1", "Prepare"),
    ShortcutDef("view_bottom", "Bottom", "Ctrl+2", "Prepare"),
    ShortcutDef("view_front", "Front", "Ctrl+3", "Prepare"),
    ShortcutDef("view_rear", "Rear", "Ctrl+4", "Prepare"),
    ShortcutDef("view_left", "Left", "Ctrl+5", "Prepare"),
    ShortcutDef("view_right", "Right", "Ctrl+6", "Prepare"),
    ShortcutDef("show_labels", "Show Labels", "Ctrl+E", "Prepare"),
    ShortcutDef("prepare_mouse_wheel", "Zoom View", "Mouse wheel", "Prepare"),
    ShortcutDef("prepare_arrange_all", "Arrange all objects", "A", "Prepare"),
    ShortcutDef("prepare_arrange_selected", "Arrange objects on selected plates", "Shift+A", "Prepare"),
    ShortcutDef(
        "prepare_auto_orient",
        "This auto orients selected objects or all objects. If there are selected objects, it just orients the selected ones. Otherwise, it will orient all objects in the current plate.",
        "Shift+R",
        "Prepare",
    ),
    ShortcutDef("prepare_toggle_sidebar", "Collapse/Expand the sidebar", "Shift+Tab", "Prepare"),
    ShortcutDef("prepare_move_camera", "Movement in camera space", "Ctrl+Any arrow", "Prepare"),
    ShortcutDef("prepare_select_part", "Select a part", "Alt+Left mouse button", "Prepare"),
    ShortcutDef("prepare_select_multiple", "Select multiple objects", "Ctrl+Left mouse button", "Prepare"),
    ShortcutDef("prepare_move_up", "Move selection 10mm in positive Y direction", "Arrow Up", "Prepare"),
    ShortcutDef("prepare_move_down", "Move selection 10mm in negative Y direction", "Arrow Down", "Prepare"),
    ShortcutDef("prepare_move_left", "Move selection 10mm in negative X direction", "Arrow Left", "Prepare"),
    ShortcutDef("prepare_move_right", "Move selection 10mm in positive X direction", "Arrow Right", "Prepare"),
    ShortcutDef("prepare_move_step_1mm", "Movement step set to 1mm", "Shift+Any arrow", "Prepare"),
    ShortcutDef("prepare_deselect_all", "Deselect All", "Esc", "Prepare"),
    ShortcutDef("prepare_set_filament", "Keyboard 1-9: set filament for object/part", "1-9", "Prepare"),
    ShortcutDef("prepare_select_all", "Select all objects", "Ctrl+A", "Prepare"),
    ShortcutDef("prepare_delete_all", "Delete All", "Ctrl+D", "Prepare"),
    ShortcutDef("prepare_undo", "Undo", "Ctrl+Z", "Prepare"),
    ShortcutDef("prepare_redo", "Redo", "Ctrl+Y", "Prepare"),
    ShortcutDef("prepare_gizmo_move", "Gizmo move", "M", "Prepare"),
    ShortcutDef("prepare_gizmo_scale", "Gizmo scale", "S", "Prepare"),
    ShortcutDef("prepare_gizmo_rotate", "Gizmo rotate", "R", "Prepare"),
    ShortcutDef("prepare_gizmo_cut", "Gizmo cut", "C", "Prepare"),
    ShortcutDef("prepare_gizmo_place", "Gizmo Place face on bed", "F", "Prepare"),
    ShortcutDef("prepare_gizmo_sla", "Gizmo SLA support points", "L", "Prepare"),
    ShortcutDef("prepare_gizmo_fdm", "Gizmo FDM paint-on seam", "P", "Prepare"),
    ShortcutDef("prepare_gizmo_text", "Gizmo Text emboss / engrave", "T", "Prepare"),
    ShortcutDef("prepare_zoom_in", "Zoom in", "I", "Prepare"),
    ShortcutDef("prepare_zoom_out", "Zoom out", "O", "Prepare"),
    ShortcutDef("prepare_switch_mode", "Switch between Prepare/Preview", "Tab", "Prepare"),
    ShortcutDef("prepare_scheme1_left", "Select objects by rectangle", "Left mouse button", "Prepare"),
    ShortcutDef("prepare_scheme1_right", "Rotate View", "Right mouse button", "Prepare"),
    ShortcutDef("prepare_scheme1_shift_left", "Pan View", "Shift+Left mouse button", "Prepare"),
    ShortcutDef("prepare_scheme2_left", "Rotate View", "Left mouse button", "Prepare"),
    ShortcutDef("prepare_scheme2_right", "Pan View", "Right mouse button", "Prepare"),
    ShortcutDef("prepare_scheme2_shift_left", "Select objects by rectangle", "Shift+Left mouse button", "Prepare"),
    ShortcutDef("toolbar_deselect_all", "Deselect All", "Esc", "Toolbar"),
    ShortcutDef("toolbar_snap_1mm", "Move: press to snap by 1mm", "Shift", "Toolbar"),
    ShortcutDef("toolbar_paint_radius", "Support/Color Painting: adjust pen radius", "Ctrl+Mouse wheel", "Toolbar"),
    ShortcutDef("toolbar_paint_section", "Support/Color Painting: adjust section position", "Alt+Mouse wheel", "Toolbar"),
    ShortcutDef("undo", "Undo", "Ctrl+Z", "Objects list"),
    ShortcutDef("redo", "Redo", "Ctrl+Y", "Objects list"),
    ShortcutDef("cut", "Cut", "Ctrl+X", "Objects list"),
    ShortcutDef("copy", "Copy", "Ctrl+C", "Objects list"),
    ShortcutDef("paste", "Paste", "Ctrl+V", "Objects list"),
    ShortcutDef("delete_selected", "Delete Selected", "Del", "Objects list"),
    ShortcutDef("delete_all", "Delete All", "Ctrl+D", "Objects list"),
    ShortcutDef("clone_selected", "Clone Selected", "Ctrl+K", "Objects list"),
    ShortcutDef("select_all", "Select All", "Ctrl+A", "Objects list"),
    ShortcutDef("deselect_all", "Deselect All", "Esc", "Objects list"),
    ShortcutDef("objects_set_extruder", "Set extruder number for the objects and parts", "1-9", "Objects list"),
    ShortcutDef("objects_copy", "Copy to clipboard", "Ctrl+C", "Objects list"),
    ShortcutDef("objects_paste", "Paste from clipboard", "Ctrl+V", "Objects list"),
    ShortcutDef("objects_cut", "Cut", "Ctrl+X", "Objects list"),
    ShortcutDef("objects_space_rename", "Select the object/part and press space to change the name", "Space", "Objects list"),
    ShortcutDef("objects_click_rename", "Select the object/part and mouse click to change the name", "Mouse click", "Objects list"),
    ShortcutDef("objects_alt_click", "Mouse clicks can select parts in the assembly model", "Alt", "Objects list"),
    ShortcutDef("objects_center_selected", "Center Selected", "F3", "Objects list"),
    ShortcutDef("preview_arrow_up", "Vertical slider - Move active thumb Up", "Arrow Up", "Preview"),
    ShortcutDef("preview_arrow_down", "Vertical slider - Move active thumb Down", "Arrow Down", "Preview"),
    ShortcutDef("preview_arrow_left", "Horizontal slider - Move active thumb Left", "Arrow Left", "Preview"),
    ShortcutDef("preview_arrow_right", "Horizontal slider - Move active thumb Right", "Arrow Right", "Preview"),
    ShortcutDef("preview_toggle_layer", "On/Off one layer mode of the vertical slider", "L", "Preview"),
    ShortcutDef("preview_toggle_gcode", "On/Off g-code window", "C", "Preview"),
    ShortcutDef("preview_switch_mode", "Switch between Prepare/Preview", "Tab", "Preview"),
    ShortcutDef("preview_shift_arrow", "Move slider 5x faster", "Shift+Any arrow", "Preview"),
    ShortcutDef("preview_shift_wheel", "Move slider 5x faster", "Shift+Mouse wheel", "Preview"),
    ShortcutDef("preview_ctrl_arrow", "Move slider 5x faster", "Ctrl+Any arrow", "Preview"),
    ShortcutDef("preview_ctrl_wheel", "Move slider 5x faster", "Ctrl+Mouse wheel", "Preview"),
    ShortcutDef("preview_home", "Horizontal slider - Move to start position", "Home", "Preview"),
    ShortcutDef("preview_end", "Horizontal slider - Move to last position", "End", "Preview"),
]

SHORTCUTS_BY_ID = {shortcut.id: shortcut for shortcut in SHORTCUTS}


def shortcut_label(action_id: str) -> str:
    return SHORTCUTS_BY_ID[action_id].label


def shortcut_key(action_id: str) -> str:
    return SHORTCUTS_BY_ID[action_id].keys


def shortcut_category(action_id: str) -> str:
    return SHORTCUTS_BY_ID[action_id].category


def shortcuts_by_category(categories: Sequence[str] = SHORTCUT_CATEGORIES) -> Dict[str, List[ShortcutDef]]:
    grouped = {name: [] for name in categories}
    for shortcut in SHORTCUTS:
        grouped.setdefault(shortcut.category, []).append(shortcut)
    return grouped

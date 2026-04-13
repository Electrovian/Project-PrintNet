from __future__ import annotations

from PyQt5 import QtWidgets, QtGui, QtCore

from .shortcuts import shortcut_key


class TransformToolbar(QtWidgets.QToolBar):
    actionTriggered = QtCore.pyqtSignal(str)

    ACTION_DEFS = (
        ("actions", "add_model", "Add", "prepare_add_model", False),
        ("actions", "add_plate", "Add plate", "prepare_add_plate", False),
        ("actions", "auto_orient", "Auto orient", "prepare_auto_orient", False),
        ("actions", "arrange", "Arrange", "prepare_arrange_all", False),
        ("actions", "add_instance", "Add instance", "prepare_add_instance", False),
        ("actions", "remove_instance", "Remove instance", "prepare_remove_instance", False),
        ("actions", "split_objects", "Split to objects", "prepare_split_objects", False),
        ("actions", "split_parts", "Split to parts", "prepare_split_parts", False),
        ("actions", "variable_layer", "Variable layer height", "prepare_variable_layer", False),
        ("actions", "assembly_view", "Assembly View", "prepare_gizmo_assembly", True),
        ("gizmos", "move", "Move", "prepare_gizmo_move", True),
        ("gizmos", "rotate", "Rotate", "prepare_gizmo_rotate", True),
        ("gizmos", "scale", "Scale", "prepare_gizmo_scale", True),
        ("gizmos", "lay_on_face", "Lay on Face", "prepare_gizmo_place", False),
        ("gizmos", "cut", "Cut", "prepare_gizmo_cut", True),
        ("gizmos", "mesh_boolean", "Mesh Boolean", "prepare_mesh_boolean", False),
        ("gizmos", "support_paint", "Support Painting", "prepare_gizmo_sla", True),
        ("gizmos", "seam_paint", "Seam Painting", "prepare_gizmo_fdm", True),
        ("gizmos", "fuzzy_paint", "Paint-on fuzzy skin", "prepare_gizmo_fuzzy", True),
        ("gizmos", "emboss", "Emboss", "prepare_gizmo_text", False),
        ("gizmos", "measure", "Measure", "prepare_gizmo_measure", True),
        ("gizmos", "brim_ears", "Brim Ears", "prepare_gizmo_brim_ears", False),
    )

    MODE_ACTIONS = {
        "move",
        "rotate",
        "scale",
        "cut",
        "support_paint",
        "seam_paint",
        "fuzzy_paint",
        "measure",
        "assembly_view",
    }

    def __init__(self, parent=None):
        super().__init__("Prepare", parent)
        self.setMovable(False)
        self.setFloatable(False)
        self.setIconSize(QtCore.QSize(26, 26))
        self._actions: dict[str, QtWidgets.QAction] = {}
        self._buttons: dict[str, QtWidgets.QToolButton] = {}
        self._build_ui()

    @property
    def action_registry(self) -> dict[str, QtWidgets.QAction]:
        return dict(self._actions)

    def _build_ui(self):
        container = QtWidgets.QWidget(self)
        root = QtWidgets.QVBoxLayout(container)
        root.setContentsMargins(8, 6, 8, 6)
        root.setSpacing(6)

        action_row = QtWidgets.QHBoxLayout()
        action_row.setContentsMargins(0, 0, 0, 0)
        action_row.setSpacing(4)
        gizmo_row = QtWidgets.QHBoxLayout()
        gizmo_row.setContentsMargins(0, 0, 0, 0)
        gizmo_row.setSpacing(4)

        action_group = QtWidgets.QActionGroup(self)
        action_group.setExclusive(True)

        for row_name, action_id, label, shortcut_id, checkable in self.ACTION_DEFS:
            action = QtWidgets.QAction(self._icon_for_action(action_id), label, self)
            action.setData(action_id)
            action.setToolTip(f"{label} [{shortcut_key(shortcut_id)}]" if shortcut_id else label)
            action.setCheckable(bool(checkable))
            if shortcut_id:
                action.setShortcut(shortcut_key(shortcut_id))
            if action_id in self.MODE_ACTIONS:
                action_group.addAction(action)
            action.triggered.connect(lambda checked=False, aid=action_id: self._on_action_triggered(aid))
            self._actions[action_id] = action

            button = QtWidgets.QToolButton(container)
            button.setObjectName("PrepareToolButton")
            button.setAutoRaise(True)
            button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
            button.setDefaultAction(action)
            button.setCursor(QtCore.Qt.PointingHandCursor)
            button.setFixedSize(34, 34)
            self._buttons[action_id] = button
            if row_name == "actions":
                action_row.addWidget(button)
            else:
                gizmo_row.addWidget(button)

        self._actions["move"].setChecked(True)
        self.move_action = self._actions["move"]
        self.rotate_action = self._actions["rotate"]
        self.scale_action = self._actions["scale"]
        self.auto_orient_action = self._actions["auto_orient"]
        self.auto_arrange_action = self._actions["arrange"]
        self.lay_on_face_action = self._actions["lay_on_face"]

        root.addLayout(action_row)
        root.addLayout(gizmo_row)
        self.addWidget(container)
        self._container = container
        self._action_row = action_row
        self._gizmo_row = gizmo_row
        self._apply_style()

    def _on_action_triggered(self, action_id: str):
        if action_id not in self.MODE_ACTIONS:
            for mode_action in self.MODE_ACTIONS:
                action = self._actions.get(mode_action)
                if action is not None and action_id != mode_action and mode_action != self.active_tool():
                    action.setChecked(mode_action == self.active_tool())
        self.actionTriggered.emit(str(action_id))

    def active_tool(self) -> str:
        for action_id in self.MODE_ACTIONS:
            action = self._actions.get(action_id)
            if action is not None and action.isChecked():
                return action_id
        return "move"

    def set_active_tool(self, action_id: str):
        resolved = str(action_id or "").strip()
        if resolved not in self.MODE_ACTIONS:
            resolved = "move"
        for key, action in self._actions.items():
            if key in self.MODE_ACTIONS:
                prev = action.blockSignals(True)
                action.setChecked(key == resolved)
                action.blockSignals(prev)

    def set_action_enabled(self, action_id: str, enabled: bool):
        action = self._actions.get(str(action_id))
        if action is not None:
            action.setEnabled(bool(enabled))

    def widgetForAction(self, action):  # type: ignore[override]
        if isinstance(action, QtWidgets.QAction):
            action_id = str(action.data() or "")
            if action_id in self._buttons:
                return self._buttons[action_id]
        return super().widgetForAction(action)

    def _apply_style(self):
        self.setStyleSheet(
            "QToolBar { border: none; spacing: 0; }"
            "QToolButton#PrepareToolButton {"
            "  border: 1px solid transparent;"
            "  border-radius: 4px;"
            "  padding: 2px;"
            "}"
            "QToolButton#PrepareToolButton:hover {"
            "  background: rgba(127, 127, 127, 0.12);"
            "  border-color: rgba(127, 127, 127, 0.22);"
            "}"
            "QToolButton#PrepareToolButton:checked {"
            "  background: rgba(0, 174, 169, 0.16);"
            "  border-color: rgba(0, 174, 169, 0.55);"
            "}"
        )

    def _icon_for_action(self, action_id: str) -> QtGui.QIcon:
        size = 24
        pm = QtGui.QPixmap(size, size)
        pm.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pm)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        pen = QtGui.QPen(QtGui.QColor("#4f555a"), 1.7)
        pen.setCapStyle(QtCore.Qt.RoundCap)
        pen.setJoinStyle(QtCore.Qt.RoundJoin)
        accent = QtGui.QColor("#00aea9")
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.NoBrush)

        if action_id == "add_model":
            painter.drawRect(4, 5, 12, 12)
            painter.drawLine(18, 14, 22, 14)
            painter.drawLine(20, 12, 20, 16)
        elif action_id == "add_plate":
            for offset in (5, 10, 15):
                painter.drawLine(4, offset, 18, offset)
                painter.drawLine(offset, 4, offset, 18)
            painter.drawLine(18, 18, 22, 18)
            painter.drawLine(20, 16, 20, 20)
        elif action_id == "auto_orient":
            painter.drawPolygon(QtGui.QPolygonF([QtCore.QPointF(12, 3), QtCore.QPointF(21, 12), QtCore.QPointF(12, 21), QtCore.QPointF(3, 12)]))
            painter.drawLine(6, 18, 10, 22)
            painter.drawLine(10, 22, 15, 17)
        elif action_id == "arrange":
            for x in (4, 12):
                for y in (4, 12):
                    painter.drawRoundedRect(QtCore.QRectF(x, y, 7, 7), 1.5, 1.5)
        elif action_id == "add_instance":
            painter.drawEllipse(QtCore.QRectF(4, 4, 16, 16))
            painter.setPen(QtGui.QPen(accent, 1.7))
            painter.drawLine(17, 17, 22, 17)
            painter.drawLine(QtCore.QLineF(19.5, 14.5, 19.5, 19.5))
        elif action_id == "remove_instance":
            painter.drawEllipse(QtCore.QRectF(4, 4, 16, 16))
            painter.setPen(QtGui.QPen(accent, 1.7))
            painter.drawLine(17, 17, 22, 17)
        elif action_id == "split_objects":
            painter.drawRoundedRect(QtCore.QRectF(3.5, 5.0, 7.5, 14.0), 1.5, 1.5)
            painter.drawRoundedRect(QtCore.QRectF(13.0, 5.0, 7.5, 14.0), 1.5, 1.5)
        elif action_id == "split_parts":
            for y in (6, 11, 16):
                painter.drawLine(4, y, 20, y)
        elif action_id == "variable_layer":
            for x in (5, 10, 15):
                painter.drawLine(x, 5, x, 19)
            painter.drawLine(17, 17, 21, 21)
            painter.drawLine(19, 15, 21, 21)
        elif action_id == "assembly_view":
            painter.drawRect(4, 4, 7, 7)
            painter.drawRect(13, 4, 7, 7)
            painter.drawRect(4, 13, 7, 7)
            painter.drawRect(13, 13, 7, 7)
        elif action_id == "move":
            painter.drawLine(12, 3, 12, 21)
            painter.drawLine(3, 12, 21, 12)
            painter.drawLine(9, 6, 12, 3)
            painter.drawLine(15, 6, 12, 3)
        elif action_id == "rotate":
            painter.drawArc(QtCore.QRectF(4, 4, 16, 16), 40 * 16, 280 * 16)
            painter.drawLine(16, 4, 20, 4)
            painter.drawLine(20, 4, 20, 8)
        elif action_id == "scale":
            painter.drawRect(5, 5, 14, 14)
            painter.drawLine(18, 6, 22, 2)
            painter.drawLine(18, 6, 22, 6)
        elif action_id == "lay_on_face":
            painter.drawPolygon(QtGui.QPolygonF([QtCore.QPointF(12, 3), QtCore.QPointF(21, 12), QtCore.QPointF(12, 21), QtCore.QPointF(3, 12)]))
            painter.drawLine(4, 20, 20, 20)
        elif action_id == "cut":
            painter.drawLine(6, 4, 18, 16)
            painter.drawLine(18, 4, 6, 16)
            painter.drawLine(4, 20, 20, 20)
        elif action_id == "mesh_boolean":
            painter.drawEllipse(QtCore.QRectF(4, 6, 9, 9))
            painter.drawEllipse(QtCore.QRectF(11, 6, 9, 9))
        elif action_id == "support_paint":
            painter.drawLine(6, 5, 18, 5)
            painter.drawLine(6, 10, 16, 10)
            painter.drawLine(6, 15, 14, 15)
            painter.drawLine(16, 15, 20, 19)
        elif action_id == "seam_paint":
            for y in (5, 8, 11, 14, 17):
                painter.drawLine(6, y, 18, y)
            painter.drawLine(17, 14, 21, 18)
        elif action_id == "fuzzy_paint":
            path = QtGui.QPainterPath()
            path.moveTo(5, 16)
            path.cubicTo(8, 7, 16, 20, 20, 8)
            painter.drawPath(path)
        elif action_id == "emboss":
            font = painter.font()
            font.setBold(True)
            font.setPointSize(12)
            painter.setFont(font)
            painter.drawText(pm.rect(), QtCore.Qt.AlignCenter, "T")
        elif action_id == "measure":
            painter.drawLine(4, 18, 20, 6)
            painter.drawLine(4, 18, 7, 18)
            painter.drawLine(20, 6, 20, 9)
        elif action_id == "brim_ears":
            painter.drawEllipse(QtCore.QRectF(4, 7, 6, 10))
            painter.drawEllipse(QtCore.QRectF(14, 7, 6, 10))
            painter.drawLine(10, 12, 14, 12)
        else:
            font = painter.font()
            font.setBold(True)
            font.setPointSize(8)
            painter.setFont(font)
            painter.drawText(pm.rect(), QtCore.Qt.AlignCenter, action_id[:2].upper())

        painter.end()
        return QtGui.QIcon(pm)

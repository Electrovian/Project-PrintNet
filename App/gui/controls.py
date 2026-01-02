from PyQt5 import QtWidgets, QtGui, QtCore

class TransformToolbar(QtWidgets.QToolBar):
    """Toolbar with transform actions (icons are temporary placeholders)."""
    addRequested = QtCore.pyqtSignal()
    moveRequested = QtCore.pyqtSignal()
    rotateRequested = QtCore.pyqtSignal()
    scaleRequested = QtCore.pyqtSignal()
    autoOrientRequested = QtCore.pyqtSignal()
    autoArrangeRequested = QtCore.pyqtSignal()
    layOnFaceRequested = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__("Transform", parent)
        self.setMovable(False)
        self.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.setIconSize(QtCore.QSize(28, 28))
        self._build_actions()

    def _build_actions(self):
        self.add_action = self._add_icon_action("Add", "ADD", 0)
        self.add_action.triggered.connect(self.addRequested.emit)

        self.addSeparator()

        group = QtWidgets.QActionGroup(self)
        group.setExclusive(True)

        self.move_action = self._add_icon_action("Move", "MV", 1, checkable=True)
        self.rotate_action = self._add_icon_action("Rotate", "RT", 2, checkable=True)
        self.scale_action = self._add_icon_action("Scale", "SC", 3, checkable=True)

        group.addAction(self.move_action)
        group.addAction(self.rotate_action)
        group.addAction(self.scale_action)
        self.move_action.setChecked(True)

        self.move_action.triggered.connect(self.moveRequested.emit)
        self.rotate_action.triggered.connect(self.rotateRequested.emit)
        self.scale_action.triggered.connect(self.scaleRequested.emit)

        self.addSeparator()

        self.auto_orient_action = self._add_icon_action("Auto Orient", "AO", 4)
        self.auto_arrange_action = self._add_icon_action("Auto Arrange", "AR", 5)
        self.lay_on_face_action = self._add_icon_action("Lay on Face", "LF", 6)

        self.auto_orient_action.triggered.connect(self.autoOrientRequested.emit)
        self.auto_arrange_action.triggered.connect(self.autoArrangeRequested.emit)
        self.lay_on_face_action.triggered.connect(self.layOnFaceRequested.emit)

    def _add_icon_action(self, label: str, short_label: str, variant: int, checkable: bool = False):
        action = QtWidgets.QAction(self._make_temp_icon(short_label, variant), label, self)
        action.setCheckable(checkable)
        self.addAction(action)
        return action

    def _make_temp_icon(self, short_label: str, variant: int):
        size = 28
        pm = QtGui.QPixmap(size, size)
        pm.fill(QtCore.Qt.transparent)

        pal = self.palette()
        base = pal.color(QtGui.QPalette.Button)
        border = pal.color(QtGui.QPalette.Dark)
        text = pal.color(QtGui.QPalette.ButtonText)

        accent = pal.color(QtGui.QPalette.Highlight)
        hue = accent.hue()
        if hue < 0:
            hue = 200
        accent = QtGui.QColor.fromHsv((hue + variant * 40) % 360, max(80, accent.saturation()), accent.value())

        p = QtGui.QPainter(pm)
        p.setRenderHint(QtGui.QPainter.Antialiasing, True)
        p.setPen(QtGui.QPen(border, 1))
        p.setBrush(QtGui.QBrush(base))
        p.drawRoundedRect(1, 1, size - 2, size - 2, 6, 6)

        p.setBrush(QtGui.QBrush(accent))
        p.setPen(QtCore.Qt.NoPen)
        p.drawEllipse(size - 9, 3, 6, 6)

        font = p.font()
        font.setBold(True)
        font.setPointSize(8)
        p.setFont(font)
        p.setPen(QtGui.QPen(text))
        p.drawText(pm.rect(), QtCore.Qt.AlignCenter, short_label)
        p.end()

        return QtGui.QIcon(pm)

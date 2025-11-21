from PyQt5 import QtWidgets

class TransformToolbar(QtWidgets.QToolBar):
    """Toolbar with basic transform actions (lay flat, center, reset)."""
    def __init__(self, parent=None):
        super().__init__("Transform", parent)
        self.setMovable(False)
        self.lay_flat_action = self.addAction("Lay Flat")
        self.center_action = self.addAction("Center")
        self.reset_action = self.addAction("Reset")

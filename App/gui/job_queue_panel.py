from PyQt5 import QtWidgets, QtCore

class JobQueuePanel(QtWidgets.QWidget):
    """Very simple local job queue panel."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        btn_layout = QtWidgets.QHBoxLayout()
        self.add_btn = QtWidgets.QPushButton("Add current model")
        self.remove_btn = QtWidgets.QPushButton("Remove")
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.remove_btn)

        layout.addWidget(self.list_widget)
        layout.addLayout(btn_layout)

        self.remove_btn.clicked.connect(self._remove_selected)

    def add_job(self, description: str, payload: dict):
        item = QtWidgets.QListWidgetItem(description)
        item.setData(QtCore.Qt.UserRole, payload)
        self.list_widget.addItem(item)

    def get_selected_job(self):
        item = self.list_widget.currentItem()
        if not item:
            return None
        return item.data(QtCore.Qt.UserRole)

    def _remove_selected(self):
        row = self.list_widget.currentRow()
        if row >= 0:
            self.list_widget.takeItem(row)

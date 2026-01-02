from PyQt5 import QtWidgets, QtCore


class ModelPanel(QtWidgets.QWidget):
    """Panel listing all loaded models with ability to remove/select."""
    MAX_DISPLAY_NAME = 28

    model_selected = QtCore.pyqtSignal(int)  # model_id
    request_remove = QtCore.pyqtSignal(int)  # model_id

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        layout.addWidget(self.list_widget)

        btn_row = QtWidgets.QHBoxLayout()
        self.remove_btn = QtWidgets.QPushButton("Remove selected")
        btn_row.addStretch(1)
        btn_row.addWidget(self.remove_btn)
        layout.addLayout(btn_row)

        self.list_widget.currentItemChanged.connect(self._on_selection_changed)
        self.remove_btn.clicked.connect(self._on_remove_clicked)

    def add_model(self, name: str, model_id: int):
        full_name = (name or "").strip()
        if not full_name:
            full_name = f"Model {model_id}"
        display_name = self._truncate_name(full_name)
        item = QtWidgets.QListWidgetItem(display_name)
        item.setToolTip(full_name)
        item.setData(QtCore.Qt.UserRole, model_id)
        self.list_widget.addItem(item)
        self.list_widget.setCurrentItem(item)

    def remove_model(self, model_id: int):
        for row in range(self.list_widget.count()):
            item = self.list_widget.item(row)
            if item is None:
                continue
            if item.data(QtCore.Qt.UserRole) == model_id:
                self.list_widget.takeItem(row)
                break

    def current_model_id(self):
        return item.data(QtCore.Qt.UserRole) if (item := self.list_widget.currentItem()) else None

    def _on_selection_changed(self, current, previous):
        if current:
            self.model_selected.emit(current.data(QtCore.Qt.UserRole))

    def _on_remove_clicked(self):
        if (mid := self.current_model_id()) is not None:
            self.request_remove.emit(mid)

    def _truncate_name(self, name: str) -> str:
        return name if len(name) <= self.MAX_DISPLAY_NAME else name[: self.MAX_DISPLAY_NAME - 3] + "..."

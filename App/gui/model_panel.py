from PyQt5 import QtWidgets, QtCore


class ModelPanel(QtWidgets.QWidget):
    """Panel listing all loaded models with ability to remove/select."""
    MAX_DISPLAY_NAME = 28

    model_selected = QtCore.pyqtSignal(int)  # model_id
    selection_changed = QtCore.pyqtSignal(list)  # model_ids
    request_remove = QtCore.pyqtSignal(int)  # model_id
    duplicate_requested = QtCore.pyqtSignal(int, int, int)  # count, rows, cols
    select_all_requested = QtCore.pyqtSignal()
    deselect_all_requested = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ObjectsPanel")
        self._build_ui()

    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.setObjectName("ObjectsList")
        self.list_widget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        layout.addWidget(self.list_widget)

        select_row = QtWidgets.QHBoxLayout()
        self.select_all_btn = QtWidgets.QPushButton("Select all")
        self.select_all_btn.setObjectName("ObjectsButton")
        self.clear_selection_btn = QtWidgets.QPushButton("Clear selection")
        self.clear_selection_btn.setObjectName("ObjectsButton")
        select_row.addWidget(self.select_all_btn)
        select_row.addWidget(self.clear_selection_btn)
        layout.addLayout(select_row)

        btn_row = QtWidgets.QHBoxLayout()
        self.duplicate_btn = QtWidgets.QPushButton("Duplicate")
        self.duplicate_btn.setObjectName("ObjectsButton")
        self.remove_btn = QtWidgets.QPushButton("Remove selected")
        self.remove_btn.setObjectName("ObjectsButton")
        btn_row.addWidget(self.duplicate_btn)
        btn_row.addStretch(1)
        btn_row.addWidget(self.remove_btn)
        layout.addLayout(btn_row)

        self.list_widget.currentItemChanged.connect(self._on_current_changed)
        self.list_widget.itemSelectionChanged.connect(self._on_selection_changed)
        self.remove_btn.clicked.connect(self._on_remove_clicked)
        self.duplicate_btn.clicked.connect(self._on_duplicate_clicked)
        self.select_all_btn.clicked.connect(self._on_select_all_clicked)
        self.clear_selection_btn.clicked.connect(self._on_clear_selection_clicked)

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

    def _on_selection_changed(self):
        selected = []
        for row in range(self.list_widget.count()):
            item = self.list_widget.item(row)
            if item is not None and item.isSelected():
                selected.append(item.data(QtCore.Qt.UserRole))
        self.selection_changed.emit(selected)

    def _on_current_changed(self, current, previous):
        _ = previous
        if current:
            self.model_selected.emit(current.data(QtCore.Qt.UserRole))

    def _on_remove_clicked(self):
        if (mid := self.current_model_id()) is not None:
            self.request_remove.emit(mid)

    def _on_duplicate_clicked(self):
        dlg = DuplicateDialog(self)
        if dlg.exec_() != QtWidgets.QDialog.Accepted:
            return
        count, rows, cols = dlg.values()
        if count > 0:
            self.duplicate_requested.emit(count, rows, cols)

    def _on_select_all_clicked(self):
        self.select_all_requested.emit()

    def _on_clear_selection_clicked(self):
        self.deselect_all_requested.emit()

    def _truncate_name(self, name: str) -> str:
        return name if len(name) <= self.MAX_DISPLAY_NAME else name[: self.MAX_DISPLAY_NAME - 3] + "..."


class DuplicateDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Duplicate")
        self.setModal(True)
        layout = QtWidgets.QFormLayout(self)

        self.count_spin = QtWidgets.QSpinBox(self)
        self.count_spin.setRange(1, 200)
        self.count_spin.setValue(1)
        layout.addRow("Copy count", self.count_spin)

        self.rows_spin = QtWidgets.QSpinBox(self)
        self.rows_spin.setRange(1, 200)
        self.rows_spin.setValue(1)
        layout.addRow("Grid rows", self.rows_spin)

        self.cols_spin = QtWidgets.QSpinBox(self)
        self.cols_spin.setRange(1, 200)
        self.cols_spin.setValue(1)
        layout.addRow("Grid columns", self.cols_spin)

        btn_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addRow(btn_box)

    def values(self):
        return (int(self.count_spin.value()),
                int(self.rows_spin.value()),
                int(self.cols_spin.value()))

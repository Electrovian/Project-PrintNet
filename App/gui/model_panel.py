from __future__ import annotations

from typing import Iterable

from PyQt5 import QtWidgets, QtCore


class SceneTreeWidget(QtWidgets.QTreeWidget):
    ENTITY_ROLE = QtCore.Qt.UserRole
    MODEL_ID_ROLE = QtCore.Qt.UserRole + 1

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderHidden(True)
        self.setRootIsDecorated(True)
        self.setUniformRowHeights(False)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

    def _leaf_items(self) -> list[QtWidgets.QTreeWidgetItem]:
        leaves: list[QtWidgets.QTreeWidgetItem] = []

        def visit(item: QtWidgets.QTreeWidgetItem):
            entity_type = str(item.data(0, self.ENTITY_ROLE) or "")
            if entity_type == "instance" and item.data(0, self.MODEL_ID_ROLE) is not None:
                leaves.append(item)
            for index in range(item.childCount()):
                visit(item.child(index))

        for index in range(self.topLevelItemCount()):
            visit(self.topLevelItem(index))
        return leaves

    def count(self) -> int:
        return len(self._leaf_items())

    def item(self, row: int):
        leaves = self._leaf_items()
        if 0 <= int(row) < len(leaves):
            return leaves[int(row)]
        return None

    def setCurrentRow(self, row: int):
        selected_ids = {
            int(item.data(0, self.MODEL_ID_ROLE))
            for item in self.selectedItems()
            if item.data(0, self.MODEL_ID_ROLE) is not None
        }
        item = self.item(int(row))
        if item is not None:
            self.setCurrentItem(item)
            for leaf in self._leaf_items():
                leaf_id = leaf.data(0, self.MODEL_ID_ROLE)
                if leaf_id is not None and int(leaf_id) in selected_ids:
                    leaf.setSelected(True)

    def selectAll(self):
        self.clearSelection()
        for item in self._leaf_items():
            item.setSelected(True)


class ModelPanel(QtWidgets.QWidget):
    MAX_DISPLAY_NAME = 48

    model_selected = QtCore.pyqtSignal(int)
    selection_changed = QtCore.pyqtSignal(list)
    request_remove = QtCore.pyqtSignal(int)
    duplicate_requested = QtCore.pyqtSignal(int, int, int)
    select_all_requested = QtCore.pyqtSignal()
    deselect_all_requested = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ObjectsPanel")
        self._build_ui()

    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        self.list_widget = SceneTreeWidget(self)
        self.list_widget.setObjectName("ObjectsTree")
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

    def refresh_from_viewer(self, viewer):
        tree = self.list_widget
        block = tree.blockSignals(True)
        try:
            tree.clear()
            if viewer is None or not hasattr(viewer, "scene_state"):
                return
            scene = viewer.scene_state
            for plate_id in viewer.get_plate_ids():
                plate = scene.plates.get(int(plate_id))
                if plate is None:
                    continue
                plate_item = QtWidgets.QTreeWidgetItem([f"Plate {str(plate.name or plate_id).strip() or plate_id}"])
                plate_item.setData(0, SceneTreeWidget.ENTITY_ROLE, "plate")
                plate_item.setData(0, SceneTreeWidget.MODEL_ID_ROLE, None)
                tree.addTopLevelItem(plate_item)

                instance_ids = viewer.get_plate_model_ids(int(plate_id))
                object_ids = []
                for instance_id in instance_ids:
                    model = viewer.models.get(int(instance_id), {})
                    object_id = int(model.get("object_id", 0))
                    if object_id and object_id not in object_ids:
                        object_ids.append(object_id)

                for object_id in object_ids:
                    obj = scene.objects.get(int(object_id))
                    if obj is None:
                        continue
                    object_item = QtWidgets.QTreeWidgetItem([self._truncate_name(str(obj.name or f"Object {object_id}"))])
                    object_item.setToolTip(0, str(obj.name or f"Object {object_id}"))
                    object_item.setData(0, SceneTreeWidget.ENTITY_ROLE, "object")
                    object_item.setData(0, SceneTreeWidget.MODEL_ID_ROLE, self._first_instance_id_for_object(viewer, int(object_id), int(plate_id)))
                    plate_item.addChild(object_item)

                    for part_id in obj.part_ids:
                        part = scene.parts.get(int(part_id))
                        if part is None:
                            continue
                        part_item = QtWidgets.QTreeWidgetItem([self._truncate_name(str(part.name or f"Part {part_id}"))])
                        part_item.setToolTip(0, str(part.name or f"Part {part_id}"))
                        part_item.setData(0, SceneTreeWidget.ENTITY_ROLE, "part")
                        part_item.setData(0, SceneTreeWidget.MODEL_ID_ROLE, self._first_instance_id_for_object(viewer, int(object_id), int(plate_id)))
                        object_item.addChild(part_item)

                    for instance_id in instance_ids:
                        model = viewer.models.get(int(instance_id), {})
                        if int(model.get("object_id", 0)) != int(object_id):
                            continue
                        label = str(model.get("name") or f"Instance {instance_id}")
                        instance_item = QtWidgets.QTreeWidgetItem([self._truncate_name(label)])
                        instance_item.setToolTip(0, label)
                        instance_item.setData(0, SceneTreeWidget.ENTITY_ROLE, "instance")
                        instance_item.setData(0, SceneTreeWidget.MODEL_ID_ROLE, int(instance_id))
                        object_item.addChild(instance_item)

                    object_item.setExpanded(True)
                plate_item.setExpanded(True)
        finally:
            tree.blockSignals(block)

    def add_model(self, name: str, model_id: int):
        full_name = (name or "").strip() or f"Model {model_id}"
        item = QtWidgets.QTreeWidgetItem([self._truncate_name(full_name)])
        item.setToolTip(0, full_name)
        item.setData(0, SceneTreeWidget.ENTITY_ROLE, "instance")
        item.setData(0, SceneTreeWidget.MODEL_ID_ROLE, int(model_id))
        self.list_widget.addTopLevelItem(item)
        self.list_widget.setCurrentItem(item)

    def remove_model(self, model_id: int):
        target = int(model_id)
        for item in self.list_widget._leaf_items():
            if int(item.data(0, SceneTreeWidget.MODEL_ID_ROLE) or -1) != target:
                continue
            parent = item.parent()
            if parent is None:
                index = self.list_widget.indexOfTopLevelItem(item)
                if index >= 0:
                    self.list_widget.takeTopLevelItem(index)
            else:
                parent.removeChild(item)
            break

    def current_model_id(self):
        item = self.list_widget.currentItem()
        if item is None:
            return None
        ids = self._item_model_ids(item)
        return ids[0] if ids else None

    def clear_selection(self):
        self.list_widget.clearSelection()

    def _item_model_ids(self, item: QtWidgets.QTreeWidgetItem | None) -> list[int]:
        if item is None:
            return []
        direct = item.data(0, SceneTreeWidget.MODEL_ID_ROLE)
        entity = str(item.data(0, SceneTreeWidget.ENTITY_ROLE) or "")
        if entity == "instance" and direct is not None:
            return [int(direct)]
        ids: list[int] = []

        def visit(node: QtWidgets.QTreeWidgetItem):
            node_entity = str(node.data(0, SceneTreeWidget.ENTITY_ROLE) or "")
            node_id = node.data(0, SceneTreeWidget.MODEL_ID_ROLE)
            if node_entity == "instance" and node_id is not None:
                ids.append(int(node_id))
            for index in range(node.childCount()):
                visit(node.child(index))

        visit(item)
        if not ids and direct is not None:
            ids.append(int(direct))
        return ids

    def _selected_model_ids(self) -> list[int]:
        selected: list[int] = []
        for item in self.list_widget.selectedItems():
            for model_id in self._item_model_ids(item):
                if model_id not in selected:
                    selected.append(int(model_id))
        return selected

    def _on_selection_changed(self):
        self.selection_changed.emit(self._selected_model_ids())

    def _on_current_changed(self, current, previous):
        _ = previous
        ids = self._item_model_ids(current)
        if ids:
            self.model_selected.emit(ids[0])

    def _on_remove_clicked(self):
        current_id = self.current_model_id()
        if current_id is not None:
            self.request_remove.emit(current_id)

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

    def _first_instance_id_for_object(self, viewer, object_id: int, plate_id: int) -> int | None:
        for instance_id in viewer.get_plate_model_ids(int(plate_id)):
            model = viewer.models.get(int(instance_id), {})
            if int(model.get("object_id", 0)) == int(object_id):
                return int(instance_id)
        return None


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
        return (
            int(self.count_spin.value()),
            int(self.rows_spin.value()),
            int(self.cols_spin.value()),
        )

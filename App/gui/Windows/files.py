import os
import time

from PyQt5 import QtWidgets, QtCore

from ..theme import theme_css


class FilesView(QtWidgets.QWidget):
    add_files_requested = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._models = []
        self._build_ui()

    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        header_row = QtWidgets.QHBoxLayout()
        title = QtWidgets.QLabel("Files", self)
        title.setObjectName("FilesTitle")
        header_row.addWidget(title)
        header_row.addStretch(1)
        layout.addLayout(header_row)

        toolbar = QtWidgets.QHBoxLayout()
        self._search_input = QtWidgets.QLineEdit(self)
        self._search_input.setPlaceholderText("Search files")
        self._search_input.setObjectName("FilesSearch")
        toolbar.addWidget(self._search_input, 1)
        self._add_btn = QtWidgets.QPushButton("Add files", self)
        self._add_btn.setObjectName("FilesAddButton")
        toolbar.addWidget(self._add_btn)
        layout.addLayout(toolbar)

        self._stack = QtWidgets.QStackedWidget(self)
        self._table = QtWidgets.QTableWidget(0, 4, self._stack)
        self._table.setHorizontalHeaderLabels(["Name", "Type", "Size", "Modified"])
        self._table.verticalHeader().setVisible(False)
        self._table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self._table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self._table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self._table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self._stack.addWidget(self._table)

        self._empty_label = QtWidgets.QLabel("No files yet. Use Add files to import models.", self._stack)
        self._empty_label.setAlignment(QtCore.Qt.AlignCenter)
        self._empty_label.setObjectName("FilesEmpty")
        self._stack.addWidget(self._empty_label)
        self._stack.setCurrentWidget(self._empty_label)

        layout.addWidget(self._stack, 1)

        self._add_btn.clicked.connect(self.add_files_requested.emit)
        self._search_input.textChanged.connect(self._apply_filter)

        self.apply_theme()

    def set_models(self, models):
        self._models = list(models or [])
        self._apply_filter()

    def refresh_from_viewer(self, viewer):
        models = []
        if viewer is not None:
            for mid, payload in viewer.models.items():
                models.append(
                    {
                        "id": mid,
                        "name": payload.get("name") or f"Model {mid}",
                        "path": payload.get("path") or "",
                    }
                )
        self.set_models(models)

    def _apply_filter(self):
        query = self._search_input.text().strip().lower()
        rows = [m for m in self._models if query in (m.get("name") or "").lower()]
        self._table.setRowCount(len(rows))
        for row, model in enumerate(rows):
            name = model.get("name") or "Model"
            path = model.get("path") or ""
            ext = os.path.splitext(path)[1].lstrip(".").lower() if path else ""
            file_type = ext if ext else "model"
            size = self._format_size(path)
            modified = self._format_age(path)
            self._table.setItem(row, 0, QtWidgets.QTableWidgetItem(name))
            self._table.setItem(row, 1, QtWidgets.QTableWidgetItem(file_type))
            self._table.setItem(row, 2, QtWidgets.QTableWidgetItem(size))
            self._table.setItem(row, 3, QtWidgets.QTableWidgetItem(modified))
        self._stack.setCurrentWidget(self._table if rows else self._empty_label)

    def _format_size(self, path: str) -> str:
        if not path or not os.path.exists(path):
            return "n/a"
        try:
            size_bytes = os.path.getsize(path)
        except OSError:
            return "n/a"
        if size_bytes <= 0:
            return "0 B"
        for unit in ("B", "KB", "MB", "GB"):
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}" if unit != "B" else f"{size_bytes:.0f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    def _format_age(self, path: str) -> str:
        if not path or not os.path.exists(path):
            return "n/a"
        try:
            ts = os.path.getmtime(path)
        except OSError:
            return "n/a"
        delta = max(0.0, time.time() - ts)
        if delta < 60:
            return "just now"
        if delta < 3600:
            return f"{int(delta // 60)}m ago"
        if delta < 86400:
            return f"{int(delta // 3600)}h ago"
        if delta < 86400 * 7:
            return f"{int(delta // 86400)}d ago"
        return time.strftime("%Y-%m-%d", time.localtime(ts))

    def apply_theme(self):
        self.setStyleSheet(
            "QWidget {"
            f"  background: {theme_css('popup_bg')};"
            f"  color: {theme_css('popup_text')};"
            "}"
            "QLabel#FilesTitle {"
            "  font-size: 18px;"
            "  font-weight: 600;"
            "}"
            "QLineEdit#FilesSearch {"
            f"  background: {theme_css('popup_input_bg')};"
            f"  color: {theme_css('popup_input_text')};"
            f"  border: 1px solid {theme_css('popup_input_border')};"
            "  padding: 4px 8px;"
            "  border-radius: 6px;"
            "}"
            "QPushButton#FilesAddButton {"
            f"  background: {theme_css('action_button_bg')};"
            f"  color: {theme_css('action_button_text')};"
            f"  border: 1px solid {theme_css('action_panel_border')};"
            "  border-radius: 6px;"
            "  padding: 6px 14px;"
            "}"
            "QPushButton#FilesAddButton:hover {"
            f"  background: {theme_css('action_button_hover_bg')};"
            "}"
            "QTableWidget {"
            f"  background: {theme_css('action_panel_bg')};"
            f"  border: 1px solid {theme_css('action_panel_border')};"
            "  border-radius: 8px;"
            "  gridline-color: transparent;"
            "}"
            "QHeaderView::section {"
            f"  background: {theme_css('popup_header_bg')};"
            f"  color: {theme_css('popup_text')};"
            "  padding: 6px;"
            "  border: none;"
            "}"
            "QTableWidget::item {"
            "  padding: 6px;"
            "}"
            "QLabel#FilesEmpty {"
            f"  color: {theme_css('popup_muted_text')};"
            "  font-size: 13px;"
            "}"
        )

from PyQt5 import QtWidgets, QtCore

from ..theme import theme_css


class ActivityView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._me_entries = []
        self._printer_entries = []
        self._build_ui()

    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        header = QtWidgets.QLabel("Activity", self)
        header.setObjectName("ActivityTitle")
        layout.addWidget(header)

        filter_row = QtWidgets.QHBoxLayout()
        self._date_filter = QtWidgets.QComboBox(self)
        self._date_filter.addItems(["Any time", "Today", "Last 7 days", "Last 30 days"])
        self._date_filter.setObjectName("ActivityCombo")
        filter_row.addWidget(self._date_filter)
        self._search_input = QtWidgets.QLineEdit(self)
        self._search_input.setPlaceholderText("Search by printer, user, job")
        self._search_input.setObjectName("ActivitySearch")
        filter_row.addWidget(self._search_input, 1)
        layout.addLayout(filter_row)

        tabs_row = QtWidgets.QHBoxLayout()
        self._me_btn = QtWidgets.QToolButton(self)
        self._me_btn.setText("Me")
        self._me_btn.setCheckable(True)
        self._me_btn.setObjectName("ActivityTab")
        self._printers_btn = QtWidgets.QToolButton(self)
        self._printers_btn.setText("Printers")
        self._printers_btn.setCheckable(True)
        self._printers_btn.setObjectName("ActivityTab")
        tabs_group = QtWidgets.QButtonGroup(self)
        tabs_group.setExclusive(True)
        tabs_group.addButton(self._me_btn)
        tabs_group.addButton(self._printers_btn)
        tabs_row.addWidget(self._me_btn)
        tabs_row.addWidget(self._printers_btn)
        tabs_row.addStretch(1)
        layout.addLayout(tabs_row)

        self._stack = QtWidgets.QStackedWidget(self)
        self._me_table = self._build_table(self._stack)
        self._printer_table = self._build_table(self._stack)
        self._stack.addWidget(self._me_table)
        self._stack.addWidget(self._printer_table)
        layout.addWidget(self._stack, 1)

        self._me_btn.setChecked(True)
        self._stack.setCurrentWidget(self._me_table)

        tabs_group.buttonClicked.connect(self._on_tab_changed)
        self._search_input.textChanged.connect(self._refresh_tables)
        self._date_filter.currentIndexChanged.connect(self._refresh_tables)

        self.apply_theme()

    def _build_table(self, parent):
        table = QtWidgets.QTableWidget(0, 6, parent)
        table.setHorizontalHeaderLabels(["Job", "Status", "Duration", "Material", "When", "Printer"])
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        return table

    def set_me_activity(self, entries):
        self._me_entries = list(entries or [])
        self._refresh_tables()

    def set_printer_activity(self, entries):
        self._printer_entries = list(entries or [])
        self._refresh_tables()

    def _refresh_tables(self):
        query = self._search_input.text().strip().lower()
        self._populate_table(self._me_table, self._me_entries, query)
        self._populate_table(self._printer_table, self._printer_entries, query)

    def _populate_table(self, table, entries, query):
        rows = []
        for entry in entries:
            job = str(entry.get("job", ""))
            printer = str(entry.get("printer", ""))
            user = str(entry.get("user", ""))
            if query and query not in job.lower() and query not in printer.lower() and query not in user.lower():
                continue
            rows.append(entry)
        table.setRowCount(len(rows))
        for row, entry in enumerate(rows):
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(entry.get("job", ""))))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(entry.get("status", ""))))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(entry.get("duration", ""))))
            table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(entry.get("material", ""))))
            table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(entry.get("when", ""))))
            table.setItem(row, 5, QtWidgets.QTableWidgetItem(str(entry.get("printer", ""))))

    def _on_tab_changed(self, button):
        if button is self._me_btn:
            self._stack.setCurrentWidget(self._me_table)
        elif button is self._printers_btn:
            self._stack.setCurrentWidget(self._printer_table)

    def apply_theme(self):
        self.setStyleSheet(
            "QWidget {"
            f"  background: {theme_css('popup_bg')};"
            f"  color: {theme_css('popup_text')};"
            "}"
            "QLabel#ActivityTitle {"
            "  font-size: 18px;"
            "  font-weight: 600;"
            "}"
            "QLineEdit#ActivitySearch {"
            f"  background: {theme_css('popup_input_bg')};"
            f"  color: {theme_css('popup_input_text')};"
            f"  border: 1px solid {theme_css('popup_input_border')};"
            "  padding: 4px 8px;"
            "  border-radius: 6px;"
            "}"
            "QComboBox#ActivityCombo {"
            f"  background: {theme_css('popup_input_bg')};"
            f"  color: {theme_css('popup_input_text')};"
            f"  border: 1px solid {theme_css('popup_input_border')};"
            "  padding: 3px 8px;"
            "  border-radius: 6px;"
            "}"
            "QToolButton#ActivityTab {"
            "  padding: 6px 12px;"
            "  border-radius: 6px;"
            "  border: 1px solid transparent;"
            "}"
            "QToolButton#ActivityTab:checked {"
            f"  background: {theme_css('topbar_accent')};"
            f"  color: {theme_css('popup_text')};"
            "  font-weight: 600;"
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
        )

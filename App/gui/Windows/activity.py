from datetime import datetime, timedelta

from PyQt5 import QtCore, QtWidgets

from ..i18n import tr
from ..theme import theme_css


class ActivityView(QtWidgets.QWidget):
    """Activity dashboard with only Me/Printers tabs."""

    _DATE_FILTER_KEYS = (
        "activity.filter.any_time",
        "activity.filter.today",
        "activity.filter.last_7_days",
        "activity.filter.last_30_days",
    )
    _STAT_ORDER = ("jobs", "printing", "queued", "completed", "failed")
    _STAT_LABELS = {
        "jobs": "activity.stat.jobs",
        "printing": "activity.stat.printing",
        "queued": "activity.stat.in_queue",
        "completed": "activity.stat.completed",
        "failed": "activity.stat.errors",
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self._me_entries = []
        self._printer_entries = []
        self._stats_values: dict[str, QtWidgets.QLabel] = {}
        self._build_ui()

    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        title_row = QtWidgets.QHBoxLayout()
        title_row.setSpacing(8)
        title_col = QtWidgets.QVBoxLayout()
        title_col.setSpacing(1)
        header = QtWidgets.QLabel(tr("activity.title"), self)
        header.setObjectName("ActivityTitle")
        subtitle = QtWidgets.QLabel(tr("activity.subtitle"), self)
        subtitle.setObjectName("ActivitySubtitle")
        title_col.addWidget(header)
        title_col.addWidget(subtitle)
        title_row.addLayout(title_col)
        title_row.addStretch(1)
        layout.addLayout(title_row)

        controls_row = QtWidgets.QHBoxLayout()
        controls_row.setSpacing(10)
        tabs_row = QtWidgets.QHBoxLayout()
        tabs_row.setSpacing(8)
        self._me_btn = QtWidgets.QToolButton(self)
        self._me_btn.setText(tr("activity.tab.me"))
        self._me_btn.setCheckable(True)
        self._me_btn.setObjectName("ActivityTab")
        self._printers_btn = QtWidgets.QToolButton(self)
        self._printers_btn.setText(tr("activity.tab.printers"))
        self._printers_btn.setCheckable(True)
        self._printers_btn.setObjectName("ActivityTab")
        tabs_group = QtWidgets.QButtonGroup(self)
        tabs_group.setExclusive(True)
        tabs_group.addButton(self._me_btn)
        tabs_group.addButton(self._printers_btn)
        tabs_row.addWidget(self._me_btn)
        tabs_row.addWidget(self._printers_btn)
        controls_row.addLayout(tabs_row)
        controls_row.addStretch(1)

        self._date_filter = QtWidgets.QComboBox(self)
        self._date_filter.addItems([tr(key) for key in self._DATE_FILTER_KEYS])
        self._date_filter.setObjectName("ActivityCombo")
        controls_row.addWidget(self._date_filter)

        self._search_input = QtWidgets.QLineEdit(self)
        self._search_input.setPlaceholderText(tr("activity.search.placeholder"))
        self._search_input.setObjectName("ActivitySearch")
        controls_row.addWidget(self._search_input, 1)

        self._refresh_btn = QtWidgets.QPushButton(tr("activity.button.refresh"), self)
        self._refresh_btn.setObjectName("ActivityRefresh")
        controls_row.addWidget(self._refresh_btn)
        layout.addLayout(controls_row)

        self._compliance_banner = QtWidgets.QLabel("", self)
        self._compliance_banner.setObjectName("ActivityComplianceBanner")
        self._compliance_banner.setWordWrap(True)
        self._compliance_banner.hide()
        layout.addWidget(self._compliance_banner)

        stats_strip = QtWidgets.QFrame(self)
        stats_strip.setObjectName("ActivityStatsStrip")
        stats_layout = QtWidgets.QHBoxLayout(stats_strip)
        stats_layout.setContentsMargins(10, 10, 10, 10)
        stats_layout.setSpacing(8)
        for key in self._STAT_ORDER:
            card = QtWidgets.QFrame(stats_strip)
            card.setObjectName("ActivityStatCard")
            card_layout = QtWidgets.QVBoxLayout(card)
            card_layout.setContentsMargins(10, 8, 10, 8)
            card_layout.setSpacing(2)
            value = QtWidgets.QLabel("0", card)
            value.setObjectName("ActivityStatValue")
            value.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            label_key = self._STAT_LABELS.get(key, "")
            label = QtWidgets.QLabel(tr(label_key, key), card)
            label.setObjectName("ActivityStatLabel")
            label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            card_layout.addWidget(value)
            card_layout.addWidget(label)
            stats_layout.addWidget(card, 1)
            self._stats_values[key] = value
        layout.addWidget(stats_strip)

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
        self._refresh_btn.clicked.connect(self._refresh_tables)

        self.apply_theme()
        self._refresh_tables()

    def set_compliance_banner(self, message: str = ""):
        text = str(message or "").strip()
        if not text:
            self._compliance_banner.clear()
            self._compliance_banner.hide()
            return
        prefix = tr("activity.compliance.banner", "Cloud activity is restricted:")
        self._compliance_banner.setText(f"{prefix} {text}")
        self._compliance_banner.show()

    def _build_table(self, parent):
        table = QtWidgets.QTableWidget(0, 7, parent)
        table.setHorizontalHeaderLabels(
            [
                tr("activity.table.job"),
                tr("activity.table.status"),
                tr("activity.table.duration"),
                tr("activity.table.material"),
                tr("activity.table.when"),
                tr("activity.table.user"),
                tr("activity.table.printer"),
            ]
        )
        table.verticalHeader().setVisible(False)
        table.verticalHeader().setDefaultSectionSize(30)
        table.setShowGrid(False)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        table.setFocusPolicy(QtCore.Qt.NoFocus)
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        for idx in range(1, 7):
            header.setSectionResizeMode(idx, QtWidgets.QHeaderView.ResizeToContents)
        return table

    def set_me_activity(self, entries):
        self._me_entries = list(entries or [])
        self._refresh_tables()

    def set_printer_activity(self, entries):
        self._printer_entries = list(entries or [])
        self._refresh_tables()

    def _refresh_tables(self):
        query = self._search_input.text().strip().lower()
        date_mode = int(self._date_filter.currentIndex())
        me_rows = self._filtered_rows(self._me_entries, query, date_mode)
        printer_rows = self._filtered_rows(self._printer_entries, query, date_mode)
        self._populate_table(self._me_table, me_rows)
        self._populate_table(self._printer_table, printer_rows)
        active_rows = me_rows if self._stack.currentWidget() is self._me_table else printer_rows
        self._update_stats(active_rows)

    @staticmethod
    def _entry_datetime(entry):
        raw = str(entry.get("created_at_utc", "")).strip()
        if not raw:
            raw = str(entry.get("when", "")).strip()
        if not raw:
            return None
        normalized = raw
        if normalized.endswith("Z"):
            normalized = normalized[:-1] + "+00:00"
        try:
            return datetime.fromisoformat(normalized)
        except ValueError:
            return None

    @staticmethod
    def _matches_date_filter(entry_dt, date_mode):
        if date_mode <= 0:
            return True
        if entry_dt is None:
            return False
        now = datetime.now(entry_dt.tzinfo) if entry_dt.tzinfo is not None else datetime.now()
        if date_mode == 1:
            return entry_dt.date() == now.date()
        if date_mode == 2:
            return entry_dt >= (now - timedelta(days=7))
        if date_mode == 3:
            return entry_dt >= (now - timedelta(days=30))
        return True

    def _filtered_rows(self, entries, query, date_mode):
        rows = []
        for entry in entries:
            row = self._normalize_entry(entry)
            if query and query not in row["job"].lower() and query not in row["printer"].lower() and query not in row["user"].lower():
                continue
            entry_dt = self._entry_datetime(entry)
            if not self._matches_date_filter(entry_dt, date_mode):
                continue
            rows.append(row)
        return rows

    @staticmethod
    def _normalize_entry(entry):
        job = str(entry.get("job", "") or entry.get("job_id", "")).strip() or "-"
        status = str(entry.get("status", "")).strip() or "-"
        duration = str(entry.get("duration", "")).strip() or "-"
        material = str(entry.get("material", "")).strip() or "-"
        when = str(entry.get("when", "") or entry.get("created_at_utc", "")).strip() or "-"
        user = str(entry.get("user", "") or entry.get("requested_by", "")).strip() or "-"
        printer = str(entry.get("printer", "") or entry.get("printer_id", "")).strip() or "-"
        return {
            "job": job,
            "status": status,
            "duration": duration,
            "material": material,
            "when": when,
            "user": user,
            "printer": printer,
        }

    def _populate_table(self, table, rows):
        table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            values = (
                row["job"],
                row["status"],
                row["duration"],
                row["material"],
                row["when"],
                row["user"],
                row["printer"],
            )
            for col_idx, value in enumerate(values):
                item = QtWidgets.QTableWidgetItem(str(value))
                if col_idx in (1, 2, 3):
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                table.setItem(row_idx, col_idx, item)

    def _update_stats(self, rows):
        statuses = [str(row.get("status", "")).strip().lower() for row in rows]
        printing = sum(1 for status in statuses if status in ("running", "printing"))
        queued = sum(1 for status in statuses if status in ("queued", "pending", "pending_printer"))
        completed = sum(1 for status in statuses if status == "completed")
        failed = sum(1 for status in statuses if status in ("failed", "error", "cancelled"))
        values = {
            "jobs": len(rows),
            "printing": printing,
            "queued": queued,
            "completed": completed,
            "failed": failed,
        }
        for key, label in self._stats_values.items():
            label.setText(str(values.get(key, 0)))

    def _on_tab_changed(self, button):
        if button is self._me_btn:
            self._stack.setCurrentWidget(self._me_table)
        elif button is self._printers_btn:
            self._stack.setCurrentWidget(self._printer_table)
        self._refresh_tables()

    def apply_theme(self):
        self.setStyleSheet(
            "QWidget {"
            f"  background: {theme_css('popup_bg')};"
            f"  color: {theme_css('popup_text')};"
            "}"
            "QLabel#ActivityTitle {"
            "  font-size: 20px;"
            "  font-weight: 700;"
            "}"
            "QLabel#ActivitySubtitle {"
            f"  color: {theme_css('popup_muted_text')};"
            "  font-size: 12px;"
            "}"
            "QLineEdit#ActivitySearch, QComboBox#ActivityCombo {"
            f"  background: {theme_css('popup_input_bg')};"
            f"  color: {theme_css('popup_input_text')};"
            f"  border: 1px solid {theme_css('popup_input_border')};"
            "  padding: 4px 8px;"
            "  border-radius: 6px;"
            "  min-height: 26px;"
            "}"
            "QPushButton#ActivityRefresh {"
            f"  background: {theme_css('action_button_bg')};"
            f"  color: {theme_css('action_button_text')};"
            f"  border: 1px solid {theme_css('action_panel_border')};"
            "  border-radius: 6px;"
            "  padding: 5px 10px;"
            "  font-weight: 600;"
            "}"
            "QPushButton#ActivityRefresh:hover {"
            f"  background: {theme_css('action_button_hover_bg')};"
            "}"
            "QPushButton#ActivityRefresh:pressed {"
            f"  background: {theme_css('action_button_active_bg')};"
            "}"
            "QLabel#ActivityComplianceBanner {"
            f"  background: {theme_css('warning_bg')};"
            f"  color: {theme_css('warning_text')};"
            f"  border: 1px solid {theme_css('warning_border')};"
            "  border-radius: 8px;"
            "  padding: 6px 8px;"
            "}"
            "QToolButton#ActivityTab {"
            f"  background: {theme_css('action_button_bg')};"
            f"  color: {theme_css('popup_text')};"
            f"  border: 1px solid {theme_css('action_panel_border')};"
            "  border-radius: 6px;"
            "  padding: 5px 12px;"
            "  font-weight: 600;"
            "}"
            "QToolButton#ActivityTab:checked {"
            f"  background: {theme_css('topbar_accent')};"
            "  border: 1px solid transparent;"
            "}"
            "QFrame#ActivityStatsStrip {"
            f"  background: {theme_css('action_panel_bg')};"
            f"  border: 1px solid {theme_css('action_panel_border')};"
            "  border-radius: 10px;"
            "}"
            "QFrame#ActivityStatCard {"
            f"  background: {theme_css('popup_header_bg')};"
            f"  border: 1px solid {theme_css('action_panel_border')};"
            "  border-radius: 8px;"
            "}"
            "QLabel#ActivityStatValue {"
            "  font-size: 19px;"
            "  font-weight: 700;"
            "}"
            "QLabel#ActivityStatLabel {"
            f"  color: {theme_css('popup_muted_text')};"
            "  font-size: 11px;"
            "  font-weight: 600;"
            "}"
            "QTableWidget {"
            f"  background: {theme_css('action_panel_bg')};"
            f"  border: 1px solid {theme_css('action_panel_border')};"
            "  border-radius: 10px;"
            "  gridline-color: transparent;"
            "}"
            "QTableCornerButton::section {"
            f"  background: {theme_css('popup_header_bg')};"
            "  border: none;"
            "}"
            "QHeaderView::section {"
            f"  background: {theme_css('popup_header_bg')};"
            f"  color: {theme_css('popup_text')};"
            "  border: none;"
            "  border-bottom: 1px solid rgba(0, 0, 0, 0);"
            "  padding: 6px 8px;"
            "  font-weight: 600;"
            "}"
            "QTableWidget::item {"
            "  padding: 5px 8px;"
            f"  border-bottom: 1px solid {theme_css('action_panel_border')};"
            "}"
        )

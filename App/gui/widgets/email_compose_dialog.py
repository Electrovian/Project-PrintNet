from __future__ import annotations

from PyQt5 import QtCore, QtWidgets

from ..theme import theme_css


class EmailComposeDialog(QtWidgets.QDialog):
    def __init__(
        self,
        *,
        recipient: str = "",
        subject: str = "",
        context_lines: list[str] | None = None,
        note: str = "",
        parent=None,
    ):
        super().__init__(parent)
        self.setWindowTitle("Send email")
        self.setModal(True)
        self.resize(560, 420)
        self._context_lines = [str(line).strip() for line in list(context_lines or []) if str(line).strip()]
        self._build_ui(recipient=recipient, subject=subject, note=note)
        self._apply_theme()

    def _build_ui(self, *, recipient: str, subject: str, note: str) -> None:
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        intro = QtWidgets.QLabel(
            "Compose a handoff email for the current printer job. The app will try SMTP first, then offer your mail app as a fallback.",
            self,
        )
        intro.setWordWrap(True)
        intro.setObjectName("EmailComposeIntro")
        layout.addWidget(intro)

        form = QtWidgets.QFormLayout()
        form.setHorizontalSpacing(12)
        form.setVerticalSpacing(10)

        self._recipient_edit = QtWidgets.QLineEdit(self)
        self._recipient_edit.setPlaceholderText("recipient@example.com")
        self._recipient_edit.setText(str(recipient or "").strip())
        form.addRow("To", self._recipient_edit)

        self._subject_edit = QtWidgets.QLineEdit(self)
        self._subject_edit.setText(str(subject or "").strip())
        form.addRow("Subject", self._subject_edit)
        layout.addLayout(form)

        summary_label = QtWidgets.QLabel("Included details", self)
        summary_label.setObjectName("EmailComposeHeading")
        layout.addWidget(summary_label)

        self._summary_view = QtWidgets.QPlainTextEdit(self)
        self._summary_view.setObjectName("EmailComposeSummary")
        self._summary_view.setReadOnly(True)
        self._summary_view.setPlainText("\n".join(self._context_lines))
        self._summary_view.setMinimumHeight(140)
        layout.addWidget(self._summary_view)

        note_label = QtWidgets.QLabel("Optional note", self)
        note_label.setObjectName("EmailComposeHeading")
        layout.addWidget(note_label)

        self._note_edit = QtWidgets.QPlainTextEdit(self)
        self._note_edit.setPlaceholderText("Add any operator notes or delivery instructions here.")
        self._note_edit.setPlainText(str(note or "").strip())
        self._note_edit.setMinimumHeight(110)
        layout.addWidget(self._note_edit)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            parent=self,
        )
        buttons.button(QtWidgets.QDialogButtonBox.Ok).setText("Continue")
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def payload(self) -> dict[str, str]:
        return {
            "recipient": self._recipient_edit.text().strip(),
            "subject": self._subject_edit.text().strip(),
            "note": self._note_edit.toPlainText().strip(),
        }

    def accept(self) -> None:
        recipient = self._recipient_edit.text().strip()
        if not recipient or "@" not in recipient:
            QtWidgets.QMessageBox.warning(self, "Send email", "Enter a valid recipient email address.")
            self._recipient_edit.setFocus(QtCore.Qt.OtherFocusReason)
            return
        super().accept()

    def _apply_theme(self) -> None:
        self.setStyleSheet(
            "QDialog {"
            f"  background: {theme_css('popup_bg')};"
            f"  color: {theme_css('popup_text')};"
            "}"
            "QLabel#EmailComposeIntro {"
            f"  color: {theme_css('popup_muted_text')};"
            "}"
            "QLabel#EmailComposeHeading {"
            "  font-weight: 600;"
            "}"
            "QLineEdit, QPlainTextEdit {"
            f"  background: {theme_css('popup_input_bg')};"
            f"  color: {theme_css('popup_input_text')};"
            f"  border: 1px solid {theme_css('popup_input_border')};"
            "  border-radius: 6px;"
            "  padding: 6px 8px;"
            "}"
            "QPushButton {"
            f"  background: {theme_css('action_button_bg')};"
            f"  color: {theme_css('action_button_text')};"
            f"  border: 1px solid {theme_css('action_panel_border')};"
            "  border-radius: 6px;"
            "  padding: 6px 14px;"
            "}"
            "QPushButton:hover {"
            f"  background: {theme_css('action_button_hover_bg')};"
            "}"
        )

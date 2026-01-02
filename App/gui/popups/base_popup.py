from PyQt5 import QtWidgets, QtCore

from ..theme import theme_css


class BasePopup(QtWidgets.QFrame):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self._title = title
        self._build_base()

    def _build_base(self):
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._header = QtWidgets.QFrame(self)
        self._header_layout = QtWidgets.QHBoxLayout(self._header)
        self._header_layout.setContentsMargins(10, 6, 10, 6)
        self._header_layout.setSpacing(6)

        self._title_label = QtWidgets.QLabel(self._title)
        self._header_layout.addWidget(self._title_label)
        self._header_layout.addStretch(1)

        self._content = QtWidgets.QFrame(self)
        self._content_layout = QtWidgets.QVBoxLayout(self._content)
        self._content_layout.setContentsMargins(12, 10, 12, 10)
        self._content_layout.setSpacing(8)

        layout.addWidget(self._header)
        layout.addWidget(self._content)
        self.setObjectName("PopupRoot")
        self._header.setObjectName("PopupHeader")
        self._title_label.setObjectName("Header")
        self._apply_theme()

    def _apply_theme(self):
        self.setStyleSheet(
            "QFrame#PopupRoot {"
            f"  background: {theme_css('popup_bg')};"
            f"  border: 1px solid {theme_css('popup_border')};"
            "  border-radius: 6px;"
            "}"
            "QFrame#PopupHeader {"
            f"  background: {theme_css('popup_header_bg')};"
            f"  border-bottom: 1px solid {theme_css('popup_border')};"
            "  border-top-left-radius: 6px;"
            "  border-top-right-radius: 6px;"
            "}"
            "QLabel {"
            f"  color: {theme_css('popup_text')};"
            "  font-size: 9pt;"
            "}"
            "QLabel#Muted {"
            f"  color: {theme_css('popup_muted_text')};"
            "}"
            "QDoubleSpinBox {"
            f"  background: {theme_css('popup_input_bg')};"
            f"  color: {theme_css('popup_input_text')};"
            f"  border: 1px solid {theme_css('popup_input_border')};"
            "  border-radius: 4px;"
            "  padding: 2px 6px;"
            "}"
            "QCheckBox {"
            f"  color: {theme_css('popup_text')};"
            "}"
            "QRadioButton {"
            f"  color: {theme_css('popup_text')};"
            "}"
            "QPushButton {"
            f"  background: {theme_css('popup_button_bg')};"
            f"  color: {theme_css('popup_button_text')};"
            f"  border: 1px solid {theme_css('popup_button_border')};"
            "  border-radius: 4px;"
            "  padding: 3px 10px;"
            "}"
            "QPushButton:hover {"
            f"  background: {theme_css('popup_button_hover_bg')};"
            "}"
            "QPushButton:pressed {"
            f"  background: {theme_css('popup_button_active_bg')};"
            "}"
            "QSlider::groove:horizontal {"
            f"  background: {theme_css('popup_input_bg')};"
            "  height: 6px;"
            "  border-radius: 3px;"
            "}"
            "QSlider::handle:horizontal {"
            f"  background: {theme_css('popup_button_active_bg')};"
            "  width: 14px;"
            "  margin: -4px 0;"
            "  border-radius: 7px;"
            "}"
        )

    def content_layout(self):
        return self._content_layout

    def header_layout(self):
        return self._header_layout

    def apply_theme(self):
        self._apply_theme()

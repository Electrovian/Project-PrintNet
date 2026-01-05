from PyQt5 import QtCore, QtGui, QtWidgets


class SplashScreen(QtWidgets.QDialog):
    def __init__(self, title: str = "OpenSlicer", message: str = "Loading configuration...", parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.Dialog
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        outer = QtWidgets.QFrame(self)
        outer.setObjectName("SplashOuter")
        layout = QtWidgets.QVBoxLayout(outer)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title_label = QtWidgets.QLabel(title, outer)
        title_label.setObjectName("SplashTitle")
        title_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        message_label = QtWidgets.QLabel(message, outer)
        message_label.setObjectName("SplashMessage")
        message_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        bar = QtWidgets.QProgressBar(outer)
        bar.setRange(0, 100)
        bar.setValue(0)
        bar.setTextVisible(False)
        bar.setFixedHeight(10)
        self._progress_bar = bar
        self._progress_anim = None

        version_label = QtWidgets.QLabel("Version: 0.1", outer)
        version_label.setObjectName("SplashVersion")
        version_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        layout.addWidget(title_label)
        layout.addWidget(message_label)
        layout.addWidget(bar)
        layout.addWidget(version_label)

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.addWidget(outer)

        self._apply_style()
        self.setFixedSize(360, 240)

    def start_progress(self, duration_ms: int = 3000):
        if self._progress_bar is None:
            return
        if self._progress_anim is None:
            self._progress_anim = QtCore.QPropertyAnimation(self._progress_bar, b"value", self)
            self._progress_anim.setEasingCurve(QtCore.QEasingCurve.Linear)
        self._progress_bar.setValue(0)
        self._progress_anim.stop()
        self._progress_anim.setDuration(max(100, int(duration_ms)))
        self._progress_anim.setStartValue(0)
        self._progress_anim.setEndValue(100)
        self._progress_anim.start()

    def _apply_style(self):
        self.setStyleSheet(
            "QFrame#SplashOuter {"
            "  background-color: #f6f7f9;"
            "  border-radius: 12px;"
            "  border: 1px solid #d7dae0;"
            "}"
            "QLabel#SplashTitle {"
            "  font-size: 18px;"
            "  font-weight: 700;"
            "  color: #1c1f24;"
            "}"
            "QLabel#SplashMessage {"
            "  font-size: 12px;"
            "  color: #4a4f57;"
            "}"
            "QLabel#SplashVersion {"
            "  font-size: 10px;"
            "  color: #7c8086;"
            "}"
            "QProgressBar {"
            "  background: #e6e9ef;"
            "  border-radius: 5px;"
            "}"
            "QProgressBar::chunk {"
            "  background: #19c15b;"
            "  border-radius: 5px;"
            "}"
        )

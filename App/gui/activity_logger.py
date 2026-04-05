import json
import logging
import os
import time
from datetime import datetime, timezone

from PyQt5 import QtCore, QtWidgets


def _utc_timestamp():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _short_text(value, max_len=160):
    if value is None:
        return None
    text = str(value)
    if not text:
        return None
    if len(text) > max_len:
        return text[: max_len - 3] + "..."
    return text


def _modifier_names(modifiers):
    mapping = (
        (QtCore.Qt.ShiftModifier, "shift"),
        (QtCore.Qt.ControlModifier, "ctrl"),
        (QtCore.Qt.AltModifier, "alt"),
        (QtCore.Qt.MetaModifier, "meta"),
    )
    names = [name for flag, name in mapping if modifiers & flag]
    return names


def _mouse_button_names(buttons):
    mapping = (
        (QtCore.Qt.LeftButton, "left"),
        (QtCore.Qt.RightButton, "right"),
        (QtCore.Qt.MiddleButton, "middle"),
        (QtCore.Qt.BackButton, "back"),
        (QtCore.Qt.ForwardButton, "forward"),
    )
    names = [name for flag, name in mapping if buttons & flag]
    return names or ["none"]


class ActivityEventFilter(QtCore.QObject):
    def __init__(self, logger):
        super().__init__()
        self._logger = logger

    def eventFilter(self, a0, a1):
        obj = a0
        event = a1
        etype = event.type()
        if etype == QtCore.QEvent.MouseMove:
            self._logger.log_mouse_event("mouse_move", obj, event)
        elif etype == QtCore.QEvent.MouseButtonPress:
            self._logger.log_mouse_event("mouse_press", obj, event)
        elif etype == QtCore.QEvent.MouseButtonRelease:
            self._logger.log_mouse_event("mouse_release", obj, event)
        elif etype == QtCore.QEvent.MouseButtonDblClick:
            self._logger.log_mouse_event("mouse_double_click", obj, event)
        elif etype == QtCore.QEvent.Wheel:
            self._logger.log_wheel_event(obj, event)
        elif etype == QtCore.QEvent.KeyPress:
            self._logger.log_key_event("key_press", obj, event)
        elif etype == QtCore.QEvent.KeyRelease:
            self._logger.log_key_event("key_release", obj, event)
        elif etype == QtCore.QEvent.ChildAdded:
            if isinstance(event, QtCore.QChildEvent):
                child = event.child()
            else:
                child = None
            if child is not None:
                self._logger.track_widget_tree(child)
        return False


class ActivityLogger:
    def __init__(self, log_dir=None):
        self.log_dir = log_dir or self._default_log_dir()
        os.makedirs(self.log_dir, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_path = os.path.join(self.log_dir, f"activity_{stamp}.log")
        self._logger = logging.getLogger(f"activity.{id(self)}")
        self._logger.setLevel(logging.INFO)
        handler = logging.FileHandler(self.log_path, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(message)s"))
        self._logger.addHandler(handler)
        self._logger.propagate = False
        self._event_filter = None
        self._tracked_ids = set()
        self.last_record = None
        self.last_record_ts = None
        self._log_mouse_move = self._read_bool_env("EON_ACTIVITY_LOG_MOUSE_MOVE", False)
        self._mouse_move_interval_s = self._read_interval_env(
            "EON_ACTIVITY_MOUSE_MOVE_INTERVAL_MS",
            default_ms=120,
        )
        self._last_mouse_move_ts = 0.0
        self._last_mouse_move_pos = None
        self._stdout_enabled = self._read_bool_env("EON_ACTIVITY_LOG_STDOUT", False)
        self._stdout_pretty = self._read_bool_env("EON_ACTIVITY_LOG_STDOUT_PRETTY", False)
        self._stdout_events = self._read_event_filter_env(
            "EON_ACTIVITY_LOG_STDOUT_EVENTS",
            default="action,mouse_press,mouse_release,mouse_double_click,mouse_wheel,key_press,key_release",
        )

    def install(self, app):
        if app is None or self._event_filter is not None:
            return
        self._event_filter = ActivityEventFilter(self)
        app.installEventFilter(self._event_filter)

    def log_action(self, action_name, **payload):
        record = {"ts": _utc_timestamp(), "event": "action", "action": action_name}
        record.update(payload)
        self._write(record)

    def track_action(self, action, action_name=None):
        if action is None:
            return
        name = action_name or _short_text(action.objectName()) or _short_text(action.text()) or "action"

        def _on_triggered(checked=False):
            self.log_action(name, checked=bool(checked))

        action.triggered.connect(_on_triggered)

    def track_button(self, button, action_name=None):
        if button is None:
            return
        name = action_name or _short_text(button.objectName()) or _short_text(button.text()) or "button"

        def _on_clicked(checked=False):
            self.log_action(name, checked=bool(checked))

        button.clicked.connect(_on_clicked)

    def log_mouse_event(self, event_name, obj, event):
        if event_name == "mouse_move" and not self._should_log_mouse_move(event):
            return
        pos = event.pos()
        global_pos = event.globalPos()
        record = {
            "ts": _utc_timestamp(),
            "event": event_name,
            "pos": {"x": int(pos.x()), "y": int(pos.y())},
            "global": {"x": int(global_pos.x()), "y": int(global_pos.y())},
            "button": _mouse_button_names(event.button()),
            "buttons": _mouse_button_names(event.buttons()),
            "modifiers": _modifier_names(event.modifiers()),
        }
        record.update(self._widget_context(obj))
        self._write(record)

    def log_wheel_event(self, obj, event):
        pos = event.pos()
        global_pos = event.globalPos()
        delta = event.angleDelta()
        record = {
            "ts": _utc_timestamp(),
            "event": "mouse_wheel",
            "pos": {"x": int(pos.x()), "y": int(pos.y())},
            "global": {"x": int(global_pos.x()), "y": int(global_pos.y())},
            "delta": {"x": int(delta.x()), "y": int(delta.y())},
            "modifiers": _modifier_names(event.modifiers()),
        }
        record.update(self._widget_context(obj))
        self._write(record)

    def log_key_event(self, event_name, obj, event):
        key = int(event.key())
        text = _short_text(event.text(), max_len=32)
        record = {
            "ts": _utc_timestamp(),
            "event": event_name,
            "key": key,
            "text": text,
            "modifiers": _modifier_names(event.modifiers()),
        }
        record.update(self._widget_context(obj))
        self._write(record)

    def track_widget_tree(self, root):
        if root is None:
            return
        for action in root.findChildren(QtWidgets.QAction):
            if id(action) in self._tracked_ids:
                continue
            self._tracked_ids.add(id(action))
            self.track_action(action)
        for button in root.findChildren(QtWidgets.QAbstractButton):
            if id(button) in self._tracked_ids:
                continue
            self._tracked_ids.add(id(button))
            self.track_button(button)
        for combo in root.findChildren(QtWidgets.QComboBox):
            if id(combo) in self._tracked_ids:
                continue
            self._tracked_ids.add(id(combo))
            name = _short_text(combo.objectName()) or "combo"
            combo.currentIndexChanged.connect(
                lambda idx, n=name: self.log_action(n, index=int(idx))
            )
        for spin in root.findChildren(QtWidgets.QAbstractSpinBox):
            if id(spin) in self._tracked_ids:
                continue
            self._tracked_ids.add(id(spin))
            name = _short_text(spin.objectName()) or "spin"
            if hasattr(spin, "valueChanged"):
                spin.valueChanged.connect(lambda val, n=name: self.log_action(n, value=val))
        for slider in root.findChildren(QtWidgets.QSlider):
            if id(slider) in self._tracked_ids:
                continue
            self._tracked_ids.add(id(slider))
            name = _short_text(slider.objectName()) or "slider"
            slider.valueChanged.connect(lambda val, n=name: self.log_action(n, value=int(val)))
        for line in root.findChildren(QtWidgets.QLineEdit):
            if id(line) in self._tracked_ids:
                continue
            self._tracked_ids.add(id(line))
            name = _short_text(line.objectName()) or "line_edit"
            line.textChanged.connect(
                lambda text, n=name: self.log_action(n, text=_short_text(text, max_len=120))
            )
        for text_edit in root.findChildren(QtWidgets.QPlainTextEdit):
            if id(text_edit) in self._tracked_ids:
                continue
            self._tracked_ids.add(id(text_edit))
            name = _short_text(text_edit.objectName()) or "plain_text"

            def _on_text_changed(edit=text_edit, n=name):
                self.log_action(n, text=_short_text(edit.toPlainText(), max_len=120))

            text_edit.textChanged.connect(_on_text_changed)

    def _write(self, record):
        self._logger.info(json.dumps(record, ensure_ascii=True))
        self._emit_stdout(record)
        self.last_record = record
        self.last_record_ts = record.get("ts")

    def _emit_stdout(self, record):
        if not self._stdout_enabled:
            return
        event_name = str(record.get("event", "")).strip().lower()
        if self._stdout_events is not None and event_name not in self._stdout_events:
            return
        try:
            if self._stdout_pretty:
                payload = json.dumps(record, ensure_ascii=True, sort_keys=True)
            else:
                payload = json.dumps(record, ensure_ascii=True)
            print(payload, flush=True)
        except Exception:
            return

    def _widget_context(self, obj):
        if not isinstance(obj, QtCore.QObject):
            return {}
        context = {"object_class": obj.__class__.__name__}
        name = _short_text(obj.objectName())
        if name:
            context["object_name"] = name
        widget = obj if isinstance(obj, QtWidgets.QWidget) else None
        if widget is not None:
            window = widget.window()
            if window is not None:
                title = _short_text(window.windowTitle())
                if title:
                    context["window_title"] = title
            text = None
            if isinstance(widget, (QtWidgets.QAbstractButton, QtWidgets.QLabel, QtWidgets.QLineEdit)):
                text = _short_text(widget.text())
            if not text and hasattr(widget, "toolTip"):
                try:
                    text = _short_text(widget.toolTip())
                except Exception:
                    text = None
            if text:
                context["label"] = text
            if isinstance(widget, QtWidgets.QToolButton):
                action = widget.defaultAction()
                if action is not None:
                    action_text = _short_text(action.text())
                    if action_text:
                        context["action_label"] = action_text
        return context

    def _default_log_dir(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        return os.path.join(base_dir, "logs")

    def _read_bool_env(self, key, default):
        raw = str(os.environ.get(key, "1" if default else "0")).strip().lower()
        if raw in ("1", "true", "yes", "on"):
            return True
        if raw in ("0", "false", "no", "off"):
            return False
        return bool(default)

    def _read_interval_env(self, key, default_ms=120):
        raw = str(os.environ.get(key, str(int(default_ms)))).strip()
        try:
            value_ms = int(raw)
        except (TypeError, ValueError):
            value_ms = int(default_ms)
        value_ms = max(16, min(1000, value_ms))
        return float(value_ms) / 1000.0

    def _read_event_filter_env(self, key, default):
        raw = str(os.environ.get(key, default)).strip().lower()
        if not raw:
            raw = str(default).strip().lower()
        if raw in ("all", "*"):
            return None
        values = set()
        for item in raw.split(","):
            text = item.strip().lower()
            if text:
                values.add(text)
        return values if values else None

    def _should_log_mouse_move(self, event):
        if not self._log_mouse_move:
            return False
        now = time.monotonic()
        global_pos = event.globalPos()
        point = (int(global_pos.x()), int(global_pos.y()))
        if self._last_mouse_move_pos == point:
            return False
        if now - self._last_mouse_move_ts < self._mouse_move_interval_s:
            return False
        self._last_mouse_move_ts = now
        self._last_mouse_move_pos = point
        return True

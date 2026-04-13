import faulthandler
import json
import os
import platform
import sys
import threading
import time
import traceback
from datetime import datetime, timezone
from urllib.parse import quote

from PyQt5 import QtCore, QtGui


def _utc_timestamp():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _safe_text(value, max_len=200):
    if value is None:
        return ""
    text = str(value)
    if len(text) > max_len:
        return text[: max_len - 3] + "..."
    return text


def _ascii_text(value):
    if value is None:
        return ""
    return str(value).encode("ascii", "backslashreplace").decode("ascii")


class CrashReporter:
    def __init__(self, activity_logger=None, log_dir=None, issue_url=None):
        self.activity_logger = activity_logger
        self.log_dir = log_dir or self._default_log_dir()
        self.issue_url = (
            issue_url
            or "https://github.com/Electrovian/Project-PrintNet/issues/new"
        )
        self._installed = False
        self._handling = False
        self._handled_once = False
        self._prev_hook = None
        self._prev_thread_hook = None
        self._watchdog_thread = None
        self._heartbeat_timer = None
        self._last_heartbeat = None
        self._watchdog_interval = None
        self._watchdog_timeout = None
        self._hang_handled = False
        self._main_thread_id = threading.main_thread().ident
        self._fault_file = None
        self._fault_path = None
        self._faulthandler_was_enabled = False
        self._watchdog_stop_event = threading.Event()
        self._installed_hook = None
        self._installed_thread_hook = None

    def install(self):
        if self._installed:
            return
        self._installed = True
        self._prev_hook = sys.excepthook
        self._installed_hook = self._excepthook
        sys.excepthook = self._installed_hook
        if hasattr(threading, "excepthook"):
            self._prev_thread_hook = threading.excepthook
            self._installed_thread_hook = self._thread_excepthook
            threading.excepthook = self._installed_thread_hook

    def install_faulthandler(self):
        if self._fault_file is not None:
            return
        try:
            self._faulthandler_was_enabled = bool(faulthandler.is_enabled())
            os.makedirs(self.log_dir, exist_ok=True)
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self._fault_path = os.path.join(self.log_dir, f"fault_{stamp}.log")
            self._fault_file = open(self._fault_path, "w", encoding="utf-8")
            self._fault_file.write(f"timestamp: {_utc_timestamp()}\n")
            self._fault_file.write(f"python: {sys.version}\n")
            self._fault_file.write(f"platform: {platform.platform()}\n")
            self._fault_file.write("\n")
            self._fault_file.flush()
            faulthandler.enable(file=self._fault_file, all_threads=True)
        except Exception:
            self._fault_file = None

    def install_watchdog(self, app, interval_ms: int = 500, timeout_s: float = 12.0):
        if app is None or self._watchdog_thread is not None:
            return
        self._main_thread_id = threading.main_thread().ident
        self._watchdog_interval = max(100, int(interval_ms))
        self._watchdog_timeout = max(1.0, float(timeout_s))
        self._last_heartbeat = time.monotonic()
        self._watchdog_stop_event.clear()

        self._heartbeat_timer = QtCore.QTimer(app)
        self._heartbeat_timer.setInterval(self._watchdog_interval)
        self._heartbeat_timer.timeout.connect(self._heartbeat_tick)
        self._heartbeat_timer.start()

        self._watchdog_thread = threading.Thread(
            target=self._watchdog_loop,
            name="CrashReporterWatchdog",
            daemon=True,
        )
        self._watchdog_thread.start()

    def _heartbeat_tick(self):
        self._last_heartbeat = time.monotonic()

    def _watchdog_loop(self):
        while not self._watchdog_stop_event.is_set():
            interval = self._watchdog_interval or 500
            time.sleep(interval / 1000.0)
            if self._watchdog_stop_event.is_set():
                return
            if self._hang_handled or self._handling:
                return
            last = self._last_heartbeat
            timeout = self._watchdog_timeout or 12.0
            if last is None:
                continue
            if time.monotonic() - last > timeout:
                self._handle_hang("event_loop_stall")
                return

    def _excepthook(self, exc_type, exc, tb):
        self._handle_exception(exc_type, exc, tb, thread_name=None)
        if self._prev_hook is not None:
            self._prev_hook(exc_type, exc, tb)

    def _thread_excepthook(self, args):
        thread_name = None
        if getattr(args, "thread", None) is not None:
            thread_name = args.thread.name
        self._handle_exception(
            args.exc_type, args.exc_value, args.exc_traceback, thread_name=thread_name
        )
        if self._prev_thread_hook is not None:
            self._prev_thread_hook(args)

    def _handle_exception(self, exc_type, exc, tb, thread_name=None):
        if self._handling or self._handled_once:
            return
        self._handling = True
        try:
            os.makedirs(self.log_dir, exist_ok=True)
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_path = os.path.join(self.log_dir, f"crash_{stamp}.log")
            trace_lines = traceback.format_exception(exc_type, exc, tb)
            trace_text = "".join(trace_lines)

            activity_path = None
            if self.activity_logger is not None:
                activity_path = getattr(self.activity_logger, "log_path", None)

            with open(log_path, "w", encoding="utf-8") as handle:
                handle.write(f"timestamp: {_utc_timestamp()}\n")
                handle.write(f"python: {sys.version}\n")
                handle.write(f"platform: {platform.platform()}\n")
                handle.write(f"thread: {thread_name or 'main'}\n")
                handle.write(f"argv: {sys.argv}\n")
                if activity_path:
                    handle.write(f"activity_log: {activity_path}\n")
                self._write_last_activity(handle)
                handle.write("\n")
                handle.write(trace_text)

            if self.activity_logger is not None:
                self.activity_logger.log_action(
                    "crash",
                    log_path=log_path,
                    exc_type=_safe_text(getattr(exc_type, "__name__", "Exception")),
                    message=_safe_text(exc),
                )

            self._open_issue(log_path, trace_text, exc_type, exc, activity_path)
            self._handled_once = True
        finally:
            self._handling = False

    def _handle_hang(self, reason: str):
        if self._handling or self._hang_handled:
            return
        self._handling = True
        try:
            os.makedirs(self.log_dir, exist_ok=True)
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_path = os.path.join(self.log_dir, f"crash_hang_{stamp}.log")
            frames = sys._current_frames()
            thread_id = self._main_thread_id or threading.main_thread().ident
            if thread_id in frames:
                trace_text = "".join(traceback.format_stack(frames[thread_id]))
            else:
                trace_text = "<no main thread traceback available>\n"

            activity_path = None
            if self.activity_logger is not None:
                activity_path = getattr(self.activity_logger, "log_path", None)

            with open(log_path, "w", encoding="utf-8") as handle:
                handle.write(f"timestamp: {_utc_timestamp()}\n")
                handle.write(f"python: {sys.version}\n")
                handle.write(f"platform: {platform.platform()}\n")
                handle.write("thread: main\n")
                handle.write(f"reason: {reason}\n")
                if activity_path:
                    handle.write(f"activity_log: {activity_path}\n")
                self._write_last_activity(handle)
                handle.write("\n")
                handle.write("traceback (main thread):\n")
                handle.write(trace_text)

            if self.activity_logger is not None:
                self.activity_logger.log_action(
                    "hang_detected",
                    log_path=log_path,
                    reason=_safe_text(reason),
                )
                self._hang_handled = True
        finally:
            self._handling = False

    def uninstall(self, app=None):
        timer = self._heartbeat_timer
        self._heartbeat_timer = None
        if timer is not None:
            try:
                timer.stop()
            except Exception:
                pass
            try:
                timer.deleteLater()
            except Exception:
                pass

        self._watchdog_stop_event.set()
        watchdog = self._watchdog_thread
        self._watchdog_thread = None
        if watchdog is not None and watchdog.is_alive() and watchdog is not threading.current_thread():
            try:
                watchdog.join(timeout=1.0)
            except Exception:
                pass

        if self._installed:
            if self._installed_hook is not None and sys.excepthook is self._installed_hook:
                sys.excepthook = self._prev_hook
            if (
                hasattr(threading, "excepthook")
                and self._installed_thread_hook is not None
                and threading.excepthook is self._installed_thread_hook
            ):
                threading.excepthook = self._prev_thread_hook
            self._installed = False

        self._installed_hook = None
        self._installed_thread_hook = None

        if self._fault_file is not None:
            try:
                if self._faulthandler_was_enabled:
                    faulthandler.enable(all_threads=True)
                else:
                    faulthandler.disable()
            except Exception:
                pass
            try:
                self._fault_file.close()
            except Exception:
                pass
            self._fault_file = None
            self._fault_path = None

    def _open_issue(self, log_path, trace_text, exc_type, exc, activity_path):
        if not self.issue_url:
            return
        title = f"Crash report: {getattr(exc_type, '__name__', 'Exception')}"
        message = _safe_text(exc, max_len=120)
        if message:
            title = f"{title} - {message}"

        body = self._build_issue_body(log_path, trace_text, activity_path)
        url = f"{self.issue_url}?title={quote(title)}&body={quote(body)}"

        qurl = QtCore.QUrl(url)
        opened = QtGui.QDesktopServices.openUrl(qurl)
        if not opened:
            try:
                import webbrowser
            except Exception:
                return
            webbrowser.open(url)

    def _build_issue_body(self, log_path, trace_text, activity_path):
        parts = [
            "## Crash Report",
            f"- Timestamp: {_utc_timestamp()}",
            f"- Platform: {platform.platform()}",
            f"- Python: {sys.version.split()[0]}",
            f"- Crash log: {log_path}",
        ]
        if activity_path:
            parts.append(f"- Activity log: {activity_path}")
        parts.append("")
        parts.append("## Traceback")
        body = "\n".join(parts) + "\n```\n" + trace_text + "\n```\n"

        body = _ascii_text(body)
        max_len = 6000
        if len(body) > max_len:
            body = body[: max_len - 40] + "\n```\n...truncated...\n```\n"
        return body

    def _write_last_activity(self, handle):
        if self.activity_logger is None:
            return
        record = getattr(self.activity_logger, "last_record", None)
        if not record:
            return
        try:
            payload = json.dumps(record, ensure_ascii=True)
        except Exception:
            payload = _safe_text(record, max_len=400)
        if payload:
            handle.write(f"last_activity: {payload}\n")

    def _default_log_dir(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        return os.path.join(base_dir, "logs")

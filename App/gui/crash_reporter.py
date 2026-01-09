import os
import platform
import sys
import threading
import traceback
from datetime import datetime
from urllib.parse import quote

from PyQt5 import QtCore, QtGui


def _utc_timestamp():
    return datetime.utcnow().isoformat(timespec="milliseconds") + "Z"


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

    def install(self):
        if self._installed:
            return
        self._installed = True
        self._prev_hook = sys.excepthook
        sys.excepthook = self._excepthook
        if hasattr(threading, "excepthook"):
            self._prev_thread_hook = threading.excepthook
            threading.excepthook = self._thread_excepthook

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

    def _default_log_dir(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        return os.path.join(base_dir, "logs")

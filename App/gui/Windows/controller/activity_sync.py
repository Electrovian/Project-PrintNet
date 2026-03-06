from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any, Mapping

from PyQt5 import QtCore

from ...workers import Worker
from integrations.web_backend_activity import WebBackendActivityClient, WebBackendActivityError


def _env_bool(name: str, default: bool) -> bool:
    raw = str(os.environ.get(name, "1" if default else "0")).strip().lower()
    if raw in ("1", "true", "yes", "on"):
        return True
    if raw in ("0", "false", "no", "off"):
        return False
    return bool(default)


def _env_int(name: str, default: int, minimum: int, maximum: int) -> int:
    raw = str(os.environ.get(name, str(default))).strip()
    try:
        value = int(raw)
    except (TypeError, ValueError):
        value = int(default)
    value = max(minimum, min(maximum, value))
    return int(value)


def _parse_iso_datetime(value: object) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    normalized = text
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _format_when(created_at: datetime | None, fallback: str = "") -> str:
    if created_at is None:
        return str(fallback or "").strip()
    try:
        return created_at.astimezone().strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return str(fallback or "").strip()


def _format_age(created_at: datetime | None) -> str:
    if created_at is None:
        return "n/a"
    now = datetime.now(timezone.utc)
    delta_seconds = int(max(0, (now - created_at.astimezone(timezone.utc)).total_seconds()))
    if delta_seconds < 60:
        return f"{delta_seconds}s"
    if delta_seconds < 3600:
        mins = delta_seconds // 60
        secs = delta_seconds % 60
        if secs <= 0:
            return f"{mins}m"
        return f"{mins}m {secs}s"
    if delta_seconds < 86400:
        hours = delta_seconds // 3600
        mins = (delta_seconds % 3600) // 60
        if mins <= 0:
            return f"{hours}h"
        return f"{hours}h {mins}m"
    days = delta_seconds // 86400
    hours = (delta_seconds % 86400) // 3600
    if hours <= 0:
        return f"{days}d"
    return f"{days}d {hours}h"


def _job_to_activity_entry(job: Mapping[str, Any]) -> dict[str, Any]:
    job_id = str(job.get("job_id", "")).strip()
    model_name = str(job.get("model_name", "")).strip()
    status = str(job.get("status", "")).strip() or "unknown"
    profile_id = str(job.get("profile_id", "")).strip()
    printer_id = str(job.get("printer_id", "")).strip() or "Unassigned"
    requested_by = str(job.get("requested_by", "")).strip() or "unknown"
    created_raw = str(job.get("created_at_utc", "")).strip()
    created_at = _parse_iso_datetime(created_raw)
    sort_ts = float(created_at.timestamp()) if created_at is not None else 0.0

    label = model_name or job_id or "job"
    return {
        "job": label,
        "status": status,
        "duration": _format_age(created_at),
        "material": profile_id or "n/a",
        "when": _format_when(created_at, fallback=created_raw),
        "printer": printer_id,
        "user": requested_by,
        "_sort_ts": sort_ts,
    }


class ActivitySyncMixin:
    def _init_activity_sync(self) -> None:
        timer = getattr(self, "_activity_sync_timer", None)
        if isinstance(timer, QtCore.QTimer):
            timer.stop()
            timer.deleteLater()

        self._activity_sync_inflight = False
        self._activity_sync_last_error = ""
        self._activity_sync_last_count = -1
        self._activity_rows_cache = []
        self._activity_me_user = self._resolve_activity_me_user()

        self._activity_sync_client = self._build_activity_sync_client()
        self._activity_sync_interval_ms = _env_int(
            "EON_ACTIVITY_SYNC_INTERVAL_MS",
            default=5000,
            minimum=1000,
            maximum=60000,
        )
        self._activity_sync_timer = QtCore.QTimer(self)
        self._activity_sync_timer.setInterval(self._activity_sync_interval_ms)
        self._activity_sync_timer.timeout.connect(self._on_activity_sync_timer)
        if self._activity_sync_client is not None:
            self._activity_sync_timer.start()

    def _resolve_activity_me_user(self) -> str:
        explicit = str(os.environ.get("EON_ACTIVITY_ME_USER", "")).strip().lower()
        if explicit:
            return explicit
        username = str(os.environ.get("USERNAME", "")).strip().lower()
        return username

    def _build_activity_sync_client(self) -> WebBackendActivityClient | None:
        enabled = _env_bool("EON_ACTIVITY_SYNC_ENABLED", True)
        if not enabled:
            return None

        base_url = str(os.environ.get("EON_ACTIVITY_BACKEND_URL", "http://127.0.0.1:8000/api/v1")).strip()
        if not base_url:
            return None

        actor_user = str(os.environ.get("EON_ACTIVITY_SYNC_USER", "desktop-operator")).strip() or "desktop-operator"
        actor_role = str(os.environ.get("EON_ACTIVITY_SYNC_ROLE", "operator")).strip().lower() or "operator"
        timeout_ms = _env_int(
            "EON_ACTIVITY_SYNC_TIMEOUT_MS",
            default=4000,
            minimum=500,
            maximum=30000,
        )
        try:
            return WebBackendActivityClient(
                base_url=base_url,
                actor_user=actor_user,
                actor_role=actor_role,
                timeout_seconds=float(timeout_ms) / 1000.0,
            )
        except WebBackendActivityError:
            return None

    def _on_activity_sync_timer(self) -> None:
        if str(getattr(self, "_active_mode", "")).strip().lower() != "activity":
            return
        self._request_activity_refresh(force=False)

    def _request_activity_refresh(self, force: bool = False) -> None:
        if not hasattr(self, "activity_view"):
            return
        if self._activity_sync_client is None:
            return
        if not force and str(getattr(self, "_active_mode", "")).strip().lower() != "activity":
            return
        if bool(getattr(self, "_activity_sync_inflight", False)):
            return

        self._activity_sync_inflight = True
        worker = Worker(self._fetch_activity_rows)
        worker.signals.finished.connect(self._on_activity_rows_ready)
        worker.signals.error.connect(self._on_activity_rows_error)
        self._start_worker(worker)

    def _fetch_activity_rows(self) -> dict[str, Any]:
        if self._activity_sync_client is None:
            return {"rows": []}
        snapshot = self._activity_sync_client.fetch_queue_snapshot()
        jobs = snapshot.get("jobs", [])
        rows: list[dict[str, Any]] = []
        if isinstance(jobs, list):
            for item in jobs:
                if isinstance(item, Mapping):
                    rows.append(_job_to_activity_entry(item))
        rows.sort(key=lambda row: float(row.get("_sort_ts", 0.0)), reverse=True)
        for row in rows:
            row.pop("_sort_ts", None)
        return {
            "rows": rows,
            "job_count": int(snapshot.get("job_count", len(rows)) or len(rows)),
        }

    def _on_activity_rows_ready(self, payload: object) -> None:
        self._activity_sync_inflight = False
        rows = []
        if isinstance(payload, Mapping):
            raw_rows = payload.get("rows", [])
            if isinstance(raw_rows, list):
                rows = [dict(item) for item in raw_rows if isinstance(item, Mapping)]
        self._activity_rows_cache = rows

        me_rows = self._build_me_rows(rows)
        if hasattr(self, "activity_view"):
            self.activity_view.set_me_activity(me_rows)
            self.activity_view.set_printer_activity(rows)

        self._activity_sync_last_error = ""
        if str(getattr(self, "_active_mode", "")).strip().lower() == "activity":
            count = len(rows)
            if count != int(getattr(self, "_activity_sync_last_count", -1)):
                self._activity_sync_last_count = count
                self.statusBar().showMessage(f"Activity synced ({count} jobs)")

    def _on_activity_rows_error(self, message: str) -> None:
        self._activity_sync_inflight = False
        detail = str(message or "").strip() or "Activity sync failed."
        if detail != str(getattr(self, "_activity_sync_last_error", "")):
            self._activity_sync_last_error = detail
            if str(getattr(self, "_active_mode", "")).strip().lower() == "activity":
                self.statusBar().showMessage(f"Activity sync unavailable: {detail}")

    def _build_me_rows(self, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if not rows:
            return []
        hint = str(getattr(self, "_activity_me_user", "")).strip().lower()
        if not hint:
            return list(rows)
        filtered = []
        for row in rows:
            user = str(row.get("user", "")).strip().lower()
            if user == hint:
                filtered.append(row)
        if filtered:
            return filtered
        return list(rows)

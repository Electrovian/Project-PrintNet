from __future__ import annotations

from collections import deque
from datetime import datetime, timezone
from typing import Any


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _normalize_job_value(value: object, fallback: str = "") -> str:
    text = str(value or "").strip()
    if text:
        return text
    return str(fallback or "").strip()


class ActivityStore:
    def __init__(self, *, max_events: int = 5000, max_jobs: int = 1000):
        self.max_events = max(10, int(max_events))
        self.max_jobs = max(1, int(max_jobs))
        self._seq = 0
        self._events: deque[dict[str, Any]] = deque()
        self._jobs_by_id: dict[str, dict[str, Any]] = {}
        self._jobs_by_user: dict[str, set[str]] = {}
        self._jobs_by_status: dict[str, set[str]] = {}
        self._recent_job_ids: list[str] = []

    @property
    def max_cursor(self) -> int:
        return int(self._seq)

    def record_job_event(
        self,
        *,
        event_type: object,
        job_id: object,
        status: object,
        model_name: object,
        profile_id: object,
        printer_id: object,
        requested_by: object,
        queue: object,
        ts_utc: object | None = None,
        created_at_utc: object | None = None,
        print_started_at_utc: object | None = None,
    ) -> dict[str, Any]:
        normalized_job_id = _normalize_job_value(job_id)
        if not normalized_job_id:
            return {}
        event_ts = _normalize_job_value(ts_utc, fallback=_utc_now_iso())
        created_ts = _normalize_job_value(created_at_utc, fallback=event_ts)
        normalized_status = _normalize_job_value(status, fallback="unknown")
        status_key = normalized_status.lower()
        normalized_user = _normalize_job_value(requested_by)
        existing = self._jobs_by_id.get(normalized_job_id)
        existing_started = str(existing.get("print_started_at_utc", "")).strip() if existing else ""
        explicit_started = _normalize_job_value(print_started_at_utc)
        if explicit_started:
            started_ts = explicit_started
        elif status_key in {"running", "printing"}:
            started_ts = existing_started or event_ts
        elif status_key in {"completed", "failed", "error", "cancelled"}:
            started_ts = existing_started
        else:
            started_ts = ""

        self._seq += 1
        item = {
            "seq": int(self._seq),
            "ts_utc": event_ts,
            "job_id": normalized_job_id,
            "status": normalized_status,
            "event_type": _normalize_job_value(event_type, fallback=normalized_status),
            "model_name": _normalize_job_value(model_name),
            "profile_id": _normalize_job_value(profile_id),
            "printer_id": _normalize_job_value(printer_id),
            "requested_by": normalized_user,
            "queue": _normalize_job_value(queue),
            "created_at_utc": created_ts,
            "print_started_at_utc": started_ts,
        }
        self._events.append(item)
        while len(self._events) > self.max_events:
            self._events.popleft()

        self._upsert_job_row(item)
        return dict(item)

    def _upsert_job_row(self, item: dict[str, Any]) -> None:
        job_id = str(item.get("job_id", "")).strip()
        if not job_id:
            return
        existing = self._jobs_by_id.get(job_id)
        existing_user = str(existing.get("requested_by", "")).strip() if existing else ""
        existing_status = str(existing.get("status", "")).strip() if existing else ""
        existing_started = str(existing.get("print_started_at_utc", "")).strip() if existing else ""
        created_ts = str(item.get("created_at_utc", "")).strip()
        if not created_ts and existing is not None:
            created_ts = str(existing.get("created_at_utc", "")).strip()
        if not created_ts:
            created_ts = str(item.get("ts_utc", "")).strip()
        status = str(item.get("status", "")).strip() or "unknown"
        status_key = status.lower()
        event_ts = str(item.get("ts_utc", "")).strip()
        started_ts = str(item.get("print_started_at_utc", "")).strip()
        if status_key in {"running", "printing"}:
            if not started_ts:
                started_ts = existing_started or event_ts
        elif status_key in {"completed", "failed", "error", "cancelled"}:
            if not started_ts:
                started_ts = existing_started
        else:
            started_ts = ""

        row = {
            "job_id": job_id,
            "model_name": str(item.get("model_name", "")).strip(),
            "profile_id": str(item.get("profile_id", "")).strip(),
            "printer_id": str(item.get("printer_id", "")).strip(),
            "requested_by": str(item.get("requested_by", "")).strip(),
            "queue": str(item.get("queue", "")).strip(),
            "status": status,
            "created_at_utc": created_ts,
            "updated_at_utc": str(item.get("ts_utc", "")).strip(),
            "print_started_at_utc": started_ts,
            "latest_seq": int(item.get("seq", 0) or 0),
        }
        self._jobs_by_id[job_id] = row

        user = str(row.get("requested_by", "")).strip()
        if existing_user and existing_user != user:
            self._remove_from_index(self._jobs_by_user, existing_user, job_id)
        if user:
            self._jobs_by_user.setdefault(user, set()).add(job_id)

        status = str(row.get("status", "")).strip()
        if existing_status and existing_status != status:
            self._remove_from_index(self._jobs_by_status, existing_status, job_id)
        if status:
            self._jobs_by_status.setdefault(status, set()).add(job_id)

        if job_id in self._recent_job_ids:
            self._recent_job_ids.remove(job_id)
        self._recent_job_ids.insert(0, job_id)
        while len(self._recent_job_ids) > self.max_jobs:
            dropped = self._recent_job_ids.pop()
            self._drop_job(dropped)

    def _drop_job(self, job_id: str) -> None:
        row = self._jobs_by_id.pop(job_id, None)
        if not row:
            return
        user = str(row.get("requested_by", "")).strip()
        status = str(row.get("status", "")).strip()
        if user:
            self._remove_from_index(self._jobs_by_user, user, job_id)
        if status:
            self._remove_from_index(self._jobs_by_status, status, job_id)

    @staticmethod
    def _remove_from_index(index: dict[str, set[str]], key: str, job_id: str) -> None:
        rows = index.get(key)
        if not rows:
            return
        rows.discard(job_id)
        if not rows:
            index.pop(key, None)

    def list_recent_jobs(self, *, requested_by: str = "") -> list[dict[str, Any]]:
        normalized_user = str(requested_by or "").strip()
        allowed: set[str] | None = None
        if normalized_user:
            allowed = self._jobs_by_user.get(normalized_user, set())
        rows: list[dict[str, Any]] = []
        for job_id in self._recent_job_ids:
            if allowed is not None and job_id not in allowed:
                continue
            row = self._jobs_by_id.get(job_id)
            if row is None:
                continue
            rows.append(dict(row))
        return rows

    def read_feed(
        self,
        *,
        cursor: int = 0,
        limit: int = 200,
        requested_by: str = "",
    ) -> dict[str, Any]:
        cursor_in = max(0, int(cursor))
        bounded_limit = max(1, min(1000, int(limit)))
        max_cursor = int(self._seq)
        if self._events:
            first_seq = int(self._events[0].get("seq", 1) or 1)
        else:
            first_seq = max_cursor + 1
        reset_required = bool(self._events) and cursor_in > 0 and cursor_in < (first_seq - 1)
        effective_cursor = (first_seq - 1) if reset_required else cursor_in
        owner = str(requested_by or "").strip()

        filtered: list[dict[str, Any]] = []
        for item in self._events:
            seq = int(item.get("seq", 0) or 0)
            if seq <= effective_cursor:
                continue
            if owner and str(item.get("requested_by", "")).strip() != owner:
                continue
            filtered.append(dict(item))
        has_more = len(filtered) > bounded_limit
        items = filtered[:bounded_limit]

        cursor_out = effective_cursor
        if items:
            cursor_out = int(items[-1].get("seq", effective_cursor) or effective_cursor)
        elif cursor_out > max_cursor:
            cursor_out = max_cursor

        return {
            "items": items,
            "cursor_in": cursor_in,
            "cursor_out": int(cursor_out),
            "max_cursor": max_cursor,
            "has_more": bool(has_more),
            "reset_required": bool(reset_required),
        }

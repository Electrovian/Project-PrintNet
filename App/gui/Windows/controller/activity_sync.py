from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any, Mapping

from PyQt5 import QtCore, QtWidgets

from ...workers import Worker
from ...i18n import tr
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


def _coerce_duration_seconds(value: object) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    try:
        seconds = float(value)
    except (TypeError, ValueError):
        text = str(value or "").strip()
        if not text:
            return None
        try:
            seconds = float(text)
        except (TypeError, ValueError):
            return None
    if not seconds >= 0.0:
        return None
    return float(seconds)


def _format_duration(seconds: float | None) -> str:
    if seconds is None:
        return "n/a"
    total = int(max(0, round(float(seconds))))
    if total < 60:
        return f"{total}s"
    if total < 3600:
        mins = total // 60
        secs = total % 60
        return f"{mins}m" if secs <= 0 else f"{mins}m {secs}s"
    if total < 86400:
        hours = total // 3600
        mins = (total % 3600) // 60
        return f"{hours}h" if mins <= 0 else f"{hours}h {mins}m"
    days = total // 86400
    hours = (total % 86400) // 3600
    return f"{days}d" if hours <= 0 else f"{days}d {hours}h"


def _derive_print_duration_seconds(
    *,
    status: str,
    created_at: datetime | None,
    updated_at: datetime | None,
) -> float | None:
    normalized_status = str(status or "").strip().lower()
    if normalized_status not in {"running", "printing", "completed", "failed", "error", "cancelled"}:
        return None
    if created_at is None:
        return None
    created_utc = created_at.astimezone(timezone.utc)
    if normalized_status in {"completed", "failed", "error", "cancelled"}:
        end_utc = updated_at.astimezone(timezone.utc) if updated_at is not None else created_utc
        return max(0.0, (end_utc - created_utc).total_seconds())
    now_utc = datetime.now(timezone.utc)
    return max(0.0, (now_utc - created_utc).total_seconds())


def _coerce_int(value: object, *, default: int, minimum: int, maximum: int) -> int:
    try:
        parsed = int(value)  # type: ignore[arg-type]
    except Exception:
        parsed = int(default)
    if parsed < minimum:
        return int(minimum)
    if parsed > maximum:
        return int(maximum)
    return int(parsed)


def _normalize_job_payload(value: Mapping[str, Any]) -> dict[str, Any]:
    created = str(value.get("created_at_utc", "")).strip()
    updated = str(value.get("updated_at_utc", "")).strip() or created
    seq = _coerce_int(value.get("latest_seq", value.get("_seq", 0)), default=0, minimum=0, maximum=2_000_000_000)
    return {
        "job_id": str(value.get("job_id", "")).strip(),
        "model_name": str(value.get("model_name", "")).strip(),
        "status": str(value.get("status", "")).strip() or "unknown",
        "profile_id": str(value.get("profile_id", "")).strip(),
        "printer_id": str(value.get("printer_id", "")).strip(),
        "requested_by": str(value.get("requested_by", "")).strip(),
        "queue": str(value.get("queue", "")).strip(),
        "created_at_utc": created,
        "updated_at_utc": updated,
        "_seq": seq,
    }


def _job_sort_key(job: Mapping[str, Any]) -> tuple[int, float]:
    seq = _coerce_int(job.get("_seq", 0), default=0, minimum=0, maximum=2_000_000_000)
    updated_at = _parse_iso_datetime(job.get("updated_at_utc"))
    updated_ts = float(updated_at.timestamp()) if updated_at is not None else 0.0
    return seq, updated_ts


def _merge_feed_items(
    jobs_by_id: dict[str, dict[str, Any]],
    feed_items: list[Mapping[str, Any]],
) -> dict[str, dict[str, Any]]:
    merged = {key: dict(value) for key, value in jobs_by_id.items()}
    for item in feed_items:
        job_id = str(item.get("job_id", "")).strip()
        if not job_id:
            continue
        seq = _coerce_int(item.get("seq", 0), default=0, minimum=0, maximum=2_000_000_000)
        existing = merged.get(job_id)
        if existing is not None:
            existing_seq = _coerce_int(existing.get("_seq", 0), default=0, minimum=0, maximum=2_000_000_000)
            if seq < existing_seq:
                continue
        created_raw = str(item.get("created_at_utc", "")).strip()
        updated_raw = str(item.get("ts_utc", "")).strip()
        if not created_raw and existing is not None:
            created_raw = str(existing.get("created_at_utc", "")).strip()
        if not created_raw:
            created_raw = updated_raw
        merged[job_id] = {
            "job_id": job_id,
            "model_name": str(item.get("model_name", "")).strip(),
            "status": str(item.get("status", "")).strip() or "unknown",
            "profile_id": str(item.get("profile_id", "")).strip(),
            "printer_id": str(item.get("printer_id", "")).strip(),
            "requested_by": str(item.get("requested_by", "")).strip(),
            "queue": str(item.get("queue", "")).strip(),
            "created_at_utc": created_raw,
            "updated_at_utc": updated_raw or created_raw,
            "_seq": seq,
        }
    return merged


def _job_to_activity_entry(job: Mapping[str, Any]) -> dict[str, Any]:
    job_id = str(job.get("job_id", "")).strip()
    model_name = str(job.get("model_name", "")).strip()
    status = str(job.get("status", "")).strip() or "unknown"
    profile_id = str(job.get("profile_id", "")).strip()
    printer_id = str(job.get("printer_id", "")).strip() or "Unassigned"
    requested_by = str(job.get("requested_by", "")).strip() or "unknown"
    created_raw = str(job.get("created_at_utc", "")).strip()
    updated_raw = str(job.get("updated_at_utc", "")).strip()
    created_at = _parse_iso_datetime(created_raw)
    updated_at = _parse_iso_datetime(updated_raw)
    explicit_duration = None
    for key in (
        "duration_seconds",
        "duration_s",
        "print_duration_seconds",
        "print_duration_s",
        "print_duration",
        "time_seconds",
    ):
        explicit_duration = _coerce_duration_seconds(job.get(key))
        if explicit_duration is not None:
            break
    duration_seconds = (
        explicit_duration
        if explicit_duration is not None
        else _derive_print_duration_seconds(
            status=status,
            created_at=created_at,
            updated_at=updated_at,
        )
    )
    sort_dt = updated_at or created_at
    sort_ts = float(sort_dt.timestamp()) if sort_dt is not None else 0.0
    seq = _coerce_int(job.get("_seq", 0), default=0, minimum=0, maximum=2_000_000_000)

    label = model_name or job_id or "job"
    return {
        "job_id": job_id,
        "job": label,
        "status": status,
        "duration": _format_duration(duration_seconds),
        "material": profile_id or "n/a",
        "when": _format_when(created_at, fallback=created_raw),
        "created_at_utc": created_raw,
        "printer": printer_id,
        "user": requested_by,
        "_sort_ts": sort_ts,
        "_seq": seq,
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
        self._compliance_blocked = False
        self._compliance_reason_code = ""
        self._compliance_detail = ""
        self._compliance_dialog_shown = False
        self._activity_jobs_by_id: dict[str, dict[str, Any]] = {}
        self._activity_cursor = 0
        self._activity_me_user = self._resolve_activity_me_user()

        self._activity_sync_client = self._build_activity_sync_client()
        self._activity_feed_limit = _env_int(
            "EON_ACTIVITY_FEED_LIMIT",
            default=200,
            minimum=20,
            maximum=1000,
        )
        self._activity_sync_interval_ms = _env_int(
            "EON_ACTIVITY_SYNC_INTERVAL_MS",
            default=5000,
            minimum=1000,
            maximum=60000,
        )
        self._activity_sync_timer = QtCore.QTimer(self)
        self._activity_sync_timer.setInterval(self._activity_sync_interval_ms)
        self._activity_sync_timer.timeout.connect(self._on_activity_sync_timer)
        self._refresh_compliance_status()
        if self._activity_sync_client is not None:
            if not bool(getattr(self, "_compliance_blocked", False)):
                self._activity_sync_timer.start()
        self._apply_compliance_banner()

    def _refresh_compliance_status(self) -> None:
        client = getattr(self, "_activity_sync_client", None)
        if client is None:
            return
        try:
            payload = client.fetch_compliance_region()
        except Exception:
            return
        decision = str(payload.get("decision", "allow")).strip().lower()
        reason_code = str(payload.get("reason_code", "")).strip()
        detail = str(payload.get("detail", "")).strip()
        if decision == "deny":
            self._set_compliance_block(reason_code=reason_code, detail=detail)
            return
        self._clear_compliance_block()

    def _set_compliance_block(self, *, reason_code: str, detail: str) -> None:
        self._compliance_blocked = True
        self._compliance_reason_code = str(reason_code or "REGION_BLOCKED").strip()
        self._compliance_detail = str(detail or "Cloud-backed actions are blocked by region policy.").strip()
        timer = getattr(self, "_activity_sync_timer", None)
        if isinstance(timer, QtCore.QTimer):
            timer.stop()
        self._apply_compliance_banner()
        status_text = tr(
            "compliance.desktop.blocked_status",
            "Cloud activity disabled by compliance policy.",
        )
        if hasattr(self, "statusBar"):
            self.statusBar().showMessage(status_text)
        if not bool(getattr(self, "_compliance_dialog_shown", False)):
            self._compliance_dialog_shown = True

            def _show_dialog() -> None:
                parent = getattr(self, "main", None)
                if not isinstance(parent, QtWidgets.QWidget):
                    parent = None
                QtWidgets.QMessageBox.warning(
                    parent,
                    tr("compliance.desktop.dialog_title", "Compliance Restriction"),
                    f"{self._compliance_reason_code}\n\n{self._compliance_detail}",
                )

            QtCore.QTimer.singleShot(0, _show_dialog)

    def _clear_compliance_block(self) -> None:
        self._compliance_blocked = False
        self._compliance_reason_code = ""
        self._compliance_detail = ""
        self._apply_compliance_banner()

    def _apply_compliance_banner(self) -> None:
        if not hasattr(self, "activity_view"):
            return
        if bool(getattr(self, "_compliance_blocked", False)):
            self.activity_view.set_compliance_banner(self._compliance_detail)
        else:
            self.activity_view.set_compliance_banner("")

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

        service_token = str(os.environ.get("EON_ACTIVITY_SERVICE_TOKEN", "")).strip()
        if not service_token:
            return None
        timeout_ms = _env_int(
            "EON_ACTIVITY_SYNC_TIMEOUT_MS",
            default=4000,
            minimum=500,
            maximum=30000,
        )
        try:
            return WebBackendActivityClient(
                base_url=base_url,
                service_token=service_token,
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
        if bool(getattr(self, "_compliance_blocked", False)):
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
        cursor = _coerce_int(getattr(self, "_activity_cursor", 0), default=0, minimum=0, maximum=2_000_000_000)
        jobs_by_id = {
            str(key): dict(value)
            for key, value in getattr(self, "_activity_jobs_by_id", {}).items()
            if isinstance(value, Mapping)
        }

        feed = self._activity_sync_client.fetch_activity_feed(cursor=cursor, limit=self._activity_feed_limit)
        if bool(feed.get("reset_required", False)):
            snapshot = self._activity_sync_client.fetch_queue_snapshot()
            jobs_by_id = {}
            snapshot_jobs = snapshot.get("jobs", [])
            if isinstance(snapshot_jobs, list):
                for item in snapshot_jobs:
                    if isinstance(item, Mapping):
                        row = _normalize_job_payload(item)
                        job_id = str(row.get("job_id", "")).strip()
                        if job_id:
                            jobs_by_id[job_id] = row

        feed_items: list[Mapping[str, Any]] = []
        raw_items = feed.get("items", [])
        if isinstance(raw_items, list):
            feed_items = [item for item in raw_items if isinstance(item, Mapping)]
        jobs_by_id = _merge_feed_items(jobs_by_id, feed_items)
        cursor_out = _coerce_int(feed.get("cursor_out", cursor), default=cursor, minimum=0, maximum=2_000_000_000)

        ordered_jobs = sorted(jobs_by_id.values(), key=_job_sort_key, reverse=True)
        rows: list[dict[str, Any]] = [_job_to_activity_entry(item) for item in ordered_jobs]
        rows.sort(
            key=lambda row: (
                _coerce_int(row.get("_seq", 0), default=0, minimum=0, maximum=2_000_000_000),
                float(row.get("_sort_ts", 0.0)),
            ),
            reverse=True,
        )
        for row in rows:
            row.pop("_sort_ts", None)
            row.pop("_seq", None)
        return {
            "rows": rows,
            "jobs_by_id": jobs_by_id,
            "cursor": cursor_out,
            "job_count": len(jobs_by_id),
        }

    def _on_activity_rows_ready(self, payload: object) -> None:
        self._activity_sync_inflight = False
        rows = []
        if isinstance(payload, Mapping):
            raw_rows = payload.get("rows", [])
            if isinstance(raw_rows, list):
                rows = [dict(item) for item in raw_rows if isinstance(item, Mapping)]
            raw_jobs = payload.get("jobs_by_id", {})
            if isinstance(raw_jobs, Mapping):
                self._activity_jobs_by_id = {
                    str(key): dict(value)
                    for key, value in raw_jobs.items()
                    if isinstance(value, Mapping)
                }
            self._activity_cursor = _coerce_int(
                payload.get("cursor", getattr(self, "_activity_cursor", 0)),
                default=int(getattr(self, "_activity_cursor", 0)),
                minimum=0,
                maximum=2_000_000_000,
            )
        self._activity_rows_cache = rows

        me_rows = self._build_me_rows(rows)
        if hasattr(self, "activity_view"):
            self.activity_view.set_me_activity(me_rows)
            self.activity_view.set_printer_activity(rows)

        self._activity_sync_last_error = ""
        self._apply_compliance_banner()
        if str(getattr(self, "_active_mode", "")).strip().lower() == "activity":
            count = len(rows)
            if count != int(getattr(self, "_activity_sync_last_count", -1)):
                self._activity_sync_last_count = count
                self.statusBar().showMessage(f"Activity synced ({count} jobs)")

    def _on_activity_rows_error(self, message: str) -> None:
        self._activity_sync_inflight = False
        detail = str(message or "").strip() or "Activity sync failed."
        upper = detail.upper()
        if "REGION_BLOCKED" in upper or "REGION_GEO_UNDETERMINED" in upper:
            reason = "REGION_BLOCKED" if "REGION_BLOCKED" in upper else "REGION_GEO_UNDETERMINED"
            self._set_compliance_block(reason_code=reason, detail=detail)
            return
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
        return filtered

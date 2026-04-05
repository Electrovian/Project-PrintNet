import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

try:
    from gui.Windows.controller.activity_sync import (  # noqa: E402
        ActivitySyncMixin,
        _load_activity_jobs_cache,
        _normalize_job_payload,
        _rows_from_jobs_by_id,
        _save_activity_jobs_cache,
    )
    from gui.i18n import tr  # noqa: E402
except Exception:
    ActivitySyncMixin = None
    _load_activity_jobs_cache = None
    _normalize_job_payload = None
    _rows_from_jobs_by_id = None
    _save_activity_jobs_cache = None
    tr = None


def _job(
    job_id: str,
    *,
    seq: int,
    status: str,
    created_at: str,
    updated_at: str,
    requested_by: str = "alice",
    model_name: str | None = None,
    printer_id: str = "printer-01",
) -> dict[str, object]:
    return {
        "job_id": job_id,
        "model_name": model_name or f"{job_id}.stl",
        "status": status,
        "profile_id": "p-default-pla",
        "printer_id": printer_id,
        "requested_by": requested_by,
        "queue": "default",
        "created_at_utc": created_at,
        "updated_at_utc": updated_at,
        "print_started_at_utc": created_at if status in {"running", "printing", "completed"} else "",
        "_seq": seq,
    }


class _FakeActivityView:
    def __init__(self) -> None:
        self.me_rows = []
        self.printer_rows = []
        self.compliance_banner = ""
        self.cache_banner = ""

    def set_me_activity(self, rows) -> None:
        self.me_rows = list(rows or [])

    def set_printer_activity(self, rows) -> None:
        self.printer_rows = list(rows or [])

    def set_compliance_banner(self, message: str = "") -> None:
        self.compliance_banner = str(message or "")

    def set_cache_banner(self, message: str = "") -> None:
        self.cache_banner = str(message or "")


class _FakeStatusBar:
    def __init__(self) -> None:
        self.messages: list[str] = []

    def showMessage(self, message: str) -> None:
        self.messages.append(str(message))


class _FakeTimer:
    class _Signal:
        def __init__(self) -> None:
            self.callbacks = []

        def connect(self, callback) -> None:
            self.callbacks.append(callback)

    def __init__(self, *_args, **_kwargs) -> None:
        self.interval_ms = 0
        self.started = False
        self.timeout = self._Signal()

    def setInterval(self, value: int) -> None:
        self.interval_ms = int(value)

    def start(self) -> None:
        self.started = True

    def stop(self) -> None:
        self.started = False

    def deleteLater(self) -> None:
        return None


class _Holder(ActivitySyncMixin if ActivitySyncMixin is not None else object):
    def __init__(self, *, client=None, compliance_blocked: bool = False):
        self.activity_view = _FakeActivityView()
        self._status_bar = _FakeStatusBar()
        self._active_mode = "activity"
        self._client = client
        self._compliance_should_block = compliance_blocked
        self.main = None

    def statusBar(self):
        return self._status_bar

    def _start_worker(self, worker) -> None:
        self.worker = worker

    def _build_activity_sync_client(self):
        return self._client

    def _resolve_activity_me_user(self) -> str:
        return ""

    def _refresh_compliance_status(self) -> None:
        if self._compliance_should_block:
            self._compliance_blocked = True
            self._compliance_reason_code = "REGION_BLOCKED"
            self._compliance_detail = "blocked by policy"
            self._apply_compliance_banner()
            return
        self._clear_compliance_block()


@unittest.skipIf(ActivitySyncMixin is None, "activity sync module unavailable")
class ActivitySyncPersistenceTests(unittest.TestCase):
    def test_cache_round_trip_preserves_normalized_jobs_and_cursor(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache_path = Path(tmp).joinpath("activity_jobs_cache.json")
            jobs_by_id = {
                "job-2": _job(
                    "job-2",
                    seq=20,
                    status="completed",
                    created_at="2026-03-01T12:00:00+00:00",
                    updated_at="2026-03-01T12:30:00+00:00",
                    requested_by="bob",
                ),
                "job-1": _job(
                    "job-1",
                    seq=10,
                    status="queued",
                    created_at="2026-03-01T11:00:00+00:00",
                    updated_at="2026-03-01T11:00:00+00:00",
                ),
            }
            _save_activity_jobs_cache(jobs_by_id, 321, cache_path)

            payload = _load_activity_jobs_cache(cache_path)

            self.assertTrue(payload["available"])
            self.assertEqual(payload["cursor"], 321)
            self.assertEqual(
                payload["jobs_by_id"],
                {job_id: _normalize_job_payload(job) for job_id, job in jobs_by_id.items()},
            )
            raw_payload = json.loads(cache_path.read_text(encoding="utf-8"))
            self.assertEqual(raw_payload["version"], 1)
            self.assertTrue(str(raw_payload.get("saved_at_utc", "")).strip())

    def test_cache_load_ignores_invalid_payloads_and_bad_jobs(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache_path = Path(tmp).joinpath("activity_jobs_cache.json")

            cache_path.write_text("{not-json", encoding="utf-8")
            self.assertFalse(_load_activity_jobs_cache(cache_path)["available"])

            cache_path.write_text(json.dumps({"version": 999, "jobs": [], "cursor": 0}), encoding="utf-8")
            self.assertFalse(_load_activity_jobs_cache(cache_path)["available"])

            cache_path.write_text(json.dumps({"version": 1, "jobs": {}, "cursor": 0}), encoding="utf-8")
            self.assertFalse(_load_activity_jobs_cache(cache_path)["available"])

            cache_path.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "saved_at_utc": "2026-03-01T12:00:00+00:00",
                        "cursor": 9,
                        "jobs": [
                            "bad-entry",
                            {"job_id": "", "status": "queued"},
                            _job(
                                "job-3",
                                seq=3,
                                status="running",
                                created_at="2026-03-01T12:00:00+00:00",
                                updated_at="2026-03-01T12:05:00+00:00",
                            ),
                        ],
                    }
                ),
                encoding="utf-8",
            )

            payload = _load_activity_jobs_cache(cache_path)

            self.assertTrue(payload["available"])
            self.assertEqual(payload["cursor"], 9)
            self.assertEqual(list(payload["jobs_by_id"].keys()), ["job-3"])

    def test_cache_restore_rebuilds_rows_in_live_sort_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache_path = Path(tmp).joinpath("activity_jobs_cache.json")
            jobs_by_id = {
                "job-1": _job(
                    "job-1",
                    seq=4,
                    status="queued",
                    created_at="2026-03-01T09:00:00+00:00",
                    updated_at="2026-03-01T09:00:00+00:00",
                ),
                "job-3": _job(
                    "job-3",
                    seq=9,
                    status="completed",
                    created_at="2026-03-01T11:00:00+00:00",
                    updated_at="2026-03-01T11:20:00+00:00",
                    requested_by="bob",
                ),
                "job-2": _job(
                    "job-2",
                    seq=7,
                    status="running",
                    created_at="2026-03-01T10:00:00+00:00",
                    updated_at="2026-03-01T10:10:00+00:00",
                ),
            }
            _save_activity_jobs_cache(jobs_by_id, 44, cache_path)
            holder = _Holder(client=None)
            holder._activity_jobs_cache_file = cache_path
            holder._activity_rows_cache = []
            holder._activity_jobs_by_id = {}
            holder._activity_cursor = 0
            holder._activity_cache_notice = ""
            holder._compliance_blocked = False
            holder._activity_me_user = ""

            restored = holder._restore_activity_rows_from_cache(notice_key="activity.cache.notice.not_configured")
            expected_payload = _load_activity_jobs_cache(cache_path)
            expected_rows = _rows_from_jobs_by_id(expected_payload["jobs_by_id"])

            self.assertTrue(restored)
            self.assertEqual(holder._activity_jobs_by_id, expected_payload["jobs_by_id"])
            self.assertEqual(holder._activity_cursor, 44)
            self.assertEqual(holder._activity_rows_cache, expected_rows)
            self.assertEqual(holder.activity_view.printer_rows, expected_rows)
            self.assertEqual(holder.activity_view.cache_banner, tr("activity.cache.notice.not_configured"))

    def test_forced_refresh_without_client_restores_cached_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache_path = Path(tmp).joinpath("activity_jobs_cache.json")
            jobs_by_id = {
                "job-2": _job(
                    "job-2",
                    seq=12,
                    status="running",
                    created_at="2026-03-01T10:00:00+00:00",
                    updated_at="2026-03-01T10:05:00+00:00",
                ),
                "job-1": _job(
                    "job-1",
                    seq=7,
                    status="queued",
                    created_at="2026-03-01T09:00:00+00:00",
                    updated_at="2026-03-01T09:00:00+00:00",
                ),
            }
            _save_activity_jobs_cache(jobs_by_id, 19, cache_path)

            holder = _Holder(client=None)
            holder._activity_jobs_cache_file = cache_path
            holder._activity_rows_cache = []
            holder._activity_jobs_by_id = {}
            holder._activity_cursor = 0
            holder._activity_cache_notice = ""
            holder._activity_me_user = ""
            holder._compliance_blocked = False
            holder._activity_sync_inflight = False

            holder._request_activity_refresh(force=True)

            expected_rows = _rows_from_jobs_by_id(_load_activity_jobs_cache(cache_path)["jobs_by_id"])
            self.assertEqual(holder._activity_rows_cache, expected_rows)
            self.assertEqual(holder.activity_view.printer_rows, expected_rows)
            self.assertEqual(holder.activity_view.cache_banner, tr("activity.cache.notice.not_configured"))
            self.assertEqual(holder._activity_cursor, 19)
            self.assertFalse(hasattr(holder, "worker"))

    def test_compliance_denial_prevents_cached_restore_during_init(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache_path = Path(tmp).joinpath("activity_jobs_cache.json")
            _save_activity_jobs_cache(
                {
                    "job-1": _job(
                        "job-1",
                        seq=1,
                        status="queued",
                        created_at="2026-03-01T09:00:00+00:00",
                        updated_at="2026-03-01T09:00:00+00:00",
                    )
                },
                7,
                cache_path,
            )
            holder = _Holder(client=object(), compliance_blocked=True)

            with mock.patch("gui.Windows.controller.activity_sync.QtCore.QTimer", _FakeTimer):
                with mock.patch("gui.Windows.controller.activity_sync._activity_jobs_cache_path", return_value=cache_path):
                    holder._init_activity_sync()

            self.assertEqual(holder._activity_rows_cache, [])
            self.assertEqual(holder._activity_jobs_by_id, {})
            self.assertEqual(holder.activity_view.printer_rows, [])
            self.assertEqual(holder.activity_view.cache_banner, "")
            self.assertEqual(holder.activity_view.compliance_banner, "blocked by policy")
            self.assertFalse(holder._activity_sync_timer.started)

    def test_successful_live_refresh_writes_cache_and_clears_cache_notice(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache_path = Path(tmp).joinpath("activity_jobs_cache.json")
            holder = _Holder(client=None)
            holder._activity_jobs_cache_file = cache_path
            holder._activity_sync_inflight = True
            holder._activity_sync_last_error = "offline"
            holder._activity_sync_last_count = -1
            holder._activity_jobs_by_id = {}
            holder._activity_cursor = 0
            holder._activity_me_user = ""
            holder._activity_cache_notice = ""
            holder._show_activity_cache_notice("stale cache")

            jobs_by_id = {
                "job-2": _job(
                    "job-2",
                    seq=3,
                    status="running",
                    created_at="2026-03-01T12:00:00+00:00",
                    updated_at="2026-03-01T12:05:00+00:00",
                ),
                "job-1": _job(
                    "job-1",
                    seq=2,
                    status="queued",
                    created_at="2026-03-01T11:00:00+00:00",
                    updated_at="2026-03-01T11:00:00+00:00",
                ),
            }
            rows = _rows_from_jobs_by_id(jobs_by_id)

            holder._on_activity_rows_ready({"rows": rows, "jobs_by_id": jobs_by_id, "cursor": 55})
            cached = _load_activity_jobs_cache(cache_path)

            self.assertTrue(cached["available"])
            self.assertEqual(cached["cursor"], 55)
            self.assertEqual(cached["jobs_by_id"], {job_id: _normalize_job_payload(job) for job_id, job in jobs_by_id.items()})
            self.assertEqual(holder._activity_rows_cache, rows)
            self.assertEqual(holder.activity_view.printer_rows, rows)
            self.assertEqual(holder.activity_view.cache_banner, "")
            self.assertEqual(holder._activity_cache_notice, "")
            self.assertIn("Activity synced (2 jobs)", holder.statusBar().messages)

    def test_sync_error_preserves_rows_and_sets_cache_notice(self):
        holder = _Holder(client=None)
        holder._activity_sync_inflight = True
        holder._activity_sync_last_error = ""
        holder._activity_me_user = ""
        rows = _rows_from_jobs_by_id(
            {
                "job-1": _job(
                    "job-1",
                    seq=5,
                    status="running",
                    created_at="2026-03-01T12:00:00+00:00",
                    updated_at="2026-03-01T12:10:00+00:00",
                )
            }
        )
        holder._apply_activity_rows(rows)

        holder._on_activity_rows_error("backend down")

        self.assertEqual(holder._activity_rows_cache, rows)
        self.assertEqual(holder.activity_view.printer_rows, rows)
        self.assertEqual(holder.activity_view.cache_banner, tr("activity.cache.notice.unavailable"))
        self.assertIn("Activity sync unavailable: backend down", holder.statusBar().messages)


if __name__ == "__main__":
    unittest.main()

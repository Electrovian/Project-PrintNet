from __future__ import annotations

import base64
from dataclasses import dataclass, replace
from datetime import datetime, timezone
import os
import re
from typing import Any, Mapping

from .authz import normalize_role
from .errors import BackendConflictError, BackendNotFoundError, BackendOrchestrationError, BackendValidationError
from .models import JobRecord, PrinterRecord, ProfileRecord, SessionRecord, utc_now_iso
from .observability import ObservabilityState
from .orchestration import InMemoryQueueOrchestrator


@dataclass
class BackendState:
    queue_name: str = "default"
    queue_worker_max_jobs_per_tick: int = 1
    queue_worker_heartbeat_ttl_seconds: int = 60
    observability_max_audit_records: int = 200
    observability_max_metric_keys: int = 256
    release_required_checks: tuple[str, ...] = (
        "backend_health",
        "authz_enforced",
        "queue_worker_operational",
        "kubernetes_packaging_validated",
    )
    model_store_dir: str = "Website/backend/uploads"

    def __post_init__(self):
        self.queue_name = str(self.queue_name or "default").strip() or "default"
        self.queue_worker_max_jobs_per_tick = _as_bounded_int(
            self.queue_worker_max_jobs_per_tick,
            field="queue_worker_max_jobs_per_tick",
            minimum=1,
            maximum=100,
        )
        self.queue_worker_heartbeat_ttl_seconds = _as_bounded_int(
            self.queue_worker_heartbeat_ttl_seconds,
            field="queue_worker_heartbeat_ttl_seconds",
            minimum=1,
            maximum=86400,
        )
        self.observability_max_audit_records = _as_bounded_int(
            self.observability_max_audit_records,
            field="observability_max_audit_records",
            minimum=10,
            maximum=5000,
        )
        self.observability_max_metric_keys = _as_bounded_int(
            self.observability_max_metric_keys,
            field="observability_max_metric_keys",
            minimum=10,
            maximum=5000,
        )
        self.release_required_checks = _normalize_required_checks(self.release_required_checks)
        self.model_store_dir = _normalize_model_store_dir(self.model_store_dir)
        self._session_counter = 0
        self._job_counter = 0
        self._sessions: dict[str, SessionRecord] = {}
        self._printers: dict[str, PrinterRecord] = {}
        self._jobs: dict[str, JobRecord] = {}
        self._job_events: dict[str, list[str]] = {}
        self._queue_orchestrator = InMemoryQueueOrchestrator(
            heartbeat_ttl_seconds=self.queue_worker_heartbeat_ttl_seconds,
            max_jobs_per_tick=self.queue_worker_max_jobs_per_tick,
        )
        self._observability = ObservabilityState(
            max_audit_records=self.observability_max_audit_records,
            max_metric_keys=self.observability_max_metric_keys,
            required_release_checks=self.release_required_checks,
        )
        self._observability.set_release_check(
            name="backend_health",
            passed=True,
            detail="backend state initialized",
        )
        self._profiles: list[ProfileRecord] = [
            ProfileRecord(
                profile_id="p-default-pla",
                vendor="EON",
                model="Generic 220",
                nozzle="0.4",
                process="standard",
                filament="PLA",
            ),
            ProfileRecord(
                profile_id="p-fast-pla",
                vendor="EON",
                model="Generic 220",
                nozzle="0.4",
                process="fast",
                filament="PLA",
            ),
            ProfileRecord(
                profile_id="p-precision-pla",
                vendor="EON",
                model="Generic 220",
                nozzle="0.2",
                process="precision",
                filament="PLA",
            ),
        ]
        os.makedirs(self.model_store_dir, exist_ok=True)

    def create_session(self, *, user_id: str, role: str) -> SessionRecord:
        user = str(user_id or "").strip()
        if not user:
            raise BackendValidationError("SESSION_USER_ID_REQUIRED: user_id is required.")
        normalized_role = normalize_role(role)
        self._session_counter += 1
        token = f"session-{self._session_counter:06d}"
        session = SessionRecord(
            token=token,
            user_id=user,
            role=normalized_role,
            issued_at_utc=utc_now_iso(),
        )
        self._sessions[token] = session
        self.record_operation_metric(event="auth.session.create", status="ok", duration_ms=0.0)
        return session

    def get_session(self, token: str) -> SessionRecord:
        key = str(token or "").strip()
        if not key:
            raise BackendValidationError("SESSION_TOKEN_REQUIRED: token is required.")
        session = self._sessions.get(key)
        if session is None:
            raise BackendNotFoundError(f"SESSION_NOT_FOUND: {key}")
        return session

    def list_profiles(
        self,
        *,
        vendor: str = "",
        model: str = "",
        nozzle: str = "",
        process: str = "",
        filament: str = "",
    ) -> list[ProfileRecord]:
        vendor_q = str(vendor or "").strip().lower()
        model_q = str(model or "").strip().lower()
        nozzle_q = str(nozzle or "").strip().lower()
        process_q = str(process or "").strip().lower()
        filament_q = str(filament or "").strip().lower()

        result: list[ProfileRecord] = []
        for item in self._profiles:
            if vendor_q and vendor_q not in item.vendor.lower():
                continue
            if model_q and model_q not in item.model.lower():
                continue
            if nozzle_q and nozzle_q != item.nozzle.lower():
                continue
            if process_q and process_q != item.process.lower():
                continue
            if filament_q and filament_q != item.filament.lower():
                continue
            result.append(item)
        return result

    def profile_exists(self, profile_id: str) -> bool:
        key = str(profile_id or "").strip()
        for item in self._profiles:
            if item.profile_id == key:
                return True
        return False

    def register_printer(
        self,
        *,
        printer_id: str,
        name: str,
        connector_type: str,
        endpoint: str,
    ) -> PrinterRecord:
        key = str(printer_id or "").strip()
        if not key:
            raise BackendValidationError("PRINTER_ID_REQUIRED: printer_id is required.")
        if key in self._printers:
            raise BackendConflictError(f"PRINTER_ALREADY_EXISTS: {key}")

        normalized_name = str(name or "").strip()
        if not normalized_name:
            raise BackendValidationError("PRINTER_NAME_REQUIRED: name is required.")

        normalized_connector = str(connector_type or "").strip().lower()
        if normalized_connector not in ("octoprint", "moonraker", "prusalink", "local_file"):
            raise BackendValidationError(
                "PRINTER_CONNECTOR_INVALID: connector_type must be octoprint/moonraker/prusalink/local_file."
            )
        normalized_endpoint = str(endpoint or "").strip()
        if not normalized_endpoint:
            raise BackendValidationError("PRINTER_ENDPOINT_REQUIRED: endpoint is required.")

        printer = PrinterRecord(
            printer_id=key,
            name=normalized_name,
            connector_type=normalized_connector,
            endpoint=normalized_endpoint,
            created_at_utc=utc_now_iso(),
        )
        self._printers[key] = printer
        self.record_operation_metric(event="printer.register", status="ok", duration_ms=0.0)
        return printer

    def list_printers(self) -> list[PrinterRecord]:
        rows = list(self._printers.values())
        rows.sort(key=lambda item: item.printer_id.lower())
        return rows

    def submit_job(
        self,
        *,
        model_name: str,
        profile_id: str,
        requested_by: str,
        printer_id: str = "",
    ) -> JobRecord:
        normalized_model = str(model_name or "").strip()
        if not normalized_model:
            raise BackendValidationError("JOB_MODEL_NAME_REQUIRED: model_name is required.")

        normalized_profile = str(profile_id or "").strip()
        if not normalized_profile:
            raise BackendValidationError("JOB_PROFILE_ID_REQUIRED: profile_id is required.")
        if not self.profile_exists(normalized_profile):
            raise BackendNotFoundError(f"JOB_PROFILE_NOT_FOUND: {normalized_profile}")

        normalized_user = str(requested_by or "").strip()
        if not normalized_user:
            raise BackendValidationError("JOB_REQUESTED_BY_REQUIRED: requested_by is required.")

        normalized_printer = str(printer_id or "").strip()
        if normalized_printer and normalized_printer not in self._printers:
            raise BackendNotFoundError(f"JOB_PRINTER_NOT_FOUND: {normalized_printer}")

        self._job_counter += 1
        job_id = f"job-{self._job_counter:06d}"
        status = "queued" if normalized_printer else "pending_printer"
        job = JobRecord(
            job_id=job_id,
            model_name=normalized_model,
            profile_id=normalized_profile,
            requested_by=normalized_user,
            queue=self.queue_name,
            status=status,
            printer_id=normalized_printer,
            created_at_utc=utc_now_iso(),
        )
        self._jobs[job_id] = job
        self._job_events[job_id] = []
        self._append_job_event(job_id, f"submitted:{status}")
        if status == "queued":
            self._queue_orchestrator.enqueue(job_id)
        self.record_operation_metric(event="job.submit", status="ok", duration_ms=0.0)
        return job

    def store_uploaded_model(
        self,
        *,
        file_name: str,
        data_base64: str,
        requested_by: str,
    ) -> Mapping[str, Any]:
        normalized_name = _sanitize_upload_file_name(file_name)
        if not normalized_name:
            raise BackendValidationError("UPLOAD_FILE_NAME_REQUIRED: file_name is required.")
        normalized_user = _sanitize_upload_owner(requested_by)
        payload = str(data_base64 or "").strip()
        if not payload:
            raise BackendValidationError("UPLOAD_PAYLOAD_REQUIRED: data_base64 is required.")
        try:
            blob = base64.b64decode(payload, validate=True)
        except Exception as exc:
            raise BackendValidationError("UPLOAD_PAYLOAD_INVALID: data_base64 must be valid base64.") from exc
        if len(blob) <= 0:
            raise BackendValidationError("UPLOAD_PAYLOAD_EMPTY: uploaded model content is empty.")
        if len(blob) > 250 * 1024 * 1024:
            raise BackendValidationError("UPLOAD_PAYLOAD_TOO_LARGE: maximum supported upload is 250MB.")
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
        stored_name = f"{stamp}_{normalized_user}_{normalized_name}"
        stored_path = os.path.join(self.model_store_dir, stored_name)
        try:
            with open(stored_path, "wb") as handle:
                handle.write(blob)
        except Exception as exc:
            raise BackendOrchestrationError(f"UPLOAD_WRITE_FAILED: {stored_name}") from exc
        self.record_operation_metric(event="job.model.upload", status="ok", duration_ms=0.0)
        return {
            "model_name": stored_name,
            "original_name": normalized_name,
            "size_bytes": len(blob),
            "stored_path": stored_path,
        }

    def get_job(self, job_id: str) -> JobRecord:
        key = str(job_id or "").strip()
        if not key:
            raise BackendValidationError("JOB_ID_REQUIRED: job_id is required.")
        job = self._jobs.get(key)
        if job is None:
            raise BackendNotFoundError(f"JOB_NOT_FOUND: {key}")
        return job

    def list_job_events(self, job_id: str) -> list[str]:
        key = str(job_id or "").strip()
        if not key:
            raise BackendValidationError("JOB_ID_REQUIRED: job_id is required.")
        if key not in self._jobs:
            raise BackendNotFoundError(f"JOB_NOT_FOUND: {key}")
        return list(self._job_events.get(key, []))

    def list_jobs(self, *, requested_by: str = "") -> list[JobRecord]:
        normalized_user = str(requested_by or "").strip()
        rows: list[JobRecord] = []
        for job in self._jobs.values():
            if normalized_user and job.requested_by != normalized_user:
                continue
            rows.append(job)
        rows.sort(key=lambda item: item.job_id.lower())
        return rows

    def queue_snapshot(self, *, requested_by: str = "") -> Mapping[str, Any]:
        jobs = self.list_jobs(requested_by=requested_by)
        status_counts: dict[str, int] = {}
        visible_queue_depth = 0
        for job in jobs:
            status_counts[job.status] = status_counts.get(job.status, 0) + 1
            if job.status == "queued":
                visible_queue_depth += 1
        workers = [item.to_dict() for item in self._queue_orchestrator.list_heartbeats()]
        return {
            "queue": self.queue_name,
            "queue_depth": visible_queue_depth,
            "job_count": len(jobs),
            "status_counts": status_counts,
            "workers": workers,
            "jobs": [item.to_dict() for item in jobs],
        }

    def record_worker_heartbeat(self, *, worker_id: str) -> Mapping[str, Any]:
        heartbeat = self._queue_orchestrator.record_heartbeat(worker_id)
        self.record_operation_metric(event="queue.worker.heartbeat", status="ok", duration_ms=0.0)
        return heartbeat.to_dict()

    def run_worker_tick(
        self,
        *,
        worker_id: str,
        max_jobs: object | None = None,
    ) -> Mapping[str, Any]:
        result = self._queue_orchestrator.run_cycle(
            worker_id=worker_id,
            max_jobs=max_jobs,
            process_job=self._process_queued_job,
        )
        self.record_operation_metric(event="queue.worker.tick", status="ok", duration_ms=0.0)
        return {
            "cycle": result.to_dict(),
            "snapshot": self.queue_snapshot(),
        }

    def record_operation_metric(
        self,
        *,
        event: str,
        status: str,
        duration_ms: float = 0.0,
    ) -> Mapping[str, Any]:
        sample = self._observability.record_metric(
            event=event,
            status=status,
            duration_ms=duration_ms,
        )
        return sample.to_dict()

    def append_security_audit(
        self,
        *,
        actor: str,
        action: str,
        resource: str,
        outcome: str,
        details: object | None = None,
    ) -> Mapping[str, Any]:
        record = self._observability.append_audit(
            actor=actor,
            action=action,
            resource=resource,
            outcome=outcome,
            details=details,
        )
        return record.to_dict()

    def observability_metrics_snapshot(self) -> Mapping[str, Any]:
        return self._observability.metrics_snapshot()

    def observability_audit_snapshot(self, *, limit: object = 50) -> list[Mapping[str, Any]]:
        rows = self._observability.list_audit(limit=limit)
        return [dict(item) for item in rows]

    def set_release_readiness_check(
        self,
        *,
        check_name: str,
        passed: object,
        detail: object = "",
    ) -> Mapping[str, Any]:
        check = self._observability.set_release_check(
            name=check_name,
            passed=passed,
            detail=detail,
        )
        return check.to_dict()

    def release_readiness_snapshot(self) -> Mapping[str, Any]:
        return self._observability.release_snapshot()

    def status_snapshot(self) -> Mapping[str, Any]:
        metrics = self.observability_metrics_snapshot()
        release = self.release_readiness_snapshot()
        return {
            "sessions": len(self._sessions),
            "profiles": len(self._profiles),
            "printers": len(self._printers),
            "jobs": len(self._jobs),
            "queue": self.queue_name,
            "queue_depth": self._queue_orchestrator.queue_depth(),
            "workers": len(self._queue_orchestrator.list_heartbeats()),
            "metric_count": int(metrics.get("metric_count", 0)),
            "release_ready": bool(release.get("ready", False)),
        }

    def _append_job_event(self, job_id: str, event: str) -> None:
        key = str(job_id or "").strip()
        if key not in self._jobs:
            raise BackendNotFoundError(f"JOB_NOT_FOUND: {key}")
        normalized_event = str(event or "").strip()
        if not normalized_event:
            raise BackendValidationError("JOB_EVENT_REQUIRED: event is required.")
        rows = self._job_events.setdefault(key, [])
        rows.append(f"{utc_now_iso()} {normalized_event}")

    def _set_job_status(self, job_id: str, status: str, event: str) -> JobRecord:
        normalized_status = str(status or "").strip()
        if normalized_status not in (
            "pending_printer",
            "queued",
            "running",
            "completed",
            "failed",
            "cancelled",
        ):
            raise BackendValidationError(f"JOB_STATUS_INVALID: {normalized_status}")
        key = str(job_id or "").strip()
        current = self.get_job(key)
        updated = replace(current, status=normalized_status)
        self._jobs[key] = updated
        self._append_job_event(key, event)
        return updated

    def _process_queued_job(self, job_id: str) -> None:
        key = str(job_id or "").strip()
        if not key:
            raise BackendValidationError("JOB_ID_REQUIRED: job_id is required.")
        current = self.get_job(key)
        if current.status != "queued":
            raise BackendOrchestrationError(
                f"QUEUE_JOB_NOT_READY: expected queued status for {key}, got {current.status}."
            )
        self._set_job_status(key, "running", "worker:running")
        self._set_job_status(key, "completed", "worker:completed")


def _as_bounded_int(value: object, *, field: str, minimum: int, maximum: int) -> int:
    if isinstance(value, bool):
        raise BackendValidationError(f"{field} must be an integer.")
    if isinstance(value, int):
        parsed = value
    elif isinstance(value, float):
        parsed = int(round(value))
    else:
        text = str(value or "").strip()
        if not text:
            raise BackendValidationError(f"{field} must be an integer.")
        try:
            parsed = int(round(float(text)))
        except Exception as exc:
            raise BackendValidationError(f"{field} must be an integer.") from exc
    if parsed < minimum or parsed > maximum:
        raise BackendValidationError(f"{field} must be between {minimum} and {maximum}.")
    return parsed


def _normalize_required_checks(values: object) -> tuple[str, ...]:
    if isinstance(values, tuple):
        rows = list(values)
    elif isinstance(values, list):
        rows = list(values)
    elif isinstance(values, str):
        rows = [part.strip() for part in values.split(",")]
    else:
        rows = [str(values or "").strip()]
    cleaned: list[str] = []
    seen: set[str] = set()
    for item in rows:
        text = str(item or "").strip()
        if not text:
            continue
        if text in seen:
            continue
        seen.add(text)
        cleaned.append(text)
    return tuple(cleaned)


def _normalize_model_store_dir(value: object) -> str:
    text = str(value or "").strip()
    if not text:
        return os.path.abspath("Website/backend/uploads")
    return os.path.abspath(text)


def _sanitize_upload_owner(value: object) -> str:
    text = str(value or "").strip().lower()
    cleaned = re.sub(r"[^a-z0-9_.-]+", "-", text).strip("-")
    return cleaned or "web-user"


def _sanitize_upload_file_name(value: object) -> str:
    text = os.path.basename(str(value or "").strip())
    if not text:
        return ""
    cleaned = re.sub(r"[^A-Za-z0-9_. -]+", "_", text).strip(" .")
    if not cleaned:
        return ""
    lower = cleaned.lower()
    if lower.endswith(".stl") or lower.endswith(".step") or lower.endswith(".stp"):
        return cleaned
    return f"{cleaned}.stl"

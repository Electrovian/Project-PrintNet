from __future__ import annotations

import base64
from dataclasses import dataclass, replace
from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import os
import re
import secrets
import smtplib
from email.message import EmailMessage
from typing import Any, Mapping

from .activity_store import ActivityStore
from .authz import normalize_role
from .errors import (
    BackendAuthenticationError,
    BackendConflictError,
    BackendNotFoundError,
    BackendOrchestrationError,
    BackendValidationError,
)
from .models import AccountRecord, JobRecord, PrinterRecord, ProfileRecord, SessionRecord, utc_now_iso
from .observability import ObservabilityState
from .orchestration import InMemoryQueueOrchestrator


@dataclass
class BackendState:
    default_role: str = "student"
    allow_client_role_override: bool = False
    operator_user_ids: tuple[str, ...] = tuple()
    admin_user_ids: tuple[str, ...] = tuple()
    activity_service_token: str = ""
    activity_max_jobs: int = 1000
    activity_max_events: int = 5000
    queue_name: str = "default"
    queue_worker_max_jobs_per_tick: int = 1
    queue_worker_heartbeat_ttl_seconds: int = 60
    observability_max_audit_records: int = 200
    observability_max_metric_keys: int = 256
    super_admin_email: str = ""
    super_admin_password: str = ""
    auth_verification_code_ttl_seconds: int = 600
    auth_verification_max_attempts: int = 5
    auth_expose_debug_code: bool = False
    auth_email_require_smtp: bool = False
    auth_email_from: str = "no-reply@printnet.local"
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_starttls: bool = True
    smtp_use_ssl: bool = False
    release_required_checks: tuple[str, ...] = (
        "backend_health",
        "authz_enforced",
        "queue_worker_operational",
        "kubernetes_packaging_validated",
    )
    model_store_dir: str = "Website/backend/runtime/uploads"

    def __post_init__(self):
        self.default_role = normalize_role(self.default_role)
        self.allow_client_role_override = bool(self.allow_client_role_override)
        self.operator_user_ids = _normalize_user_id_set(self.operator_user_ids)
        self.admin_user_ids = _normalize_user_id_set(self.admin_user_ids)
        self.activity_service_token = str(self.activity_service_token or "").strip()
        self.activity_max_jobs = _as_bounded_int(
            self.activity_max_jobs,
            field="activity_max_jobs",
            minimum=1,
            maximum=50000,
        )
        self.activity_max_events = _as_bounded_int(
            self.activity_max_events,
            field="activity_max_events",
            minimum=10,
            maximum=500000,
        )
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
        self.super_admin_email = str(self.super_admin_email or "").strip().lower()
        self.super_admin_password = str(self.super_admin_password or "")
        self.auth_verification_code_ttl_seconds = _as_bounded_int(
            self.auth_verification_code_ttl_seconds,
            field="auth_verification_code_ttl_seconds",
            minimum=60,
            maximum=3600,
        )
        self.auth_verification_max_attempts = _as_bounded_int(
            self.auth_verification_max_attempts,
            field="auth_verification_max_attempts",
            minimum=1,
            maximum=10,
        )
        self.auth_expose_debug_code = bool(self.auth_expose_debug_code)
        self.auth_email_require_smtp = bool(self.auth_email_require_smtp)
        self.auth_email_from = str(self.auth_email_from or "no-reply@printnet.local").strip() or "no-reply@printnet.local"
        self.smtp_host = str(self.smtp_host or "").strip()
        self.smtp_port = _as_bounded_int(
            self.smtp_port,
            field="smtp_port",
            minimum=1,
            maximum=65535,
        )
        self.smtp_username = str(self.smtp_username or "").strip()
        self.smtp_password = str(self.smtp_password or "")
        self.smtp_starttls = bool(self.smtp_starttls)
        self.smtp_use_ssl = bool(self.smtp_use_ssl)
        self.release_required_checks = _normalize_required_checks(self.release_required_checks)
        self.model_store_dir = _normalize_model_store_dir(self.model_store_dir)
        self._session_counter = 0
        self._auth_challenge_counter = 0
        self._job_counter = 0
        self._sessions: dict[str, SessionRecord] = {}
        self._login_challenges: dict[str, dict[str, Any]] = {}
        self._accounts: dict[str, AccountRecord] = {}
        self._printers: dict[str, PrinterRecord] = {}
        self._jobs: dict[str, JobRecord] = {}
        self._job_events: dict[str, list[str]] = {}
        self._activity_store = ActivityStore(
            max_events=self.activity_max_events,
            max_jobs=self.activity_max_jobs,
        )
        self._queue_snapshot_version = 0
        self._queue_snapshot_cache: dict[str, tuple[int, Mapping[str, Any]]] = {}
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
        self._bootstrap_super_admin_account()
        os.makedirs(self.model_store_dir, exist_ok=True)

    def create_session(self, *, user_id: str, role: str, trusted_role: bool = False) -> SessionRecord:
        user = str(user_id or "").strip()
        if not user:
            raise BackendValidationError("SESSION_USER_ID_REQUIRED: user_id is required.")
        if not trusted_role and not self._allow_legacy_session_issue(user_id=user):
            raise BackendAuthenticationError(
                "SESSION_LEGACY_DISABLED: use /auth/login or /auth/register for interactive users."
            )
        if trusted_role:
            normalized_role = self._resolve_trusted_session_role(user_id=user, requested_role=role)
        else:
            normalized_role = self._resolve_session_role(user_id=user, requested_role=role)
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

    def register_account(self, *, user_id: str, password: str, role: str = "student") -> AccountRecord:
        user = _normalize_account_user_id(user_id)
        if user in self._accounts:
            raise BackendConflictError(f"AUTH_ACCOUNT_EXISTS: {user}")
        normalized_role = normalize_role(role or "student")
        if normalized_role != "student":
            raise BackendValidationError("AUTH_ROLE_INVALID: self-registration role must be student.")
        normalized_password = _normalize_password(password)
        salt_hex, hash_hex = _hash_password(normalized_password)
        now = utc_now_iso()
        account = AccountRecord(
            user_id=user,
            role=normalized_role,
            active=True,
            password_salt_hex=salt_hex,
            password_hash_hex=hash_hex,
            created_at_utc=now,
            updated_at_utc=now,
        )
        self._accounts[user] = account
        self.record_operation_metric(event="auth.account.register", status="ok", duration_ms=0.0)
        return account

    def authenticate_account(self, *, user_id: str, password: str) -> AccountRecord:
        user = _normalize_account_user_id(user_id)
        account = self._accounts.get(user)
        if account is None:
            raise BackendAuthenticationError("AUTH_ACCOUNT_INVALID_CREDENTIALS: invalid user_id or password.")
        if not account.active:
            raise BackendAuthenticationError("AUTH_ACCOUNT_DISABLED: account access is disabled.")
        normalized_password = _normalize_password(password)
        if not _verify_password(normalized_password, account.password_salt_hex, account.password_hash_hex):
            raise BackendAuthenticationError("AUTH_ACCOUNT_INVALID_CREDENTIALS: invalid user_id or password.")
        self.record_operation_metric(event="auth.account.login", status="ok", duration_ms=0.0)
        return account

    def request_login_verification(self, *, user_id: str, password: str) -> Mapping[str, Any]:
        account = self.authenticate_account(user_id=user_id, password=password)
        self._auth_challenge_counter += 1
        challenge_id = f"challenge-{self._auth_challenge_counter:06d}"
        code = f"{secrets.randbelow(1_000_000):06d}"
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=self.auth_verification_code_ttl_seconds)
        code_hash = _hash_verification_code(challenge_id=challenge_id, code=code)
        delivery_channel, destination = self._send_auth_verification_code(
            target_user_id=account.user_id,
            code=code,
            expires_at_utc=expires_at.isoformat(),
        )
        challenge = {
            "challenge_id": challenge_id,
            "user_id": account.user_id,
            "role": account.role,
            "expires_at_utc": expires_at.isoformat(),
            "attempt_count": 0,
            "max_attempts": self.auth_verification_max_attempts,
            "delivery_channel": delivery_channel,
            "delivery_destination": destination,
            "code_hash_hex": code_hash,
        }
        self._login_challenges[challenge_id] = challenge
        self.record_operation_metric(event="auth.login.challenge.create", status="ok", duration_ms=0.0)
        response = {
            "challenge_id": challenge_id,
            "user_id": account.user_id,
            "role": account.role,
            "expires_at_utc": challenge["expires_at_utc"],
            "delivery": {
                "channel": delivery_channel,
                "destination": destination,
            },
        }
        if self.auth_expose_debug_code:
            response["debug_code"] = code
        return response

    def verify_login_verification(self, *, challenge_id: str, verification_code: str) -> tuple[AccountRecord, SessionRecord]:
        key = str(challenge_id or "").strip()
        if not key:
            raise BackendAuthenticationError("AUTH_VERIFICATION_CHALLENGE_REQUIRED: challenge_id is required.")
        challenge = self._login_challenges.get(key)
        if challenge is None:
            raise BackendAuthenticationError("AUTH_VERIFICATION_CHALLENGE_INVALID: challenge not found.")
        expires_at = _parse_iso_datetime(str(challenge.get("expires_at_utc", "")))
        if expires_at is None or expires_at <= datetime.now(timezone.utc):
            self._login_challenges.pop(key, None)
            raise BackendAuthenticationError("AUTH_VERIFICATION_EXPIRED: verification challenge expired.")
        attempts = int(challenge.get("attempt_count", 0)) + 1
        challenge["attempt_count"] = attempts
        max_attempts = int(challenge.get("max_attempts", self.auth_verification_max_attempts))
        if attempts > max_attempts:
            self._login_challenges.pop(key, None)
            raise BackendAuthenticationError("AUTH_VERIFICATION_ATTEMPTS_EXCEEDED: verification challenge locked.")
        candidate = _hash_verification_code(challenge_id=key, code=str(verification_code or ""))
        expected = str(challenge.get("code_hash_hex", ""))
        if not hmac.compare_digest(candidate, expected):
            if attempts >= max_attempts:
                self._login_challenges.pop(key, None)
            raise BackendAuthenticationError("AUTH_VERIFICATION_CODE_INVALID: verification code is invalid.")
        user_key = str(challenge.get("user_id", "")).strip().lower()
        account = self._accounts.get(user_key)
        if account is None or not account.active:
            self._login_challenges.pop(key, None)
            raise BackendAuthenticationError("AUTH_ACCOUNT_DISABLED: account access is disabled.")
        self._login_challenges.pop(key, None)
        session = self.create_session(user_id=account.user_id, role=account.role, trusted_role=True)
        self.record_operation_metric(event="auth.login.challenge.verify", status="ok", duration_ms=0.0)
        return account, session

    def _resolve_session_role(self, *, user_id: str, requested_role: str) -> str:
        user_key = str(user_id or "").strip().lower()
        if user_key in self.admin_user_ids:
            return "admin"
        if user_key in self.operator_user_ids:
            return "operator"
        if self.allow_client_role_override:
            return normalize_role(requested_role or self.default_role)
        return self.default_role

    def _allow_legacy_session_issue(self, *, user_id: str) -> bool:
        user_key = str(user_id or "").strip().lower()
        if not user_key:
            return False
        if user_key in self.admin_user_ids:
            return True
        if user_key in self.operator_user_ids:
            return True
        return False

    def _resolve_trusted_session_role(self, *, user_id: str, requested_role: str) -> str:
        normalized = normalize_role(requested_role or self.default_role)
        user_key = str(user_id or "").strip().lower()
        if user_key in self.admin_user_ids:
            return "admin"
        if user_key in self.operator_user_ids:
            if normalized == "admin":
                return "admin"
            return "operator"
        return normalized

    def _bootstrap_super_admin_account(self) -> None:
        email = str(self.super_admin_email or "").strip().lower()
        password = str(self.super_admin_password or "")
        if not email and not password:
            return
        if not email or not password:
            raise BackendValidationError(
                "AUTH_SUPER_ADMIN_CONFIG_INVALID: set both BACKEND_SUPER_ADMIN_EMAIL and BACKEND_SUPER_ADMIN_PASSWORD."
            )
        user_id = _normalize_account_user_id(email)
        normalized_password = _normalize_password(password)
        salt_hex, hash_hex = _hash_password(normalized_password)
        now = utc_now_iso()
        existing = self._accounts.get(user_id)
        if existing is None:
            account = AccountRecord(
                user_id=user_id,
                role="admin",
                active=True,
                password_salt_hex=salt_hex,
                password_hash_hex=hash_hex,
                created_at_utc=now,
                updated_at_utc=now,
            )
        else:
            account = replace(
                existing,
                role="admin",
                active=True,
                password_salt_hex=salt_hex,
                password_hash_hex=hash_hex,
                updated_at_utc=now,
            )
        self._accounts[user_id] = account
        self.record_operation_metric(event="auth.super_admin.bootstrap", status="ok", duration_ms=0.0)

    def _send_auth_verification_code(
        self,
        *,
        target_user_id: str,
        code: str,
        expires_at_utc: str,
    ) -> tuple[str, str]:
        destination = _mask_email(target_user_id)
        if self.smtp_host:
            message = EmailMessage()
            sender = self.auth_email_from or self.smtp_username or "no-reply@printnet.local"
            message["From"] = sender
            message["To"] = target_user_id
            message["Subject"] = "EON PrintNet verification code"
            message.set_content(
                f"Your verification code is {code}. This code expires at {expires_at_utc}.",
            )
            try:
                if self.smtp_use_ssl:
                    client = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port, timeout=10)
                else:
                    client = smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=10)
                with client:
                    if self.smtp_starttls and not self.smtp_use_ssl:
                        client.starttls()
                    if self.smtp_username:
                        client.login(self.smtp_username, self.smtp_password)
                    client.send_message(message)
                return "smtp", destination
            except Exception as exc:
                if self.auth_email_require_smtp:
                    raise BackendOrchestrationError(
                        f"AUTH_VERIFICATION_DELIVERY_FAILED: unable to send verification email via SMTP ({exc})."
                    ) from exc
        if self.auth_email_require_smtp:
            raise BackendOrchestrationError(
                "AUTH_VERIFICATION_DELIVERY_UNAVAILABLE: SMTP delivery is required but SMTP is not configured."
            )
        print(
            f"AUTH_VERIFICATION_CODE user={target_user_id} code={code} expires_at={expires_at_utc}",
            flush=True,
        )
        return "console", destination

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
        if normalized_connector not in ("octoprint", "moonraker", "prusalink", "local_file", "bambu_lan", "creality"):
            raise BackendValidationError(
                "PRINTER_CONNECTOR_INVALID: connector_type must be octoprint/moonraker/prusalink/local_file/bambu_lan/creality."
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
        self._record_activity_event(job, event_type="submitted")
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
        normalized_user = str(requested_by or "").strip()
        cache_key = normalized_user
        cached = self._queue_snapshot_cache.get(cache_key)
        if cached is not None:
            version, payload = cached
            if int(version) == int(self._queue_snapshot_version):
                return payload

        jobs = self._activity_store.list_recent_jobs(requested_by=normalized_user)
        if not jobs and self._jobs:
            legacy_rows = self.list_jobs(requested_by=normalized_user)
            jobs = [item.to_dict() for item in legacy_rows]
        status_counts: dict[str, int] = {}
        visible_queue_depth = 0
        for job in jobs:
            status = str(job.get("status", "")).strip() or "unknown"
            status_counts[status] = status_counts.get(status, 0) + 1
            if status == "queued":
                visible_queue_depth += 1
        workers = [item.to_dict() for item in self._queue_orchestrator.list_heartbeats()]
        snapshot = {
            "queue": self.queue_name,
            "queue_depth": visible_queue_depth,
            "job_count": len(jobs),
            "status_counts": status_counts,
            "workers": workers,
            "jobs": [dict(item) for item in jobs],
        }
        self._queue_snapshot_cache[cache_key] = (int(self._queue_snapshot_version), snapshot)
        return snapshot

    def activity_feed(
        self,
        *,
        cursor: object = 0,
        limit: object = 200,
        requested_by: str = "",
    ) -> Mapping[str, Any]:
        cursor_value = _coerce_bounded_int(cursor, default=0, minimum=0, maximum=2_000_000_000)
        limit_value = _coerce_bounded_int(limit, default=200, minimum=1, maximum=1000)
        return self._activity_store.read_feed(
            cursor=cursor_value,
            limit=limit_value,
            requested_by=str(requested_by or "").strip(),
        )

    def record_worker_heartbeat(self, *, worker_id: str) -> Mapping[str, Any]:
        heartbeat = self._queue_orchestrator.record_heartbeat(worker_id)
        self._invalidate_queue_snapshot_cache()
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

    def _invalidate_queue_snapshot_cache(self) -> None:
        self._queue_snapshot_version += 1
        self._queue_snapshot_cache.clear()

    def _record_activity_event(self, job: JobRecord | Mapping[str, Any], *, event_type: str) -> None:
        if isinstance(job, JobRecord):
            payload = job.to_dict()
        else:
            payload = dict(job)
        item = self._activity_store.record_job_event(
            event_type=event_type,
            job_id=payload.get("job_id", ""),
            status=payload.get("status", ""),
            model_name=payload.get("model_name", ""),
            profile_id=payload.get("profile_id", ""),
            printer_id=payload.get("printer_id", ""),
            requested_by=payload.get("requested_by", ""),
            queue=payload.get("queue", self.queue_name),
            created_at_utc=payload.get("created_at_utc", ""),
        )
        if item:
            self._invalidate_queue_snapshot_cache()

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
        self._record_activity_event(updated, event_type=normalized_status)
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


def _coerce_bounded_int(
    value: object,
    *,
    default: int,
    minimum: int,
    maximum: int,
) -> int:
    if value is None:
        parsed = int(default)
    elif isinstance(value, bool):
        parsed = int(default)
    elif isinstance(value, int):
        parsed = int(value)
    elif isinstance(value, float):
        parsed = int(round(value))
    else:
        text = str(value or "").strip()
        if not text:
            parsed = int(default)
        else:
            try:
                parsed = int(round(float(text)))
            except Exception:
                parsed = int(default)
    if parsed < minimum:
        return int(minimum)
    if parsed > maximum:
        return int(maximum)
    return int(parsed)


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


def _backend_root_dir() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _project_root_dir() -> str:
    return os.path.abspath(os.path.join(_backend_root_dir(), "..", ".."))


def _backend_runtime_dir() -> str:
    return os.path.abspath(os.path.join(_backend_root_dir(), "runtime"))


def _default_model_store_dir() -> str:
    return os.path.abspath(os.path.join(_backend_runtime_dir(), "uploads"))


def _normalize_model_store_dir(value: object) -> str:
    text = str(value or "").strip()
    if not text:
        return _default_model_store_dir()
    if os.path.isabs(text):
        return os.path.abspath(text)
    normalized = text.replace("\\", "/")
    legacy_normalized = normalized.lower().strip("/")
    if (
        legacy_normalized in {"uploads", "backend/uploads", "website/backend/uploads"}
        or legacy_normalized.endswith("/backend/uploads")
        or legacy_normalized.endswith("/website/backend/uploads")
    ):
        return _default_model_store_dir()
    if normalized.startswith("Website/"):
        project_root = _project_root_dir()
        if os.path.isdir(os.path.join(project_root, "Website")):
            return os.path.abspath(os.path.join(project_root, normalized))
        normalized = normalized[len("Website/") :]
        if normalized.startswith("backend/"):
            normalized = normalized[len("backend/") :]
    if normalized.startswith("runtime/"):
        return os.path.abspath(os.path.join(_backend_root_dir(), normalized))
    return os.path.abspath(os.path.join(_backend_root_dir(), normalized))


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


def _normalize_user_id_set(values: object) -> tuple[str, ...]:
    if isinstance(values, tuple):
        rows = list(values)
    elif isinstance(values, list):
        rows = list(values)
    elif isinstance(values, str):
        rows = [part.strip() for part in values.split(",")]
    else:
        rows = [str(values or "").strip()]
    result: list[str] = []
    seen: set[str] = set()
    for item in rows:
        text = str(item or "").strip().lower()
        if not text or text in seen:
            continue
        seen.add(text)
        result.append(text)
    return tuple(result)


def _normalize_account_user_id(value: object) -> str:
    text = str(value or "").strip().lower()
    if not text:
        raise BackendValidationError("AUTH_USER_ID_REQUIRED: user_id is required.")
    if len(text) < 3 or len(text) > 254:
        raise BackendValidationError("AUTH_USER_ID_INVALID: user_id length must be between 3 and 254.")
    if not re.fullmatch(r"[a-z0-9._@+\-]+", text):
        raise BackendValidationError("AUTH_USER_ID_INVALID: unsupported characters in user_id.")
    return text


def _normalize_password(value: object) -> str:
    text = str(value or "")
    if len(text) < 8:
        raise BackendValidationError("AUTH_PASSWORD_TOO_SHORT: password must be at least 8 characters.")
    if len(text) > 512:
        raise BackendValidationError("AUTH_PASSWORD_TOO_LONG: password exceeds maximum length.")
    return text


def _hash_password(password: str) -> tuple[str, str]:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 240_000)
    return salt.hex(), digest.hex()


def _hash_verification_code(*, challenge_id: str, code: str) -> str:
    digest = hashlib.sha256(f"{challenge_id}:{code}".encode("utf-8")).hexdigest()
    return digest


def _parse_iso_datetime(value: str) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        parsed = datetime.fromisoformat(text)
    except Exception:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed


def _mask_email(value: object) -> str:
    text = str(value or "").strip().lower()
    if "@" not in text:
        return "***"
    local, domain = text.split("@", 1)
    if len(local) <= 2:
        masked_local = f"{local[:1]}*"
    else:
        masked_local = f"{local[:1]}***{local[-1:]}"
    return f"{masked_local}@{domain}"


def _verify_password(password: str, salt_hex: str, hash_hex: str) -> bool:
    try:
        salt = bytes.fromhex(str(salt_hex or ""))
        expected = bytes.fromhex(str(hash_hex or ""))
    except Exception:
        return False
    actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 240_000)
    return hmac.compare_digest(actual, expected)

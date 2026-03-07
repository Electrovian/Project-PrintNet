from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Mapping

from .errors import BackendValidationError


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _as_non_empty(value: object, *, field: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise BackendValidationError(f"{field} is required.")
    return text


@dataclass(frozen=True)
class SessionRecord:
    token: str
    user_id: str
    role: str
    issued_at_utc: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AccountRecord:
    user_id: str
    role: str
    active: bool
    password_salt_hex: str
    password_hash_hex: str
    created_at_utc: str
    updated_at_utc: str

    def to_public_dict(self) -> dict[str, Any]:
        return {
            "user_id": self.user_id,
            "role": self.role,
            "active": bool(self.active),
            "created_at_utc": self.created_at_utc,
            "updated_at_utc": self.updated_at_utc,
        }


@dataclass(frozen=True)
class ProfileRecord:
    profile_id: str
    vendor: str
    model: str
    nozzle: str
    process: str
    filament: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PrinterRecord:
    printer_id: str
    name: str
    connector_type: str
    endpoint: str
    created_at_utc: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class JobRecord:
    job_id: str
    model_name: str
    profile_id: str
    requested_by: str
    queue: str
    status: str
    printer_id: str
    created_at_utc: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def parse_session_payload(payload: Mapping[str, Any]) -> tuple[str, str]:
    user_id = _as_non_empty(payload.get("user_id"), field="user_id")
    role = str(payload.get("role", "student") or "student").strip().lower() or "student"
    return user_id, role


def parse_register_payload(payload: Mapping[str, Any]) -> tuple[str, str, str]:
    user_id = _as_non_empty(payload.get("user_id"), field="user_id")
    password = _as_non_empty(payload.get("password"), field="password")
    role = str(payload.get("role", "student") or "student").strip().lower() or "student"
    return user_id, password, role


def parse_login_payload(payload: Mapping[str, Any]) -> tuple[str, str]:
    user_id = _as_non_empty(payload.get("user_id"), field="user_id")
    password = _as_non_empty(payload.get("password"), field="password")
    return user_id, password


def parse_login_verification_payload(payload: Mapping[str, Any]) -> tuple[str, str]:
    challenge_id = _as_non_empty(payload.get("challenge_id"), field="challenge_id")
    code = _as_non_empty(payload.get("verification_code"), field="verification_code")
    return challenge_id, code


def parse_printer_payload(payload: Mapping[str, Any]) -> tuple[str, str, str, str]:
    printer_id = _as_non_empty(payload.get("printer_id"), field="printer_id")
    name = _as_non_empty(payload.get("name"), field="name")
    connector_type = _as_non_empty(payload.get("connector_type"), field="connector_type").lower()
    endpoint = _as_non_empty(payload.get("endpoint"), field="endpoint")
    return printer_id, name, connector_type, endpoint


def parse_job_payload(payload: Mapping[str, Any]) -> tuple[str, str, str, str]:
    model_name = _as_non_empty(payload.get("model_name"), field="model_name")
    profile_id = _as_non_empty(payload.get("profile_id"), field="profile_id")
    requested_by = _as_non_empty(payload.get("requested_by"), field="requested_by")
    printer_id = str(payload.get("printer_id", "") or "").strip()
    return model_name, profile_id, requested_by, printer_id


def parse_model_upload_payload(payload: Mapping[str, Any]) -> tuple[str, str]:
    file_name = _as_non_empty(payload.get("file_name"), field="file_name")
    data_base64 = _as_non_empty(payload.get("data_base64"), field="data_base64")
    return file_name, data_base64

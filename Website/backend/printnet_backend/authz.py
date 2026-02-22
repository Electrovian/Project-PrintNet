from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from .errors import (
    BackendAuthenticationError,
    BackendAuthorizationError,
    BackendNotFoundError,
    BackendValidationError,
)


VALID_ROLES: tuple[str, ...] = ("student", "operator", "admin")


@dataclass(frozen=True)
class AuthContext:
    token: str
    user_id: str
    role: str


def normalize_role(role: str) -> str:
    normalized = str(role or "").strip().lower() or "student"
    if normalized not in VALID_ROLES:
        raise BackendValidationError(f"AUTH_ROLE_INVALID: role must be one of {', '.join(VALID_ROLES)}.")
    return normalized


def resolve_auth_context(state, auth_token: str) -> AuthContext:
    token = str(auth_token or "").strip()
    if not token:
        raise BackendAuthenticationError("AUTH_TOKEN_REQUIRED: auth_token is required.")
    try:
        session = state.get_session(token)
    except BackendNotFoundError as exc:
        raise BackendAuthenticationError(f"AUTH_TOKEN_INVALID: {token}") from exc
    return AuthContext(token=session.token, user_id=session.user_id, role=session.role)


def require_any_role(context: AuthContext) -> None:
    if context.role not in VALID_ROLES:
        raise BackendAuthorizationError("AUTH_ROLE_DENIED: unknown role.")


def require_roles(context: AuthContext, allowed_roles: Sequence[str]) -> None:
    allowed = set(str(item or "").strip().lower() for item in allowed_roles)
    if context.role not in allowed:
        label = ", ".join(sorted(allowed)) if allowed else "none"
        raise BackendAuthorizationError(f"AUTH_ROLE_DENIED: required role in [{label}].")


def ensure_submitter_allowed(context: AuthContext, requested_by: str) -> None:
    normalized_requester = str(requested_by or "").strip()
    if context.role in ("operator", "admin"):
        return
    if not normalized_requester:
        raise BackendAuthorizationError("AUTH_SUBMITTER_INVALID: requested_by is required.")
    if normalized_requester != context.user_id:
        raise BackendAuthorizationError("AUTH_SUBMITTER_MISMATCH: student can only submit for self.")


def ensure_job_visible(context: AuthContext, job: Mapping[str, object]) -> None:
    if context.role in ("operator", "admin"):
        return
    owner = str(job.get("requested_by", "") or "").strip()
    if owner != context.user_id:
        raise BackendAuthorizationError("AUTH_JOB_ACCESS_DENIED: student can only access own jobs.")

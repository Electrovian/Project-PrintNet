from __future__ import annotations

from dataclasses import dataclass


class BackendError(Exception):
    """Base backend failure."""


class BackendValidationError(BackendError):
    """Request validation error."""


class BackendNotFoundError(BackendError):
    """Record not found."""


class BackendConflictError(BackendError):
    """Record conflict error."""


class BackendAuthenticationError(BackendError):
    """Authentication failure."""


class BackendAuthorizationError(BackendError):
    """Authorization failure."""


class BackendOrchestrationError(BackendError):
    """Queue/worker orchestration failure."""


class BackendObservabilityError(BackendError):
    """Observability/telemetry failure."""


@dataclass(frozen=True)
class BackendErrorPayload:
    code: str
    detail: str


def to_error_payload(exc: Exception) -> BackendErrorPayload:
    text = str(exc or "").strip() or "backend error"
    if isinstance(exc, BackendValidationError):
        return BackendErrorPayload(code="BACKEND_VALIDATION_ERROR", detail=text)
    if isinstance(exc, BackendNotFoundError):
        return BackendErrorPayload(code="BACKEND_NOT_FOUND", detail=text)
    if isinstance(exc, BackendConflictError):
        return BackendErrorPayload(code="BACKEND_CONFLICT", detail=text)
    if isinstance(exc, BackendAuthenticationError):
        return BackendErrorPayload(code="BACKEND_AUTHENTICATION_ERROR", detail=text)
    if isinstance(exc, BackendAuthorizationError):
        return BackendErrorPayload(code="BACKEND_AUTHORIZATION_ERROR", detail=text)
    if isinstance(exc, BackendOrchestrationError):
        return BackendErrorPayload(code="BACKEND_ORCHESTRATION_ERROR", detail=text)
    if isinstance(exc, BackendObservabilityError):
        return BackendErrorPayload(code="BACKEND_OBSERVABILITY_ERROR", detail=text)
    return BackendErrorPayload(code="BACKEND_INTERNAL_ERROR", detail=text)


def http_status_for_error(exc: Exception) -> int:
    if isinstance(exc, BackendValidationError):
        return 400
    if isinstance(exc, BackendAuthenticationError):
        return 401
    if isinstance(exc, BackendAuthorizationError):
        return 403
    if isinstance(exc, BackendNotFoundError):
        return 404
    if isinstance(exc, BackendConflictError):
        return 409
    if isinstance(exc, BackendOrchestrationError):
        return 503
    if isinstance(exc, BackendObservabilityError):
        return 503
    return 500

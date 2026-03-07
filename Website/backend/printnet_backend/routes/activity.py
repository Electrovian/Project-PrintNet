from __future__ import annotations

import hmac

from ..authz import require_any_role, resolve_auth_context
from ..compat import APIRouter, HAS_FASTAPI
from ..errors import BackendAuthenticationError
from ..services import BackendState

if HAS_FASTAPI:
    try:
        from fastapi import Request  # type: ignore
    except Exception:  # pragma: no cover - optional import guard
        Request = object  # type: ignore
else:
    Request = object  # type: ignore


def _read_service_token(request: object | None) -> str:
    if request is None:
        return ""
    headers = getattr(request, "headers", None)
    if headers is None:
        return ""
    token = str(headers.get("x-activity-service-token", "")).strip()
    if token:
        return token
    return str(headers.get("X-Activity-Service-Token", "")).strip()


def _service_token_allowed(state: BackendState, request: object | None) -> bool:
    expected = str(getattr(state, "activity_service_token", "")).strip()
    if not expected:
        return False
    provided = _read_service_token(request)
    if not provided:
        return False
    return bool(hmac.compare_digest(provided, expected))


def build_activity_router(state: BackendState) -> APIRouter:
    router = APIRouter()

    @router.get("/activity/feed")
    def activity_feed(
        auth_token: str = "",
        cursor: str = "0",
        limit: str = "200",
        request: Request = None,
    ):
        normalized_token = str(auth_token or "").strip()
        requested_by = ""
        actor = "activity-service"
        auth_mode = "service_token"
        if normalized_token:
            context = resolve_auth_context(state, normalized_token)
            require_any_role(context)
            if context.role == "student":
                requested_by = context.user_id
            actor = context.user_id
            auth_mode = "session"
        elif not _service_token_allowed(state, request):
            raise BackendAuthenticationError(
                "ACTIVITY_AUTH_REQUIRED: provide auth_token or valid x-activity-service-token."
            )
        feed = state.activity_feed(cursor=cursor, limit=limit, requested_by=requested_by)
        return {
            "ok": True,
            "feed": feed,
            "actor": actor,
            "auth": auth_mode,
        }

    return router

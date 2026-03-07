from __future__ import annotations

import hmac

from ..authz import require_any_role, require_roles, resolve_auth_context
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


def build_queue_router(state: BackendState) -> APIRouter:
    router = APIRouter()

    @router.get("/queue/snapshot")
    def queue_snapshot(auth_token: str = "", request: Request = None):
        normalized = str(auth_token or "").strip()
        actor = "activity-service"
        if normalized:
            context = resolve_auth_context(state, normalized)
            require_any_role(context)
            requested_by = context.user_id if context.role == "student" else ""
            actor = context.user_id
        elif _service_token_allowed(state, request):
            requested_by = ""
        else:
            raise BackendAuthenticationError(
                "ACTIVITY_AUTH_REQUIRED: provide auth_token or valid x-activity-service-token."
            )
        snapshot = state.queue_snapshot(requested_by=requested_by)
        return {
            "ok": True,
            "snapshot": snapshot,
            "actor": actor,
        }

    @router.post("/queue/worker/heartbeat")
    def queue_worker_heartbeat(payload: dict | None = None):
        body = dict(payload or {})
        context = resolve_auth_context(state, str(body.get("auth_token", "")).strip())
        require_roles(context, ("operator", "admin"))
        worker_id = str(body.get("worker_id", context.user_id) or context.user_id).strip() or context.user_id
        heartbeat = state.record_worker_heartbeat(worker_id=worker_id)
        return {
            "ok": True,
            "heartbeat": heartbeat,
            "actor": context.user_id,
        }

    @router.post("/queue/worker/tick")
    def queue_worker_tick(payload: dict | None = None):
        body = dict(payload or {})
        context = resolve_auth_context(state, str(body.get("auth_token", "")).strip())
        require_roles(context, ("operator", "admin"))
        worker_id = str(body.get("worker_id", context.user_id) or context.user_id).strip() or context.user_id
        result = state.run_worker_tick(worker_id=worker_id, max_jobs=body.get("max_jobs"))
        return {
            "ok": True,
            "cycle": result["cycle"],
            "snapshot": result["snapshot"],
            "actor": context.user_id,
        }

    return router

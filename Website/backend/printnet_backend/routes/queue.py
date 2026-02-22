from __future__ import annotations

from ..authz import require_any_role, require_roles, resolve_auth_context
from ..compat import APIRouter
from ..services import BackendState


def build_queue_router(state: BackendState) -> APIRouter:
    router = APIRouter()

    @router.get("/queue/snapshot")
    def queue_snapshot(auth_token: str = ""):
        context = resolve_auth_context(state, auth_token)
        require_any_role(context)
        requested_by = context.user_id if context.role == "student" else ""
        snapshot = state.queue_snapshot(requested_by=requested_by)
        return {
            "ok": True,
            "snapshot": snapshot,
            "actor": context.user_id,
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

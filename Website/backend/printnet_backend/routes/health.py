from __future__ import annotations

from ..compat import APIRouter
from ..services import BackendState


def build_health_router(state: BackendState) -> APIRouter:
    router = APIRouter()

    @router.get("/health/live")
    def health_live():
        return {"ok": True, "service": "backend-fastapi-monolith", "state": "live"}

    @router.get("/health/ready")
    def health_ready():
        snapshot = state.status_snapshot()
        return {"ok": True, "service": "backend-fastapi-monolith", "state": "ready", "snapshot": snapshot}

    return router

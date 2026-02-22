from __future__ import annotations

from ..authz import VALID_ROLES, resolve_auth_context
from ..compat import APIRouter
from ..models import parse_session_payload
from ..services import BackendState


def build_auth_router(state: BackendState) -> APIRouter:
    router = APIRouter()

    @router.post("/auth/session")
    def create_session(payload: dict | None = None):
        body = dict(payload or {})
        user_id, role = parse_session_payload(body)
        session = state.create_session(user_id=user_id, role=role)
        return {"ok": True, "session": session.to_dict()}

    @router.get("/auth/whoami")
    def whoami(auth_token: str = ""):
        context = resolve_auth_context(state, auth_token)
        return {
            "ok": True,
            "identity": {
                "token": context.token,
                "user_id": context.user_id,
                "role": context.role,
            },
            "roles": list(VALID_ROLES),
        }

    return router

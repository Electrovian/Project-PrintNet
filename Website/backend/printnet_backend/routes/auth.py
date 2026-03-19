from __future__ import annotations

from ..authz import VALID_ROLES, resolve_auth_context
from ..compat import APIRouter
from ..errors import BackendAuthenticationError
from ..models import parse_login_payload, parse_login_verification_payload, parse_register_payload, parse_session_payload
from ..services import BackendState


def build_auth_router(state: BackendState) -> APIRouter:
    router = APIRouter()

    @router.post("/auth/session")
    def create_session(payload: dict | None = None):
        body = dict(payload or {})
        user_id, role = parse_session_payload(body)
        session = state.create_session(user_id=user_id, role=role)
        return {"ok": True, "session": session.to_dict()}

    @router.post("/auth/register")
    def register_account(payload: dict | None = None):
        body = dict(payload or {})
        user_id, password, requested_role = parse_register_payload(body)
        account = state.register_account(user_id=user_id, password=password, role=requested_role)
        session = state.create_session(user_id=account.user_id, role=account.role, trusted_role=True)
        return {"ok": True, "account": account.to_public_dict(), "session": session.to_dict()}

    @router.post("/auth/login")
    def login_account(payload: dict | None = None):
        body = dict(payload or {})
        user_id, password = parse_login_payload(body)
        account = state.authenticate_account(user_id=user_id, password=password)
        session = state.create_session(user_id=account.user_id, role=account.role, trusted_role=True)
        return {"ok": True, "account": account.to_public_dict(), "session": session.to_dict()}

    @router.post("/auth/login/request-code")
    def request_login_code(payload: dict | None = None):
        body = dict(payload or {})
        user_id, password = parse_login_payload(body)
        challenge = state.request_login_verification(user_id=user_id, password=password)
        return {"ok": True, "challenge": challenge}

    @router.post("/auth/login/verify-code")
    def verify_login_code(payload: dict | None = None):
        body = dict(payload or {})
        challenge_id, verification_code = parse_login_verification_payload(body)
        account, session = state.verify_login_verification(
            challenge_id=challenge_id,
            verification_code=verification_code,
        )
        return {"ok": True, "account": account.to_public_dict(), "session": session.to_dict()}

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

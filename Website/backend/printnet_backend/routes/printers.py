from __future__ import annotations

from ..authz import require_roles, resolve_auth_context
from ..compat import APIRouter
from ..models import parse_printer_payload
from ..services import BackendState


def build_printers_router(state: BackendState) -> APIRouter:
    router = APIRouter()

    @router.post("/printers/register")
    def register_printer(payload: dict | None = None):
        body = dict(payload or {})
        context = resolve_auth_context(state, str(body.get("auth_token", "")).strip())
        require_roles(context, ("operator", "admin"))
        printer_id, name, connector_type, endpoint = parse_printer_payload(body)
        printer = state.register_printer(
            printer_id=printer_id,
            name=name,
            connector_type=connector_type,
            endpoint=endpoint,
        )
        return {"ok": True, "printer": printer.to_dict(), "actor": context.user_id}

    @router.get("/printers/list")
    def list_printers(auth_token: str = ""):
        context = resolve_auth_context(state, auth_token)
        require_roles(context, ("operator", "admin"))
        rows = state.list_printers()
        return {
            "ok": True,
            "count": len(rows),
            "printers": [item.to_dict() for item in rows],
            "actor": context.user_id,
        }

    return router

from __future__ import annotations

from ..authz import require_any_role, resolve_auth_context
from ..compat import APIRouter
from ..services import BackendState


def build_profiles_router(state: BackendState) -> APIRouter:
    router = APIRouter()

    @router.get("/profiles/catalog")
    def list_catalog(
        auth_token: str = "",
        vendor: str = "",
        model: str = "",
        nozzle: str = "",
        process: str = "",
        filament: str = "",
    ):
        context = resolve_auth_context(state, auth_token)
        require_any_role(context)
        profiles = state.list_profiles(
            vendor=vendor,
            model=model,
            nozzle=nozzle,
            process=process,
            filament=filament,
        )
        return {
            "ok": True,
            "count": len(profiles),
            "profiles": [item.to_dict() for item in profiles],
            "actor": context.user_id,
        }

    return router

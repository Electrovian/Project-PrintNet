from __future__ import annotations

from typing import Sequence

from ..compat import APIRouter, HAS_FASTAPI
from ..region_block import RegionComplianceDecision, evaluate_region_compliance
from ..services import BackendState

if HAS_FASTAPI:
    try:
        from fastapi import Request  # type: ignore
    except Exception:  # pragma: no cover - optional import guard
        Request = object  # type: ignore
else:
    Request = object  # type: ignore


def _metric_status(decision: RegionComplianceDecision) -> str:
    if decision.reason_code == "REGION_BLOCKED":
        return "blocked"
    if decision.reason_code == "REGION_GEO_UNDETERMINED":
        return "unknown_allowed" if decision.allowed else "unknown_denied"
    return "allowed"


def build_compliance_router(
    state: BackendState,
    *,
    region_block_enabled: bool,
    blocked_state_codes: Sequence[str],
    unknown_policy: str,
    trusted_header_keys: Sequence[str] | None = None,
    backend_env: str = "production",
) -> APIRouter:
    router = APIRouter()

    @router.get("/compliance/region")
    def compliance_region(request: Request = None):
        decision = evaluate_region_compliance(
            headers=getattr(request, "headers", {}),
            region_block_enabled=region_block_enabled,
            blocked_state_codes=blocked_state_codes,
            unknown_policy=unknown_policy,
            trusted_header_keys=trusted_header_keys,
        )
        try:
            state.record_operation_metric(
                event="compliance.region.precheck",
                status=_metric_status(decision),
                duration_ms=0.0,
            )
        except Exception:
            pass

        return {
            "ok": True,
            "compliance": {
                "backend_env": str(backend_env or "production"),
                "region_block_enabled": bool(region_block_enabled),
                "blocked_state_codes": list(decision.blocked_state_codes),
                "unknown_policy": str(decision.unknown_policy),
                "state_code": str(decision.state_code or ""),
                "decision": "allow" if decision.allowed else "deny",
                "reason_code": decision.reason_code,
                "detail": decision.detail,
                "http_status": 200 if decision.allowed else 451,
            },
        }

    return router

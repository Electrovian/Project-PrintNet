from __future__ import annotations

from time import perf_counter

from ..authz import require_roles, resolve_auth_context
from ..compat import APIRouter
from ..services import BackendState


def build_ops_router(state: BackendState) -> APIRouter:
    router = APIRouter()

    @router.get("/ops/metrics")
    def ops_metrics(auth_token: str = ""):
        started = perf_counter()
        status = "ok"
        try:
            context = resolve_auth_context(state, auth_token)
            require_roles(context, ("operator", "admin"))
            snapshot = state.observability_metrics_snapshot()
            state.append_security_audit(
                actor=context.user_id,
                action="ops.metrics.read",
                resource="ops/metrics",
                outcome="success",
                details={"auth_token": auth_token},
            )
            return {"ok": True, "metrics": snapshot, "actor": context.user_id}
        except Exception:
            status = "error"
            raise
        finally:
            state.record_operation_metric(
                event="ops.metrics.read",
                status=status,
                duration_ms=_duration_ms(started),
            )

    @router.get("/ops/audit")
    def ops_audit(auth_token: str = "", limit: str = "50"):
        started = perf_counter()
        status = "ok"
        try:
            context = resolve_auth_context(state, auth_token)
            require_roles(context, ("operator", "admin"))
            rows = state.observability_audit_snapshot(limit=limit)
            state.append_security_audit(
                actor=context.user_id,
                action="ops.audit.read",
                resource="ops/audit",
                outcome="success",
                details={"auth_token": auth_token, "limit": limit},
            )
            return {"ok": True, "count": len(rows), "records": rows, "actor": context.user_id}
        except Exception:
            status = "error"
            raise
        finally:
            state.record_operation_metric(
                event="ops.audit.read",
                status=status,
                duration_ms=_duration_ms(started),
            )

    @router.get("/ops/release-readiness")
    def ops_release_readiness(auth_token: str = ""):
        started = perf_counter()
        status = "ok"
        try:
            context = resolve_auth_context(state, auth_token)
            require_roles(context, ("operator", "admin"))
            snapshot = state.release_readiness_snapshot()
            state.append_security_audit(
                actor=context.user_id,
                action="ops.release.read",
                resource="ops/release-readiness",
                outcome="success",
                details={"auth_token": auth_token},
            )
            return {"ok": True, "release": snapshot, "actor": context.user_id}
        except Exception:
            status = "error"
            raise
        finally:
            state.record_operation_metric(
                event="ops.release.read",
                status=status,
                duration_ms=_duration_ms(started),
            )

    @router.post("/ops/release-readiness/check")
    def ops_release_check(payload: dict | None = None):
        body = dict(payload or {})
        started = perf_counter()
        status = "ok"
        try:
            context = resolve_auth_context(state, str(body.get("auth_token", "")).strip())
            require_roles(context, ("admin",))
            check_name = str(body.get("check_name", "")).strip()
            passed = body.get("passed", False)
            detail = str(body.get("detail", "")).strip()
            check = state.set_release_readiness_check(
                check_name=check_name,
                passed=passed,
                detail=detail,
            )
            state.append_security_audit(
                actor=context.user_id,
                action="ops.release.check.update",
                resource=f"ops/release-readiness/check/{check_name}",
                outcome="success",
                details=body,
            )
            return {"ok": True, "check": check, "actor": context.user_id}
        except Exception:
            status = "error"
            raise
        finally:
            state.record_operation_metric(
                event="ops.release.check.update",
                status=status,
                duration_ms=_duration_ms(started),
            )

    return router


def _duration_ms(started: float) -> float:
    elapsed = (perf_counter() - started) * 1000.0
    if elapsed < 0:
        return 0.0
    return round(elapsed, 3)

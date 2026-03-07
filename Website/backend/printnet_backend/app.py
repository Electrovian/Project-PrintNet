from __future__ import annotations

from typing import Any

from .compat import FastAPI, HAS_FASTAPI, JSONResponse
from .errors import BackendError, http_status_for_error, to_error_payload
from .region_block import RegionComplianceDecision, evaluate_region_compliance
from .routes import (
    build_activity_router,
    build_auth_router,
    build_compliance_router,
    build_health_router,
    build_jobs_router,
    build_ops_router,
    build_printers_router,
    build_profiles_router,
    build_queue_router,
)
from .services import BackendState
from .settings import BackendSettings

if HAS_FASTAPI:
    try:
        from fastapi.middleware.cors import CORSMiddleware  # type: ignore
    except Exception:  # pragma: no cover - optional import guard
        CORSMiddleware = None
else:
    CORSMiddleware = None


def create_app(
    *,
    settings: BackendSettings | None = None,
    state: BackendState | None = None,
):
    resolved_settings = settings or BackendSettings.from_env()
    resolved_state = state or BackendState(
        default_role=resolved_settings.default_role,
        allow_client_role_override=resolved_settings.allow_client_role_override,
        operator_user_ids=resolved_settings.operator_user_ids,
        admin_user_ids=resolved_settings.admin_user_ids,
        activity_service_token=resolved_settings.activity_service_token,
        activity_max_jobs=resolved_settings.activity_max_jobs,
        activity_max_events=resolved_settings.activity_max_events,
        queue_name=resolved_settings.queue_name,
        queue_worker_max_jobs_per_tick=resolved_settings.queue_worker_max_jobs_per_tick,
        queue_worker_heartbeat_ttl_seconds=resolved_settings.queue_worker_heartbeat_ttl_seconds,
        observability_max_audit_records=resolved_settings.observability_max_audit_records,
        observability_max_metric_keys=resolved_settings.observability_max_metric_keys,
        super_admin_email=resolved_settings.super_admin_email,
        super_admin_password=resolved_settings.super_admin_password,
        auth_verification_code_ttl_seconds=resolved_settings.auth_verification_code_ttl_seconds,
        auth_verification_max_attempts=resolved_settings.auth_verification_max_attempts,
        auth_expose_debug_code=resolved_settings.auth_expose_debug_code,
        auth_email_from=resolved_settings.auth_email_from,
        smtp_host=resolved_settings.smtp_host,
        smtp_port=resolved_settings.smtp_port,
        smtp_username=resolved_settings.smtp_username,
        smtp_password=resolved_settings.smtp_password,
        smtp_starttls=resolved_settings.smtp_starttls,
        smtp_use_ssl=resolved_settings.smtp_use_ssl,
        release_required_checks=resolved_settings.release_required_checks,
    )

    kwargs: dict[str, Any] = {
        "title": resolved_settings.app_name,
        "version": resolved_settings.app_version,
    }
    if HAS_FASTAPI and not resolved_settings.enable_docs:
        kwargs.update({"docs_url": None, "redoc_url": None, "openapi_url": None})

    app = FastAPI(**kwargs)
    if HAS_FASTAPI and CORSMiddleware is not None:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
            allow_credentials=False,
        )

    blocked_state_codes = tuple(
        str(code).strip().upper()
        for code in resolved_settings.blocked_us_state_codes
        if str(code).strip()
    )
    trusted_region_headers = tuple(
        str(item).strip().lower()
        for item in resolved_settings.region_block_trust_headers
        if str(item).strip()
    )

    def _record_region_metric(decision: RegionComplianceDecision) -> None:
        if not hasattr(resolved_state, "record_operation_metric"):
            return
        status = "allowed"
        if decision.reason_code == "REGION_BLOCKED":
            status = "blocked"
        elif decision.reason_code == "REGION_GEO_UNDETERMINED":
            status = "unknown_allowed" if decision.allowed else "unknown_denied"
        try:
            resolved_state.record_operation_metric(
                event="compliance.region",
                status=status,
                duration_ms=0.0,
            )
        except Exception:
            return

    if HAS_FASTAPI:

        @app.middleware("http")
        async def region_block_guard(request, call_next):
            path = str(getattr(getattr(request, "url", None), "path", "")).strip().rstrip("/")
            if path.endswith("/compliance/region"):
                return await call_next(request)
            decision = evaluate_region_compliance(
                headers=getattr(request, "headers", {}),
                region_block_enabled=resolved_settings.region_block_enabled,
                blocked_state_codes=blocked_state_codes,
                unknown_policy=resolved_settings.region_block_on_unknown,
                trusted_header_keys=trusted_region_headers or None,
            )
            _record_region_metric(decision)
            if not decision.allowed:
                return JSONResponse(
                    status_code=451,
                    content={
                        "ok": False,
                        "error": {
                            "code": decision.reason_code,
                            "detail": decision.detail,
                        },
                    },
                )
            response = await call_next(request)
            if decision.reason_code == "REGION_GEO_UNDETERMINED":
                response.headers["x-compliance-warning"] = "REGION_GEO_UNDETERMINED"
            return response

    _register_error_handlers(app)

    prefix = resolved_settings.api_prefix
    app.include_router(build_health_router(resolved_state), prefix=prefix)
    app.include_router(
        build_compliance_router(
            resolved_state,
            region_block_enabled=resolved_settings.region_block_enabled,
            blocked_state_codes=blocked_state_codes,
            unknown_policy=resolved_settings.region_block_on_unknown,
            trusted_header_keys=trusted_region_headers,
            backend_env=resolved_settings.backend_env,
        ),
        prefix=prefix,
    )
    app.include_router(build_auth_router(resolved_state), prefix=prefix)
    app.include_router(build_activity_router(resolved_state), prefix=prefix)
    app.include_router(build_profiles_router(resolved_state), prefix=prefix)
    app.include_router(build_printers_router(resolved_state), prefix=prefix)
    app.include_router(build_jobs_router(resolved_state), prefix=prefix)
    app.include_router(build_queue_router(resolved_state), prefix=prefix)
    app.include_router(build_ops_router(resolved_state), prefix=prefix)
    return app


def _register_error_handlers(app):
    if HAS_FASTAPI:

        def backend_error_handler(_request, exc: Exception):
            payload = to_error_payload(exc)
            return JSONResponse(
                status_code=http_status_for_error(exc),
                content={"ok": False, "error": {"code": payload.code, "detail": payload.detail}},
            )

        app.add_exception_handler(BackendError, backend_error_handler)
        return

    def backend_error_handler_fallback(exc: Exception):
        payload = to_error_payload(exc)
        return JSONResponse(
            status_code=http_status_for_error(exc),
            content={"ok": False, "error": {"code": payload.code, "detail": payload.detail}},
        )

    app.add_exception_handler(BackendError, backend_error_handler_fallback)

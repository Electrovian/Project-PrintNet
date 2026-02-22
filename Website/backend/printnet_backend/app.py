from __future__ import annotations

from typing import Any

from .compat import FastAPI, HAS_FASTAPI, JSONResponse
from .errors import BackendError, http_status_for_error, to_error_payload
from .routes import (
    build_auth_router,
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
        queue_name=resolved_settings.queue_name,
        queue_worker_max_jobs_per_tick=resolved_settings.queue_worker_max_jobs_per_tick,
        queue_worker_heartbeat_ttl_seconds=resolved_settings.queue_worker_heartbeat_ttl_seconds,
        observability_max_audit_records=resolved_settings.observability_max_audit_records,
        observability_max_metric_keys=resolved_settings.observability_max_metric_keys,
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
    _register_error_handlers(app)

    prefix = resolved_settings.api_prefix
    app.include_router(build_health_router(resolved_state), prefix=prefix)
    app.include_router(build_auth_router(resolved_state), prefix=prefix)
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

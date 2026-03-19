from __future__ import annotations

from ..authz import ensure_job_visible, ensure_submitter_allowed, require_any_role, resolve_auth_context
from ..compat import APIRouter
from ..models import parse_job_payload, parse_model_upload_payload
from ..services import BackendState


def build_jobs_router(state: BackendState) -> APIRouter:
    router = APIRouter()

    @router.post("/jobs/upload-model")
    def upload_model(payload: dict | None = None):
        body = dict(payload or {})
        context = resolve_auth_context(state, str(body.get("auth_token", "")).strip())
        require_any_role(context)
        file_name, data_base64 = parse_model_upload_payload(body)
        model = state.store_uploaded_model(
            file_name=file_name,
            data_base64=data_base64,
            requested_by=context.user_id,
        )
        return {"ok": True, "model": model, "actor": context.user_id}

    @router.post("/jobs/submit")
    def submit_job(payload: dict | None = None):
        body = dict(payload or {})
        context = resolve_auth_context(state, str(body.get("auth_token", "")).strip())
        require_any_role(context)
        model_name, profile_id, requested_by, printer_id = parse_job_payload(body)
        ensure_submitter_allowed(context, requested_by)
        job = state.submit_job(
            model_name=model_name,
            profile_id=profile_id,
            requested_by=requested_by,
            printer_id=printer_id,
        )
        return {"ok": True, "job": job.to_dict(), "actor": context.user_id}

    @router.get("/jobs/status")
    def job_status(job_id: str = "", auth_token: str = ""):
        context = resolve_auth_context(state, auth_token)
        require_any_role(context)
        job = state.get_job(job_id)
        ensure_job_visible(context, job.to_dict())
        return {"ok": True, "job": job.to_dict()}

    @router.get("/jobs/events")
    def job_events(job_id: str = "", auth_token: str = ""):
        context = resolve_auth_context(state, auth_token)
        require_any_role(context)
        job = state.get_job(job_id)
        ensure_job_visible(context, job.to_dict())
        events = state.list_job_events(job_id)
        return {"ok": True, "job_id": str(job_id), "count": len(events), "events": events}

    return router

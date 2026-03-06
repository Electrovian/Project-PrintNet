from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class BackendSettings:
    app_name: str = "EON-OpenSlicer Backend"
    app_version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    default_role: str = "student"
    allow_client_role_override: bool = False
    operator_user_ids: tuple[str, ...] = tuple()
    admin_user_ids: tuple[str, ...] = tuple()
    enable_docs: bool = True
    queue_name: str = "default"
    queue_worker_max_jobs_per_tick: int = 1
    queue_worker_heartbeat_ttl_seconds: int = 60
    observability_max_audit_records: int = 200
    observability_max_metric_keys: int = 256
    release_required_checks: tuple[str, ...] = (
        "backend_health",
        "authz_enforced",
        "queue_worker_operational",
        "kubernetes_packaging_validated",
    )

    @staticmethod
    def from_env(env: dict[str, str] | None = None) -> "BackendSettings":
        source = env or dict(os.environ)
        app_name = str(source.get("BACKEND_APP_NAME", "EON-OpenSlicer Backend")).strip() or "EON-OpenSlicer Backend"
        app_version = str(source.get("BACKEND_APP_VERSION", "0.1.0")).strip() or "0.1.0"
        api_prefix = str(source.get("BACKEND_API_PREFIX", "/api/v1")).strip() or "/api/v1"
        if not api_prefix.startswith("/"):
            api_prefix = "/" + api_prefix
        default_role = str(source.get("BACKEND_DEFAULT_ROLE", "student")).strip().lower() or "student"
        allow_client_role_override_raw = str(source.get("BACKEND_ALLOW_CLIENT_ROLE_OVERRIDE", "0")).strip().lower()
        allow_client_role_override = allow_client_role_override_raw in ("1", "true", "yes", "on")
        operator_user_ids = _read_csv(
            source,
            key="BACKEND_OPERATOR_USER_IDS",
            default="",
        )
        admin_user_ids = _read_csv(
            source,
            key="BACKEND_ADMIN_USER_IDS",
            default="",
        )
        enable_docs_raw = str(source.get("BACKEND_ENABLE_DOCS", "1")).strip().lower()
        enable_docs = enable_docs_raw not in ("0", "false", "no", "off")
        queue_name = str(source.get("BACKEND_QUEUE_NAME", "default")).strip() or "default"
        queue_worker_max_jobs_per_tick = _read_int(
            source,
            key="BACKEND_QUEUE_WORKER_MAX_JOBS_PER_TICK",
            default=1,
            minimum=1,
            maximum=100,
        )
        queue_worker_heartbeat_ttl_seconds = _read_int(
            source,
            key="BACKEND_QUEUE_WORKER_HEARTBEAT_TTL_SECONDS",
            default=60,
            minimum=1,
            maximum=86400,
        )
        observability_max_audit_records = _read_int(
            source,
            key="BACKEND_OBSERVABILITY_MAX_AUDIT_RECORDS",
            default=200,
            minimum=10,
            maximum=5000,
        )
        observability_max_metric_keys = _read_int(
            source,
            key="BACKEND_OBSERVABILITY_MAX_METRIC_KEYS",
            default=256,
            minimum=10,
            maximum=5000,
        )
        release_required_checks = _read_csv(
            source,
            key="BACKEND_RELEASE_REQUIRED_CHECKS",
            default="backend_health,authz_enforced,queue_worker_operational,kubernetes_packaging_validated",
        )
        return BackendSettings(
            app_name=app_name,
            app_version=app_version,
            api_prefix=api_prefix,
            default_role=default_role,
            allow_client_role_override=allow_client_role_override,
            operator_user_ids=operator_user_ids,
            admin_user_ids=admin_user_ids,
            enable_docs=enable_docs,
            queue_name=queue_name,
            queue_worker_max_jobs_per_tick=queue_worker_max_jobs_per_tick,
            queue_worker_heartbeat_ttl_seconds=queue_worker_heartbeat_ttl_seconds,
            observability_max_audit_records=observability_max_audit_records,
            observability_max_metric_keys=observability_max_metric_keys,
            release_required_checks=release_required_checks,
        )


def _read_int(
    source: dict[str, str],
    *,
    key: str,
    default: int,
    minimum: int,
    maximum: int,
) -> int:
    raw = str(source.get(key, str(default))).strip()
    try:
        value = int(raw)
    except Exception:
        value = int(default)
    if value < minimum:
        return minimum
    if value > maximum:
        return maximum
    return value


def _read_csv(
    source: dict[str, str],
    *,
    key: str,
    default: str,
) -> tuple[str, ...]:
    raw = str(source.get(key, default)).strip()
    if not raw:
        raw = str(default).strip()
    values: list[str] = []
    for part in raw.split(","):
        text = str(part).strip()
        if not text:
            continue
        values.append(text)
    if not values:
        return tuple()
    return tuple(values)

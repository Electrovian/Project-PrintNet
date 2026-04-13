from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class BackendSettings:
    app_name: str = "EON-OpenSlicer Backend"
    app_version: str = "1.0.0"
    api_prefix: str = "/api/v1"
    backend_env: str = "development"
    default_role: str = "student"
    allow_client_role_override: bool = False
    operator_user_ids: tuple[str, ...] = tuple()
    admin_user_ids: tuple[str, ...] = tuple()
    enable_docs: bool = True
    region_block_enabled: bool = True
    region_block_on_unknown: str = "allow"
    region_block_trust_headers: tuple[str, ...] = tuple()
    blocked_us_state_codes: tuple[str, ...] = ("CA",)
    activity_service_token: str = ""
    activity_max_jobs: int = 1000
    activity_max_events: int = 5000
    queue_name: str = "default"
    queue_worker_max_jobs_per_tick: int = 1
    queue_worker_heartbeat_ttl_seconds: int = 60
    observability_max_audit_records: int = 200
    observability_max_metric_keys: int = 256
    super_admin_email: str = ""
    super_admin_password: str = ""
    auth_verification_code_ttl_seconds: int = 600
    auth_verification_max_attempts: int = 5
    auth_expose_debug_code: bool = False
    auth_email_require_smtp: bool = False
    auth_email_from: str = "no-reply@printnet.local"
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_starttls: bool = True
    smtp_use_ssl: bool = False
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
        app_version = str(source.get("BACKEND_APP_VERSION", "1.0.0")).strip() or "1.0.0"
        api_prefix = str(source.get("BACKEND_API_PREFIX", "/api/v1")).strip() or "/api/v1"
        if not api_prefix.startswith("/"):
            api_prefix = "/" + api_prefix
        backend_env = _read_backend_env(source, key="BACKEND_ENV", default="development")
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
        region_block_enabled = _read_bool(
            source,
            key="BACKEND_REGION_BLOCK_ENABLED",
            default=True,
        )
        region_block_on_unknown = _read_region_unknown_policy(
            source,
            key="BACKEND_REGION_BLOCK_ON_UNKNOWN",
            default="allow" if backend_env == "development" else "deny",
        )
        region_block_trust_headers = _read_header_names(
            source,
            key="BACKEND_REGION_BLOCK_TRUST_HEADERS",
            default="",
        )
        blocked_us_state_codes = _read_state_codes(
            source,
            key="BACKEND_BLOCKED_US_STATE_CODES",
            default="CA",
        )
        activity_service_token = str(source.get("BACKEND_ACTIVITY_SERVICE_TOKEN", "")).strip()
        activity_max_jobs = _read_int(
            source,
            key="BACKEND_ACTIVITY_MAX_JOBS",
            default=1000,
            minimum=1,
            maximum=50000,
        )
        activity_max_events = _read_int(
            source,
            key="BACKEND_ACTIVITY_MAX_EVENTS",
            default=5000,
            minimum=10,
            maximum=500000,
        )
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
        super_admin_email = str(source.get("BACKEND_SUPER_ADMIN_EMAIL", "")).strip().lower()
        super_admin_password = str(source.get("BACKEND_SUPER_ADMIN_PASSWORD", ""))
        auth_verification_code_ttl_seconds = _read_int(
            source,
            key="BACKEND_AUTH_VERIFICATION_CODE_TTL_SECONDS",
            default=600,
            minimum=60,
            maximum=3600,
        )
        auth_verification_max_attempts = _read_int(
            source,
            key="BACKEND_AUTH_VERIFICATION_MAX_ATTEMPTS",
            default=5,
            minimum=1,
            maximum=10,
        )
        auth_expose_debug_code = _read_bool(
            source,
            key="BACKEND_AUTH_EXPOSE_DEBUG_CODE",
            default=False,
        )
        auth_email_require_smtp = _read_bool(
            source,
            key="BACKEND_AUTH_EMAIL_REQUIRE_SMTP",
            default=False,
        )
        auth_email_from = str(source.get("BACKEND_AUTH_EMAIL_FROM", "no-reply@printnet.local")).strip()
        smtp_host = str(source.get("BACKEND_SMTP_HOST", "")).strip()
        smtp_port = _read_int(
            source,
            key="BACKEND_SMTP_PORT",
            default=587,
            minimum=1,
            maximum=65535,
        )
        smtp_username = str(source.get("BACKEND_SMTP_USERNAME", "")).strip()
        smtp_password = str(source.get("BACKEND_SMTP_PASSWORD", ""))
        smtp_starttls = _read_bool(
            source,
            key="BACKEND_SMTP_STARTTLS",
            default=True,
        )
        smtp_use_ssl = _read_bool(
            source,
            key="BACKEND_SMTP_USE_SSL",
            default=False,
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
            backend_env=backend_env,
            default_role=default_role,
            allow_client_role_override=allow_client_role_override,
            operator_user_ids=operator_user_ids,
            admin_user_ids=admin_user_ids,
            enable_docs=enable_docs,
            region_block_enabled=region_block_enabled,
            region_block_on_unknown=region_block_on_unknown,
            region_block_trust_headers=region_block_trust_headers,
            blocked_us_state_codes=blocked_us_state_codes,
            activity_service_token=activity_service_token,
            activity_max_jobs=activity_max_jobs,
            activity_max_events=activity_max_events,
            queue_name=queue_name,
            queue_worker_max_jobs_per_tick=queue_worker_max_jobs_per_tick,
            queue_worker_heartbeat_ttl_seconds=queue_worker_heartbeat_ttl_seconds,
            observability_max_audit_records=observability_max_audit_records,
            observability_max_metric_keys=observability_max_metric_keys,
            super_admin_email=super_admin_email,
            super_admin_password=super_admin_password,
            auth_verification_code_ttl_seconds=auth_verification_code_ttl_seconds,
            auth_verification_max_attempts=auth_verification_max_attempts,
            auth_expose_debug_code=auth_expose_debug_code,
            auth_email_require_smtp=auth_email_require_smtp,
            auth_email_from=auth_email_from,
            smtp_host=smtp_host,
            smtp_port=smtp_port,
            smtp_username=smtp_username,
            smtp_password=smtp_password,
            smtp_starttls=smtp_starttls,
            smtp_use_ssl=smtp_use_ssl,
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


def _read_bool(
    source: dict[str, str],
    *,
    key: str,
    default: bool,
) -> bool:
    raw = str(source.get(key, "1" if default else "0")).strip().lower()
    if raw in ("1", "true", "yes", "on"):
        return True
    if raw in ("0", "false", "no", "off"):
        return False
    return bool(default)


def _read_backend_env(
    source: dict[str, str],
    *,
    key: str,
    default: str,
) -> str:
    raw = str(source.get(key, default)).strip().lower()
    if raw in ("dev", "development", "local", "test", "testing"):
        return "development"
    return "production"


def _read_region_unknown_policy(
    source: dict[str, str],
    *,
    key: str,
    default: str,
) -> str:
    raw = str(source.get(key, default)).strip().lower()
    if raw in ("allow", "permit", "1", "true", "yes", "on"):
        return "allow"
    if raw in ("deny", "block", "0", "false", "no", "off"):
        return "deny"
    fallback = str(default or "").strip().lower()
    if fallback in ("allow", "deny"):
        return fallback
    return "deny"


def _read_header_names(
    source: dict[str, str],
    *,
    key: str,
    default: str,
) -> tuple[str, ...]:
    rows = _read_csv(source, key=key, default=default)
    values: list[str] = []
    seen: set[str] = set()
    for item in rows:
        name = str(item or "").strip().lower()
        if not name:
            continue
        if name in seen:
            continue
        seen.add(name)
        values.append(name)
    return tuple(values)


def _read_state_codes(
    source: dict[str, str],
    *,
    key: str,
    default: str,
) -> tuple[str, ...]:
    rows = _read_csv(source, key=key, default=default)
    values: list[str] = []
    for item in rows:
        text = str(item or "").strip().upper()
        if text.startswith("US-") and len(text) >= 5:
            text = text[3:].strip()
        if len(text) == 2 and text.isalpha():
            values.append(text)
    # Preserve order while removing duplicates.
    if not values:
        return tuple()
    deduped: list[str] = []
    seen: set[str] = set()
    for code in values:
        if code in seen:
            continue
        seen.add(code)
        deduped.append(code)
    return tuple(deduped)

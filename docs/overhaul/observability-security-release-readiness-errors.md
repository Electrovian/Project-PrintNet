# Observability, Security Hardening, and Release Readiness Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T394`

## Backend Errors

- `BACKEND_AUTHENTICATION_ERROR` -> HTTP `401`
  - Trigger: missing/invalid `auth_token` for ops endpoints.

- `BACKEND_AUTHORIZATION_ERROR` -> HTTP `403`
  - Trigger: insufficient role for observability/release operations.

- `BACKEND_VALIDATION_ERROR` -> HTTP `400`
  - Trigger: invalid `limit`, invalid release check payload, invalid boolean value.

- `BACKEND_OBSERVABILITY_ERROR` -> HTTP `503`
  - Trigger: observability subsystem failure (telemetry/audit/release snapshot operations).

## Security Hardening Rules

- Sensitive keys are redacted in audit details:
  - keys containing `auth`, `token`, `secret`, `password`, `api_key`, `credential`.
- Audit logs are bounded by `BACKEND_OBSERVABILITY_MAX_AUDIT_RECORDS`.
- Metric key growth is bounded by `BACKEND_OBSERVABILITY_MAX_METRIC_KEYS`.

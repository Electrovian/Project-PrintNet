# Observability, Security Hardening, and Release Readiness Contract

Date: 2026-02-13  
Checklist ID: `T392`

## Backend Modules

- `Website/backend/printnet_backend/observability.py`
  - `redact_sensitive_fields(...)`
  - `ObservabilityState`
  - `MetricCounter`
  - `AuditRecord`
  - `ReleaseReadinessCheck`
- `Website/backend/printnet_backend/services.py`
  - observability and release-readiness state integration
  - `record_operation_metric(...)`
  - `append_security_audit(...)`
  - `observability_metrics_snapshot(...)`
  - `observability_audit_snapshot(...)`
  - `set_release_readiness_check(...)`
  - `release_readiness_snapshot(...)`
- `Website/backend/printnet_backend/routes/ops.py`
  - secure ops endpoints for metrics, audit, and release gate updates

## Settings Contract

- `BACKEND_OBSERVABILITY_MAX_AUDIT_RECORDS`
- `BACKEND_OBSERVABILITY_MAX_METRIC_KEYS`
- `BACKEND_RELEASE_REQUIRED_CHECKS`

## API Contract

- `GET /ops/metrics`
  - role: `operator/admin`
- `GET /ops/audit`
  - role: `operator/admin`
  - query: `limit`
- `GET /ops/release-readiness`
  - role: `operator/admin`
- `POST /ops/release-readiness/check`
  - role: `admin`
  - body: `check_name`, `passed`, optional `detail`

## Frontend Client Contract

- `Website/frontend/src/api/backendClient.js`
  - `getOpsMetrics(...)`
  - `getOpsAudit(...)`
  - `getReleaseReadiness(...)`
  - `setReleaseCheck(...)`

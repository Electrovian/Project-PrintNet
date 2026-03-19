# Observability, Security Hardening, and Release Readiness Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T398`

## Run Smoke

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-observability-security-release-readiness-smoke.ps1
```

## Run Unit and Integration Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-observability-security-release-readiness-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-observability-security-release-readiness-integration.ps1
```

## Defaults

- `BACKEND_OBSERVABILITY_MAX_AUDIT_RECORDS=200`
- `BACKEND_OBSERVABILITY_MAX_METRIC_KEYS=256`
- `BACKEND_RELEASE_REQUIRED_CHECKS=backend_health,authz_enforced,queue_worker_operational,kubernetes_packaging_validated`
- Ops route permissions:
  - `operator/admin`: `GET /ops/metrics`, `GET /ops/audit`, `GET /ops/release-readiness`
  - `admin`: `POST /ops/release-readiness/check`
- Runtime budgets:
  - Unit: `30s`
  - Integration: `30s`
- Smoke report paths:
  - `docs/_observability_security_release_readiness_report.json`
  - `docs/_observability_security_release_readiness_summary.txt`

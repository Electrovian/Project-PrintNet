# Kubernetes Packaging and Deployment Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T388`

## Run Smoke

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-kubernetes-packaging-smoke.ps1
```

## Run Unit and Integration Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-kubernetes-packaging-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-kubernetes-packaging-integration.ps1
```

## Deploy to k3d

```powershell
powershell -ExecutionPolicy Bypass -File scripts/k3d-deploy.ps1
```

## Default Deployment Knobs

- Helm chart path: `deploy/helm/printnet`
- Default namespace: `printnet`
- Default release name: `eon-printnet`
- k3d values file: `deploy/helm/printnet/values-k3d.yaml`
- Ingress host default: `printnet.local`
- Backend queue worker env defaults:
  - `BACKEND_QUEUE_WORKER_MAX_JOBS_PER_TICK=1`
  - `BACKEND_QUEUE_WORKER_HEARTBEAT_TTL_SECONDS=60`
- Runtime budgets:
  - Unit: `30s`
  - Integration: `30s`
- Smoke report paths:
  - `docs/_kubernetes_packaging_report.json`
  - `docs/_kubernetes_packaging_summary.txt`

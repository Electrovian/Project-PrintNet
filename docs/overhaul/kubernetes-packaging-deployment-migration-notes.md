# Kubernetes Packaging and Deployment Migration Notes

Date: 2026-02-13  
Checklist ID: `T389`

## Legacy Baseline

- `deploy/helm/printnet` existed as an empty scaffold with no chart artifacts.
- No automated `k3d` deployment flow was available.
- No packaging smoke or contract tests existed.

## Current Baseline

- Helm chart now defines core platform stack resources:
  - backend, worker, frontend, redis, mongo, ingress.
- Added `values-k3d.yaml` for local development cluster defaults.
- Added deterministic smoke/unit/integration checks for chart structure and deployment script contract.
- Added `k3d` deployment helper for local cluster provisioning and chart install/upgrade.

## Migration Impact

- Platform deployment workflow now has a concrete path and validation gates.
- Future CI can reuse smoke/integration scripts as pre-deploy checks.
- Cloud promotion can build on the same chart by extending values files rather than creating a parallel manifest set.

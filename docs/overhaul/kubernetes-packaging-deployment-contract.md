# Kubernetes Packaging and Deployment Contract

Date: 2026-02-13  
Checklist ID: `T382`

## Chart and Values Contract

- Chart root: `deploy/helm/printnet`
  - `Chart.yaml`
  - `values.yaml`
  - `values-k3d.yaml`
- Required top-level values:
  - `namespace`
  - `backend`
  - `worker`
  - `frontend`
  - `redis`
  - `mongo`
  - `ingress`

## Resource Template Contract

- Namespace and platform wiring:
  - `templates/namespace.yaml`
  - `templates/_helpers.tpl`
- Backend:
  - `templates/backend-configmap.yaml`
  - `templates/backend-secret.yaml`
  - `templates/backend-deployment.yaml`
  - `templates/backend-service.yaml`
- Worker:
  - `templates/worker-deployment.yaml`
- Frontend:
  - `templates/frontend-deployment.yaml`
  - `templates/frontend-service.yaml`
- Data-plane:
  - `templates/redis-deployment.yaml`
  - `templates/redis-service.yaml`
  - `templates/mongo-statefulset.yaml`
  - `templates/mongo-service.yaml`
- Edge:
  - `templates/ingress.yaml`

## Script Contract

- Deploy helper:
  - `scripts/k3d-deploy.ps1`
- Smoke and test gates:
  - `scripts/run-kubernetes-packaging-smoke.ps1`
  - `scripts/test-kubernetes-packaging-unit.ps1`
  - `scripts/test-kubernetes-packaging-integration.ps1`

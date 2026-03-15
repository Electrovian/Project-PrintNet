# Kubernetes Packaging and Deployment Requirements

Date: 2026-02-13  
Checklist ID: `T381`

## Objective

Provide a reproducible Kubernetes packaging baseline for EON-OpenSlicer platform services (backend, worker, frontend, Redis, Mongo, ingress), with local-first deployment through `k3d`.

## Required Outcomes

- Add a Helm chart under `deploy/helm/printnet` with environment contracts and service wiring.
- Support `k3d` deployment path with explicit script automation.
- Include backend queue-worker environment knobs in deployment config.
- Add smoke/unit/integration automation for packaging integrity.
- Ensure chart validation works even when Helm is unavailable in the local environment.

## Acceptance Criteria

- Helm chart includes core resources for backend, worker, frontend, Redis, Mongo, and ingress.
- `k3d` deployment script supports cluster creation and `helm upgrade --install`.
- Smoke report confirms resource coverage and chart metadata contract.
- Unit and integration scripts pass within configured runtime budgets.
- Workstream docs (contract/errors/usage/migration/gate) are complete.

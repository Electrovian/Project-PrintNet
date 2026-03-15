# Kubernetes Deployment Assets

This directory contains Helm packaging for the EON-OpenSlicer platform stack.

## Chart

- Path: `deploy/helm/printnet`
- Includes:
  - backend
  - worker
  - frontend
  - redis
  - mongo
  - ingress

## Local k3d Deploy

```powershell
powershell -ExecutionPolicy Bypass -File scripts/k3d-deploy.ps1
```

## Validation

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-kubernetes-packaging-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-kubernetes-packaging-integration.ps1
```

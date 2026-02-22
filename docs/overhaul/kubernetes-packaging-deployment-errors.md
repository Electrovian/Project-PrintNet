# Kubernetes Packaging and Deployment Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T384`

## Script-Level Errors

- `TOOL_NOT_FOUND`
  - Trigger: required CLI (`k3d`, `helm`, or `kubectl`) missing for deployment script.

- `K3D_CREATE_FAILED`
  - Trigger: `k3d cluster create` returns non-zero exit code.

- `KUBECTL_NAMESPACE_APPLY_FAILED`
  - Trigger: namespace create/apply pipeline fails.

- `HELM_DEPLOY_FAILED`
  - Trigger: `helm upgrade --install` fails.

- `KUBERNETES_PACKAGING_SMOKE_COMMAND_FAILED`
  - Trigger: smoke harness Python command exits non-zero.

## Test/Validation Errors

- Unit gate failure:
  - Missing chart files, missing templates, or missing deployment scripts.

- Integration gate failure:
  - Smoke report `ok != true`
  - Required contract flags unresolved (`chart_name_ok`, kind checks, script command checks).

- Optional tool checks:
  - Helm may be unavailable locally; smoke gate uses static chart checks and treats Helm render as optional in that case.

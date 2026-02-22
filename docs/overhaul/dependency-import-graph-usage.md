# Dependency/Import Graph Usage and Defaults

Date: 2026-02-13
Checklist ID: `T028`

## Generator

```powershell
powershell -ExecutionPolicy Bypass -File scripts/generate-dependency-graph.ps1
```

## Parameters

- `-AppRoot` default: `App`
- `-OutputDir` default: `docs`

## Outputs

- `docs/_app_dependency_modules.txt`
- `docs/_app_dependency_graph.txt`

## Validation

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-dependency-graph.ps1
```

## Validation Defaults

- `-MaxSeconds` default: `20`

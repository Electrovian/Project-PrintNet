# Local Wi-Fi Onboarding Flow Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T328`

## Run Smoke

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-local-wifi-onboarding-smoke.ps1
```

## Run Unit and Integration Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-local-wifi-onboarding-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-local-wifi-onboarding-integration.ps1
```

## Defaults

- Target ports: `80`, `8080`, `7125`
- Probe paths:
  - `/api/version`
  - `/server/info`
- Request timeout: `1.25s`
- Max targets per run: `128`
- CIDR host limit: `64`
- Merge policy: keep first-seen identity and skip duplicates by connector URL identity.

# Frontend React UX Implementation Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T358`

## Run Smoke

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-frontend-react-ux-smoke.ps1
```

## Run Unit and Integration Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-frontend-react-ux-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-frontend-react-ux-integration.ps1
```

## Run Frontend Locally

```powershell
cd Website/frontend
npm install
npm run dev
```

## Defaults

- API base fallback: `http://127.0.0.1:8000/api/v1`
- Material default: `PLA`
- Color default: `Black`
- Infill default: `25%`
- Layer height default: `0.2 mm`
- Unit runtime budget: `20s`
- Integration runtime budget: `25s`

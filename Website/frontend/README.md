# Frontend React UX

React frontend scaffold for Project PrintNet web UX.

## Structure

- `src/App.jsx`: page composition and route switching.
- `src/components/`: UI building blocks.
- `src/state/usePrintNetState.js`: local state + backend submit orchestration.
- `src/api/backendClient.js`: backend API client contract.
- `src/contracts.js`: frontend payload validation and normalization.
- `tests/frontend_contracts.test.mjs`: contract-level unit checks.

## Local Commands

```powershell
cd Website/frontend
npm install
npm run dev
```

Contract tests:

```powershell
npm run test:contract
```

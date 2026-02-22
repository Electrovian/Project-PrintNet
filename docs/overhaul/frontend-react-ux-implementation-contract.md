# Frontend React UX Implementation Contract

Date: 2026-02-13  
Checklist ID: `T352`

## Core Modules

- `Website/frontend/src/main.jsx`
  - React bootstrap entrypoint.
- `Website/frontend/src/App.jsx`
  - route-aware page composition shell.
- `Website/frontend/src/config.js`
  - UX defaults and API base resolution.
- `Website/frontend/src/contracts.js`
  - request normalization and frontend validation errors.
- `Website/frontend/src/api/backendClient.js`
  - backend endpoint client wrapper.
- `Website/frontend/src/state/usePrintNetState.js`
  - local app state and send-job orchestration.
- `Website/frontend/src/components/*`
  - header, contact, upload, print options, queue, printer table.

## Route-State Contract

- Route keys:
  - `submit`
  - `queue`
  - `printers`
- Route switching is internal state-based and deterministic.

## API Contract

`buildBackendClient(...)` exposes:

- `healthLive()`
- `healthReady()`
- `createSession(payload)`
- `listProfiles(filters)`
- `registerPrinter(payload)`
- `submitJob(payload)`
- `getJobStatus(jobId)`
- `getJobEvents(jobId)`

## Defaults Contract

- Material default: `PLA`
- Color default: `Black`
- API default base: `http://127.0.0.1:8000/api/v1`

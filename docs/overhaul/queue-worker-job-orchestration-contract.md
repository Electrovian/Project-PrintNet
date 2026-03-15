# Queue Worker and Job Orchestration Contract

Date: 2026-02-13  
Checklist ID: `T372`

## Backend Modules

- `Website/backend/printnet_backend/orchestration.py`
  - `WorkerHeartbeat`
  - `WorkerCycleResult`
  - `InMemoryQueueOrchestrator`
- `Website/backend/printnet_backend/services.py`
  - `BackendState.queue_snapshot(...)`
  - `BackendState.record_worker_heartbeat(...)`
  - `BackendState.run_worker_tick(...)`
  - queued-job lifecycle transitions (`queued -> running -> completed`)
- `Website/backend/printnet_backend/routes/queue.py`
  - queue snapshot and worker orchestration endpoints
- `Website/backend/printnet_backend/errors.py`
  - `BackendOrchestrationError`

## Frontend Modules

- `Website/frontend/src/api/backendClient.js`
  - `getQueueSnapshot(...)`
  - `sendWorkerHeartbeat(...)`
  - `runWorkerTick(...)`
- `Website/frontend/src/state/usePrintNetState.js`
  - queue snapshot state and refresh action
- `Website/frontend/src/components/QueuePanel.jsx`
  - queue refresh trigger and multi-job rendering

## API Endpoint Contract

- `GET /queue/snapshot`
  - query: `auth_token`
  - role: any authenticated role
  - student visibility is ownership-filtered
- `POST /queue/worker/heartbeat`
  - body: `auth_token`, optional `worker_id`
  - role: `operator/admin`
- `POST /queue/worker/tick`
  - body: `auth_token`, optional `worker_id`, optional `max_jobs`
  - role: `operator/admin`

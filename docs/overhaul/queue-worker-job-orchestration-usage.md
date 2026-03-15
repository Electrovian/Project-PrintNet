# Queue Worker and Job Orchestration Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T378`

## Run Smoke

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-queue-worker-orchestration-smoke.ps1
```

## Run Unit and Integration Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-queue-worker-orchestration-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-queue-worker-orchestration-integration.ps1
```

## Defaults

- `BACKEND_QUEUE_WORKER_MAX_JOBS_PER_TICK`: `1`
- `BACKEND_QUEUE_WORKER_HEARTBEAT_TTL_SECONDS`: `60`
- Queue worker routes:
  - `/queue/snapshot`
  - `/queue/worker/heartbeat`
  - `/queue/worker/tick`
- Unit runtime budget: `30s`
- Integration runtime budget: `30s`
- Smoke report paths:
  - `docs/_queue_worker_orchestration_report.json`
  - `docs/_queue_worker_orchestration_summary.txt`

# Queue Worker and Job Orchestration Migration Notes

Date: 2026-02-13  
Checklist ID: `T379`

## Legacy Baseline

- Job submission created static queue metadata but no worker execution path.
- No queue snapshot or worker control endpoints existed.
- Queue UI only showed the last submitted job payload.

## Current Baseline

- Backend now tracks queue order and worker heartbeats.
- Operator/admin can run worker ticks to process queued jobs.
- Job lifecycle transitions and worker events are persisted in-memory.
- Queue snapshots are role-aware:
  - student: own jobs only
  - operator/admin: all jobs

## Migration Impact

- Clients may call `/queue/snapshot` for queue visibility instead of relying on local state only.
- Worker service simulations can use `/queue/worker/heartbeat` and `/queue/worker/tick`.
- Existing submit/status/events routes remain compatible.

# Container Runtime (Docker Compose)

This repository now includes first-party container definitions for:

- `backend` (`Website/backend/Dockerfile`)
- `worker` (`Website/backend/worker.py`, using backend image)
- `frontend` (`Website/frontend/Dockerfile`)
- `redis` (`redis:8.2-alpine`)
- `mongo` (`mongo:8.2`)

## Start Stack

```powershell
docker compose up --build -d
```

## Check Status

```powershell
docker compose ps
docker compose logs --tail=100 backend worker frontend
```

## Endpoints

- Frontend: `http://localhost:8080`
- Backend API: `http://localhost:8000/api/v1/health/live`

## Stop Stack

```powershell
docker compose down
```

To also remove local Mongo data:

```powershell
docker compose down -v
```

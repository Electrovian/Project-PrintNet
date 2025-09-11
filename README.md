# Project PrintNet (Starter)

This bundle includes the starter backend (Spring Boot + Kotlin), worker service (Kotlin), infra docker-compose, and VS Code configs.

## Run

**Infra**
```bash
docker compose -f infra/docker-compose.dev.yml up
```

**Backend**
```bash
cd backend
./gradlew bootRun
# health check: http://localhost:8080/api/health
```

**Worker**
```bash
cd worker
./gradlew run
```

**Frontend**
Create a Vite React app in the `frontend/` folder:
```bash
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
npm run dev
```
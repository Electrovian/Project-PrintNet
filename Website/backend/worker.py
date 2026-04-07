from __future__ import annotations

import os
import socket
import time
from typing import Any

import httpx


def _env_text(name: str, default: str) -> str:
    value = str(os.environ.get(name, default)).strip()
    return value or default


def _env_float(name: str, default: float, minimum: float) -> float:
    raw = str(os.environ.get(name, str(default))).strip()
    try:
        value = float(raw)
    except Exception:
        value = float(default)
    return max(value, minimum)


def _env_int_optional(name: str) -> int | None:
    raw = str(os.environ.get(name, "")).strip()
    if not raw:
        return None
    try:
        value = int(raw)
    except Exception:
        return None
    return max(1, value)


BACKEND_BASE_URL = _env_text("BACKEND_BASE_URL", "http://backend:8000").rstrip("/")
API_PREFIX = _env_text("BACKEND_API_PREFIX", "/api/v1")
if not API_PREFIX.startswith("/"):
    API_PREFIX = "/" + API_PREFIX
API_PREFIX = API_PREFIX.rstrip("/")

WORKER_ROLE = _env_text("WORKER_ROLE", "operator")
WORKER_USER_ID = _env_text("WORKER_USER_ID", f"worker-{socket.gethostname()}")
WORKER_ID = _env_text("WORKER_ID", WORKER_USER_ID)
WORKER_POLL_SECONDS = _env_float("WORKER_POLL_SECONDS", default=2.0, minimum=0.25)
WORKER_MAX_JOBS_PER_TICK = _env_int_optional("WORKER_MAX_JOBS_PER_TICK")
WORKER_MAX_CYCLES = _env_int_optional("WORKER_MAX_CYCLES")
HTTP_TIMEOUT_SECONDS = _env_float("WORKER_HTTP_TIMEOUT_SECONDS", default=10.0, minimum=1.0)


def _url(path: str) -> str:
    suffix = str(path or "").strip()
    if not suffix.startswith("/"):
        suffix = "/" + suffix
    return f"{BACKEND_BASE_URL}{API_PREFIX}{suffix}"


def _create_session(client: httpx.Client) -> str:
    payload = {"user_id": WORKER_USER_ID, "role": WORKER_ROLE}
    response = client.post(_url("/auth/session"), json=payload)
    response.raise_for_status()
    body: dict[str, Any] = response.json()
    session = body.get("session", {})
    token = str(session.get("token", "")).strip()
    if not token:
        raise RuntimeError("worker session token missing from backend auth response")
    return token


def _run_cycle(client: httpx.Client, token: str) -> None:
    heartbeat_payload: dict[str, Any] = {
        "auth_token": token,
        "worker_id": WORKER_ID,
    }
    heartbeat = client.post(_url("/queue/worker/heartbeat"), json=heartbeat_payload)
    heartbeat.raise_for_status()

    tick_payload: dict[str, Any] = dict(heartbeat_payload)
    if WORKER_MAX_JOBS_PER_TICK is not None:
        tick_payload["max_jobs"] = WORKER_MAX_JOBS_PER_TICK
    tick = client.post(_url("/queue/worker/tick"), json=tick_payload)
    tick.raise_for_status()

    tick_body: dict[str, Any] = tick.json()
    cycle = tick_body.get("cycle", {})
    processed = cycle.get("processed_job_ids", [])
    print(
        f"worker cycle ok worker_id={WORKER_ID} processed={len(processed)} queue_after={cycle.get('queue_depth_after')}",
        flush=True,
    )


def main() -> None:
    token = ""
    completed_cycles = 0
    print(f"worker starting base_url={BACKEND_BASE_URL}{API_PREFIX} worker_id={WORKER_ID}", flush=True)
    with httpx.Client(timeout=HTTP_TIMEOUT_SECONDS) as client:
        while True:
            try:
                if not token:
                    token = _create_session(client)
                    print("worker auth session created", flush=True)
                _run_cycle(client, token)
                completed_cycles += 1
                if WORKER_MAX_CYCLES is not None and completed_cycles >= WORKER_MAX_CYCLES:
                    print(f"worker smoke complete cycles={completed_cycles}", flush=True)
                    break
            except Exception as exc:
                token = ""
                print(f"worker cycle failed: {exc}", flush=True)
            time.sleep(WORKER_POLL_SECONDS)


if __name__ == "__main__":
    main()

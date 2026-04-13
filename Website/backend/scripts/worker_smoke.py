from __future__ import annotations

import argparse
import json
import os
import socket
import subprocess
import sys
import time
from contextlib import closing
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen


BACKEND_DIR = Path(__file__).resolve().parents[1]
SMOKE_WORKER_ID = "worker-smoke"


def _wait_for_health(url: str, timeout_seconds: float) -> dict:
    deadline = time.monotonic() + max(1.0, float(timeout_seconds))
    last_error: str = ""
    request = Request(url, headers={"Cache-Control": "no-store"})
    while time.monotonic() < deadline:
        try:
            with urlopen(request, timeout=5) as response:
                payload = json.loads(response.read().decode("utf-8", "replace"))
                if response.status == 200 and isinstance(payload, dict) and payload.get("ok"):
                    return payload
        except (URLError, TimeoutError, ValueError, OSError, json.JSONDecodeError) as exc:
            last_error = str(exc)
        time.sleep(0.5)
    raise RuntimeError(f"Backend health probe failed: {last_error or 'timeout'}")


def _reserve_port() -> int:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _launch_backend(port: int) -> subprocess.Popen[str]:
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    env["BACKEND_OPERATOR_USER_IDS"] = SMOKE_WORKER_ID
    return subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", str(port)],
        cwd=str(BACKEND_DIR),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def _launch_worker(max_cycles: int, port: int) -> subprocess.Popen[str]:
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    env["BACKEND_BASE_URL"] = f"http://127.0.0.1:{port}"
    env["WORKER_ROLE"] = "operator"
    env["WORKER_USER_ID"] = SMOKE_WORKER_ID
    env["WORKER_ID"] = SMOKE_WORKER_ID
    env["WORKER_POLL_SECONDS"] = "0.25"
    env["WORKER_HTTP_TIMEOUT_SECONDS"] = "5"
    env["WORKER_MAX_CYCLES"] = str(max(1, int(max_cycles)))
    return subprocess.Popen(
        [sys.executable, "worker.py"],
        cwd=str(BACKEND_DIR),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def _collect_output(proc: subprocess.Popen[str]) -> str:
    try:
        out, _ = proc.communicate(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        out, _ = proc.communicate(timeout=5)
    return out or ""


def run_smoke(*, backend_timeout: float, worker_timeout: float, worker_cycles: int) -> None:
    port = _reserve_port()
    backend = _launch_backend(port)
    backend_output = ""
    worker_output = ""
    try:
        _wait_for_health(f"http://127.0.0.1:{port}/api/v1/health/live", backend_timeout)
        worker = _launch_worker(worker_cycles, port)
        try:
            worker_output = worker.communicate(timeout=max(5.0, float(worker_timeout)))[0] or ""
        except subprocess.TimeoutExpired:
            worker.kill()
            worker_output = worker.communicate(timeout=5)[0] or ""

        if "worker starting" not in worker_output:
            raise RuntimeError(f"worker startup output missing:\n{worker_output}")
        if "worker auth session created" not in worker_output:
            raise RuntimeError(f"worker auth handshake missing:\n{worker_output}")
        if "worker cycle ok" not in worker_output:
            raise RuntimeError(f"worker cycle output missing:\n{worker_output}")
        if f"worker smoke complete cycles={max(1, int(worker_cycles))}" not in worker_output:
            raise RuntimeError(f"worker completion marker missing:\n{worker_output}")
    finally:
        if backend.poll() is None:
            backend.terminate()
            try:
                backend.wait(timeout=5)
            except subprocess.TimeoutExpired:
                backend.kill()
                backend.wait(timeout=5)
        backend_output = _collect_output(backend)

    print(worker_output.rstrip(), flush=True)
    if backend_output.strip():
        print(backend_output.rstrip(), flush=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a short backend + worker smoke.")
    parser.add_argument("--backend-timeout", type=float, default=45.0)
    parser.add_argument("--worker-timeout", type=float, default=30.0)
    parser.add_argument("--worker-cycles", type=int, default=1)
    args = parser.parse_args(argv)
    run_smoke(
        backend_timeout=args.backend_timeout,
        worker_timeout=args.worker_timeout,
        worker_cycles=args.worker_cycles,
    )
    print("worker smoke ok", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

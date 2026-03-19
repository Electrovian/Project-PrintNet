from __future__ import annotations

from printnet_backend import create_app
from printnet_backend.compat import HAS_FASTAPI

app = create_app()


def main() -> int:
    if not HAS_FASTAPI:
        print(
            "FastAPI/uvicorn are not installed. Install backend dependencies to run the HTTP server."
        )
        print("You can still run backend unit/integration automation with the compatibility layer.")
        return 0

    try:
        import uvicorn  # type: ignore
    except Exception:
        print("uvicorn is missing. Install uvicorn to run the backend server.")
        return 1

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

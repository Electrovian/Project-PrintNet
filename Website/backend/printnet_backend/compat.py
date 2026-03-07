from __future__ import annotations

from dataclasses import dataclass
import inspect
from typing import Any, Callable, Mapping
from urllib.parse import parse_qs, urlparse

HAS_FASTAPI = False
_FastApiTestClient: Any | None = None

try:
    from fastapi import APIRouter, FastAPI, HTTPException  # type: ignore
    from fastapi.responses import JSONResponse  # type: ignore
    from fastapi.testclient import TestClient as _FastApiTestClient  # type: ignore

    HAS_FASTAPI = True
except Exception:  # pragma: no cover - fallback path

    class HTTPException(Exception):
        def __init__(self, status_code: int, detail: str):
            super().__init__(str(detail))
            self.status_code = int(status_code)
            self.detail = str(detail)

    class JSONResponse:
        def __init__(self, content: Mapping[str, Any] | list[Any] | str | int | float | None, status_code: int = 200):
            self.content = content
            self.status_code = int(status_code)

    @dataclass(frozen=True)
    class _Route:
        method: str
        path: str
        endpoint: Callable[..., Any]

    class APIRouter:
        def __init__(self):
            self._routes: list[_Route] = []

        @property
        def routes(self) -> tuple[_Route, ...]:
            return tuple(self._routes)

        def add_api_route(self, path: str, endpoint: Callable[..., Any], methods: list[str] | tuple[str, ...]):
            for method in methods:
                self._routes.append(_Route(method=str(method).upper(), path=_normalize_path(path), endpoint=endpoint))

        def get(self, path: str):
            return self._decorate(path, ("GET",))

        def post(self, path: str):
            return self._decorate(path, ("POST",))

        def put(self, path: str):
            return self._decorate(path, ("PUT",))

        def delete(self, path: str):
            return self._decorate(path, ("DELETE",))

        def patch(self, path: str):
            return self._decorate(path, ("PATCH",))

        def _decorate(self, path: str, methods: tuple[str, ...]):
            def decorator(fn: Callable[..., Any]):
                self.add_api_route(path, fn, methods=methods)
                return fn

            return decorator

    class FastAPI:
        def __init__(self, *, title: str = "Backend", version: str = "0.1.0", **_kwargs: Any):
            self.title = str(title)
            self.version = str(version)
            self._routes: list[_Route] = []
            self._handlers: dict[type[BaseException], Callable[..., Any]] = {}

        @property
        def routes(self) -> tuple[_Route, ...]:
            return tuple(self._routes)

        def add_exception_handler(self, exc_type: type[BaseException], handler: Callable[..., Any]) -> None:
            self._handlers[exc_type] = handler

        def include_router(self, router: APIRouter, *, prefix: str = "") -> None:
            base = _normalize_path(prefix)
            for route in router.routes:
                merged = _normalize_path(base + route.path)
                self._routes.append(_Route(method=route.method, path=merged, endpoint=route.endpoint))

        def get(self, path: str):
            return self._decorate(path, ("GET",))

        def post(self, path: str):
            return self._decorate(path, ("POST",))

        def _decorate(self, path: str, methods: tuple[str, ...]):
            def decorator(fn: Callable[..., Any]):
                normalized = _normalize_path(path)
                for method in methods:
                    self._routes.append(_Route(method=str(method).upper(), path=normalized, endpoint=fn))
                return fn

            return decorator

        def _dispatch(
            self,
            method: str,
            url_path: str,
            payload: Mapping[str, Any] | None = None,
            headers: Mapping[str, str] | None = None,
        ):
            parsed = urlparse(url_path)
            path = _normalize_path(parsed.path)
            query_pairs = parse_qs(parsed.query, keep_blank_values=True)
            query: dict[str, str] = {}
            for key, values in query_pairs.items():
                query[str(key)] = str(values[0]) if values else ""
            for route in self._routes:
                if route.method != str(method).upper():
                    continue
                if route.path != path:
                    continue
                try:
                    kwargs = _build_call_kwargs(route.endpoint, query, payload, headers=headers)
                    result = route.endpoint(**kwargs)
                    if isinstance(result, JSONResponse):
                        return _SimpleResponse(result.status_code, result.content)
                    return _SimpleResponse(200, result)
                except HTTPException as exc:
                    return _SimpleResponse(int(exc.status_code), {"detail": str(exc.detail)})
                except Exception as exc:  # pragma: no cover - fallback handler path
                    for exc_type, handler in self._handlers.items():
                        if isinstance(exc, exc_type):
                            handled = _invoke_exception_handler(handler, exc)
                            if isinstance(handled, JSONResponse):
                                return _SimpleResponse(handled.status_code, handled.content)
                            return _SimpleResponse(500, {"detail": str(handled)})
                    return _SimpleResponse(500, {"detail": str(exc)})
            return _SimpleResponse(404, {"detail": "Not Found"})

    class _SimpleResponse:
        def __init__(self, status_code: int, payload: Any):
            self.status_code = int(status_code)
            self._payload = payload

        def json(self):
            return self._payload

    class _SimpleRequest:
        def __init__(self, headers: Mapping[str, str] | None = None):
            self.headers = dict(headers or {})

    class _SimpleTestClient:
        def __init__(self, app: FastAPI):
            self._app = app

        def get(self, path: str, headers: Mapping[str, str] | None = None):
            return self._app._dispatch("GET", path, payload=None, headers=headers)

        def post(
            self,
            path: str,
            json: Mapping[str, Any] | None = None,
            headers: Mapping[str, str] | None = None,
        ):
            return self._app._dispatch("POST", path, payload=json, headers=headers)

        def put(
            self,
            path: str,
            json: Mapping[str, Any] | None = None,
            headers: Mapping[str, str] | None = None,
        ):
            return self._app._dispatch("PUT", path, payload=json, headers=headers)

        def patch(
            self,
            path: str,
            json: Mapping[str, Any] | None = None,
            headers: Mapping[str, str] | None = None,
        ):
            return self._app._dispatch("PATCH", path, payload=json, headers=headers)

        def delete(self, path: str, headers: Mapping[str, str] | None = None):
            return self._app._dispatch("DELETE", path, payload=None, headers=headers)


def create_test_client(app):
    if HAS_FASTAPI and _FastApiTestClient is not None:
        return _FastApiTestClient(app)
    return _SimpleTestClient(app)


def _normalize_path(path: str) -> str:
    value = str(path or "").strip()
    if not value:
        return "/"
    if not value.startswith("/"):
        value = "/" + value
    while len(value) > 1 and value.endswith("/"):
        value = value[:-1]
    return value


def _build_call_kwargs(
    endpoint: Callable[..., Any],
    query: Mapping[str, str],
    payload: Mapping[str, Any] | None,
    headers: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    sig = inspect.signature(endpoint)
    kwargs: dict[str, Any] = {}
    for name, parameter in sig.parameters.items():
        if name == "request":
            kwargs[name] = _SimpleRequest(headers=headers)
            continue
        if name == "payload":
            kwargs[name] = dict(payload or {})
            continue
        if name in query:
            kwargs[name] = query[name]
            continue
        if parameter.default is inspect.Parameter.empty:
            kwargs[name] = None
    return kwargs


def _invoke_exception_handler(handler: Callable[..., Any], exc: Exception):
    sig = inspect.signature(handler)
    arg_count = len(sig.parameters)
    if arg_count <= 1:
        return handler(exc)
    return handler(None, exc)

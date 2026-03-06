from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

import requests


class WebBackendActivityError(RuntimeError):
    """Raised when the web backend activity API cannot be read safely."""


@dataclass
class WebBackendActivityClient:
    base_url: str
    actor_user: str = "desktop-operator"
    actor_role: str = "operator"
    timeout_seconds: float = 4.0
    _session_token: str = field(default="", init=False, repr=False)

    def __post_init__(self) -> None:
        base = str(self.base_url or "").strip().rstrip("/")
        if not base:
            raise WebBackendActivityError("ACTIVITY_BACKEND_URL_REQUIRED: base_url is required.")
        self.base_url = base

        user = str(self.actor_user or "").strip()
        self.actor_user = user or "desktop-operator"

        role = str(self.actor_role or "").strip().lower()
        self.actor_role = role or "operator"

        try:
            timeout = float(self.timeout_seconds)
        except (TypeError, ValueError):
            timeout = 4.0
        self.timeout_seconds = min(30.0, max(1.0, timeout))

    def fetch_queue_snapshot(self) -> dict[str, Any]:
        token = self._ensure_session_token()
        try:
            payload = self._request(
                "GET",
                "/queue/snapshot",
                params={"auth_token": token},
            )
        except WebBackendActivityError as exc:
            message = str(exc)
            if "AUTH_TOKEN_INVALID" in message or "AUTH_TOKEN_REQUIRED" in message:
                token = self._ensure_session_token(force_refresh=True)
                payload = self._request(
                    "GET",
                    "/queue/snapshot",
                    params={"auth_token": token},
                )
            else:
                raise

        snapshot = payload.get("snapshot")
        if not isinstance(snapshot, Mapping):
            raise WebBackendActivityError("ACTIVITY_QUEUE_SNAPSHOT_INVALID: missing snapshot payload.")
        return dict(snapshot)

    def _ensure_session_token(self, force_refresh: bool = False) -> str:
        if self._session_token and not force_refresh:
            return self._session_token
        payload = self._request(
            "POST",
            "/auth/session",
            json_payload={
                "user_id": self.actor_user,
                "role": self.actor_role,
            },
        )
        session = payload.get("session")
        if not isinstance(session, Mapping):
            raise WebBackendActivityError("ACTIVITY_SESSION_INVALID: missing session payload.")
        token = str(session.get("token", "")).strip()
        if not token:
            raise WebBackendActivityError("ACTIVITY_SESSION_TOKEN_INVALID: missing session token.")
        self._session_token = token
        return token

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, str] | None = None,
        json_payload: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        url = self._build_url(path)
        try:
            response = requests.request(
                method=method,
                url=url,
                params=dict(params or {}),
                json=dict(json_payload or {}),
                timeout=self.timeout_seconds,
            )
        except requests.RequestException as exc:
            raise WebBackendActivityError(f"ACTIVITY_BACKEND_UNREACHABLE: {exc}") from exc

        payload: Any
        try:
            payload = response.json()
        except ValueError:
            payload = {}

        if not response.ok:
            detail = _extract_error_detail(payload) or response.text or f"HTTP {response.status_code}"
            raise WebBackendActivityError(detail)

        if not isinstance(payload, Mapping):
            raise WebBackendActivityError("ACTIVITY_BACKEND_RESPONSE_INVALID: expected JSON object payload.")

        ok_value = payload.get("ok")
        if ok_value is not None and not bool(ok_value):
            detail = _extract_error_detail(payload) or "ACTIVITY_BACKEND_ERROR: backend returned ok=false."
            raise WebBackendActivityError(detail)
        return dict(payload)

    def _build_url(self, path: str) -> str:
        suffix = str(path or "").strip()
        if not suffix.startswith("/"):
            suffix = "/" + suffix
        return f"{self.base_url}{suffix}"


def _extract_error_detail(payload: object) -> str:
    if not isinstance(payload, Mapping):
        return ""
    err = payload.get("error")
    if isinstance(err, Mapping):
        detail = str(err.get("detail", "")).strip()
        if detail:
            return detail
        code = str(err.get("code", "")).strip()
        if code:
            return code
    detail = str(payload.get("detail", "")).strip()
    if detail:
        return detail
    return ""

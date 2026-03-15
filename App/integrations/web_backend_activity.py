from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

import requests


class WebBackendActivityError(RuntimeError):
    """Raised when the web backend activity API cannot be read safely."""


@dataclass
class WebBackendActivityClient:
    base_url: str
    service_token: str = ""
    timeout_seconds: float = 4.0
    _session: requests.Session = field(default_factory=requests.Session, init=False, repr=False)

    def __post_init__(self) -> None:
        base = str(self.base_url or "").strip().rstrip("/")
        if not base:
            raise WebBackendActivityError("ACTIVITY_BACKEND_URL_REQUIRED: base_url is required.")
        self.base_url = base

        token = str(self.service_token or "").strip()
        if not token:
            raise WebBackendActivityError("ACTIVITY_SERVICE_TOKEN_REQUIRED: service_token is required.")
        self.service_token = token

        try:
            timeout = float(self.timeout_seconds)
        except (TypeError, ValueError):
            timeout = 4.0
        self.timeout_seconds = min(30.0, max(1.0, timeout))

    def fetch_queue_snapshot(self) -> dict[str, Any]:
        payload = self._request("GET", "/queue/snapshot")
        snapshot = payload.get("snapshot")
        if not isinstance(snapshot, Mapping):
            raise WebBackendActivityError("ACTIVITY_QUEUE_SNAPSHOT_INVALID: missing snapshot payload.")
        return dict(snapshot)

    def fetch_compliance_region(self) -> dict[str, Any]:
        payload = self._request("GET", "/compliance/region")
        compliance = payload.get("compliance")
        if not isinstance(compliance, Mapping):
            raise WebBackendActivityError("ACTIVITY_COMPLIANCE_INVALID: missing compliance payload.")
        return dict(compliance)

    def fetch_activity_feed(self, *, cursor: int = 0, limit: int = 200) -> dict[str, Any]:
        payload = self._request(
            "GET",
            "/activity/feed",
            params={
                "cursor": str(max(0, int(cursor))),
                "limit": str(max(1, min(1000, int(limit)))),
            },
        )
        feed = payload.get("feed")
        if not isinstance(feed, Mapping):
            raise WebBackendActivityError("ACTIVITY_FEED_INVALID: missing feed payload.")
        return dict(feed)

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, str] | None = None,
        json_payload: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        url = self._build_url(path)
        headers = {"x-activity-service-token": self.service_token}
        try:
            response = self._session.request(
                method=method,
                url=url,
                params=dict(params or {}),
                json=dict(json_payload or {}),
                headers=headers,
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

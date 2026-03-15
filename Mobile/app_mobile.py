from __future__ import annotations

import json
from typing import Any, List, Optional, Tuple

import toga
from toga.style import Pack


class MobileBackend:
    def __init__(self, base_url: str, api_token: str = "") -> None:
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token.strip()

    def _request(
        self,
        method: str,
        path: str,
        payload: Optional[dict] = None,
        query: Optional[dict] = None,
    ) -> Tuple[Optional[Any], Optional[str]]:
        try:
            import requests
        except Exception as exc:
            return None, f"requests unavailable: {exc}"

        url = f"{self.base_url}/{path.lstrip('/')}"
        body = dict(payload or {})
        params = dict(query or {})
        if self.api_token:
            if method.strip().upper() == "GET":
                params.setdefault("auth_token", self.api_token)
            else:
                body.setdefault("auth_token", self.api_token)
        try:
            resp = requests.request(method, url, json=body or None, params=params or None, timeout=10)
        except Exception as exc:
            return None, str(exc)
        if not resp.ok:
            return None, f"{resp.status_code} {resp.reason}"
        if not resp.text:
            return {}, None
        try:
            return resp.json(), None
        except json.JSONDecodeError:
            return resp.text, None

    def fetch_summary(self) -> Tuple[Optional[dict], Optional[str]]:
        data, err = self._request("GET", "/api/v1/queue/snapshot")
        if not isinstance(data, dict):
            return None, err or "Invalid summary response"
        snapshot = data.get("snapshot")
        if not isinstance(snapshot, dict):
            return None, "Invalid queue snapshot payload"
        queued = int(snapshot.get("queue_depth", 0) or 0)
        total = int(snapshot.get("job_count", 0) or 0)
        jobs = snapshot.get("jobs", [])
        return {
            "status": f"Connected | queued: {queued} | jobs: {total}",
            "jobs": jobs if isinstance(jobs, list) else [],
        }, None

    def job_action(self, job_id: str, action: str) -> Tuple[bool, str]:
        key = str(job_id or "").strip()
        if not key:
            return False, "Missing job ID."
        status_data, status_err = self._request("GET", "/api/v1/jobs/status", query={"job_id": key})
        if status_err:
            return False, status_err
        if not isinstance(status_data, dict):
            return False, "Invalid status response."
        job_payload = status_data.get("job")
        if not isinstance(job_payload, dict):
            return False, "Job not found."
        events_data, events_err = self._request("GET", "/api/v1/jobs/events", query={"job_id": key})
        if events_err:
            return False, events_err
        latest_event = ""
        if isinstance(events_data, dict):
            events = events_data.get("events", [])
            if isinstance(events, list) and events:
                latest_event = str(events[-1])
        current_status = str(job_payload.get("status", "unknown")).strip() or "unknown"
        verb = str(action or "status").strip().lower() or "status"
        message = f"{verb.title()} check: {current_status}"
        if latest_event:
            message = f"{message} | latest event: {latest_event}"
        return True, message


class MobileApp(toga.App):
    def startup(self) -> None:
        self.backend: Optional[MobileBackend] = None
        self.status_label = toga.Label("Disconnected", style=Pack(padding=(0, 0, 8, 0)))

        self.server_input = toga.TextInput(placeholder="https://printlab.example.edu",
                                           style=Pack(flex=1))
        self.token_input = toga.PasswordInput(placeholder="API token (optional)",
                                              style=Pack(flex=1, padding_top=6))

        connect_btn = toga.Button("Connect", on_press=self.connect, style=Pack(padding_left=8))
        refresh_btn = toga.Button("Refresh", on_press=self.refresh, style=Pack(padding_left=8))

        controls_row = toga.Box(style=Pack(direction="row", padding=(0, 0, 8, 0)))
        controls_row.add(self.server_input)
        controls_row.add(connect_btn)
        controls_row.add(refresh_btn)

        self.jobs_table = toga.Table(
            headings=["Job ID", "Name", "Status"],
            data=[],
            style=Pack(flex=1, padding_top=8),
        )

        self.job_id_input = toga.TextInput(placeholder="Job ID",
                                           style=Pack(flex=1))
        pause_btn = toga.Button("Pause", on_press=self.pause_job, style=Pack(padding_left=6))
        resume_btn = toga.Button("Resume", on_press=self.resume_job, style=Pack(padding_left=6))
        cancel_btn = toga.Button("Cancel", on_press=self.cancel_job, style=Pack(padding_left=6))

        job_row = toga.Box(style=Pack(direction="row", padding_top=8))
        job_row.add(self.job_id_input)
        job_row.add(pause_btn)
        job_row.add(resume_btn)
        job_row.add(cancel_btn)

        content = toga.Box(style=Pack(direction="column", padding=12))
        content.add(self.status_label)
        content.add(controls_row)
        content.add(self.token_input)
        content.add(self.jobs_table)
        content.add(job_row)

        main_window = toga.MainWindow(title=self.formal_name)
        main_window.content = content
        main_window.show()
        self.main_window = main_window

    def _set_status(self, message: str) -> None:
        self.status_label.text = message

    def connect(self, widget) -> None:
        url = (self.server_input.value or "").strip()
        if not url:
            self._set_status("Enter a server URL.")
            return
        token = (self.token_input.value or "").strip()
        self.backend = MobileBackend(url, token)
        self._set_status(f"Connected to {url}.")
        self.refresh(widget)

    def refresh(self, widget) -> None:
        if self.backend is None:
            self._set_status("Not connected.")
            self.jobs_table.data = []
            return
        data, err = self.backend.fetch_summary()
        if err:
            self._set_status(f"Refresh failed: {err}")
            return
        status = str(data.get("status", "Connected")) if data else "Connected"
        self._set_status(status)
        jobs = data.get("jobs", []) if data else []
        rows: List[List[str]] = []
        for job in jobs:
            if not isinstance(job, dict):
                continue
            rows.append([
                str(job.get("job_id", "")),
                str(job.get("model_name", "")),
                str(job.get("status", "")),
            ])
        self.jobs_table.data = rows

    def _job_action(self, action: str) -> None:
        if self.backend is None:
            self._set_status("Not connected.")
            return
        job_id = (self.job_id_input.value or "").strip()
        if not job_id:
            self._set_status("Enter a job ID.")
            return
        ok, msg = self.backend.job_action(job_id, action)
        if ok:
            self._set_status(msg)
            self.refresh(None)
        else:
            self._set_status(msg)

    def pause_job(self, widget) -> None:
        self._job_action("pause")

    def resume_job(self, widget) -> None:
        self._job_action("resume")

    def cancel_job(self, widget) -> None:
        self._job_action("cancel")


def main() -> MobileApp:
    return MobileApp("EON-OpenSlicer Mobile", "edu.uc.eon.openslicer.mobile")

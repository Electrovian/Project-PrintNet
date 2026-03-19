from __future__ import annotations

from dataclasses import dataclass
import ipaddress
import json
from typing import Any, Callable, Mapping, Sequence

import requests

from .errors import LocalWifiOnboardingError


ProbeHook = Callable[["LocalWifiProbeTarget", float], Mapping[str, Any]]

DEFAULT_SCAN_PORTS: tuple[int, ...] = (80, 8080, 7125, 9999)
DEFAULT_SCAN_PATHS: tuple[str, ...] = ("/api/version", "/server/info", "/api/v1/status", "/api/printer")
DEFAULT_TIMEOUT_S = 1.25
DEFAULT_MAX_TARGETS = 128
DEFAULT_CIDR_HOST_LIMIT = 64


@dataclass(frozen=True)
class LocalWifiProbeTarget:
    host: str
    port: int
    path: str
    url: str


class LocalWifiOnboarding:
    """Local Wi-Fi discovery and onboarding helper for supported printer protocols."""

    def __init__(
        self,
        *,
        timeout_s: float = DEFAULT_TIMEOUT_S,
        max_targets: int = DEFAULT_MAX_TARGETS,
        session: requests.Session | None = None,
        probe_hook: ProbeHook | None = None,
    ):
        self._timeout_s = float(timeout_s)
        self._max_targets = int(max_targets)
        self._session = session if session is not None else requests.Session()
        self._probe_hook = probe_hook
        if self._timeout_s <= 0.0:
            raise LocalWifiOnboardingError("WIFI_TIMEOUT_INVALID: timeout_s must be > 0.")
        if self._max_targets <= 0:
            raise LocalWifiOnboardingError("WIFI_MAX_TARGETS_INVALID: max_targets must be > 0.")

    def discover(
        self,
        *,
        hosts: Sequence[str] | None,
        ports: Sequence[int] | None = None,
        timeout_s: float | None = None,
        max_targets: int | None = None,
    ) -> dict[str, Any]:
        timeout_value = self._normalize_timeout(timeout_s)
        limit = self._normalize_max_targets(max_targets)
        normalized_hosts = self._normalize_hosts(hosts)
        normalized_ports = self._normalize_ports(ports)
        targets, truncated = self._build_targets(
            hosts=normalized_hosts,
            ports=normalized_ports,
            max_targets=limit,
        )

        warnings: list[str] = []
        if truncated:
            warnings.append("WIFI_TARGET_TRUNCATED: target count limited by max_targets.")

        online_target_count = 0
        printers: list[dict[str, Any]] = []
        seen: dict[str, int] = {}

        for target in targets:
            probe_result = self._run_probe(target, timeout_value)
            ok = bool(probe_result.get("ok", False))
            if not ok:
                continue
            connector_type = str(probe_result.get("connector_type", "")).strip().lower()
            if not connector_type:
                continue
            online_target_count += 1
            candidate = self._candidate_from_probe(target, connector_type, probe_result)
            identity = self._discovery_identity(candidate)
            existing_index = seen.get(identity)
            if existing_index is not None:
                existing = printers[existing_index]
                if self._prefer_discovered_candidate(existing, candidate):
                    printers[existing_index] = candidate
                continue
            seen[identity] = len(printers)
            printers.append(candidate)

        printers.sort(key=lambda item: str(item.get("name", "")).lower())
        return {
            "ok": True,
            "scanned_target_count": len(targets),
            "online_target_count": int(online_target_count),
            "printer_count": len(printers),
            "printers": printers,
            "warnings": warnings,
            "config": {
                "host_count": len(normalized_hosts),
                "ports": list(normalized_ports),
                "timeout_s": float(timeout_value),
                "max_targets": int(limit),
            },
        }

    def discover_from_cidr(
        self,
        cidr: str,
        *,
        ports: Sequence[int] | None = None,
        host_limit: int = DEFAULT_CIDR_HOST_LIMIT,
        timeout_s: float | None = None,
        max_targets: int | None = None,
    ) -> dict[str, Any]:
        normalized_cidr = str(cidr or "").strip()
        if not normalized_cidr:
            raise LocalWifiOnboardingError("WIFI_CIDR_REQUIRED: cidr is required.")

        limit = int(host_limit)
        if limit <= 0:
            raise LocalWifiOnboardingError("WIFI_HOST_LIMIT_INVALID: host_limit must be > 0.")

        try:
            network = ipaddress.ip_network(normalized_cidr, strict=False)
        except ValueError as exc:
            raise LocalWifiOnboardingError(f"WIFI_CIDR_INVALID: {normalized_cidr}") from exc

        hosts: list[str] = []
        for host in network.hosts():
            if len(hosts) >= limit:
                break
            hosts.append(str(host))

        if not hosts:
            raise LocalWifiOnboardingError("WIFI_CIDR_NO_HOSTS: cidr has no host addresses.")

        result = self.discover(
            hosts=hosts,
            ports=ports,
            timeout_s=timeout_s,
            max_targets=max_targets,
        )
        result["cidr"] = normalized_cidr
        result["cidr_host_limit"] = int(limit)
        result["cidr_host_count"] = len(hosts)
        return result

    def merge_printers(
        self,
        existing_printers: Sequence[Mapping[str, Any]] | None,
        discovered_printers: Sequence[Mapping[str, Any]] | None,
    ) -> list[dict[str, Any]]:
        merged: list[dict[str, Any]] = []
        seen: set[str] = set()

        for row in existing_printers or []:
            if not isinstance(row, Mapping):
                continue
            item = dict(row)
            identity = self._printer_identity(item)
            if identity in seen:
                continue
            seen.add(identity)
            merged.append(item)

        for row in discovered_printers or []:
            if not isinstance(row, Mapping):
                continue
            item = dict(row)
            identity = self._printer_identity(item)
            if identity in seen:
                continue
            seen.add(identity)
            merged.append(item)

        return merged

    def _normalize_timeout(self, timeout_s: float | None) -> float:
        value = self._timeout_s if timeout_s is None else float(timeout_s)
        if value <= 0.0:
            raise LocalWifiOnboardingError("WIFI_TIMEOUT_INVALID: timeout_s must be > 0.")
        return value

    def _normalize_max_targets(self, max_targets: int | None) -> int:
        value = self._max_targets if max_targets is None else int(max_targets)
        if value <= 0:
            raise LocalWifiOnboardingError("WIFI_MAX_TARGETS_INVALID: max_targets must be > 0.")
        return value

    def _normalize_hosts(self, hosts: Sequence[str] | None) -> list[str]:
        normalized: list[str] = []
        seen = set()
        for raw in hosts or []:
            host = str(raw or "").strip()
            if not host:
                continue
            key = host.lower()
            if key in seen:
                continue
            seen.add(key)
            normalized.append(host)
        if not normalized:
            raise LocalWifiOnboardingError("WIFI_HOSTS_REQUIRED: hosts must contain at least one host.")
        return normalized

    def _normalize_ports(self, ports: Sequence[int] | None) -> list[int]:
        normalized: list[int] = []
        seen = set()
        source = list(ports) if ports is not None else list(DEFAULT_SCAN_PORTS)
        for raw in source:
            value = int(raw)
            if value < 1 or value > 65535:
                raise LocalWifiOnboardingError(f"WIFI_PORT_INVALID: {value}")
            if value in seen:
                continue
            seen.add(value)
            normalized.append(value)
        if not normalized:
            raise LocalWifiOnboardingError("WIFI_PORTS_REQUIRED: ports must contain at least one port.")
        return normalized

    def _build_targets(
        self,
        *,
        hosts: Sequence[str],
        ports: Sequence[int],
        max_targets: int,
    ) -> tuple[list[LocalWifiProbeTarget], bool]:
        targets: list[LocalWifiProbeTarget] = []
        truncated = False
        for host in hosts:
            for port in ports:
                for path in DEFAULT_SCAN_PATHS:
                    if len(targets) >= max_targets:
                        truncated = True
                        break
                    url = f"http://{host}:{port}{path}"
                    targets.append(
                        LocalWifiProbeTarget(
                            host=str(host),
                            port=int(port),
                            path=str(path),
                            url=url,
                        )
                    )
                if truncated:
                    break
            if truncated:
                break
        return targets, truncated

    def _run_probe(self, target: LocalWifiProbeTarget, timeout_s: float) -> Mapping[str, Any]:
        if self._probe_hook is not None:
            result = self._probe_hook(target, timeout_s)
            if not isinstance(result, Mapping):
                raise LocalWifiOnboardingError("WIFI_PROBE_INVALID: probe hook must return mapping.")
            return result
        return self._probe_target(target, timeout_s)

    def _probe_target(self, target: LocalWifiProbeTarget, timeout_s: float) -> Mapping[str, Any]:
        try:
            response = self._session.get(target.url, timeout=float(timeout_s))
        except requests.RequestException:
            return {"ok": False}

        if int(response.status_code) >= 400:
            return {"ok": False}

        payload: dict[str, Any] = {}
        try:
            parsed = response.json()
            if isinstance(parsed, dict):
                payload = dict(parsed)
        except ValueError:
            payload = {}

        connector_type = self._infer_connector_type(target.path, payload)
        if not connector_type:
            return {"ok": False}

        return {
            "ok": True,
            "connector_type": connector_type,
            "status_code": int(response.status_code),
        }

    def _infer_connector_type(self, path: str, payload: Mapping[str, Any]) -> str:
        normalized_path = str(path or "").strip().lower()
        if normalized_path == "/server/info":
            result = payload.get("result", {})
            if isinstance(result, Mapping):
                version = str(result.get("moonraker_version", "")).strip()
                if version:
                    if self._payload_contains(payload, "creality", "ender", "k1", "k2"):
                        return "creality"
                    return "moonraker"
            version = str(payload.get("moonraker_version", "")).strip()
            if version:
                if self._payload_contains(payload, "creality", "ender", "k1", "k2"):
                    return "creality"
                return "moonraker"
            return ""

        if normalized_path == "/api/v1/status":
            if self._payload_contains(payload, "bambu", "x1", "a1", "p1s", "p1p"):
                return "bambu_lan"
            if self._payload_contains(payload, "creality", "ender", "k1", "k2"):
                return "creality"
            return ""

        if normalized_path == "/api/printer":
            if self._payload_contains(payload, "creality", "ender", "k1", "k2"):
                return "creality"
            if self._payload_contains(payload, "octoprint"):
                return "octoprint"
            return ""

        if normalized_path != "/api/version":
            return ""

        server_name = str(payload.get("server", "")).strip().lower()
        if "prusa" in server_name:
            return "prusalink"
        if "octoprint" in server_name:
            return "octoprint"
        if "bambu" in server_name:
            return "bambu_lan"
        if "creality" in server_name:
            return "creality"
        return ""

    @staticmethod
    def _payload_contains(payload: Mapping[str, Any], *keywords: str) -> bool:
        try:
            text = json.dumps(payload, sort_keys=True).lower()
        except Exception:
            text = str(payload).lower()
        for keyword in keywords:
            token = str(keyword or "").strip().lower()
            if token and token in text:
                return True
        return False

    def _candidate_from_probe(
        self,
        target: LocalWifiProbeTarget,
        connector_type: str,
        probe_result: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        display = {
            "octoprint": "OctoPrint",
            "moonraker": "Moonraker",
            "prusalink": "PrusaLink",
            "bambu_lan": "Bambu",
            "creality": "Creality",
        }.get(connector_type, connector_type.title())
        base_url = f"http://{target.host}:{target.port}"
        candidate = {
            "name": f"{display} {target.host}:{target.port}",
            "connector_type": connector_type,
            "host": target.host,
            "port": int(target.port),
            "discovered_via": "local_wifi_scan",
            "network_transport": "wifi_local",
            "catalog_only": False,
        }
        if connector_type == "octoprint":
            candidate["octoprint_url"] = base_url
            candidate["octoprint_api_key"] = ""
        elif connector_type == "prusalink":
            candidate["prusalink_url"] = base_url
            candidate["prusalink_api_key"] = ""
        elif connector_type == "moonraker":
            candidate["moonraker_url"] = base_url
            candidate["moonraker_token"] = ""
        elif connector_type == "bambu_lan":
            candidate["bambu_url"] = base_url
            candidate["bambu_access_code"] = ""
            candidate["bambu_serial"] = ""
        elif connector_type == "creality":
            candidate["creality_url"] = base_url
            protocol_hint = str((probe_result or {}).get("creality_protocol", "")).strip().lower()
            if protocol_hint not in {"moonraker", "octoprint"}:
                if str(target.path or "").strip().lower() == "/server/info":
                    protocol_hint = "moonraker"
                else:
                    protocol_hint = "moonraker" if int(target.port) == 7125 else "octoprint"
            candidate["creality_protocol"] = protocol_hint
            candidate["creality_token"] = ""
        return candidate

    def _printer_identity(self, printer: Mapping[str, Any]) -> str:
        connector_type = str(printer.get("connector_type", "")).strip().lower()
        if connector_type == "octoprint":
            url = str(printer.get("octoprint_url", "")).strip().rstrip("/").lower()
            return f"octoprint|{url}"
        if connector_type == "prusalink":
            url = str(printer.get("prusalink_url", "")).strip().rstrip("/").lower()
            return f"prusalink|{url}"
        if connector_type == "moonraker":
            url = str(printer.get("moonraker_url", "")).strip().rstrip("/").lower()
            return f"moonraker|{url}"
        if connector_type == "bambu_lan":
            url = str(printer.get("bambu_url", "") or printer.get("endpoint", "")).strip().rstrip("/").lower()
            return f"bambu_lan|{url}"
        if connector_type == "creality":
            url = str(printer.get("creality_url", "") or printer.get("endpoint", "")).strip().rstrip("/").lower()
            protocol = str(printer.get("creality_protocol", "")).strip().lower()
            return f"creality|{protocol}|{url}"

        host = str(printer.get("host", "")).strip().lower()
        port = int(printer.get("port", 0) or 0)
        if host and port > 0:
            return f"{connector_type}|{host}:{port}"

        name = str(printer.get("name", "")).strip().lower()
        return f"{connector_type}|{name}"

    def _discovery_identity(self, printer: Mapping[str, Any]) -> str:
        connector_type = str(printer.get("connector_type", "")).strip().lower()
        if connector_type == "creality":
            url = str(printer.get("creality_url", "") or printer.get("endpoint", "")).strip().rstrip("/").lower()
            if url:
                return f"creality|{url}"
            host = str(printer.get("host", "")).strip().lower()
            port = int(printer.get("port", 0) or 0)
            if host and port > 0:
                return f"creality|{host}:{port}"
        return self._printer_identity(printer)

    @staticmethod
    def _prefer_discovered_candidate(existing: Mapping[str, Any], candidate: Mapping[str, Any]) -> bool:
        existing_type = str(existing.get("connector_type", "")).strip().lower()
        candidate_type = str(candidate.get("connector_type", "")).strip().lower()
        if existing_type == "creality" and candidate_type == "creality":
            existing_protocol = str(existing.get("creality_protocol", "")).strip().lower()
            candidate_protocol = str(candidate.get("creality_protocol", "")).strip().lower()
            return existing_protocol != "moonraker" and candidate_protocol == "moonraker"
        return False

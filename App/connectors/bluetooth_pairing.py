from __future__ import annotations

import asyncio
import os
import sys
from typing import Any, Awaitable, Callable, Mapping, Sequence

from .errors import LocalWifiOnboardingError

try:
    from bleak import BleakClient, BleakScanner  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    BleakClient = None  # type: ignore
    BleakScanner = None  # type: ignore


DiscoveryHook = Callable[[float], Sequence[Mapping[str, Any]]]
PairHook = Callable[[str], Mapping[str, Any]]


def _env_bool(name: str, default: bool = False) -> bool:
    raw = str(os.environ.get(name, "1" if default else "0")).strip().lower()
    if raw in ("1", "true", "yes", "on"):
        return True
    if raw in ("0", "false", "no", "off"):
        return False
    return bool(default)


def _run_async(coro: Awaitable[Any]) -> Any:
    try:
        return asyncio.run(coro)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()


class BluetoothPairingManager:
    def __init__(
        self,
        *,
        linux_beta_env: str = "EON_BLUETOOTH_LINUX_BETA",
        discovery_hook: DiscoveryHook | None = None,
        pair_hook: PairHook | None = None,
    ):
        self._linux_beta_env = str(linux_beta_env or "EON_BLUETOOTH_LINUX_BETA")
        self._discovery_hook = discovery_hook
        self._pair_hook = pair_hook

    def platform_mode(self) -> str:
        if sys.platform.startswith("win"):
            return "windows"
        if sys.platform.startswith("linux"):
            if _env_bool(self._linux_beta_env, False):
                return "linux_beta"
            return "linux_disabled"
        return "unsupported"

    def is_supported(self) -> bool:
        mode = self.platform_mode()
        if mode == "windows":
            return True
        if mode == "linux_beta":
            return True
        return False

    def discover(self, *, timeout_s: float = 5.0) -> Mapping[str, Any]:
        timeout = max(1.0, float(timeout_s))
        if not self.is_supported():
            return {
                "ok": False,
                "state": "unsupported",
                "mode": self.platform_mode(),
                "devices": [],
                "message": "Bluetooth discovery is not enabled on this platform.",
            }
        if self._discovery_hook is not None:
            rows = [dict(item) for item in self._discovery_hook(timeout) if isinstance(item, Mapping)]
            return {"ok": True, "state": "ready", "mode": self.platform_mode(), "devices": rows}
        if BleakScanner is None:
            return {
                "ok": False,
                "state": "dependency_missing",
                "mode": self.platform_mode(),
                "devices": [],
                "message": "bleak package is required for Bluetooth discovery.",
            }
        try:
            devices = _run_async(BleakScanner.discover(timeout=timeout))
        except Exception as exc:
            return {
                "ok": False,
                "state": "scan_failed",
                "mode": self.platform_mode(),
                "devices": [],
                "message": str(exc),
            }
        normalized: list[dict[str, Any]] = []
        for item in devices or []:
            address = str(getattr(item, "address", "") or "").strip()
            if not address:
                continue
            normalized.append(
                {
                    "id": address,
                    "address": address,
                    "name": str(getattr(item, "name", "") or "").strip() or "Bluetooth Device",
                    "rssi": int(getattr(item, "rssi", 0) or 0),
                }
            )
        return {"ok": True, "state": "ready", "mode": self.platform_mode(), "devices": normalized}

    def pair(self, *, device_id: str) -> Mapping[str, Any]:
        identifier = str(device_id or "").strip()
        if not identifier:
            raise LocalWifiOnboardingError("BLUETOOTH_DEVICE_ID_REQUIRED: device_id is required.")
        if not self.is_supported():
            return {
                "ok": False,
                "state": "unsupported",
                "mode": self.platform_mode(),
                "device_id": identifier,
            }
        if self._pair_hook is not None:
            payload = dict(self._pair_hook(identifier))
            payload.setdefault("device_id", identifier)
            payload.setdefault("mode", self.platform_mode())
            return payload
        if BleakClient is None:
            return {
                "ok": False,
                "state": "dependency_missing",
                "mode": self.platform_mode(),
                "device_id": identifier,
                "message": "bleak package is required for Bluetooth pairing.",
            }
        return self._pair_with_bleak(identifier)

    def _pair_with_bleak(self, identifier: str) -> Mapping[str, Any]:
        async def _pair_async() -> Mapping[str, Any]:
            client = BleakClient(identifier)
            try:
                await client.connect(timeout=10.0)
                paired = True
                if hasattr(client, "pair"):
                    try:
                        pair_result = await client.pair()  # type: ignore[misc]
                        paired = bool(pair_result) if pair_result is not None else True
                    except Exception:
                        paired = False
                return {
                    "ok": bool(paired),
                    "state": "paired" if paired else "pair_failed",
                    "mode": self.platform_mode(),
                    "device_id": identifier,
                }
            finally:
                try:
                    await client.disconnect()
                except Exception:
                    pass

        try:
            return dict(_run_async(_pair_async()))
        except Exception as exc:
            return {
                "ok": False,
                "state": "pair_failed",
                "mode": self.platform_mode(),
                "device_id": identifier,
                "message": str(exc),
            }

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


try:
    import keyring  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    keyring = None  # type: ignore


@dataclass
class KeychainStore:
    service_name: str = "EON-OpenSlicer"
    _memory_fallback: Dict[str, str] = field(default_factory=dict, init=False, repr=False)
    _runtime_disabled: bool = field(default=False, init=False, repr=False)

    def is_available(self) -> bool:
        if keyring is None or self._runtime_disabled:
            return False
        try:
            backend = keyring.get_keyring()
        except Exception:
            return False
        priority = getattr(backend, "priority", 0)
        try:
            return float(priority) > 0.0
        except Exception:
            return False

    def set_secret(self, account: str, secret: str) -> None:
        key = str(account or "").strip()
        if not key:
            raise ValueError("KEYCHAIN_ACCOUNT_REQUIRED")
        value = str(secret or "")
        if not self.is_available():
            self._memory_fallback[key] = value
            return
        try:
            keyring.set_password(self.service_name, key, value)
        except Exception:
            self._runtime_disabled = True
            self._memory_fallback[key] = value

    def get_secret(self, account: str) -> str:
        key = str(account or "").strip()
        if not key:
            return ""
        if not self.is_available():
            return str(self._memory_fallback.get(key, "") or "")
        try:
            value = keyring.get_password(self.service_name, key)
        except Exception:
            self._runtime_disabled = True
            return str(self._memory_fallback.get(key, "") or "")
        if value is None:
            return str(self._memory_fallback.get(key, "") or "")
        return str(value or "")

    def delete_secret(self, account: str) -> None:
        key = str(account or "").strip()
        if not key:
            return
        if not self.is_available():
            self._memory_fallback.pop(key, None)
            return
        try:
            keyring.delete_password(self.service_name, key)
        except Exception:
            self._runtime_disabled = True
        self._memory_fallback.pop(key, None)

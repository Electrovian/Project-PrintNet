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

    def is_available(self) -> bool:
        return keyring is not None

    def set_secret(self, account: str, secret: str) -> None:
        key = str(account or "").strip()
        if not key:
            raise ValueError("KEYCHAIN_ACCOUNT_REQUIRED")
        value = str(secret or "")
        if keyring is None:
            self._memory_fallback[key] = value
            return
        keyring.set_password(self.service_name, key, value)

    def get_secret(self, account: str) -> str:
        key = str(account or "").strip()
        if not key:
            return ""
        if keyring is None:
            return str(self._memory_fallback.get(key, "") or "")
        value = keyring.get_password(self.service_name, key)
        return str(value or "")

    def delete_secret(self, account: str) -> None:
        key = str(account or "").strip()
        if not key:
            return
        if keyring is None:
            self._memory_fallback.pop(key, None)
            return
        try:
            keyring.delete_password(self.service_name, key)
        except Exception:
            return

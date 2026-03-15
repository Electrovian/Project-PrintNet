from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Mapping

from .errors import InvalidPrinterConfigError


@dataclass(frozen=True)
class ConnectorCapabilities:
    connector_type: str
    display_name: str
    protocol: str
    supports_connect: bool = True
    supports_upload: bool = True
    supports_start: bool = True
    supports_pause: bool = True
    supports_resume: bool = True
    supports_cancel: bool = True
    supports_status: bool = True


class PrinterConnector(ABC):
    """Abstract printer connector contract for desktop and backend flows."""

    @property
    @abstractmethod
    def capabilities(self) -> ConnectorCapabilities:
        raise NotImplementedError

    @property
    def connector_type(self) -> str:
        return self.capabilities.connector_type

    def validate_printer(self, printer: Mapping[str, Any] | None) -> None:
        if printer is None or not isinstance(printer, Mapping):
            raise InvalidPrinterConfigError("PRINTER_CONFIG_INVALID: expected mapping.")

    @abstractmethod
    def connect(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def upload(self, printer: Mapping[str, Any], gcode_path: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def start_print(
        self,
        printer: Mapping[str, Any],
        *,
        remote_path: str | None = None,
        gcode_path: str | None = None,
    ) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def pause(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def resume(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def cancel(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def status(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

from __future__ import annotations


class ConnectorError(Exception):
    """Base connector failure."""


class InvalidPrinterConfigError(ConnectorError):
    """Printer configuration does not satisfy connector requirements."""


class UnsupportedConnectorError(ConnectorError):
    """Connector type is not registered."""


class ConnectorOperationError(ConnectorError):
    """Connector operation failed at runtime."""


class LocalWifiOnboardingError(ConnectorError):
    """Local Wi-Fi onboarding configuration or execution failed."""

"""External integrations: Airtable, OctoPrint, web backend activity, printer manager."""

from .web_backend_activity import WebBackendActivityClient, WebBackendActivityError

__all__ = [
    "WebBackendActivityClient",
    "WebBackendActivityError",
]

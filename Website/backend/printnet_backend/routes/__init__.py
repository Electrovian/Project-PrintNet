from .auth import build_auth_router
from .health import build_health_router
from .jobs import build_jobs_router
from .ops import build_ops_router
from .printers import build_printers_router
from .profiles import build_profiles_router
from .queue import build_queue_router

__all__ = [
    "build_auth_router",
    "build_health_router",
    "build_jobs_router",
    "build_ops_router",
    "build_printers_router",
    "build_profiles_router",
    "build_queue_router",
]

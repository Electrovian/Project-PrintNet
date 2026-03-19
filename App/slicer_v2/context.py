from __future__ import annotations

from .settings import normalize_settings
from .types import SlicerContext


def create_context(
    *,
    job_id: str,
    mesh_path: str,
    resolved_settings: dict[str, object] | None = None,
    runtime_settings: dict[str, object] | None = None,
) -> SlicerContext:
    return SlicerContext(
        job_id=job_id,
        mesh_path=mesh_path,
        resolved_settings=normalize_settings(resolved_settings),
        runtime_settings=dict(runtime_settings or {}),
    )

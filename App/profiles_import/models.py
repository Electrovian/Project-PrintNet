from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ImportFailure:
    category: str
    message: str
    path: str = ""


@dataclass(frozen=True)
class ResolvedProfile:
    machine_id: str
    nozzle: str
    process_id: str
    filament_id: str
    settings: dict[str, Any]


@dataclass
class ImportReport:
    success: bool
    machines: list[dict[str, Any]] = field(default_factory=list)
    processes: list[dict[str, Any]] = field(default_factory=list)
    filaments: list[dict[str, Any]] = field(default_factory=list)
    nozzles: list[str] = field(default_factory=list)
    resolved_profiles: list[ResolvedProfile] = field(default_factory=list)
    failures: list[ImportFailure] = field(default_factory=list)

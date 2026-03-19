from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ValidationIssue:
    level: str
    code: str
    message: str


@dataclass
class ValidationReport:
    ok: bool = True
    issues: list[ValidationIssue] = field(default_factory=list)

    def add_error(self, code: str, message: str) -> None:
        self.ok = False
        self.issues.append(ValidationIssue(level="error", code=code, message=message))

    def add_warning(self, code: str, message: str) -> None:
        self.issues.append(ValidationIssue(level="warning", code=code, message=message))

    def extend(self, other: "ValidationReport") -> None:
        if not other.ok:
            self.ok = False
        self.issues.extend(other.issues)


@dataclass
class StageTrace:
    stage_name: str
    started_at_utc: str
    ended_at_utc: str
    duration_ms: float
    status: str


@dataclass
class SlicePlan:
    layer_count: int = 0
    layer_heights_mm: list[float] = field(default_factory=list)
    region_count: int = 0
    perimeter_path_count: int = 0
    infill_path_count: int = 0
    support_path_count: int = 0


@dataclass
class GCodePlan:
    lines: list[str] = field(default_factory=list)
    estimated_time_seconds: float = 0.0
    estimated_filament_mm: float = 0.0


@dataclass
class SlicerContext:
    job_id: str
    mesh_path: str
    resolved_settings: dict[str, object]
    runtime_settings: dict[str, object] = field(default_factory=dict)
    stage_artifacts: dict[str, dict] = field(default_factory=dict)
    stage_order_executed: list[str] = field(default_factory=list)
    cancellation_requested: bool = False


@dataclass
class PipelineResult:
    context: SlicerContext
    validation: ValidationReport
    stage_traces: list[StageTrace]

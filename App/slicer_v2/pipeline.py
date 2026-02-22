from __future__ import annotations

from datetime import datetime, timezone
from time import perf_counter
from typing import Callable

from . import bridges, gcode, infill, islands, mesh, perimeters, regions, slice_grid, supports, travel
from .errors import SlicerV2CancelledError, SlicerV2StageError, SlicerV2ValidationError
from .types import PipelineResult, SlicerContext, StageTrace, ValidationReport
from .validators import validate_context, validate_stage_artifact, validate_stage_sequence


StageRunner = Callable[[SlicerContext], dict]

STAGE_SEQUENCE: list[tuple[str, StageRunner]] = [
    (mesh.STAGE_NAME, mesh.run),
    (slice_grid.STAGE_NAME, slice_grid.run),
    (regions.STAGE_NAME, regions.run),
    (islands.STAGE_NAME, islands.run),
    (perimeters.STAGE_NAME, perimeters.run),
    (infill.STAGE_NAME, infill.run),
    (supports.STAGE_NAME, supports.run),
    (bridges.STAGE_NAME, bridges.run),
    (travel.STAGE_NAME, travel.run),
    (gcode.STAGE_NAME, gcode.run),
]


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def run_pipeline(context: SlicerContext) -> PipelineResult:
    validation = validate_context(context)
    if not validation.ok:
        raise SlicerV2ValidationError(f"PRE_PIPELINE_VALIDATION_FAILED: {len(validation.issues)} issue(s)")

    traces: list[StageTrace] = []

    for stage_name, stage_runner in STAGE_SEQUENCE:
        if context.cancellation_requested:
            raise SlicerV2CancelledError(f"SLICER_V2_CANCELLED_BEFORE_STAGE: {stage_name}")

        started = _utc_now_iso()
        begin_perf = perf_counter()
        try:
            stage_runner(context)
        except Exception as exc:
            raise SlicerV2StageError(f"STAGE_FAILED:{stage_name}:{exc}") from exc
        duration_ms = (perf_counter() - begin_perf) * 1000.0
        ended = _utc_now_iso()

        context.stage_order_executed.append(stage_name)
        traces.append(
            StageTrace(
                stage_name=stage_name,
                started_at_utc=started,
                ended_at_utc=ended,
                duration_ms=duration_ms,
                status="ok",
            )
        )

        artifact_validation = validate_stage_artifact(context, stage_name)
        validation.extend(artifact_validation)

    expected = [stage_name for stage_name, _runner in STAGE_SEQUENCE]
    sequence_validation = validate_stage_sequence(context.stage_order_executed, expected)
    validation.extend(sequence_validation)

    if not validation.ok:
        raise SlicerV2ValidationError(f"POST_PIPELINE_VALIDATION_FAILED: {len(validation.issues)} issue(s)")

    return PipelineResult(context=context, validation=validation, stage_traces=traces)

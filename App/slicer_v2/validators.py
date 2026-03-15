from __future__ import annotations

from pathlib import Path

from .types import SlicerContext, ValidationReport


def validate_context(context: SlicerContext) -> ValidationReport:
    report = ValidationReport(ok=True)

    if not str(context.job_id).strip():
        report.add_error("JOB_ID_EMPTY", "SlicerContext.job_id must not be empty.")

    if not str(context.mesh_path).strip():
        report.add_error("MESH_PATH_EMPTY", "SlicerContext.mesh_path must not be empty.")
    else:
        path = Path(context.mesh_path).expanduser()
        if not path.exists():
            report.add_error("MESH_PATH_MISSING", f"Mesh path missing: {path}")
        elif not path.is_file():
            report.add_error("MESH_PATH_NOT_FILE", f"Mesh path is not a file: {path}")

    if not isinstance(context.resolved_settings, dict):
        report.add_error("SETTINGS_NOT_DICT", "SlicerContext.resolved_settings must be dict.")

    return report


def validate_stage_artifact(context: SlicerContext, stage_name: str) -> ValidationReport:
    report = ValidationReport(ok=True)
    artifact = context.stage_artifacts.get(stage_name)
    if artifact is None:
        report.add_error("STAGE_ARTIFACT_MISSING", f"Stage artifact missing for: {stage_name}")
        return report
    if not isinstance(artifact, dict):
        report.add_error("STAGE_ARTIFACT_NOT_DICT", f"Stage artifact must be dict for: {stage_name}")
    return report


def validate_stage_sequence(executed: list[str], expected: list[str]) -> ValidationReport:
    report = ValidationReport(ok=True)
    if executed != expected:
        report.add_error("STAGE_SEQUENCE_MISMATCH", f"Expected {expected}, got {executed}")
    return report

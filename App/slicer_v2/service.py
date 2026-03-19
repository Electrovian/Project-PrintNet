from __future__ import annotations

import os
import uuid
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Mapping

from .context import create_context
from .pipeline import run_pipeline


def _resolved_settings_payload(settings: object | None) -> dict[str, object]:
    if settings is None:
        return {}
    if is_dataclass(settings):
        return asdict(settings)
    if isinstance(settings, Mapping):
        return dict(settings)
    if hasattr(settings, "__dict__"):
        return {str(key): value for key, value in vars(settings).items()}
    return {}


def slice_file(
    stl_path: str,
    output_gcode_path: str | None = None,
    settings: object | None = None,
    runtime_settings: dict[str, object] | None = None,
) -> str:
    input_path = Path(str(stl_path)).expanduser().resolve()
    if not input_path.exists() or not input_path.is_file():
        raise FileNotFoundError(f"SLICER_V2_INPUT_MISSING:{input_path}")

    resolved_settings = _resolved_settings_payload(settings)
    context = create_context(
        job_id=f"slicer-v2-{uuid.uuid4().hex[:12]}",
        mesh_path=str(input_path),
        resolved_settings=resolved_settings,
        runtime_settings=dict(runtime_settings or {}),
    )
    result = run_pipeline(context)
    gcode_artifact = result.context.stage_artifacts.get("gcode", {})
    lines = gcode_artifact.get("lines", [])
    if not isinstance(lines, list) or not lines:
        raise RuntimeError("SLICER_V2_NO_GCODE_LINES")

    if output_gcode_path:
        out_path = Path(str(output_gcode_path)).expanduser()
    else:
        out_path = input_path.with_suffix(".gcode")
    out_path = out_path.resolve()
    if out_path.parent and not out_path.parent.exists():
        os.makedirs(out_path.parent, exist_ok=True)

    text = "\n".join(str(line) for line in lines)
    if text and not text.endswith("\n"):
        text += "\n"
    out_path.write_text(text, encoding="utf-8", newline="\n")
    return str(out_path)

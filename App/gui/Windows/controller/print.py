from __future__ import annotations

import json
import os
import re
import socket
import tempfile
import uuid
from dataclasses import asdict, is_dataclass, replace
from typing import TYPE_CHECKING, Any, Mapping

import numpy as np
import trimesh
from PyQt5 import QtCore, QtGui, QtWidgets

from ...workers import Worker
from ...widgets.email_compose_dialog import EmailComposeDialog
from config.defaults import DEFAULTS
from config.performance import resolve_performance_limits
from integrations.email_delivery import (
    EmailConfigurationError,
    EmailDeliveryError,
    build_mailto_url,
    send_email_via_smtp,
)
from slicer_v2.legacy_ai_checks import run_ai_checks
from slicer_v2.legacy_gcode_preview import parse_gcode_preview, parse_gcode_preview_file
from slicer_v2.legacy_gcode_stats import estimate_gcode_file
from slicer_v2.legacy_gcode_writer import SliceSettings
from slicer_v2.gcode_contract import resolve_output_settings_payload
from slicer_v2.supports import build_preview_support_diagnostics
try:
    from slicer_v2.legacy_slicer.emit import slice_trimesh_auto as slice_v2_trimesh_auto
except Exception:
    slice_v2_trimesh_auto = None

try:
    from slicer_v2.context import create_context as create_v2_context
    from slicer_v2.pipeline import run_pipeline as run_v2_pipeline
except Exception:
    create_v2_context = None
    run_v2_pipeline = None


PLATE_EMPTY_MESSAGE = "Load model(s) first."
PLATE_DATA_UNAVAILABLE_MESSAGE = "Model data unavailable for slicing."


def _sanitize_gcode_basename(value: str, default: str = "plate") -> str:
    text = str(value or "").strip()
    if not text:
        return default
    cleaned = re.sub(r"[^\w\-. ]+", "_", text)
    cleaned = cleaned.replace(" ", "_").strip("._")
    cleaned = re.sub(r"_+", "_", cleaned)
    return cleaned or default


def _settings_to_dict(settings: Any) -> dict[str, Any]:
    if settings is None:
        return {}
    if is_dataclass(settings):
        return asdict(settings)
    if isinstance(settings, Mapping):
        return dict(settings)
    try:
        return dict(settings)
    except Exception:
        pass
    try:
        return {
            str(key): value
            for key, value in vars(settings).items()
            if not str(key).startswith("_")
        }
    except Exception:
        return {}


def _resolve_slice_output_contract(
    settings: SliceSettings,
    *,
    runtime_printer_state: object | None = None,
    printer: dict[str, object] | None = None,
) -> tuple[SliceSettings, dict[str, Any]]:
    payload = resolve_output_settings_payload(
        settings,
        runtime_printer_state=runtime_printer_state,
        printer=printer,
    )
    resolved_settings = replace(
        settings,
        firmware_flavor=str(payload.get("firmware_flavor", settings.firmware_flavor)),
        start_gcode=list(payload.get("start_gcode", settings.start_gcode or [])),
        end_gcode=list(payload.get("end_gcode", settings.end_gcode or [])),
        bed_x=float(payload.get("bed_x", settings.bed_x)),
        bed_y=float(payload.get("bed_y", settings.bed_y)),
        gcode_absolute_extrusion=bool(payload.get("gcode_absolute_extrusion", True)),
        nozzle_temperature_c=payload.get("nozzle_temperature_c"),
        bed_temperature_c=payload.get("bed_temperature_c"),
    )
    return resolved_settings, payload


def _merged_adaptive_layer_ranges(raw_ranges: list[dict[str, object]] | tuple[dict[str, object], ...] | None) -> list[dict[str, float]]:
    normalized: list[dict[str, float]] = []
    for item in list(raw_ranges or []):
        if not isinstance(item, dict):
            continue
        try:
            z_min = float(item.get("z_min_mm", item.get("z_min", item.get("start", 0.0))))
            z_max = float(item.get("z_max_mm", item.get("z_max", item.get("end", 0.0))))
            layer_height = float(item.get("layer_height_mm", item.get("layer_height", item.get("height", 0.0))))
        except (TypeError, ValueError):
            continue
        if z_max <= z_min or layer_height <= 0.0:
            continue
        normalized.append(
            {
                "z_min_mm": z_min,
                "z_max_mm": z_max,
                "layer_height_mm": layer_height,
            }
        )
    if not normalized:
        return []

    epsilon = 1e-9
    breakpoints = sorted({float(item["z_min_mm"]) for item in normalized} | {float(item["z_max_mm"]) for item in normalized})
    merged: list[dict[str, float]] = []
    for start, end in zip(breakpoints, breakpoints[1:]):
        if end <= start + epsilon:
            continue
        midpoint = (start + end) * 0.5
        overlapping = [
            float(item["layer_height_mm"])
            for item in normalized
            if float(item["z_min_mm"]) - epsilon <= midpoint <= float(item["z_max_mm"]) + epsilon
        ]
        if not overlapping:
            continue
        target_height = min(overlapping)
        if (
            merged
            and abs(float(merged[-1]["layer_height_mm"]) - target_height) <= epsilon
            and abs(float(merged[-1]["z_max_mm"]) - start) <= epsilon
        ):
            merged[-1]["z_max_mm"] = float(end)
        else:
            merged.append(
                {
                    "z_min_mm": float(start),
                    "z_max_mm": float(end),
                    "layer_height_mm": float(target_height),
                }
            )
    return merged


def _to_string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    output: list[str] = []
    for item in value:
        text = str(item).strip()
        if text:
            output.append(text)
    return output


def _support_settings_payload(settings: SliceSettings | None) -> dict[str, object]:
    if settings is None:
        return {}
    return {
        "support_enabled": bool(getattr(settings, "support_enabled", False)),
        "support_type": str(getattr(settings, "support_type", "normal") or "normal"),
        "support_style": str(getattr(settings, "support_style", "pillars") or "pillars"),
        "support_build_plate_only": bool(getattr(settings, "support_build_plate_only", False)),
        "support_critical_regions_only": bool(getattr(settings, "support_critical_regions_only", False)),
        "support_remove_small_overhang": bool(getattr(settings, "support_remove_small_overhang", False)),
        "tree_support_strict_parity_mode": bool(getattr(settings, "tree_support_strict_parity_mode", False)),
    }


def _build_support_diagnostics_payload(
    settings: SliceSettings | None,
    payload: Mapping[str, object] | None,
    *,
    status: str | None = None,
    source: str | None = None,
    warnings: list[str] | None = None,
    error: object | None = None,
) -> dict[str, object]:
    merged: dict[str, object] = _support_settings_payload(settings)
    if isinstance(payload, Mapping):
        merged.update(dict(payload))

    combined_warnings = _to_string_list(merged.get("warnings"))
    for warning in _to_string_list(warnings):
        if warning not in combined_warnings:
            combined_warnings.append(warning)
    if combined_warnings:
        merged["warnings"] = combined_warnings
        merged["warning_count"] = max(int(merged.get("warning_count", 0) or 0), len(combined_warnings))

    if status:
        merged["diagnostics_status"] = str(status).strip().lower()
    if source:
        merged["diagnostics_source"] = str(source).strip()
    if error is not None:
        merged["diagnostics_error"] = str(error).strip()
    return build_preview_support_diagnostics(merged)


class PrintMixin:
    if TYPE_CHECKING:
        viewer: Any
        settings_panel: Any
        printer_manager: Any
        preview_view: Any
        device_view: Any
        _mode_tabs: Any
        _slice_in_progress: bool
        _last_gcode_path: str | None
        _last_slice_signature: str | None
        _last_gcode_stats: dict | None
        _last_preview_key: tuple[str, float, int] | None
        _last_preview_data: Any | None
        _last_preview_text: str | None
        _last_slice_meshes: list[trimesh.Trimesh] | None
        _last_slicer_backend: str | None

        def statusBar(self) -> QtWidgets.QStatusBar: ...
        def _busy_dialog(self, title: str, label: str) -> QtWidgets.QProgressDialog: ...
        def _start_worker(self, worker: Worker) -> None: ...
        def _activate_mode(self, mode: str) -> None: ...
        def __getattr__(self, name: str) -> Any: ...
        def _safe_get_save_file_name(self, caption: str, directory: str, file_filter: str) -> tuple[str, str]: ...
    # ----------------------------------------------------------- slice/print
    def _invalidate_slice_cache(self, clear_preview: bool = False) -> None:
        self._last_gcode_path = None
        self._last_slice_signature = None
        self._last_gcode_stats = None
        self._last_preview_key = None
        self._last_preview_data = None
        self._last_preview_text = None
        self._last_slice_meshes = None
        self._last_slicer_backend = None
        if clear_preview:
            if hasattr(self, "preview_view") and hasattr(self.preview_view, "set_gcode_text"):
                self.preview_view.set_gcode_text("")
            if hasattr(self, "viewer") and hasattr(self.viewer, "clear_gcode_preview"):
                self.viewer.clear_gcode_preview()

    def _get_current_stl_path(self):
        if self.current_model_id is None:
            return None
        return self.viewer.get_model_path(self.current_model_id)

    def _get_current_mesh(self):
        if self.current_model_id is None:
            return None
        mesh_data = self.viewer.get_model_mesh_data(self.current_model_id)
        if not mesh_data:
            return None
        vertices, faces = mesh_data
        return trimesh.Trimesh(vertices=vertices, faces=faces, process=False)

    def _get_plate_source_path(self):
        model_ids = self.viewer.get_model_ids()
        if not model_ids:
            return None
        for mid in model_ids:
            path = self.viewer.get_model_path(mid)
            if path:
                return path
        return "plate"

    def _plate_has_models(self) -> bool:
        model_ids = self.viewer.get_model_ids()
        return bool(model_ids)

    def _warn_no_plate_models(self, message: str = PLATE_EMPTY_MESSAGE) -> None:
        QtWidgets.QMessageBox.warning(self.main, "No model", message)

    def _warn_plate_data_unavailable(self, message: str = PLATE_DATA_UNAVAILABLE_MESSAGE) -> None:
        QtWidgets.QMessageBox.warning(self.main, "No model", message)

    def _get_plate_mesh(self):
        model_ids = self.viewer.get_model_ids()
        if not model_ids:
            return None
        vertices_list = []
        faces_list = []
        vert_offset = 0
        for mid in model_ids:
            mesh_data = self.viewer.get_model_mesh_data(mid)
            if not mesh_data:
                continue
            vertices, faces = mesh_data
            vertices_list.append(np.asarray(vertices, dtype=float))
            faces_list.append(np.asarray(faces, dtype=int) + vert_offset)
            vert_offset += len(vertices)
        if not vertices_list:
            return None
        combined_vertices = np.vstack(vertices_list)
        combined_faces = np.vstack(faces_list) if faces_list else np.zeros((0, 3), dtype=int)
        return trimesh.Trimesh(vertices=combined_vertices, faces=combined_faces, process=False)

    def _get_plate_meshes(self):
        model_ids = self.viewer.get_model_ids()
        if not model_ids:
            return [], None
        meshes = []
        vertices_list = []
        faces_list = []
        vert_offset = 0
        for mid in model_ids:
            mesh_data = self.viewer.get_model_mesh_data(mid)
            if not mesh_data:
                continue
            vertices, faces = mesh_data
            v = np.asarray(vertices, dtype=float)
            f = np.asarray(faces, dtype=int)
            meshes.append(trimesh.Trimesh(vertices=v, faces=f, process=False))
            vertices_list.append(v)
            faces_list.append(f + vert_offset)
            vert_offset += len(v)
        if not meshes:
            return [], None
        combined_vertices = np.vstack(vertices_list)
        combined_faces = np.vstack(faces_list) if faces_list else np.zeros((0, 3), dtype=int)
        combined = trimesh.Trimesh(vertices=combined_vertices, faces=combined_faces, process=False)
        return meshes, combined

    def _default_plate_gcode_basename(self) -> str:
        model_ids = self.viewer.get_model_ids()
        if not model_ids:
            return "plate"
        plate_name = ""
        if hasattr(self.viewer, "get_current_plate_name"):
            plate_name = str(self.viewer.get_current_plate_name() or "").strip()
        if plate_name:
            base = plate_name
            if len(model_ids) > 1:
                base = f"{base}_plate"
            return _sanitize_gcode_basename(base, default="plate")
        source_path = self._get_plate_source_path()
        if source_path and source_path != "plate":
            base = os.path.splitext(os.path.basename(source_path))[0]
        else:
            primary_id = model_ids[0]
            primary_name = ""
            if hasattr(self.viewer, "get_model_name"):
                primary_name = str(self.viewer.get_model_name(primary_id) or "").strip()
            base = primary_name or f"model_{primary_id}"
        if len(model_ids) > 1:
            base = f"{base}_plate"
        return _sanitize_gcode_basename(base, default="plate")

    def _default_plate_gcode_path(self) -> str:
        if self._last_gcode_path:
            base_dir = os.path.dirname(self._last_gcode_path)
        else:
            source_path = self._get_plate_source_path()
            if source_path and source_path != "plate":
                base_dir = os.path.dirname(source_path)
            else:
                base_dir = os.getcwd()
        filename = f"{self._default_plate_gcode_basename()}.gcode"
        return os.path.join(base_dir, filename)

    def _build_slice_signature(self, settings: SliceSettings):
        model_ids = sorted(self.viewer.get_model_ids())
        if not model_ids:
            return None
        models_payload = []
        for mid in model_ids:
            scale_offset = self.viewer.get_model_transform(mid)
            rotation = self.viewer.get_model_rotation(mid)
            if scale_offset is None or rotation is None:
                continue
            scale, offset = scale_offset
            models_payload.append(
                {
                    "model_id": int(mid),
                    "path": self.viewer.get_model_path(mid),
                    "scale": [float(v) for v in np.asarray(scale).reshape(-1)],
                    "offset": [float(v) for v in np.asarray(offset).reshape(-1)],
                    "rotation": [float(v) for v in np.asarray(rotation).reshape(-1)],
                    "object_id": int(self.viewer.models.get(mid, {}).get("object_id", 0)),
                    "plate_id": int(self.viewer.models.get(mid, {}).get("plate_id", 0)),
                }
            )
        if not models_payload:
            return None
        tool_state = {}
        if hasattr(self.viewer, "scene_state"):
            active_ids = {str(int(mid)) for mid in model_ids}
            raw_tool_state = self.viewer.scene_state.tool_state
            tool_state = {
                "adaptive_layer_ranges": {
                    key: value
                    for key, value in dict(raw_tool_state.adaptive_layer_ranges or {}).items()
                    if key in active_ids
                },
                "annotations": {
                    key: value
                    for key, value in dict(raw_tool_state.annotations or {}).items()
                    if key in active_ids
                },
                "emboss_payloads": {
                    key: value
                    for key, value in dict(raw_tool_state.emboss_payloads or {}).items()
                    if key in active_ids
                },
            }
        payload = {
            "plate_id": int(self.viewer.get_current_plate_id()) if hasattr(self.viewer, "get_current_plate_id") else 1,
            "plate_name": str(self.viewer.get_current_plate_name() or "").strip()
            if hasattr(self.viewer, "get_current_plate_name")
            else "",
            "models": models_payload,
            "settings": _settings_to_dict(settings),
            "tool_state": tool_state,
        }
        return json.dumps(payload, sort_keys=True, default=str)

    def _resolve_reusable_gcode_path(self, settings: SliceSettings) -> str | None:
        gcode_path = self._last_gcode_path
        if not gcode_path:
            return None
        if not os.path.exists(gcode_path):
            return None
        signature = self._build_slice_signature(settings)
        if not signature:
            return None
        if signature != self._last_slice_signature:
            return None
        self._log_slicer_activity("slice_cache_hit", gcode_path=gcode_path)
        return gcode_path

    def _slicer_engine_preference(self) -> str:
        # Runtime slicing is Python-only: always use slicer_v2.
        return "v2"

    def _gpu_mode(self) -> str:
        raw = str(os.environ.get("EON_SLICER_GPU_MODE", "auto")).strip().lower()
        if raw in ("off", "false", "0", "none"):
            return "off"
        if raw in ("cuda", "opencl", "metal", "vulkan"):
            return raw
        return "auto"

    def _runtime_performance(self) -> dict[str, object]:
        limits = {}
        if hasattr(self, "performance_limits"):
            maybe_limits = getattr(self, "performance_limits", None)
            if isinstance(maybe_limits, dict):
                limits = dict(maybe_limits)
        if not limits:
            limits = resolve_performance_limits(DEFAULTS.get("performance"))

        max_threads = 1
        try:
            max_threads = int(limits.get("max_threads", 1))
        except (TypeError, ValueError, AttributeError):
            max_threads = 1
        max_threads = max(1, max_threads)

        if hasattr(self, "pool") and self.pool is not None:
            try:
                max_threads = max(max_threads, int(self.pool.maxThreadCount()))
            except Exception:
                pass
        return {
            "max_threads": max_threads,
            "gpu_mode": self._gpu_mode(),
        }

    def _log_slicer_activity(self, action: str, **payload: object) -> None:
        logger = getattr(self.main, "activity_logger", None)
        if logger is None:
            return
        try:
            logger.log_action(action, **payload)
        except Exception:
            return

    def _status_engine_text(self, engine: str, perf: dict[str, object]) -> str:
        threads = int(perf.get("max_threads", 1))
        gpu_mode = str(perf.get("gpu_mode", "auto"))
        return f"engine={engine.upper()} cpu_threads={threads} gpu={gpu_mode}"

    def _resolve_output_gcode_path(self, source_path: str | None, output_gcode_path: str | None) -> str:
        if output_gcode_path:
            return str(output_gcode_path)
        if source_path and source_path != "plate":
            return str(os.path.splitext(source_path)[0] + ".gcode")
        return self._default_plate_gcode_path()

    def _support_diagnostics_from_stage_artifacts(
        self,
        stage_artifacts: object,
        settings: SliceSettings | None,
        *,
        source: str,
        error: object | None = None,
    ) -> dict[str, object]:
        supports_artifact = None
        if isinstance(stage_artifacts, Mapping):
            supports_artifact = stage_artifacts.get("supports")
        if isinstance(supports_artifact, Mapping):
            preview_payload = supports_artifact.get("preview_diagnostics")
            diagnostics_payload = preview_payload if isinstance(preview_payload, Mapping) else supports_artifact
            return _build_support_diagnostics_payload(settings, diagnostics_payload, source=source)

        missing_warnings = None
        missing_status = None
        if bool(getattr(settings, "support_enabled", False)):
            missing_warnings = ["support_planning:diagnostics_unavailable"]
            missing_status = "unavailable"
        return _build_support_diagnostics_payload(
            settings,
            None,
            status=missing_status,
            source=source,
            warnings=missing_warnings,
            error=error,
        )

    def _normalize_slice_result_payload(
        self,
        payload: object,
        settings: SliceSettings | None,
    ) -> dict[str, object]:
        gcode_path = ""
        support_payload = None
        source = "slice_payload"
        status = None
        warnings = None

        if isinstance(payload, Mapping):
            raw_path = payload.get("gcode_path", payload.get("output_path", payload.get("path")))
            if raw_path is not None:
                gcode_path = str(raw_path)
            maybe_support_payload = payload.get("support_diagnostics")
            if isinstance(maybe_support_payload, Mapping):
                support_payload = maybe_support_payload
        elif isinstance(payload, str):
            gcode_path = payload
            source = "legacy_string_result"
        elif payload is not None:
            gcode_path = str(payload)
            source = "legacy_string_result"

        if not gcode_path:
            raise RuntimeError("slicer_v2 produced no G-code path.")

        if support_payload is None and bool(getattr(settings, "support_enabled", False)):
            status = "unavailable"
            warnings = ["support_planning:diagnostics_unavailable"]

        return {
            "gcode_path": gcode_path,
            "support_diagnostics": _build_support_diagnostics_payload(
                settings,
                support_payload,
                status=status,
                source=source,
                warnings=warnings,
            ),
        }

    def _build_slice_preview_stats(
        self,
        gcode_path: str,
        settings: SliceSettings,
        preferred_engine: str,
        perf: dict[str, object],
        support_diagnostics: Mapping[str, object] | None,
    ) -> dict[str, object]:
        stats = self._analyze_gcode(gcode_path, settings)
        stats["slicer_engine"] = str(getattr(self, "_last_slicer_backend", preferred_engine))
        stats["cpu_threads"] = int(perf.get("max_threads", 1))
        stats["gpu_mode"] = str(perf.get("gpu_mode", "auto"))
        stats["support_diagnostics"] = dict(support_diagnostics or {})
        return stats

    def _apply_slice_payload_to_preview(
        self,
        payload: object,
        settings: SliceSettings,
        signature: str | None,
        preferred_engine: str,
        perf: dict[str, object],
    ) -> tuple[dict[str, object], dict[str, object]]:
        slice_payload = self._normalize_slice_result_payload(payload, settings)
        gcode_path = str(slice_payload["gcode_path"])
        self._last_gcode_path = gcode_path
        self._last_slice_signature = signature
        stats = self._build_slice_preview_stats(
            gcode_path,
            settings,
            preferred_engine,
            perf,
            slice_payload.get("support_diagnostics") if isinstance(slice_payload, Mapping) else None,
        )
        self._update_preview_from_gcode(gcode_path, stats)
        return slice_payload, stats

    def _slice_with_v2_pipeline(
        self,
        meshes: list[trimesh.Trimesh],
        combined_mesh: trimesh.Trimesh,
        settings: SliceSettings,
        source_path: str | None,
        output_gcode_path: str | None,
        perf: dict[str, object],
    ) -> dict[str, object]:
        output_path = self._resolve_output_gcode_path(source_path, output_gcode_path)
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        active_printer = getattr(getattr(self, "printer_manager", None), "active_printer", None)
        printer_payload = dict(active_printer) if isinstance(active_printer, dict) else active_printer
        settings, resolved_output_settings = _resolve_slice_output_contract(
            settings,
            runtime_printer_state=getattr(self, "runtime_printer_state", None),
            printer=printer_payload,
        )

        mesh_for_v2 = combined_mesh.copy()
        mesh_shift = np.array([0.0, 0.0, 0.0], dtype=float)
        try:
            bounds = np.asarray(mesh_for_v2.bounds, dtype=float)
            mins = bounds[0]
            if mins.shape[0] >= 3 and mins[2] < 0.0:
                mesh_shift[2] = -float(mins[2])
            if np.any(mesh_shift):
                mesh_for_v2.apply_translation(mesh_shift)
        except Exception:
            mesh_shift = np.array([0.0, 0.0, 0.0], dtype=float)

        # Prefer the detailed legacy-v2 toolpath emitter for desktop runtime slicing.
        force_semantic_only = str(os.environ.get("EON_SLICER_V2_SEMANTIC_ONLY", "0")).strip().lower() in (
            "1",
            "true",
            "yes",
            "on",
        )
        support_diagnostics = _build_support_diagnostics_payload(settings, None, source="runtime_defaults")
        semantic_error: Exception | None = None
        semantic_lines: list[str] | None = None
        if create_v2_context is not None and run_v2_pipeline is not None:
            temp_path = ""
            fd = -1
            try:
                fd, temp_path = tempfile.mkstemp(prefix="eon_slicer_v2_", suffix=".stl")
                os.close(fd)
                fd = -1
                mesh_for_v2.export(temp_path, file_type="stl")

                runtime_settings = {
                    "cpu_threads": int(perf.get("max_threads", 1)),
                    "gpu_mode": str(perf.get("gpu_mode", "auto")),
                    "mesh_count": int(len(meshes)),
                }
                context = create_v2_context(
                    job_id=f"eon-v2-{uuid.uuid4().hex[:12]}",
                    mesh_path=temp_path,
                    resolved_settings=dict(resolved_output_settings),
                    runtime_settings=runtime_settings,
                )
                result = run_v2_pipeline(context)
                support_diagnostics = self._support_diagnostics_from_stage_artifacts(
                    result.context.stage_artifacts,
                    settings,
                    source="supports_stage",
                )
                gcode_artifact = result.context.stage_artifacts.get("gcode", {})
                lines_value = gcode_artifact.get("lines", [])
                if isinstance(lines_value, list) and lines_value:
                    semantic_lines = [str(line) for line in lines_value]
                else:
                    semantic_error = RuntimeError("slicer_v2 produced no G-code lines.")
            except Exception as exc:
                semantic_error = exc
                support_diagnostics = _build_support_diagnostics_payload(
                    settings,
                    None,
                    status="unavailable" if bool(getattr(settings, "support_enabled", False)) else None,
                    source="semantic_pipeline",
                    warnings=["support_planning:diagnostics_unavailable"]
                    if bool(getattr(settings, "support_enabled", False))
                    else None,
                    error=exc,
                )
            finally:
                if fd >= 0:
                    try:
                        os.close(fd)
                    except Exception:
                        pass
                if temp_path and os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except Exception:
                        pass
        elif bool(getattr(settings, "support_enabled", False)):
            support_diagnostics = _build_support_diagnostics_payload(
                settings,
                None,
                status="unavailable",
                source="semantic_pipeline",
                warnings=["support_planning:diagnostics_unavailable"],
                error="semantic pipeline is unavailable",
            )

        detailed_error: Exception | None = None
        if slice_v2_trimesh_auto is not None and not force_semantic_only:
            mesh_items: list[trimesh.Trimesh] = []
            for mesh in meshes:
                if mesh is None:
                    continue
                mesh_copy = mesh.copy()
                if np.any(mesh_shift):
                    try:
                        mesh_copy.apply_translation(mesh_shift)
                    except Exception:
                        pass
                mesh_items.append(mesh_copy)
            if not mesh_items:
                mesh_items = [mesh_for_v2]
            try:
                detailed_path = str(
                    slice_v2_trimesh_auto(
                        meshes=mesh_items,
                        output_gcode_path=output_path,
                        settings=settings,
                        source_path=source_path,
                        combined_mesh=mesh_for_v2,
                    )
                )
                return {
                    "gcode_path": detailed_path,
                    "support_diagnostics": support_diagnostics,
                }
            except Exception as exc:
                detailed_error = exc

        if semantic_lines:
            with open(output_path, "w", encoding="utf-8", newline="\n") as handle:
                handle.write("\n".join(semantic_lines).rstrip() + "\n")
            return {
                "gcode_path": output_path,
                "support_diagnostics": support_diagnostics,
            }

        if create_v2_context is None or run_v2_pipeline is None:
            if detailed_error is not None:
                raise RuntimeError(
                    f"slicer_v2 detailed path failed and semantic pipeline is unavailable: {detailed_error}"
                ) from detailed_error
            raise RuntimeError("slicer_v2 pipeline is unavailable.")

        if detailed_error is not None and semantic_error is not None:
            raise RuntimeError(
                f"slicer_v2 detailed path failed: {detailed_error}; semantic pipeline failed: {semantic_error}"
            ) from semantic_error
        if detailed_error is not None:
            raise RuntimeError(
                f"slicer_v2 detailed path failed: {detailed_error}; semantic pipeline produced no G-code lines."
            ) from detailed_error
        if semantic_error is not None:
            raise semantic_error
        raise RuntimeError("slicer_v2 produced no G-code lines.")

    def _slice_with_selected_engine(
        self,
        meshes: list[trimesh.Trimesh],
        combined_mesh: trimesh.Trimesh,
        settings: SliceSettings,
        source_path: str | None,
        output_gcode_path: str | None,
    ) -> dict[str, object]:
        perf = self._runtime_performance()
        preferred = self._slicer_engine_preference()
        self._last_slicer_backend = preferred
        self._log_slicer_activity(
            "slice_start",
            preferred_engine=preferred,
            cpu_threads=int(perf.get("max_threads", 1)),
            gpu_mode=str(perf.get("gpu_mode", "auto")),
            strict_v2=True,
            mesh_count=int(len(meshes)),
        )
        try:
            raw_payload = self._slice_with_v2_pipeline(
                meshes=meshes,
                combined_mesh=combined_mesh,
                settings=settings,
                source_path=source_path,
                output_gcode_path=output_gcode_path,
                perf=perf,
            )
            slice_payload = self._normalize_slice_result_payload(raw_payload, settings)
            self._last_slicer_backend = "v2"
            support_diagnostics = slice_payload.get("support_diagnostics")
            support_status = ""
            if isinstance(support_diagnostics, Mapping):
                support_status = str(support_diagnostics.get("status", "") or "").strip()
            self._log_slicer_activity(
                "slice_success",
                engine="v2",
                output_path=slice_payload["gcode_path"],
                support_status=support_status,
            )
            return slice_payload
        except Exception as exc:
            self._log_slicer_activity("slice_engine_error", engine="v2", error=str(exc))
            raise RuntimeError(f"slicer_v2 failed: {exc}") from exc

    def _slice_model(self,
                     settings: SliceSettings,
                     activate_preview: bool,
                     show_dialog: bool,
                     show_errors: bool = True):
        source_path = self._get_plate_source_path()
        if not source_path:
            if show_dialog:
                self._warn_no_plate_models()
            return
        meshes, combined = self._get_plate_meshes()
        if not meshes or combined is None:
            if show_dialog:
                self._warn_plate_data_unavailable()
            return
        self._last_slice_meshes = [m for m in meshes]
        if self._slice_in_progress:
            return

        signature = self._build_slice_signature(settings)
        dlg = None
        preferred_engine = self._slicer_engine_preference()
        perf = self._runtime_performance()
        status_hint = self._status_engine_text(preferred_engine, perf)
        if show_dialog:
            dlg = self._busy_dialog("Slicing", f"Slicing model ({status_hint})...\nPlease wait.")
            dlg.show()
        else:
            self.statusBar().showMessage(f"Slicing model ({status_hint})...")
        self._slice_in_progress = True

        def on_done(payload):
            if dlg is not None:
                dlg.close()
            self._slice_in_progress = False
            try:
                slice_payload, stats = self._apply_slice_payload_to_preview(
                    payload,
                    settings,
                    signature,
                    preferred_engine,
                    perf,
                )
            except Exception as exc:
                self.statusBar().showMessage("Slicing failed")
                if show_errors:
                    QtWidgets.QMessageBox.critical(self.main, "Slicing error", str(exc))
                return
            gcode_path = str(slice_payload["gcode_path"])
            self.statusBar().showMessage(
                f"Sliced ({stats['slicer_engine'].upper()}) to {gcode_path}"
            )
            if hasattr(self, "_mode_tabs"):
                for btn in self._mode_tabs:
                    mode_key = str(btn.property("mode_key") or "").strip().lower()
                    label_key = btn.text().strip().lower()
                    if mode_key == "preview" or label_key == "preview":
                        btn.setChecked(True)
                        break
            if activate_preview:
                self._activate_mode("preview")

        def on_err(msg):
            if dlg is not None:
                dlg.close()
            self._slice_in_progress = False
            self.statusBar().showMessage("Slicing failed")
            if show_errors:
                QtWidgets.QMessageBox.critical(self.main, "Slicing error", msg)

        worker = Worker(
            self._slice_with_selected_engine,
            meshes,
            combined,
            settings,
            source_path,
            None,
        )
        worker.signals.finished.connect(on_done)
        worker.signals.error.connect(on_err)
        self._start_worker(worker)

    def _auto_orient_plate_default(self) -> None:
        if not hasattr(self, "viewer"):
            return
        model_ids = list(self.viewer.get_model_ids())
        if not model_ids:
            return
        overhang_angle = SliceSettings().overhang_angle
        changed = False
        for model_id in model_ids:
            try:
                ok = self.viewer.auto_orient_model(
                    model_id,
                    mode="default",
                    overhang_angle=overhang_angle,
                )
            except Exception:
                ok = False
            if ok:
                changed = True
        if not changed:
            return
        if hasattr(self, "_sync_popups"):
            self._sync_popups()
        if hasattr(self, "_update_bed_warnings"):
            self._update_bed_warnings()
        if hasattr(self, "_schedule_undo_snapshot"):
            self._schedule_undo_snapshot()

    def _settings_with_slice_defaults(self) -> SliceSettings:
        settings = self.settings_panel.to_settings()
        viewer = getattr(self, "viewer", None)
        support_paint_present = False
        seam_paint_present = False
        fuzzy_paint_present = False
        brim_ears_present = False
        if viewer is not None and hasattr(viewer, "scene_state"):
            adaptive_ranges: list[dict[str, object]] = list(getattr(settings, "adaptive_layer_ranges", ()) or [])
            tool_state = viewer.scene_state.tool_state
            for model_id in viewer.get_model_ids():
                adaptive_ranges.extend(list(tool_state.adaptive_layer_ranges.get(str(int(model_id)), []) or []))
                annotation = dict(tool_state.annotations.get(str(int(model_id)), {}) or {})
                support_paint_present = support_paint_present or bool(annotation.get("support"))
                seam_paint_present = seam_paint_present or bool(annotation.get("seam"))
                fuzzy_paint_present = fuzzy_paint_present or bool(annotation.get("fuzzy"))
                brim_ears_present = brim_ears_present or bool(annotation.get("brim_ears"))
            merged_ranges = _merged_adaptive_layer_ranges(adaptive_ranges)
            if merged_ranges:
                settings.adaptive_layering_enabled = True
                settings.adaptive_layer_ranges = list(merged_ranges)
        if support_paint_present:
            settings.support_enabled = True
        if seam_paint_present and not str(settings.seam_position or "").strip():
            settings.seam_position = "aligned"
        if fuzzy_paint_present and str(settings.fuzzy_skin or "none").strip().lower() == "none":
            settings.fuzzy_skin = "all"
        if brim_ears_present and float(getattr(settings, "brim_width", 0.0) or 0.0) <= 0.0:
            settings.brim_width = 3.0
        return settings

    def slice_current_plate(self):
        settings = self._settings_with_slice_defaults()
        self._slice_model(settings, activate_preview=True, show_dialog=True, show_errors=True)

    def slice_current_model(self):
        self.slice_current_plate()

    def print_current_plate(self, printer=None):
        source_path = self._get_plate_source_path()
        if not source_path:
            self._warn_no_plate_models()
            return
        meshes, combined = self._get_plate_meshes()
        if not meshes or combined is None:
            self._warn_plate_data_unavailable()
            return

        settings = self._settings_with_slice_defaults()
        reusable_path = self._resolve_reusable_gcode_path(settings)
        if reusable_path:
            self._send_existing_gcode(printer, reusable_path)
            return

        signature = self._build_slice_signature(settings)
        self._last_slice_meshes = [m for m in meshes]
        preferred_engine = self._slicer_engine_preference()
        perf = self._runtime_performance()
        status_hint = self._status_engine_text(preferred_engine, perf)
        dlg = self._busy_dialog("Print", f"Slicing & sending to printer ({status_hint})...\nPlease wait.")
        dlg.show()

        def do_print(mesh_items, combined_mesh, s, source, active_printer):
            if active_printer is not None and hasattr(self.printer_manager, "set_active_printer"):
                self.printer_manager.set_active_printer(active_printer)
            slice_payload = self._slice_with_selected_engine(
                mesh_items,
                combined_mesh,
                s,
                source,
                None,
            )
            gcode_path = str(slice_payload["gcode_path"])
            message = self.printer_manager.print_gcode(gcode_path, printer=active_printer)
            return {
                "gcode_path": gcode_path,
                "support_diagnostics": slice_payload.get("support_diagnostics"),
                "message": message,
            }

        worker = Worker(do_print, meshes, combined, settings, source_path, printer)

        def on_done(payload):
            dlg.close()
            if not isinstance(payload, dict):
                payload = {"message": str(payload), "gcode_path": None}
            message = str(payload.get("message", "Print request sent."))
            gcode_path = payload.get("gcode_path")
            if gcode_path and isinstance(gcode_path, str) and os.path.exists(gcode_path):
                try:
                    self._apply_slice_payload_to_preview(
                        payload,
                        settings,
                        signature,
                        preferred_engine,
                        perf,
                    )
                except Exception as exc:
                    self.statusBar().showMessage("Print failed")
                    QtWidgets.QMessageBox.critical(self.main, "Print error", str(exc))
                    return
            self.statusBar().showMessage(message)
            QtWidgets.QMessageBox.information(self.main, "Print", message)

        def on_err(msg):
            dlg.close()
            self.statusBar().showMessage("Print failed")
            QtWidgets.QMessageBox.critical(self.main, "Print error", msg)

        worker.signals.finished.connect(on_done)
        worker.signals.error.connect(on_err)
        self._start_worker(worker)

    def print_current_model(self, printer=None):
        self.print_current_plate(printer=printer)

    def export_gcode(self):
        source_path = self._get_plate_source_path()
        if not source_path:
            self._warn_no_plate_models()
            return
        meshes, combined = self._get_plate_meshes()
        if not meshes or combined is None:
            self._warn_plate_data_unavailable()
            return

        suggested = self._default_plate_gcode_path()
        out_path, _ = self._safe_get_save_file_name(
            "Export G-code",
            suggested,
            "G-code files (*.gcode);;All files (*.*)",
        )
        if not out_path:
            return
        if not out_path.lower().endswith(".gcode"):
            out_path = f"{out_path}.gcode"

        settings = self._settings_with_slice_defaults()
        signature = self._build_slice_signature(settings)
        self._last_slice_meshes = [m for m in meshes]
        preferred_engine = self._slicer_engine_preference()
        perf = self._runtime_performance()
        status_hint = self._status_engine_text(preferred_engine, perf)
        dlg = self._busy_dialog("Export", f"Exporting G-code ({status_hint})...\nPlease wait.")
        dlg.show()

        worker = Worker(
            self._slice_with_selected_engine,
            meshes,
            combined,
            settings,
            source_path,
            out_path,
        )

        def on_done(payload):
            dlg.close()
            try:
                slice_payload, _stats = self._apply_slice_payload_to_preview(
                    payload,
                    settings,
                    signature,
                    preferred_engine,
                    perf,
                )
            except Exception as exc:
                self.statusBar().showMessage("Export failed")
                QtWidgets.QMessageBox.critical(self.main, "Export error", str(exc))
                return
            gcode_path = str(slice_payload["gcode_path"])
            self.statusBar().showMessage(f"Exported G-code to {gcode_path}")
            QtWidgets.QMessageBox.information(self.main, "Export complete", f"G-code written to:\n{gcode_path}")

        def on_err(msg):
            dlg.close()
            self.statusBar().showMessage("Export failed")
            QtWidgets.QMessageBox.critical(self.main, "Export error", msg)

        worker.signals.finished.connect(on_done)
        worker.signals.error.connect(on_err)
        self._start_worker(worker)

    def _on_device_send_requested(self, printer):
        settings = self._settings_with_slice_defaults()
        gcode_path = self._resolve_reusable_gcode_path(settings)
        if gcode_path:
            self._send_existing_gcode(printer, gcode_path)
            return
        self.print_current_plate(printer=printer)

    def _on_device_save_requested(self):
        self.export_gcode()

    def _default_email_subject(self, printer: Mapping[str, object] | None) -> str:
        printer_name = ""
        if isinstance(printer, Mapping):
            printer_name = str(printer.get("name", "") or "").strip()
        if not printer_name:
            printer_name = str(getattr(getattr(self, "runtime_printer_state", None), "name", "") or "").strip()
        if self.current_model_id is not None and hasattr(self.viewer, "get_model_name"):
            model_name = str(self.viewer.get_model_name(self.current_model_id) or "").strip()
        else:
            model_name = ""
        if not model_name:
            model_name = self._default_plate_gcode_basename()
        if printer_name:
            return f"Print job handoff: {model_name} -> {printer_name}"
        return f"Print job handoff: {model_name}"

    def _device_email_context_lines(self, printer: Mapping[str, object] | None) -> list[str]:
        lines = [
            f"Generated from: {socket.gethostname()}",
        ]
        if isinstance(printer, Mapping):
            printer_name = str(printer.get("name", "") or "").strip()
            if printer_name:
                lines.append(f"Printer: {printer_name}")
            connector = str(printer.get("connector_type", "") or "").strip()
            if connector:
                lines.append(f"Connector: {connector}")
            for key in (
                "endpoint",
                "octoprint_url",
                "moonraker_url",
                "prusalink_url",
                "bambu_url",
                "creality_url",
            ):
                endpoint = str(printer.get(key, "") or "").strip()
                if endpoint:
                    lines.append(f"Endpoint: {endpoint}")
                    break
        if self.current_model_id is not None and hasattr(self.viewer, "get_model_name"):
            model_name = str(self.viewer.get_model_name(self.current_model_id) or "").strip()
            if model_name:
                lines.append(f"Model: {model_name}")
        plate_name = ""
        if hasattr(self.viewer, "get_current_plate_name"):
            plate_name = str(self.viewer.get_current_plate_name() or "").strip()
        if plate_name:
            lines.append(f"Plate: {plate_name}")
        if self._current_project_path:
            lines.append(f"Project path: {self._current_project_path}")
        if self._last_gcode_path:
            lines.append(f"G-code path: {self._last_gcode_path}")
        return lines

    def _device_email_body(self, printer: Mapping[str, object] | None, note: str) -> str:
        lines = ["EON-OpenSlicer print job handoff", ""]
        lines.extend(self._device_email_context_lines(printer))
        cleaned_note = str(note or "").strip()
        if cleaned_note:
            lines.extend(["", "Operator note:", cleaned_note])
        return "\n".join(lines).strip() + "\n"

    def _on_device_email_requested(self):
        printer = self.device_view.current_printer() if hasattr(self, "device_view") else None
        last_recipient = ""
        if hasattr(self, "_ui_settings") and self._ui_settings is not None:
            last_recipient = str(self._ui_settings.value("email/last_recipient", "") or "").strip()
        dialog = EmailComposeDialog(
            recipient=last_recipient,
            subject=self._default_email_subject(printer),
            context_lines=self._device_email_context_lines(printer),
            parent=self.main,
        )
        if dialog.exec_() != QtWidgets.QDialog.Accepted:
            self.statusBar().showMessage("Email cancelled")
            return

        payload = dialog.payload()
        recipient = str(payload.get("recipient", "") or "").strip()
        subject = str(payload.get("subject", "") or "").strip()
        note = str(payload.get("note", "") or "").strip()
        body = self._device_email_body(printer, note)

        if hasattr(self, "_ui_settings") and self._ui_settings is not None:
            self._ui_settings.setValue("email/last_recipient", recipient)
            self._ui_settings.sync()

        try:
            smtp_result = send_email_via_smtp(recipient=recipient, subject=subject, body=body)
            sender = str(smtp_result.get("sender", "no-reply@printnet.local"))
            message = f"Email sent to {recipient} via SMTP."
            self.statusBar().showMessage(message)
            QtWidgets.QMessageBox.information(
                self.main,
                "Send email",
                f"{message}\n\nFrom: {sender}",
            )
            return
        except (EmailConfigurationError, EmailDeliveryError) as exc:
            fallback_error = str(exc).strip()

        reply = QtWidgets.QMessageBox.question(
            self.main,
            "Send email",
            "SMTP delivery is unavailable.\n\n"
            f"{fallback_error}\n\n"
            "Open your default mail app with this draft instead?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.Yes,
        )
        if reply != QtWidgets.QMessageBox.Yes:
            self.statusBar().showMessage("Email fallback declined")
            return

        try:
            mailto_url = build_mailto_url(recipient=recipient, subject=subject, body=body)
        except EmailConfigurationError as exc:
            QtWidgets.QMessageBox.warning(self.main, "Send email", str(exc))
            self.statusBar().showMessage("Email fallback unavailable")
            return

        opened = QtGui.QDesktopServices.openUrl(QtCore.QUrl(mailto_url))
        if not opened:
            QtWidgets.QMessageBox.warning(
                self.main,
                "Send email",
                "Unable to open the default mail application for the fallback draft.",
            )
            self.statusBar().showMessage("Email fallback failed")
            return
        self.statusBar().showMessage("Opened fallback email draft")

    def _send_existing_gcode(self, printer, gcode_path: str):
        if not gcode_path or not os.path.exists(gcode_path):
            QtWidgets.QMessageBox.warning(self.main, "Print", "No reusable G-code available; slice the current plate first.")
            return
        dlg = self._busy_dialog("Print", "Sending G-code to printer...\nPlease wait.")
        dlg.show()

        def do_send(p, path):
            if hasattr(self.printer_manager, "set_active_printer"):
                self.printer_manager.set_active_printer(p)
            return self.printer_manager.print_gcode(path, printer=p)

        worker = Worker(do_send, printer, gcode_path)

        def on_done(msg):
            dlg.close()
            self.statusBar().showMessage(str(msg))
            QtWidgets.QMessageBox.information(self.main, "Print", str(msg))

        def on_err(msg):
            dlg.close()
            self.statusBar().showMessage("Print failed")
            QtWidgets.QMessageBox.critical(self.main, "Print error", msg)

        worker.signals.finished.connect(on_done)
        worker.signals.error.connect(on_err)
        self._start_worker(worker)

    def _read_gcode_preview(self, path: str, max_lines: int = 600) -> tuple[str, int]:
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except Exception:
            return "", 0
        total_lines = len(lines)
        if total_lines > max_lines:
            preview = "".join(lines[:max_lines])
            preview += f"\n; ... trimmed {total_lines - max_lines} lines\n"
        else:
            preview = "".join(lines)
        return preview, total_lines

    def _analyze_gcode(self, gcode_path: str, settings: SliceSettings) -> dict:
        return dict(estimate_gcode_file(gcode_path, settings))

    def _update_preview_from_gcode(self, gcode_path: str, stats: dict):
        if not hasattr(self, "preview_view"):
            return
        settings = self.settings_panel.to_settings() if hasattr(self, "settings_panel") else None
        preview_settings = settings
        if preview_settings is not None:
            try:
                active_printer = getattr(getattr(self, "printer_manager", None), "active_printer", None)
                printer_payload = dict(active_printer) if isinstance(active_printer, dict) else active_printer
                preview_settings, _resolved_payload = _resolve_slice_output_contract(
                    preview_settings,
                    runtime_printer_state=getattr(self, "runtime_printer_state", None),
                    printer=printer_payload,
                )
            except Exception:
                preview_settings = settings
        stats = dict(stats or {})
        if settings is not None and self._last_slice_meshes:
            try:
                ai_report = run_ai_checks(self._last_slice_meshes, settings)
                stats["ai_warnings"] = ai_report.warnings
                stats["ai_suggestions"] = ai_report.suggestions
            except Exception:
                stats.setdefault("ai_warnings", [])
                stats.setdefault("ai_suggestions", [])
        self._last_gcode_stats = dict(stats or {})
        preview_text = None
        preview_key = None
        try:
            stat = os.stat(gcode_path)
            preview_key = (gcode_path, float(stat.st_mtime), int(stat.st_size))
        except OSError:
            preview_key = None

        if preview_key is not None and preview_key == getattr(self, "_last_preview_key", None):
            preview_text = getattr(self, "_last_preview_text", None)
            preview = getattr(self, "_last_preview_data", None)
        else:
            preview = None

        if preview_text is None:
            preview_text, _total_lines = self._read_gcode_preview(gcode_path)
        if preview is None:
            try:
                preview = parse_gcode_preview_file(gcode_path, settings=preview_settings)
            except Exception as exc:
                stats["preview_parse_error"] = str(exc)
                self._log_slicer_activity("preview_parse_error", gcode_path=gcode_path, error=str(exc))
                try:
                    preview = parse_gcode_preview(preview_text.splitlines(), settings=preview_settings)
                except Exception:
                    preview = parse_gcode_preview([], settings=preview_settings)

        self.preview_view.set_gcode_text(preview_text)
        self.preview_view.update_stats(stats)
        if hasattr(self.viewer, "set_print_stats"):
            self.viewer.set_print_stats(stats)

        if hasattr(self.preview_view, "set_preview_settings"):
            self.preview_view.set_preview_settings(preview_settings)
        if hasattr(self.viewer, "set_preview_settings"):
            self.viewer.set_preview_settings(preview_settings)
        if hasattr(self.viewer, "set_gcode_preview"):
            self.viewer.set_gcode_preview(preview)
        self.preview_view.set_preview_data(preview)

        self._last_preview_key = preview_key
        self._last_preview_data = preview
        self._last_preview_text = preview_text

    def _clear_preview(self):
        self._last_gcode_path = None
        self._last_slice_signature = None
        self._slice_in_progress = False
        self._last_gcode_stats = None
        self._last_preview_key = None
        self._last_preview_data = None
        self._last_preview_text = None
        self._last_slice_meshes = None
        self._last_slicer_backend = None
        if not hasattr(self, "preview_view"):
            return
        self.preview_view.set_gcode_text("")
        self.preview_view.update_stats({})
        self.preview_view.set_steps_count(0)
        self.preview_view.set_layer_count(0)
        self.preview_view.set_preview_data(None)
        if hasattr(self.viewer, "clear_gcode_preview"):
            self.viewer.clear_gcode_preview()
        if hasattr(self.viewer, "clear_print_stats"):
            self.viewer.clear_print_stats()

    def _update_device_status(self):
        if not hasattr(self, "device_view") or not hasattr(self, "viewer"):
            return
        head_pos = None
        if hasattr(self.viewer, "get_preview_nozzle_state"):
            state = self.viewer.get_preview_nozzle_state()
            if state is not None:
                head_pos = tuple(float(v) for v in state[0])

        time_left = None
        pla_remaining = None
        pla_low = None
        stats = self._last_gcode_stats or {}
        total_time = stats.get("time_seconds")
        total_len = stats.get("length_mm")

        progress = None
        if hasattr(self.viewer, "get_preview_progress"):
            progress = self.viewer.get_preview_progress()

        if progress and total_time is not None:
            completed, total = progress
            if total > 0:
                ratio = max(0.0, min(1.0, float(completed) / float(total)))
                time_left = max(0.0, float(total_time)) * (1.0 - ratio)
                if total_len is not None:
                    remaining_mm = max(0.0, float(total_len)) * (1.0 - ratio)
                    pla_remaining = remaining_mm / 1000.0
                    pla_low = remaining_mm <= 2000.0

        self.device_view.update_live_status(
            head_pos=head_pos,
            time_left_s=time_left,
            pla_remaining_m=pla_remaining,
            pla_low=pla_low,
        )

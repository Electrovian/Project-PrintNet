from __future__ import annotations

import json
import os
import re
import tempfile
import uuid
from dataclasses import asdict
from typing import TYPE_CHECKING, Any

import numpy as np
import trimesh
from PyQt5 import QtCore, QtGui, QtWidgets

from ...workers import Worker
from config.defaults import DEFAULTS
from config.performance import resolve_performance_limits
from slicer_v2.legacy_ai_checks import run_ai_checks
from slicer_v2.legacy_gcode_preview import parse_gcode_preview, parse_gcode_preview_file
from slicer_v2.legacy_gcode_stats import estimate_gcode_file
from slicer_v2.legacy_gcode_writer import SliceSettings
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

    def _default_plate_gcode_basename(self) -> str:
        if not hasattr(self, "viewer"):
            return "plate"
        model_ids = list(self.viewer.get_model_ids())
        if not model_ids:
            return "plate"
        first_id = model_ids[0]
        first_path = str(self.viewer.get_model_path(first_id) or "").strip()
        if first_path:
            base_name = os.path.splitext(os.path.basename(first_path))[0]
        else:
            base_name = str(self.viewer.get_model_name(first_id) or "plate").strip()
        sanitized = _sanitize_gcode_basename(base_name)
        if len(model_ids) > 1:
            return _sanitize_gcode_basename(f"{sanitized}_plate")
        return sanitized

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
                }
            )
        if not models_payload:
            return None
        payload = {"models": models_payload, "settings": asdict(settings)}
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

    def _slice_with_v2_pipeline(
        self,
        meshes: list[trimesh.Trimesh],
        combined_mesh: trimesh.Trimesh,
        settings: SliceSettings,
        source_path: str | None,
        output_gcode_path: str | None,
        perf: dict[str, object],
    ) -> str:
        output_path = self._resolve_output_gcode_path(source_path, output_gcode_path)
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

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
                return str(
                    slice_v2_trimesh_auto(
                        meshes=mesh_items,
                        output_gcode_path=output_path,
                        settings=settings,
                        source_path=source_path,
                        combined_mesh=mesh_for_v2,
                    )
                )
            except Exception as exc:
                detailed_error = exc

        if create_v2_context is None or run_v2_pipeline is None:
            if detailed_error is not None:
                raise RuntimeError(
                    f"slicer_v2 detailed path failed and semantic pipeline is unavailable: {detailed_error}"
                ) from detailed_error
            raise RuntimeError("slicer_v2 pipeline is unavailable.")

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
            resolved_settings = asdict(settings)
            resolved_settings["gcode_validation_allow_negative_xy"] = True
            context = create_v2_context(
                job_id=f"eon-v2-{uuid.uuid4().hex[:12]}",
                mesh_path=temp_path,
                resolved_settings=resolved_settings,
                runtime_settings=runtime_settings,
            )
            result = run_v2_pipeline(context)
            gcode_artifact = result.context.stage_artifacts.get("gcode", {})
            lines_value = gcode_artifact.get("lines", [])
            if not isinstance(lines_value, list) or not lines_value:
                raise RuntimeError("slicer_v2 produced no G-code lines.")
            lines = [str(line) for line in lines_value]
            with open(output_path, "w", encoding="utf-8", newline="\n") as handle:
                handle.write("\n".join(lines).rstrip() + "\n")
            return output_path
        except Exception as exc:
            if detailed_error is not None:
                raise RuntimeError(
                    f"slicer_v2 detailed path failed: {detailed_error}; semantic pipeline failed: {exc}"
                ) from exc
            raise
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

    def _slice_with_selected_engine(
        self,
        meshes: list[trimesh.Trimesh],
        combined_mesh: trimesh.Trimesh,
        settings: SliceSettings,
        source_path: str | None,
        output_gcode_path: str | None,
    ) -> str:
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
            out_path = self._slice_with_v2_pipeline(
                meshes=meshes,
                combined_mesh=combined_mesh,
                settings=settings,
                source_path=source_path,
                output_gcode_path=output_gcode_path,
                perf=perf,
            )
            self._last_slicer_backend = "v2"
            self._log_slicer_activity("slice_success", engine="v2", output_path=out_path)
            return out_path
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

        def on_done(gcode_path):
            if dlg is not None:
                dlg.close()
            self._slice_in_progress = False
            self._last_gcode_path = gcode_path
            self._last_slice_signature = signature
            stats = self._analyze_gcode(gcode_path, settings)
            stats["slicer_engine"] = str(getattr(self, "_last_slicer_backend", preferred_engine))
            stats["cpu_threads"] = int(perf.get("max_threads", 1))
            stats["gpu_mode"] = str(perf.get("gpu_mode", "auto"))
            self._update_preview_from_gcode(gcode_path, stats)
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
        settings.support_enabled = True
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

        settings = self.settings_panel.to_settings()
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
            gcode_path = self._slice_with_selected_engine(
                mesh_items,
                combined_mesh,
                s,
                source,
                None,
            )
            message = self.printer_manager.print_gcode(gcode_path, printer=active_printer)
            return {"gcode_path": gcode_path, "message": message}

        worker = Worker(do_print, meshes, combined, settings, source_path, printer)

        def on_done(payload):
            dlg.close()
            if not isinstance(payload, dict):
                payload = {"message": str(payload), "gcode_path": None}
            gcode_path = payload.get("gcode_path")
            message = str(payload.get("message", "Print request sent."))
            if gcode_path and isinstance(gcode_path, str) and os.path.exists(gcode_path):
                self._last_gcode_path = gcode_path
                self._last_slice_signature = signature
                stats = self._analyze_gcode(gcode_path, settings)
                stats["slicer_engine"] = str(getattr(self, "_last_slicer_backend", preferred_engine))
                stats["cpu_threads"] = int(perf.get("max_threads", 1))
                stats["gpu_mode"] = str(perf.get("gpu_mode", "auto"))
                self._update_preview_from_gcode(gcode_path, stats)
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

        settings = self.settings_panel.to_settings()
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

        def on_done(gcode_path):
            dlg.close()
            self._last_gcode_path = gcode_path
            self._last_slice_signature = signature
            stats = self._analyze_gcode(gcode_path, settings)
            stats["slicer_engine"] = str(getattr(self, "_last_slicer_backend", preferred_engine))
            stats["cpu_threads"] = int(perf.get("max_threads", 1))
            stats["gpu_mode"] = str(perf.get("gpu_mode", "auto"))
            self._update_preview_from_gcode(gcode_path, stats)
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
        settings = self.settings_panel.to_settings()
        gcode_path = self._resolve_reusable_gcode_path(settings)
        if gcode_path:
            self._send_existing_gcode(printer, gcode_path)
            return
        self.print_current_plate(printer=printer)

    def _on_device_save_requested(self):
        self.export_gcode()

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
                preview = parse_gcode_preview_file(gcode_path, settings=settings)
            except Exception as exc:
                stats["preview_parse_error"] = str(exc)
                try:
                    preview = parse_gcode_preview(preview_text.splitlines(), settings=settings)
                except Exception:
                    preview = parse_gcode_preview([], settings=settings)

        self.preview_view.set_gcode_text(preview_text)
        self.preview_view.update_stats(stats)
        if hasattr(self.viewer, "set_print_stats"):
            self.viewer.set_print_stats(stats)

        if hasattr(self.preview_view, "set_preview_settings"):
            self.preview_view.set_preview_settings(settings)
        if hasattr(self.viewer, "set_preview_settings"):
            self.viewer.set_preview_settings(settings)
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

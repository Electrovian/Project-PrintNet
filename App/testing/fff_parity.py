from __future__ import annotations

import argparse
import hashlib
import json
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
APP_ROOT = REPO_ROOT / "App"
DEFAULT_MANIFEST_PATH = REPO_ROOT / "App/Tests/fixtures/fff_parity/corpus_manifest.json"
DEFAULT_PROFILE_PATH = REPO_ROOT / "App/Tests/fixtures/fff_parity/profile_fff_default.json"


def _bootstrap_import_paths() -> None:
    for candidate in (APP_ROOT, REPO_ROOT):
        candidate_text = str(candidate)
        if candidate_text not in sys.path:
            sys.path.insert(0, candidate_text)


if __package__ in (None, ""):
    _bootstrap_import_paths()

try:  # pragma: no cover - import path depends on caller cwd / sys.path setup
    from slicer_v2.context import create_context
    from slicer_v2.pipeline import STAGE_SEQUENCE, run_pipeline
except Exception:  # pragma: no cover
    _bootstrap_import_paths()
    from App.slicer_v2.context import create_context  # type: ignore
    from App.slicer_v2.pipeline import STAGE_SEQUENCE, run_pipeline  # type: ignore


@dataclass(frozen=True)
class ParityTolerance:
    path_count_abs: int = 2
    path_count_ratio: float = 0.05
    path_length_ratio: float = 0.07
    bridge_ratio_abs: float = 0.08
    tree_count_ratio: float = 0.10

    def to_dict(self) -> dict[str, object]:
        return {
            "path_count_abs": int(self.path_count_abs),
            "path_count_ratio": float(self.path_count_ratio),
            "path_length_ratio": float(self.path_length_ratio),
            "bridge_ratio_abs": float(self.bridge_ratio_abs),
            "tree_count_ratio": float(self.tree_count_ratio),
        }


class FffParityCorpusError(RuntimeError):
    pass


def _to_float(value: object, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return default
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    if not text:
        return default
    try:
        return float(text)
    except (TypeError, ValueError, OverflowError):
        return default


def _to_int(value: object, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    if isinstance(value, int):
        return int(value)
    if isinstance(value, float):
        return int(value)
    text = str(value).strip()
    if not text:
        return default
    try:
        return int(float(text))
    except (TypeError, ValueError, OverflowError):
        return default


def _stable_digest(payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _resolve_mesh_path(path_value: str) -> Path:
    candidate = Path(path_value).expanduser()
    if candidate.is_absolute():
        return candidate
    return (REPO_ROOT / candidate).resolve()


def _display_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(REPO_ROOT)).replace("\\", "/")
    except ValueError:
        return str(resolved)


def _collect_models(manifest_payload: dict[str, object]) -> list[dict[str, object]]:
    raw_models = manifest_payload.get("models", []) if isinstance(manifest_payload, dict) else []
    if not isinstance(raw_models, list) or not raw_models:
        raise FffParityCorpusError("FFF_PARITY_MANIFEST_MODELS_EMPTY")

    collected: list[dict[str, object]] = []
    malformed: list[str] = []
    missing: list[str] = []

    for index, item in enumerate(raw_models):
        if not isinstance(item, dict):
            malformed.append(f"index_{index}:not_a_dict")
            continue
        mesh_value = str(item.get("path", "")).strip()
        if not mesh_value:
            malformed.append(f"{str(item.get('id', f'index_{index}'))}:missing_path")
            continue
        mesh_path = _resolve_mesh_path(mesh_value)
        if not mesh_path.exists() or not mesh_path.is_file():
            missing.append(_display_path(mesh_path))
            continue
        collected.append(
            {
                "id": str(item.get("id", f"index_{index}")).strip() or f"index_{index}",
                "path": str(mesh_path),
                "settings_override": item.get("settings_override", {}),
            }
        )

    if malformed:
        raise FffParityCorpusError("FFF_PARITY_MANIFEST_INVALID:" + ";".join(malformed))
    if missing:
        raise FileNotFoundError("FFF_PARITY_CORPUS_MISSING_MODELS:" + ";".join(missing))
    if not collected:
        raise FileNotFoundError("FFF_PARITY_CORPUS_NO_VALID_MODELS")
    return collected


def _extract_metrics(stage_artifacts: dict[str, dict], stage_order: list[str], resolved_settings: dict[str, object]) -> dict[str, object]:
    perimeters = stage_artifacts.get("perimeters", {}) if isinstance(stage_artifacts.get("perimeters"), dict) else {}
    infill = stage_artifacts.get("infill", {}) if isinstance(stage_artifacts.get("infill"), dict) else {}
    supports = stage_artifacts.get("supports", {}) if isinstance(stage_artifacts.get("supports"), dict) else {}
    bridges = stage_artifacts.get("bridges", {}) if isinstance(stage_artifacts.get("bridges"), dict) else {}
    travel = stage_artifacts.get("travel", {}) if isinstance(stage_artifacts.get("travel"), dict) else {}
    gcode = stage_artifacts.get("gcode", {}) if isinstance(stage_artifacts.get("gcode"), dict) else {}
    slice_grid = stage_artifacts.get("slice_grid", {}) if isinstance(stage_artifacts.get("slice_grid"), dict) else {}

    layer_count = _to_int(slice_grid.get("layer_count"), 0)
    if layer_count <= 0:
        heights = slice_grid.get("layer_heights_mm", [])
        if isinstance(heights, list):
            layer_count = len(heights)

    metrics = {
        "layer_count": int(max(0, layer_count)),
        "stage_order": [str(item) for item in stage_order],
        "stage_presence": sorted(str(key) for key in stage_artifacts.keys()),
        "settings_digest": _stable_digest(resolved_settings),
        "settings_key_count": int(len(resolved_settings)),
        "path_counts": {
            "perimeter": _to_int(perimeters.get("perimeter_path_count"), 0),
            "infill": _to_int(infill.get("infill_path_count"), 0),
            "support": _to_int(supports.get("support_path_count"), 0),
            "solid": _to_int(bridges.get("solid_path_count_total"), 0),
            "bridge": _to_int(bridges.get("bridge_path_count"), 0),
            "travel": _to_int(travel.get("travel_move_count"), 0),
            "gcode_extrusion": _to_int(gcode.get("gcode_extrusion_command_count_total"), 0),
        },
        "path_lengths_mm": {
            "perimeter": _to_float(perimeters.get("perimeter_length_mm_total"), 0.0),
            "infill": _to_float(infill.get("infill_path_length_mm_total"), 0.0),
            "support": _to_float(supports.get("support_path_length_mm_total"), 0.0),
            "solid": _to_float(bridges.get("solid_path_length_mm_total"), 0.0),
            "bridge": _to_float(bridges.get("bridge_path_length_mm_total"), 0.0),
            "travel": _to_float(travel.get("travel_length_mm_total"), 0.0),
            "extrusion": _to_float(gcode.get("extrusion_path_length_mm_total"), 0.0),
        },
        "bridge_candidate_ratio_avg": _to_float(bridges.get("bridge_candidate_ratio_avg"), 0.0),
        "bridge_support_surface_ratio_avg": _to_float(bridges.get("bridge_support_surface_ratio_avg"), 0.0),
        "tree_branch_count_total": _to_int(supports.get("tree_branch_count_total"), 0),
        "tree_trunk_count_total": _to_int(supports.get("tree_trunk_count_total"), 0),
        "gcode_validation_ok": bool(gcode.get("gcode_validation_ok", False)),
        "gcode_validation_error_count": _to_int(gcode.get("gcode_validation_error_count"), 0),
    }
    return metrics


def run_fff_corpus(
    *,
    manifest_path: str | Path = DEFAULT_MANIFEST_PATH,
    profile_path: str | Path = DEFAULT_PROFILE_PATH,
    max_models: int | None = None,
    continue_on_error: bool = True,
    runtime_settings: dict[str, object] | None = None,
) -> dict[str, object]:
    manifest_file = Path(manifest_path).expanduser().resolve()
    profile_file = Path(profile_path).expanduser().resolve()
    manifest_payload = json.loads(manifest_file.read_text(encoding="utf-8"))
    profile_payload = json.loads(profile_file.read_text(encoding="utf-8"))

    if not isinstance(profile_payload, dict):
        raise ValueError("FFF_PARITY_PROFILE_INVALID")

    selected_models = _collect_models(manifest_payload)
    if max_models is not None:
        selected_models = selected_models[: max(0, int(max_models))]
    if not selected_models:
        raise FileNotFoundError("FFF_PARITY_CORPUS_NO_EXECUTABLE_MODELS")

    results: list[dict[str, object]] = []
    expected_stage_order = [stage_name for stage_name, _runner in STAGE_SEQUENCE]

    for index, item in enumerate(selected_models):
        model_id = str(item.get("id", f"index_{index}")).strip() or f"index_{index}"
        mesh_path = Path(str(item["path"]))

        settings = dict(profile_payload)
        override = item.get("settings_override", {})
        if isinstance(override, dict):
            settings.update(override)

        started = time.perf_counter()
        try:
            context = create_context(
                job_id=f"fff-parity-{model_id}-{uuid.uuid4().hex[:8]}",
                mesh_path=str(mesh_path),
                resolved_settings=settings,
                runtime_settings=dict(runtime_settings or {}),
            )
            pipeline_result = run_pipeline(context)
            runtime_ms = (time.perf_counter() - started) * 1000.0
            results.append(
                {
                    "model_id": model_id,
                    "mesh_path": _display_path(mesh_path),
                    "status": "ok",
                    "runtime_ms": float(runtime_ms),
                    "error": "",
                    "metrics": _extract_metrics(
                        stage_artifacts=pipeline_result.context.stage_artifacts,
                        stage_order=pipeline_result.context.stage_order_executed,
                        resolved_settings=pipeline_result.context.resolved_settings,
                    ),
                }
            )
        except Exception as exc:  # pragma: no cover - exception path is model/environment dependent
            runtime_ms = (time.perf_counter() - started) * 1000.0
            result = {
                "model_id": model_id,
                "mesh_path": _display_path(mesh_path),
                "status": "failed",
                "runtime_ms": float(runtime_ms),
                "error": str(exc),
            }
            results.append(result)
            if not continue_on_error:
                raise

    executed = sum(1 for item in results if str(item.get("status")) == "ok")
    failed = sum(1 for item in results if str(item.get("status")) == "failed")
    skipped = sum(1 for item in results if str(item.get("status")) == "skipped")

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "manifest_path": _display_path(manifest_file),
        "profile_path": _display_path(profile_file),
        "model_count": len(results),
        "executed_model_count": int(executed),
        "failed_model_count": int(failed),
        "skipped_model_count": int(skipped),
        "stage_order_expected": expected_stage_order,
        "results": results,
    }


def compare_report_payloads(
    current_payload: dict[str, object],
    baseline_payload: dict[str, object],
    *,
    tolerance: ParityTolerance | None = None,
) -> dict[str, object]:
    tol = tolerance or ParityTolerance()
    current_results = current_payload.get("results", [])
    baseline_results = baseline_payload.get("results", [])

    current_by_id = {
        str(item.get("model_id")): item
        for item in current_results
        if isinstance(item, dict) and str(item.get("status")) == "ok"
    }
    baseline_by_id = {
        str(item.get("model_id")): item
        for item in baseline_results
        if isinstance(item, dict) and str(item.get("status")) == "ok"
    }

    compared_ids = sorted(set(current_by_id.keys()) & set(baseline_by_id.keys()))
    issues: list[dict[str, object]] = []

    def _add_issue(model_id: str, code: str, message: str, *, current: object, baseline: object, limit: object) -> None:
        issues.append(
            {
                "model_id": model_id,
                "severity": "error",
                "code": code,
                "message": message,
                "current": current,
                "baseline": baseline,
                "tolerance": limit,
            }
        )

    for model_id in compared_ids:
        current_item = current_by_id[model_id]
        baseline_item = baseline_by_id[model_id]
        current_metrics = current_item.get("metrics", {}) if isinstance(current_item.get("metrics"), dict) else {}
        baseline_metrics = baseline_item.get("metrics", {}) if isinstance(baseline_item.get("metrics"), dict) else {}

        for key in ("layer_count", "settings_digest"):
            if current_metrics.get(key) != baseline_metrics.get(key):
                _add_issue(
                    model_id,
                    f"exact_mismatch:{key}",
                    f"Exact parity mismatch for {key}",
                    current=current_metrics.get(key),
                    baseline=baseline_metrics.get(key),
                    limit="exact",
                )

        if current_metrics.get("stage_order") != baseline_metrics.get("stage_order"):
            _add_issue(
                model_id,
                "exact_mismatch:stage_order",
                "Stage order mismatch",
                current=current_metrics.get("stage_order"),
                baseline=baseline_metrics.get("stage_order"),
                limit="exact",
            )
        if current_metrics.get("stage_presence") != baseline_metrics.get("stage_presence"):
            _add_issue(
                model_id,
                "exact_mismatch:stage_presence",
                "Stage presence mismatch",
                current=current_metrics.get("stage_presence"),
                baseline=baseline_metrics.get("stage_presence"),
                limit="exact",
            )

        current_path_counts = current_metrics.get("path_counts", {})
        baseline_path_counts = baseline_metrics.get("path_counts", {})
        if isinstance(current_path_counts, dict) and isinstance(baseline_path_counts, dict):
            for metric_name in sorted(set(current_path_counts.keys()) | set(baseline_path_counts.keys())):
                current_value = _to_int(current_path_counts.get(metric_name), 0)
                baseline_value = _to_int(baseline_path_counts.get(metric_name), 0)
                delta = abs(current_value - baseline_value)
                max_delta = max(int(tol.path_count_abs), int(round(abs(baseline_value) * tol.path_count_ratio)))
                if delta > max_delta:
                    _add_issue(
                        model_id,
                        f"path_count_delta:{metric_name}",
                        f"Path count delta exceeds tolerance for {metric_name}",
                        current=current_value,
                        baseline=baseline_value,
                        limit=max_delta,
                    )

        current_path_lengths = current_metrics.get("path_lengths_mm", {})
        baseline_path_lengths = baseline_metrics.get("path_lengths_mm", {})
        if isinstance(current_path_lengths, dict) and isinstance(baseline_path_lengths, dict):
            for metric_name in sorted(set(current_path_lengths.keys()) | set(baseline_path_lengths.keys())):
                current_value = _to_float(current_path_lengths.get(metric_name), 0.0)
                baseline_value = _to_float(baseline_path_lengths.get(metric_name), 0.0)
                delta = abs(current_value - baseline_value)
                max_delta = abs(baseline_value) * tol.path_length_ratio
                if baseline_value <= 1e-6:
                    max_delta = tol.path_count_abs * 0.5
                if delta > max_delta:
                    _add_issue(
                        model_id,
                        f"path_length_delta:{metric_name}",
                        f"Path length delta exceeds tolerance for {metric_name}",
                        current=current_value,
                        baseline=baseline_value,
                        limit=max_delta,
                    )

        for key in ("bridge_candidate_ratio_avg", "bridge_support_surface_ratio_avg"):
            current_value = _to_float(current_metrics.get(key), 0.0)
            baseline_value = _to_float(baseline_metrics.get(key), 0.0)
            if abs(current_value - baseline_value) > tol.bridge_ratio_abs:
                _add_issue(
                    model_id,
                    f"bridge_ratio_delta:{key}",
                    f"Bridge ratio delta exceeds tolerance for {key}",
                    current=current_value,
                    baseline=baseline_value,
                    limit=tol.bridge_ratio_abs,
                )

        for key in ("tree_branch_count_total", "tree_trunk_count_total"):
            current_value = _to_int(current_metrics.get(key), 0)
            baseline_value = _to_int(baseline_metrics.get(key), 0)
            max_delta = max(1, int(round(abs(baseline_value) * tol.tree_count_ratio)))
            if abs(current_value - baseline_value) > max_delta:
                _add_issue(
                    model_id,
                    f"tree_count_delta:{key}",
                    f"Tree count delta exceeds tolerance for {key}",
                    current=current_value,
                    baseline=baseline_value,
                    limit=max_delta,
                )

        current_validation_errors = _to_int(current_metrics.get("gcode_validation_error_count"), 0)
        if current_validation_errors > 0 or not bool(current_metrics.get("gcode_validation_ok", False)):
            _add_issue(
                model_id,
                "gcode_validation_error",
                "G-code validation has hard errors",
                current=current_validation_errors,
                baseline=_to_int(baseline_metrics.get("gcode_validation_error_count"), 0),
                limit=0,
            )

    if not compared_ids:
        issues.append(
            {
                "model_id": "",
                "severity": "error",
                "code": "no_comparable_models",
                "message": "No executable models were available for parity comparison.",
                "current": current_payload.get("model_count", 0),
                "baseline": baseline_payload.get("model_count", 0),
                "tolerance": "exact",
            }
        )

    return {
        "ok": len(issues) == 0,
        "compared_model_count": len(compared_ids),
        "issue_count": len(issues),
        "issues": issues,
        "tolerance": tol.to_dict(),
    }


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run slicer_v2 FFF parity corpus and emit metrics JSON.")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST_PATH), help="Corpus manifest JSON path.")
    parser.add_argument("--profile", default=str(DEFAULT_PROFILE_PATH), help="Deterministic profile JSON path.")
    parser.add_argument("--output", default="", help="Optional output JSON path.")
    parser.add_argument("--baseline", default="", help="Optional baseline JSON path for tolerance comparison.")
    parser.add_argument("--max-models", type=int, default=0, help="Optional model cap for quick runs.")
    parser.add_argument("--fail-fast", action="store_true", help="Stop on first model slicing failure.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        report = run_fff_corpus(
            manifest_path=args.manifest,
            profile_path=args.profile,
            max_models=(args.max_models if args.max_models > 0 else None),
            continue_on_error=not bool(args.fail_fast),
        )

        payload: dict[str, object] = dict(report)
        if args.baseline:
            baseline_payload = json.loads(Path(args.baseline).expanduser().read_text(encoding="utf-8"))
            payload["comparison"] = compare_report_payloads(payload, baseline_payload)

        if args.output:
            _write_json(Path(args.output).expanduser(), payload)
        print(json.dumps(payload, indent=2))
        if args.baseline and isinstance(payload.get("comparison"), dict) and not bool(payload["comparison"].get("ok")):
            return 1
        return 0
    except Exception as exc:
        payload = {
            "ok": False,
            "error": str(exc),
            "manifest_path": str(Path(args.manifest).expanduser()),
            "profile_path": str(Path(args.profile).expanduser()),
        }
        if args.output:
            _write_json(Path(args.output).expanduser(), payload)
        print(json.dumps(payload, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

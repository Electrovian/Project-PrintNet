from __future__ import annotations

import argparse
import json
from pathlib import Path
from time import perf_counter
import uuid

from .cli_contract import (
    CliExitCode,
    CliRunResult,
    SlicedPlateInfo,
    normalize_error_string,
    write_result_json,
)
from .context import create_context
from .pipeline import STAGE_SEQUENCE, run_pipeline
from .profile_compat import (
    ProfileCompatConfigError,
    ProfileCompatFileNotFoundError,
    apply_cli_setting_overrides,
    load_and_merge_profiles,
    resolve_downward_compatible_machines,
)


DEFAULT_CLI_CONFIG_PATH = (
    Path(__file__).resolve().parents[1]
    / "printer_presets/seed_resources/profiles/BBL/cli_config.json"
)


class CliParameterError(ValueError):
    pass


class CliUnsupportedError(ValueError):
    pass


def _flatten_multi_arg(values: list[list[str]] | None) -> list[str]:
    if not values:
        return []
    flattened: list[str] = []
    for group in values:
        for value in group:
            text = str(value).strip()
            if text:
                flattened.append(text)
    return flattened


def _dedupe_preserve_order(values: list[str]) -> list[str]:
    output: list[str] = []
    seen: set[str] = set()
    for value in values:
        key = str(value)
        if key in seen:
            continue
        seen.add(key)
        output.append(key)
    return output


def _resolve_input_paths(args: argparse.Namespace) -> list[str]:
    paths = _flatten_multi_arg(args.input)
    mesh_path = str(args.mesh_path or "").strip()
    if mesh_path:
        paths.append(mesh_path)
    return _dedupe_preserve_order(paths)


def _resolve_output_gcode_path(input_path: Path, outputdir: str) -> Path:
    outdir = str(outputdir or "").strip()
    filename = f"{input_path.stem}.gcode"
    if not outdir:
        return input_path.with_suffix(".gcode")
    target_dir = Path(outdir).expanduser()
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir / filename


def _resolve_result_path(args: argparse.Namespace, input_path: Path | None) -> Path:
    explicit_result = str(args.result_path or "").strip()
    if explicit_result:
        return Path(explicit_result).expanduser()

    legacy_report = str(args.report_path or "").strip()
    if legacy_report:
        return Path(legacy_report).expanduser()

    outputdir = str(args.outputdir or "").strip()
    if outputdir:
        return Path(outputdir).expanduser() / "result.json"

    if input_path is not None:
        return input_path.parent / "result.json"
    return Path.cwd() / "result.json"


def _set_failure(
    run_result: CliRunResult,
    exit_code: CliExitCode,
    error_message: str | None = None,
) -> None:
    run_result.return_code = int(exit_code)
    run_result.error_string = normalize_error_string(int(exit_code), error_message)
    if not run_result.sliced_plates:
        run_result.plate_index = 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="EON-OpenSlicer slicer_v2 CLI")
    parser.add_argument(
        "--input",
        action="append",
        nargs="+",
        default=[],
        help="Input STL/OBJ path. May be repeated.",
    )
    parser.add_argument(
        "--mesh-path",
        default="",
        help="Backward-compatible alias for --input.",
    )
    parser.add_argument("--layer-height", type=float, default=None, help="Layer height in mm.")
    parser.add_argument("--model-height-mm", type=float, default=None, help="Model height hint in mm.")
    parser.add_argument("--infill-percent", type=float, default=None, help="Infill density percent.")
    parser.add_argument(
        "--support-enabled",
        action="store_true",
        default=None,
        help="Enable supports (CLI override).",
    )
    parser.add_argument(
        "--load-settings",
        action="append",
        nargs="+",
        default=[],
        help="Machine/process profile JSON path. May be repeated.",
    )
    parser.add_argument(
        "--load-filaments",
        action="append",
        nargs="+",
        default=[],
        help="Filament profile JSON path. May be repeated.",
    )
    parser.add_argument("--outputdir", default="", help="Optional output directory for generated G-code.")
    parser.add_argument("--result-path", default="", help="Path to result JSON output.")
    parser.add_argument("--report-path", default="", help="Backward-compatible alias for --result-path.")
    parser.add_argument("--downward-check", action="store_true", help="Enable downward compatibility lookup.")
    parser.add_argument(
        "--cli-config-path",
        default=str(DEFAULT_CLI_CONFIG_PATH),
        help="Path to EON-compatible cli_config.json.",
    )
    parser.add_argument("--printer-name", default="", help="Printer preset name for downward compatibility lookup.")
    parser.add_argument("--printer-model", default="", help="Printer model key for downward compatibility lookup.")
    parser.add_argument("--slice", type=int, default=0, help="Plate selector (single-plate mode supports 0 or 1).")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    run_started = perf_counter()
    run_result = CliRunResult()
    summary: dict[str, object] = {}
    input_path: Path | None = None
    result_path = _resolve_result_path(args, None)

    try:
        input_paths = _resolve_input_paths(args)
        if not input_paths:
            raise CliParameterError("No input mesh was provided.")
        if len(input_paths) > 1:
            raise CliUnsupportedError("Multiple input meshes are not supported in single-plate mode.")

        input_path = Path(input_paths[0]).expanduser()
        result_path = _resolve_result_path(args, input_path)
        if not input_path.exists() or not input_path.is_file():
            raise ProfileCompatFileNotFoundError(f"MISSING_INPUT_FILE:{input_path}")

        if args.slice < 0:
            raise CliParameterError("slice must be >= 0.")
        if args.slice > 1:
            raise CliUnsupportedError("slice values > 1 are not supported in single-plate mode.")
        if input_path.suffix.casefold() == ".3mf":
            raise CliUnsupportedError(".3mf input is not supported in this phase.")

        if args.downward_check:
            if not str(args.printer_name).strip() or not str(args.printer_model).strip():
                raise CliParameterError("downward-check requires printer-name and printer-model.")

        setting_files = _flatten_multi_arg(args.load_settings)
        filament_files = _flatten_multi_arg(args.load_filaments)
        merge_report = load_and_merge_profiles(setting_files, filament_files)
        resolved_settings = apply_cli_setting_overrides(
            merge_report.normalized_settings,
            layer_height=args.layer_height,
            model_height_mm=args.model_height_mm,
            infill_percent=args.infill_percent,
            support_enabled=args.support_enabled,
        )

        compat_warnings: list[str] = []
        if args.downward_check:
            compat = resolve_downward_compatible_machines(
                cli_config_path=str(args.cli_config_path),
                printer_model=str(args.printer_model),
                printer_name=str(args.printer_name),
            )
            run_result.downward_compatible_machine = compat.downward_compatible_machine
            compat_warnings = list(compat.warnings)

        run_result.prepare_time = perf_counter() - run_started

        context = create_context(
            job_id=f"slicer-v2-{uuid.uuid4().hex[:12]}",
            mesh_path=str(input_path),
            resolved_settings=resolved_settings,
        )
        slice_started = perf_counter()
        pipeline_result = run_pipeline(context)
        slice_elapsed = perf_counter() - slice_started

        gcode_artifact = pipeline_result.context.stage_artifacts.get("gcode", {})
        lines = gcode_artifact.get("lines")
        if not isinstance(lines, list) or not lines:
            raise RuntimeError("slicer_v2 produced no G-code lines.")

        output_path = _resolve_output_gcode_path(input_path, str(args.outputdir))
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_text = "\n".join(str(line) for line in lines).rstrip() + "\n"
        output_path.write_text(output_text, encoding="utf-8", newline="\n")

        mesh_artifact = pipeline_result.context.stage_artifacts.get("mesh", {})
        triangle_count = int(mesh_artifact.get("triangle_count", 0))
        run_result.plate_index = 1
        run_result.return_code = int(CliExitCode.CLI_SUCCESS)
        run_result.error_string = normalize_error_string(int(CliExitCode.CLI_SUCCESS))
        run_result.sliced_plates = [
            SlicedPlateInfo(
                plate_id=1,
                sliced_time=slice_elapsed,
                sliced_time_with_cache=slice_elapsed,
                triangle_count=triangle_count,
                warning_message="",
            )
        ]

        summary = {
            "job_id": pipeline_result.context.job_id,
            "mesh_path": pipeline_result.context.mesh_path,
            "stage_count": len(pipeline_result.context.stage_order_executed),
            "expected_stage_count": len(STAGE_SEQUENCE),
            "stages_executed": pipeline_result.context.stage_order_executed,
            "artifact_keys": sorted(pipeline_result.context.stage_artifacts.keys()),
            "gcode_line_count": int(gcode_artifact.get("line_count", 0)),
            "validation_ok": bool(pipeline_result.validation.ok),
            "gcode_path": str(output_path.resolve()),
            "profile_warning_count": int(len(merge_report.warnings)),
            "profile_warnings": merge_report.warnings,
            "compat_warning_count": int(len(compat_warnings)),
            "compat_warnings": compat_warnings,
        }
    except CliParameterError as exc:
        _set_failure(run_result, CliExitCode.CLI_INVALID_PARAMS, str(exc))
    except CliUnsupportedError as exc:
        _set_failure(run_result, CliExitCode.CLI_UNSUPPORTED_OPERATION, str(exc))
    except ProfileCompatFileNotFoundError as exc:
        _set_failure(run_result, CliExitCode.CLI_FILE_NOTFOUND, str(exc))
    except ProfileCompatConfigError as exc:
        _set_failure(run_result, CliExitCode.CLI_CONFIG_FILE_ERROR, str(exc))
    except Exception as exc:  # pragma: no cover - runtime failures are environment/data dependent
        _set_failure(run_result, CliExitCode.CLI_SLICING_ERROR, str(exc))

    run_result.export_time = perf_counter() - run_started
    result_json_path = write_result_json(result_path, run_result)
    payload = run_result.to_contract_payload()
    payload["result_path"] = result_json_path
    payload.update(summary)

    print(json.dumps(payload, indent=2))
    return int(run_result.return_code)


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

from dataclasses import asdict, dataclass
import os
import subprocess
import sys
import time
from typing import Callable, Mapping, Sequence


class DesktopRegressionError(Exception):
    """Desktop regression automation validation/runtime failure."""


@dataclass(frozen=True)
class RegressionCase:
    case_id: str
    modules: tuple[str, ...]
    max_seconds: float = 20.0


@dataclass(frozen=True)
class RegressionRunConfig:
    python_executable: str = sys.executable
    working_directory: str | None = None
    stop_on_failure: bool = False
    default_max_seconds: float = 20.0


@dataclass(frozen=True)
class CommandExecutionResult:
    exit_code: int
    stdout: str
    stderr: str
    timed_out: bool = False


@dataclass(frozen=True)
class RegressionCaseResult:
    case_id: str
    ok: bool
    exit_code: int
    duration_s: float
    timed_out: bool
    module_count: int
    command: tuple[str, ...]
    stdout: str
    stderr: str


@dataclass(frozen=True)
class DesktopRegressionReport:
    ok: bool
    case_count: int
    passed_case_count: int
    failed_case_count: int
    total_duration_s: float
    failed_case_ids: tuple[str, ...]
    results: tuple[RegressionCaseResult, ...]


CommandExecutor = Callable[[Sequence[str], float, str | None], CommandExecutionResult]


def default_desktop_regression_cases() -> tuple[RegressionCase, ...]:
    return (
        RegressionCase(case_id="desktop_plate_flow", modules=("App.Tests.test_desktop_plate_flow",), max_seconds=20.0),
        RegressionCase(
            case_id="desktop_runtime_printer_state",
            modules=("App.Tests.test_runtime_printer_state",),
            max_seconds=20.0,
        ),
        RegressionCase(case_id="connector_registry", modules=("App.Tests.test_connector_registry",), max_seconds=20.0),
        RegressionCase(
            case_id="local_wifi_onboarding",
            modules=("App.Tests.test_local_wifi_onboarding",),
            max_seconds=20.0,
        ),
    )


def run_regression_cases(
    cases: Sequence[RegressionCase],
    *,
    config: RegressionRunConfig | None = None,
    executor: CommandExecutor | None = None,
) -> DesktopRegressionReport:
    resolved_config = _validate_config(config or RegressionRunConfig())
    validated_cases = _validate_cases(cases, resolved_config.default_max_seconds)
    resolved_executor = executor or _default_executor

    results: list[RegressionCaseResult] = []
    failed_case_ids: list[str] = []
    total_duration_s = 0.0

    for case in validated_cases:
        command = _build_command(case=case, python_executable=resolved_config.python_executable)
        started = time.perf_counter()
        execution = resolved_executor(command, case.max_seconds, resolved_config.working_directory)
        duration_s = max(0.0, time.perf_counter() - started)
        total_duration_s += duration_s

        ok = int(execution.exit_code) == 0 and not bool(execution.timed_out)
        if not ok:
            failed_case_ids.append(case.case_id)

        results.append(
            RegressionCaseResult(
                case_id=case.case_id,
                ok=ok,
                exit_code=int(execution.exit_code),
                duration_s=duration_s,
                timed_out=bool(execution.timed_out),
                module_count=len(case.modules),
                command=tuple(command),
                stdout=str(execution.stdout or ""),
                stderr=str(execution.stderr or ""),
            )
        )

        if resolved_config.stop_on_failure and not ok:
            break

    passed_case_count = sum(1 for item in results if item.ok)
    failed_case_count = len(results) - passed_case_count
    return DesktopRegressionReport(
        ok=failed_case_count == 0,
        case_count=len(results),
        passed_case_count=passed_case_count,
        failed_case_count=failed_case_count,
        total_duration_s=total_duration_s,
        failed_case_ids=tuple(failed_case_ids),
        results=tuple(results),
    )


def report_to_dict(report: DesktopRegressionReport, *, include_output: bool = True) -> dict[str, object]:
    payload: dict[str, object] = {
        "ok": bool(report.ok),
        "case_count": int(report.case_count),
        "passed_case_count": int(report.passed_case_count),
        "failed_case_count": int(report.failed_case_count),
        "total_duration_s": float(report.total_duration_s),
        "failed_case_ids": list(report.failed_case_ids),
        "results": [],
    }
    rows: list[dict[str, object]] = []
    for result in report.results:
        row = asdict(result)
        if not include_output:
            row["stdout"] = ""
            row["stderr"] = ""
        rows.append(row)
    payload["results"] = rows
    return payload


def _validate_config(config: RegressionRunConfig) -> RegressionRunConfig:
    python_executable = str(config.python_executable or "").strip()
    if not python_executable:
        raise DesktopRegressionError("DESKTOP_REGRESSION_PYTHON_REQUIRED: python_executable is required.")

    default_max_seconds = float(config.default_max_seconds)
    if default_max_seconds <= 0.0:
        raise DesktopRegressionError(
            "DESKTOP_REGRESSION_DEFAULT_TIMEOUT_INVALID: default_max_seconds must be > 0."
        )

    working_directory = config.working_directory
    if working_directory is not None:
        value = str(working_directory).strip()
        if not value:
            working_directory = None
        elif not os.path.isdir(value):
            raise DesktopRegressionError(
                f"DESKTOP_REGRESSION_WORKDIR_INVALID: working directory does not exist: {value}"
            )
        else:
            working_directory = value

    return RegressionRunConfig(
        python_executable=python_executable,
        working_directory=working_directory,
        stop_on_failure=bool(config.stop_on_failure),
        default_max_seconds=default_max_seconds,
    )


def _validate_cases(cases: Sequence[RegressionCase], default_max_seconds: float) -> tuple[RegressionCase, ...]:
    if not cases:
        raise DesktopRegressionError("DESKTOP_REGRESSION_CASES_REQUIRED: at least one case is required.")

    validated: list[RegressionCase] = []
    seen = set()
    for raw_case in cases:
        case_id = str(getattr(raw_case, "case_id", "") or "").strip().lower()
        if not case_id:
            raise DesktopRegressionError("DESKTOP_REGRESSION_CASE_ID_REQUIRED: case_id is required.")
        if case_id in seen:
            raise DesktopRegressionError(f"DESKTOP_REGRESSION_DUPLICATE_CASE_ID: {case_id}")
        seen.add(case_id)

        raw_modules = tuple(getattr(raw_case, "modules", ()) or ())
        modules: list[str] = []
        for module in raw_modules:
            value = str(module or "").strip()
            if not value:
                continue
            modules.append(value)
        if not modules:
            raise DesktopRegressionError(f"DESKTOP_REGRESSION_MODULES_REQUIRED: {case_id}")

        case_timeout = float(getattr(raw_case, "max_seconds", 0.0) or 0.0)
        if case_timeout <= 0.0:
            case_timeout = float(default_max_seconds)
        if case_timeout <= 0.0:
            raise DesktopRegressionError(f"DESKTOP_REGRESSION_TIMEOUT_INVALID: {case_id}")

        validated.append(
            RegressionCase(
                case_id=case_id,
                modules=tuple(modules),
                max_seconds=case_timeout,
            )
        )
    return tuple(validated)


def _build_command(case: RegressionCase, python_executable: str) -> tuple[str, ...]:
    command = [str(python_executable), "-m", "unittest"]
    for module in case.modules:
        command.append(str(module))
    return tuple(command)


def _default_executor(
    command: Sequence[str],
    timeout_s: float,
    working_directory: str | None,
) -> CommandExecutionResult:
    try:
        completed = subprocess.run(
            list(command),
            cwd=working_directory,
            check=False,
            text=True,
            capture_output=True,
            timeout=float(timeout_s),
        )
    except subprocess.TimeoutExpired as exc:
        stdout = str(getattr(exc, "stdout", "") or "")
        stderr = str(getattr(exc, "stderr", "") or "")
        return CommandExecutionResult(exit_code=124, stdout=stdout, stderr=stderr, timed_out=True)

    return CommandExecutionResult(
        exit_code=int(completed.returncode),
        stdout=str(completed.stdout or ""),
        stderr=str(completed.stderr or ""),
        timed_out=False,
    )


def summarize_failures(report: DesktopRegressionReport) -> tuple[str, ...]:
    summaries: list[str] = []
    for result in report.results:
        if result.ok:
            continue
        summaries.append(
            f"{result.case_id}: exit_code={result.exit_code}, timed_out={result.timed_out}, duration_s={result.duration_s:.2f}"
        )
    return tuple(summaries)


def report_metadata(report: DesktopRegressionReport) -> Mapping[str, object]:
    return {
        "ok": bool(report.ok),
        "case_count": int(report.case_count),
        "passed_case_count": int(report.passed_case_count),
        "failed_case_count": int(report.failed_case_count),
        "total_duration_s": float(report.total_duration_s),
        "failed_case_ids": list(report.failed_case_ids),
    }

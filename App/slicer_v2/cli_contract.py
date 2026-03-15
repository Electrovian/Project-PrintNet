from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import IntEnum
from pathlib import Path


class CliExitCode(IntEnum):
    CLI_SUCCESS = 0
    CLI_INVALID_PARAMS = -2
    CLI_FILE_NOTFOUND = -3
    CLI_CONFIG_FILE_ERROR = -5
    CLI_UNSUPPORTED_OPERATION = -8
    CLI_SLICING_ERROR = -100


CLI_ERROR_MESSAGES: dict[CliExitCode, str] = {
    CliExitCode.CLI_SUCCESS: "Success.",
    CliExitCode.CLI_INVALID_PARAMS: "Invalid parameters to the slicer.",
    CliExitCode.CLI_FILE_NOTFOUND: "The input files to the slicer are not found.",
    CliExitCode.CLI_CONFIG_FILE_ERROR: "The input preset file is invalid and can not be parsed.",
    CliExitCode.CLI_UNSUPPORTED_OPERATION: "Unsupported CLI instruction.",
    CliExitCode.CLI_SLICING_ERROR: "Failed slicing the model.",
}


@dataclass
class SlicedPlateInfo:
    plate_id: int = 1
    sliced_time: float = 0.0
    sliced_time_with_cache: float = 0.0
    triangle_count: int = 0
    warning_message: str = ""

    def to_dict(self) -> dict[str, object]:
        return {
            "id": int(self.plate_id),
            "sliced_time": float(self.sliced_time),
            "sliced_time_with_cache": float(self.sliced_time_with_cache),
            "triangle_count": int(self.triangle_count),
            "warning_message": str(self.warning_message),
        }


@dataclass
class CliRunResult:
    plate_index: int = 1
    return_code: int = int(CliExitCode.CLI_SUCCESS)
    error_string: str = CLI_ERROR_MESSAGES[CliExitCode.CLI_SUCCESS]
    prepare_time: float = 0.0
    export_time: float = 0.0
    sliced_plates: list[SlicedPlateInfo] = field(default_factory=list)
    downward_compatible_machine: list[str] = field(default_factory=list)

    def to_contract_payload(self) -> dict[str, object]:
        return {
            "plate_index": int(self.plate_index),
            "return_code": int(self.return_code),
            "error_string": str(self.error_string),
            "prepare_time": float(self.prepare_time),
            "export_time": float(self.export_time),
            "sliced_plates": [item.to_dict() for item in self.sliced_plates],
            "downward_compatible_machine": [str(item) for item in self.downward_compatible_machine],
        }


def normalize_error_string(code: int, override: str | None = None) -> str:
    if override:
        text = str(override).strip()
        if text:
            return text
    try:
        enum_code = CliExitCode(int(code))
    except ValueError:
        return f"CLI error {int(code)}."
    return CLI_ERROR_MESSAGES.get(enum_code, f"CLI error {int(enum_code)}.")


def write_result_json(path: str | Path, result: CliRunResult) -> str:
    output = Path(path).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = result.to_contract_payload()
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return str(output.resolve())

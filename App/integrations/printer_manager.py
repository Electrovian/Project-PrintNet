from typing import List, Dict

from slicer.slicer import slice_file
from slicer.gcode import SliceSettings
from .octoprint_api import upload_and_print

class PrinterManager:
    """High-level helper to slice and send to printer."""
    def __init__(self, printers: List[Dict], airtable_cfg: Dict):
        self.printers = printers
        self.airtable_cfg = airtable_cfg
        # For now we just use the first printer.
        self.active_printer = printers[0] if printers else None

    def slice_and_print(self, stl_path: str, settings: SliceSettings) -> str:
        gcode_path = slice_file(stl_path, settings=settings)
        if not self.active_printer:
            return (f"No printer configured. G-code generated at "
                    f"{gcode_path}")
        url = self.active_printer.get("octoprint_url", "")
        api_key = self.active_printer.get("octoprint_api_key", "")
        return upload_and_print(url, api_key, gcode_path)

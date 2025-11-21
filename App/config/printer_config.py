import os
from typing import List, Tuple, Dict

import pandas as pd

EXCEL_FILE = "Printer Information.xlsx"

def load_printer_config() -> Tuple[List[Dict], Dict]:
    """Load printer and Airtable configuration.

    Expected Excel format (best-effort, tolerant):
    - Sheet 0: printer info, columns like:
        Name, OctoPrintURL, OctoPrintAPIKey, BedX, BedY, BedZ
    - Optional sheet named 'Airtable' with columns:
        APIKey, BaseId, TableName, StatusField

    Returns:
        (printers, airtable_cfg)
    """
    printers = []
    airtable_cfg = {
        "api_key": "",
        "base_id": "",
        "table_name": "",
        "status_field": "Status",
    }

    if os.path.exists(EXCEL_FILE):
        try:
            xls = pd.ExcelFile(EXCEL_FILE)
            # First sheet -> printers
            df = xls.parse(xls.sheet_names[0])
            for _, row in df.iterrows():
                printers.append({
                    "name": str(row.get("Name", "MakerGear M3")),
                    "octoprint_url": str(row.get("OctoPrintURL", "http://localhost")),
                    "octoprint_api_key": str(row.get("OctoPrintAPIKey", "")),
                    "bed_x": float(row.get("BedX", 200)),
                    "bed_y": float(row.get("BedY", 200)),
                    "bed_z": float(row.get("BedZ", 200)),
                })
            # Airtable sheet (optional)
            if "Airtable" in xls.sheet_names:
                adf = xls.parse("Airtable")
                if not adf.empty:
                    row = adf.iloc[0]
                    airtable_cfg["api_key"] = str(row.get("APIKey", ""))
                    airtable_cfg["base_id"] = str(row.get("BaseId", ""))
                    airtable_cfg["table_name"] = str(row.get("TableName", ""))
                    airtable_cfg["status_field"] = str(row.get("StatusField", "Status"))
        except Exception as exc:
            print(f"[printer_config] Failed to parse Excel config: {exc}")
    else:
        # Fallback dummy printer
        printers.append({
            "name": "Dummy M3",
            "octoprint_url": "http://localhost",
            "octoprint_api_key": "",
            "bed_x": 200.0,
            "bed_y": 200.0,
            "bed_z": 200.0,
        })

    return printers, airtable_cfg

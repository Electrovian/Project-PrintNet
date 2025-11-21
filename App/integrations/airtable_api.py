from typing import List, Dict

import requests

def fetch_pending_jobs(cfg: dict) -> List[Dict]:
    """Fetch pending jobs from Airtable.

    This is a safe stub: if no API key / base id is configured, it just
    returns an empty list.
    """
    api_key = cfg.get("api_key")
    base_id = cfg.get("base_id")
    table = cfg.get("table_name")
    status_field = cfg.get("status_field", "Status")

    if not api_key or not base_id or not table:
        return []

    url = f"https://api.airtable.com/v0/{base_id}/{table}"
    params = {"filterByFormula": f"{{{status_field}}}='Pending'"}
    headers = {"Authorization": f"Bearer {api_key}"}
    r = requests.get(url, headers=headers, params=params, timeout=10)
    r.raise_for_status()
    return r.json().get("records", [])

def update_job_status(cfg: dict, record_id: str, new_status: str):
    api_key = cfg.get("api_key")
    base_id = cfg.get("base_id")
    table = cfg.get("table_name")
    status_field = cfg.get("status_field", "Status")

    if not api_key or not base_id or not table:
        print("[airtable_api] No Airtable config; skipping status update.")
        return

    url = f"https://api.airtable.com/v0/{base_id}/{table}/{record_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {"fields": {status_field: new_status}}
    r = requests.patch(url, headers=headers, json=payload, timeout=10)
    try:
        r.raise_for_status()
    except Exception as exc:
        print(f"[airtable_api] Failed to update record {record_id}: {exc}")

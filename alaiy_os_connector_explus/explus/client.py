# Copyright (c) 2026, Alaiy and contributors
# For license information, please see license.txt
"""
HTTP client for the Ex Plus tracking endpoint.

  GET {base_url}/api.php?trackings=<no>[,<no>...]
  -> [{"Tracking": "...",
       "Data": {"LastMileTracking": <0 | value>,
                "Status": [{"StatusCode": int, "City": str,
                            "desc": str, "date": "YYYY-MM-DD HH:MM:SS"}, ...]}}]

The endpoint is the one Ex Plus's public tracking page itself calls. It takes
no credentials and the vendor publishes no rate limit, so requests are kept
batched and sequential. Status events come newest first.
"""

import frappe
import requests

DEFAULT_BASE_URL = "https://track.expluslogistics.com"
TIMEOUT_SECONDS = 30


class ExplusAPIError(Exception):
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code


def get_base_url():
    url = frappe.db.get_single_value("Explus Connector Settings", "explus_base_url")
    return (url or DEFAULT_BASE_URL).rstrip("/")


def fetch_trackings(tracking_numbers):
    """Return the parsed JSON list for the given tracking numbers."""
    resp = requests.get(
        f"{get_base_url()}/api.php",
        params={"trackings": ",".join(tracking_numbers)},
        headers={"Accept": "application/json"},
        timeout=TIMEOUT_SECONDS,
    )
    if resp.status_code != 200:
        raise ExplusAPIError(f"HTTP {resp.status_code} from Ex Plus tracking.", resp.status_code)
    try:
        data = resp.json()
    except ValueError:
        raise ExplusAPIError("Ex Plus tracking did not return JSON.", resp.status_code)
    if not isinstance(data, list):
        raise ExplusAPIError("Unexpected Ex Plus tracking response shape.", resp.status_code)
    return data

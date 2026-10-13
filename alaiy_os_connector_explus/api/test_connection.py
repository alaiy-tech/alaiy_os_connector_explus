# Copyright (c) 2026, Alaiy and contributors
# For license information, please see license.txt
"""
Reachability check. Wired into the registry via connector_meta["test_method"]
and called by the "Test Connection" button. Always returns
{"success": bool, "message": str} -- never raises to the caller.

The endpoint takes no credentials and has no ping route, so the check is one
tracking request: it must answer 200 with a JSON list. An unknown number is
fine for this purpose.
"""

import frappe
import requests


@frappe.whitelist()
def test_connection():
    from alaiy_os_connector_explus.explus.client import ExplusAPIError, fetch_trackings, get_base_url

    try:
        fetch_trackings(["TEST"])
        return {"success": True, "message": f"Connected successfully ({get_base_url()})."}
    except ExplusAPIError as e:
        return {"success": False, "message": str(e)}
    except requests.exceptions.ConnectionError:
        return {"success": False, "message": "Could not connect to Ex Plus tracking."}
    except requests.exceptions.Timeout:
        return {"success": False, "message": "Request timed out (30s)."}
    except Exception as e:
        return {"success": False, "message": str(e)[:200]}

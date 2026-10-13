# Copyright (c) 2026, Alaiy and contributors
# For license information, please see license.txt
"""
Pull tracking from Ex Plus for the given tracking numbers and return it. The
connector only reads: nothing is written to any ERPNext document.

Each run is recorded in Explus Sync Log (queued / running / success / failed
with counts).
"""

import json

import frappe

from alaiy_os_connector_explus.explus.client import fetch_trackings
from alaiy_os_connector_explus.explus.sync import _mark_finished, _mark_running, get_or_create_log

# Conservative batch size; the endpoint documents no limit.
_BATCH_SIZE = 20

# An unknown tracking number is not an empty result: Ex Plus answers with one
# placeholder event whose text starts like this.
_NOT_FOUND_PREFIX = "Lastmile Carrier:"


def _chunk(seq, size):
    for i in range(0, len(seq), size):
        yield seq[i:i + size]


def summarize(entry):
    """Reduce one response item to what a viewer needs. Events stay newest
    first. `found` is False for the unknown-number placeholder."""
    data = entry.get("Data") or {}
    events = data.get("Status") or []
    found = bool(events) and not str(events[0].get("desc") or "").startswith(_NOT_FOUND_PREFIX)
    return {
        "tracking": entry.get("Tracking"),
        "found": found,
        "status": entry.get("LatestStatus") if found else None,
        "destination": entry.get("Destination") if found else None,
        "last_mile_tracking": data.get("LastMileTracking") or None,
        "events": [
            {"date": e.get("date"), "status": e.get("desc"), "location": e.get("City")}
            for e in events
        ] if found else [],
    }


def pull_tracking(tracking_numbers, trigger="manual", log_name=None):
    """Pull tracking for the numbers; return [summary, ...] in request order."""
    numbers = [n.strip() for n in tracking_numbers if n and n.strip()]
    log = get_or_create_log("pull", trigger, log_name)
    _mark_running(log)

    by_number = {}
    failed = 0
    try:
        for batch in _chunk(numbers, _BATCH_SIZE):
            try:
                for entry in fetch_trackings(batch):
                    by_number[entry.get("Tracking")] = summarize(entry)
            except Exception:
                failed += len(batch)
                frappe.log_error(title="Ex Plus tracking batch failed", message=frappe.get_traceback())

        results = [by_number[n] for n in numbers if n in by_number]
        log.items_processed = len(numbers)
        log.items_updated = sum(1 for r in results if r["found"])
        log.items_failed = failed + sum(1 for r in results if not r["found"])
        _mark_finished(
            log,
            "success" if log.items_failed == 0 else "failed",
            error_message=(f"{log.items_failed} number(s) not tracked -- unknown to Ex Plus or request failed."
                           if log.items_failed else None),
        )
    except Exception:
        _mark_finished(log, "failed", frappe.get_traceback())
        frappe.log_error(title="Ex Plus track pull failed", message=json.dumps(numbers))
        raise

    return results

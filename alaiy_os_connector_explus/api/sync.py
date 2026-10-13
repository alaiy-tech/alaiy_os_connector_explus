# Copyright (c) 2026, Alaiy and contributors
# For license information, please see license.txt
"""
Whitelisted entry points. The connector only pulls: it returns tracking and
logs the run, and writes nothing to ERPNext documents.
"""

import frappe


@frappe.whitelist()
def get_tracking(tracking_numbers):
    """Pull tracking for one or more numbers (list, or comma/space separated
    text) and return, per number, the status, destination and event timeline."""
    from alaiy_os_connector_explus.explus.tracking import pull_tracking

    if isinstance(tracking_numbers, str):
        tracking_numbers = tracking_numbers.replace(",", " ").split()
    return pull_tracking(tracking_numbers)


@frappe.whitelist()
def get_sync_status(sync_type=None):
    """Most recent Explus Sync Log rows, newest first, for the connector card."""
    return frappe.get_all(
        "Explus Sync Log",
        fields=[
            "name", "sync_type", "trigger", "status",
            "started_at", "finished_at",
            "items_processed", "items_updated", "items_failed",
            "error_message",
        ],
        order_by="started_at desc",
        limit=5,
    )

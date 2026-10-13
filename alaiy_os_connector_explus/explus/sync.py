# Copyright (c) 2026, Alaiy and contributors
# For license information, please see license.txt
"""
Explus Sync Log lifecycle helpers shared by every run. The connector has one
sync, the tracking pull (explus/tracking.py).
"""

import frappe
from frappe.utils import now_datetime


def get_or_create_log(sync_type, trigger, log_name=None):
    """Return the Sync Log for this run. A pre-created log_name (made by the API
    layer so it shows as 'queued' immediately) is reused."""
    if log_name and frappe.db.exists("Explus Sync Log", log_name):
        return frappe.get_doc("Explus Sync Log", log_name)

    log = frappe.new_doc("Explus Sync Log")
    log.sync_type = sync_type
    log.trigger = trigger
    log.status = "queued"
    log.insert(ignore_permissions=True)
    frappe.db.commit()
    return log


def _mark_running(log):
    log.status = "running"
    log.started_at = now_datetime()
    log.save(ignore_permissions=True)
    frappe.db.commit()


def _mark_finished(log, status, error_message=None):
    log.status = status
    log.finished_at = now_datetime()
    if error_message:
        log.error_message = error_message[:2000]
    log.save(ignore_permissions=True)
    frappe.db.commit()


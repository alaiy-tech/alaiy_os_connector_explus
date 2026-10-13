# Copyright (c) 2026, Alaiy and contributors
# For license information, please see license.txt
"""
Install / migrate plumbing shared by every Alaiy OS connector:

  sync_connector_registry  -> (re)register in OS Connector Registry (every migrate)
"""

import frappe


def after_install():
    pass


def sync_connector_registry():
    """Register or update this connector's row in alaiy_os's OS Connector
    Registry. Idempotent; runs on every bench migrate."""
    _fix_settings_as_single()

    if not frappe.db.exists("DocType", "OS Connector Registry"):
        return

    from alaiy_os_connector_explus.connector_meta import connector_meta

    connector_id = connector_meta["connector_id"]
    if frappe.db.exists("OS Connector Registry", connector_id):
        doc = frappe.get_doc("OS Connector Registry", connector_id)
    else:
        doc = frappe.new_doc("OS Connector Registry")

    # Owned by the running system, never overwritten from static meta.
    runtime_fields = {"connection_status", "last_tested_at"}

    for key, val in connector_meta.items():
        if not hasattr(doc, key):
            continue
        if doc.is_new() or key not in runtime_fields:
            doc.set(key, val)
    if doc.is_new():
        doc.insert(ignore_permissions=True)
    else:
        doc.save(ignore_permissions=True)

    frappe.db.commit()
    _update_alaiy_os_sidebar()


def _update_alaiy_os_sidebar():
    """Re-run alaiy_os's sidebar provisioning so the Logs link and connector card
    show up right after registration."""
    try:
        from alaiy_os.setup.install import (
            create_or_update_os_settings_workspace,
            create_or_update_os_settings_workspace_sidebar,
            create_or_update_workspace_sidebar,
        )
        create_or_update_workspace_sidebar()
        create_or_update_os_settings_workspace()
        create_or_update_os_settings_workspace_sidebar()
        frappe.db.commit()
    except Exception:
        frappe.log_error(
            title="Ex Plus connector: sidebar update failed",
            message=frappe.get_traceback(),
        )


def _fix_settings_as_single():
    """Frappe does not convert an existing DocType from table-based to Single on
    migrate, so force issingle=1 on every deploy."""
    frappe.db.sql(
        "UPDATE `tabDocType` SET issingle=1 "
        "WHERE name='Explus Connector Settings' AND issingle=0"
    )
    frappe.db.commit()

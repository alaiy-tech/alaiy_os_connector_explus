# Copyright (c) 2026, Alaiy and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ExplusConnectorSettings(Document):
    def validate(self):
        self._sync_registry_is_enabled()

    def _sync_registry_is_enabled(self):
        if frappe.db.exists("OS Connector Registry", "explus"):
            frappe.db.set_value("OS Connector Registry", "explus", "is_enabled", self.is_enabled)

app_name = "alaiy_os_connector_explus"
app_title = "Alaiy Os Connector Explus"
app_publisher = "Alaiy"
app_description = "Ex Plus Logistics tracking connector for AlaiyOS"
app_email = "mail@alaiy.com"
app_license = "agpl-3.0"

# Every Alaiy OS connector runs on top of alaiy_os (registry, workspace,
# connector card) and erpnext (Delivery Note).
required_apps = ["alaiy_os", "erpnext"]

after_install = [
    "alaiy_os_connector_explus.setup.install.after_install"
]

after_migrate = [
    "alaiy_os_connector_explus.setup.install.sync_connector_registry"
]

# Register this connector's Sync Log under the Alaiy OS "Logs" sidebar section.
alaiy_os_sidebar_log_items = [
    {
        "link_type": "DocType",
        "link_to": "Explus Sync Log",
        "label": "Explus Logs",
        "icon": "activity",
    }
]

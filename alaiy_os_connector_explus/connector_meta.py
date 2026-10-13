"""
Single source of truth for this connector's registration metadata.
Consumed by setup/install.py -> upserted into alaiy_os's OS Connector Registry.
"""

connector_meta = {
    "connector_id": "explus",
    "connector_name": "Ex Plus Logistics",
    "connector_app": "alaiy_os_connector_explus",
    # A carrier neither sells to nor supplies the business; "channel" is the
    # closest existing registry bucket (same choice as the FedEx connector).
    "connector_type": "channel",
    "description": "Ex Plus Logistics connector -- pulls first-mile shipment tracking by tracking number.",
    "icon": "box",
    "icon_url": "",
    "settings_doctype": "Explus Connector Settings",
    "test_method": "alaiy_os_connector_explus.api.test_connection.test_connection",
    "sync_status_method": "alaiy_os_connector_explus.api.sync.get_sync_status",
    "is_enabled": 0,
    "connection_status": "untested",
}

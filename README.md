# Alaiy OS Connector: Ex Plus Logistics

Carrier connector for Alaiy OS. It only pulls: given tracking numbers it
fetches the status and event timeline from Ex Plus Logistics and returns them.
It writes nothing to Delivery Notes or any other ERPNext document.

## What it does

- **Settings** (`Explus Connector Settings`): enable switch and tracking base URL.
- **Sync Log** (`Explus Sync Log`): one row per pull with queued / running /
  success / failed and processed / found / failed counts.
- **Pull** (`api.sync.get_tracking`): takes one or more tracking numbers and
  returns, for each, status, destination, last-mile tracking and the events
  (date, status, location), newest first.
- **Test Connection**: one tracking request that must answer 200 with a JSON list.

## Endpoint

```
GET {base_url}/api.php?trackings=<no>[,<no>...]
```

No credentials. Returns a JSON list, one item per tracking number:

```json
[{"Tracking": "EX...", "LatestStatus": "Delivered", "Destination": "...",
  "Data": {"LastMileTracking": 0,
  "Status": [{"StatusCode": 10, "City": "...", "desc": "Delivered", "date": "YYYY-MM-DD HH:MM:SS"}]}}]
```

Each item also carries `Rating` and `isPremium`. A number Ex Plus does not know
is not omitted or empty: it comes back with one placeholder event whose text
starts with `Lastmile Carrier:`, which the connector reports as not found.
Timestamps are as returned; the endpoint states no timezone. The endpoint is the
public tracking page's own; no other Ex Plus API is public.

## Not built

Writing tracking onto documents, shipment creation, labels, rates, cancellation
and webhooks. The last four need the vendor's account API, which is not public.

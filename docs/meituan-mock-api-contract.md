# Mock Local-Life API Contract

The mock service is implemented in [scripts/mock_meituan_service.py](../scripts/mock_meituan_service.py).

## Data Files

| File | Purpose |
| --- | --- |
| `config/meituan_poi.mock.json` | Local POI and categories. |
| `config/meituan_inventory.mock.json` | Mock SKU inventory and stock. |
| `config/meituan_delivery.mock.json` | ETA and fallback metadata. |
| `config/mira_user_profile.mock.json` | Demo preferences and privacy flags. |
| `config/mira_budget.mock.json` | Demo budget buckets. |

## Bridge Tools

```text
POST /v1/mira-life/trigger-event
POST /v1/mira-life/propose-action
POST /v1/mira-life/confirm-action
POST /v1/mira-life/cancel-action
POST /v1/mira-life/check-budget
POST /v1/mira-life/place-mock-order
POST /v1/mira-life/track-fulfillment
GET  /v1/mira-life/bundles
```

## Order Preview

```json
{
  "kind": "instant_retail_order_preview",
  "title": "常用舒缓补给包",
  "eta_minutes": 28,
  "total_price": 42.7,
  "budget_after": 1217.3,
  "requires_confirmation": true
}
```

## Mock Order

```json
{
  "order_id": "demo-order-public-001",
  "status": "mock_order_created",
  "eta_minutes": 28,
  "tracking": {
    "state": "rider_assigned"
  }
}
```

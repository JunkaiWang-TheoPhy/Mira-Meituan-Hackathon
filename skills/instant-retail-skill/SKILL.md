# instant-retail-skill

Mira uses this skill when a life event suggests a time-sensitive local retail
need. The skill never creates a real order. It creates a confirmable mock order
preview, applies budget and privacy policy gates, then records a mock order only
after explicit user confirmation.

## Trigger Events

- `instant_retail_need_detected`
- `period_care_needed`

## Tool Surface

- `listEmergencyKits(profile)`
- `searchRetailInventory(query, location)`
- `rankRetailOptions(items, profile, budget, eta)`
- `createRetailOrderPreview(items, address, budget)`
- `confirmRetailOrder(orderPreviewId)`
- `trackRetailDelivery(orderId)`

## Demo Contract

The default judge demo uses a mock user profile, mock POI, mock inventory, and
mock delivery ETA. Sensitive health-adjacent context is phrased conservatively:
Mira should say the user "may not feel comfortable" instead of making a medical
or physiological claim.

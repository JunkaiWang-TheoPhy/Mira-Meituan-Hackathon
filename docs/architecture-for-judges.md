# Architecture for Judges

Mira keeps the original Mira Light philosophy of proactive sensing, but changes
the action layer from embodied lamp scenes to local-life fulfillment.

```text
Mira Light:
camera input
-> vision event extraction
-> scene selection
-> bridge / safety layer
-> ESP32 lamp motion + light response

Mira Local-Life Butler:
watch / glasses / phone / calendar / location
-> life event extraction
-> OpenClaw-style memory + heartbeat
-> life intent decision
-> local-life skills
-> bridge / policy gate
-> recommendation / confirmation / mock order / ETA tracking
-> life memory writeback
```

## Layers

| Layer | Role |
| --- | --- |
| Gateway | Receives watch, glasses, phone, calendar, location, and user confirmation events. |
| Heartbeat | Periodically checks meal risk, commute risk, budget pressure, weather, and inventory-sensitive situations. |
| Memory | Stores mock preferences, dislikes, budget, common care items, recent meals, and addresses. |
| Skills | Encapsulates dining, instant retail, mobility, entertainment, and budget care. |
| Bridge | Presents stable high-level tools to OpenClaw-style callers. |
| Policy | Requires confirmation for money, health-adjacent context, privacy, and budget risk. |

## Primary Fulfillment Loop

```text
period_care_needed
-> instant-retail-skill
-> nearby inventory match
-> delivery ETA ranking
-> budget check
-> confirmation-required policy
-> mock order
-> delivery tracking
-> budget memory writeback
```

## Why Instant Retail Is the Main Demo

Dining and entertainment can look like ordinary recommendation. Instant retail
shows the platform fulfillment advantage: local inventory, SKU choice, LBS,
delivery ETA, substitutions, budget, and order tracking. The demo is not “what
can I buy nearby?” It is “Mira noticed a timely life need and prepared a safe,
confirmable action.”

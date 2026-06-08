# Architecture for Judges

Mira keeps the proactive sensing idea from Mira Light, but changes the action
layer from device motion to local-life fulfillment.

```text
multi-device state
-> life event extraction
-> skill routing
-> policy gate
-> mock local-life proposal
-> user confirmation
-> mock order / ETA / budget writeback
```

## What to Look For

| Stage | What the demo proves |
| --- | --- |
| State | Watch, calendar, weather, area, budget, and preferences form one life context. |
| Event | `period_care_needed` is extracted as a low-disturbance life event. |
| Skill | `instant-retail-skill` is selected instead of generic search. |
| Policy | Money and sensitive context require confirmation. |
| Fulfillment | Mock POI, inventory, ETA, order, tracking, and budget writeback complete the loop. |

## Main Loop

```text
period_care_needed
-> instant-retail-skill
-> mock inventory match
-> ETA + budget ranking
-> confirmation_required
-> user confirmation
-> demo-order-public-* created
-> budget_after recorded
```

## Why Instant Retail Is the Main Demo

餐饮和娱乐容易被理解成“推荐”。即时零售更能体现履约闭环：商品、库存、区域、配送时效、替代品、预算和确认缺一不可。Mira 的重点不是“附近有什么”，而是“它在你开口前发现了一个生活需求，并把可确认的方案准备好”。

## Non-Official Mock Boundary

All platform-like data in this repository is public mock data. The bridge and
skills use platform-shaped interfaces for demonstration, but do not call real
platform APIs or create real orders.

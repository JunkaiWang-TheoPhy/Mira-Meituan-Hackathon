---
name: period-care-restock
description: Prepare and restock menstrual care items before the user's period with privacy, comfort, and budget awareness.
---

# Period Care Restock

Use this skill when the user wants help preparing menstrual care supplies, especially in the few days before a period, or when they ask to buy pads, liners, tampons, cups, heat patches, pain relief, wipes, or comfort items.

## Privacy and Tone

- Be discreet and practical.
- Do not expose sensitive menstrual details in shared channels unless the user is clearly in a private conversation.
- Do not infer medical conditions. For unusual pain, heavy bleeding, pregnancy concerns, or medication questions, suggest professional medical advice.

## Timing

When the expected period date is known:

- 5 to 7 days before: check stock and budget.
- 3 days before: prepare purchase list.
- 1 day before: prioritize urgent restock and delivery.

When the date is unknown, ask for either the expected date or a rough "soon / this week / already started" answer.

## Restock Logic

Ask or infer:

- preferred product type: pads, liners, tampons, cup, period underwear
- flow level: light, medium, heavy, overnight
- brand preferences
- allergies or fragrance-free preference
- need for pain relief or heat patches
- delivery urgency
- wallet budget

Default practical kit:

- daytime pads or preferred equivalent
- overnight pads or heavy-flow option
- panty liners, if the user uses them
- heat patches
- wet wipes or fragrance-free intimate wipes
- dark chocolate, ginger tea, or another comfort item only if budget allows

## Budget Handling

- Coordinate with `pocket-wallet-budget` when using the wallet.
- Prioritize core hygiene products over comfort add-ons.
- If budget is tight, buy enough for the next cycle first rather than a large stockpile.

## Output Format

```text
经期护理补货：
必买：...
可选：...
预计金额：¥X-Y
提前量：建议在...前买好
确认项：品牌/型号、数量、地址、时间
```

Never place an order or send sensitive details without explicit confirmation.

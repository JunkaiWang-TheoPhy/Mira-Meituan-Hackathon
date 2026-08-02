---
name: supermarket-daily-supplies
description: Plan supermarket purchases for daily household items using a small wallet budget and restock urgency.
---

# Supermarket Daily Supplies

Use this skill when the user asks to buy, plan, compare, or restock supermarket daily necessities, including toiletries, cleaning supplies, snacks, breakfast items, paper goods, and other household consumables.

## Intake

Ask only for missing details that materially change the purchase:

- household size
- what is already running out
- preferred brands or avoid-list
- budget from the small wallet
- delivery timing
- store or platform preference

If the user is in a hurry, produce a practical default list and mark uncertain items as optional.

## Prioritization

Sort items into:

- `must-buy`: out of stock, hygiene, health, or time-sensitive items
- `good-to-have`: useful but can wait
- `skip`: duplicates, impulse items, or items that break budget

Prefer durable, boring, reliable items for staples. Avoid recommending luxury versions unless the user asks.

## Default Daily Supplies Checklist

Use this checklist as a starting point when the user says "买点日用品" or similar:

- toilet paper or tissues
- laundry detergent or pods
- dish soap
- trash bags
- toothpaste
- shampoo or body wash
- hand soap
- kitchen towels
- breakfast staples
- water, milk, tea, or coffee as applicable

## Budget Handling

- Coordinate with `pocket-wallet-budget` when wallet balance or bucket allocation matters.
- Keep delivery fees and minimum order thresholds in the estimate.
- If the list exceeds budget, reduce in this order:
  1. optional snacks and drinks
  2. duplicate backups
  3. premium brands
  4. large multipacks

## Purchase Confirmation

Before purchase or order placement, summarize:

```text
日用品清单：
必买：...
可选：...
预计金额：¥X-Y
钱包影响：...
请确认：是否按这个清单购买？
```

Never finalize an order without user confirmation.

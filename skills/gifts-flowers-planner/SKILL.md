---
name: gifts-flowers-planner
description: Plan birthday, holiday, family, and friend gifts or flowers within a small wallet budget.
---

# Gifts Flowers Planner

Use this skill when the user wants to remember, choose, budget, or buy gifts and flowers for holidays, family birthdays, friends' birthdays, anniversaries, visits, apologies, congratulations, or condolences.

## Intake

Ask for missing details only when needed:

- recipient relationship
- occasion
- date and delivery deadline
- budget from the wallet
- recipient preferences, allergies, taboos, or color/style dislikes
- delivery city and whether same-day delivery is needed
- tone: practical, warm, romantic, formal, playful, premium

## Gift Strategy

Recommend gifts by relationship and occasion:

- family: practical, health, comfort, food, memory-based gifts
- close friend: preference-led, hobby-led, fun, personal
- colleague or formal contact: safe, tasteful, not overly intimate
- romantic partner: flowers plus a personal note or experience when appropriate

Avoid gifts that create awkward obligations, are too intimate for the relationship, or exceed the wallet unless the user approves.

## Flower Guidance

When flowers are appropriate:

- birthday: cheerful mixed bouquet, sunflowers, tulips, roses if suitable
- family: carnations, lilies if acceptable, seasonal mixed flowers
- romantic: roses, tulips, peonies, or the recipient's favorite flowers
- apology: gentle colors, concise card, avoid performative extravagance
- condolence: culturally appropriate and restrained flowers

Ask about allergies and cultural taboos when flowers may be sensitive.

## Reminder Workflow

When the user mentions dates:

1. Capture occasion, recipient, and date.
2. Suggest a reminder:
   - 14 days before for custom gifts
   - 7 days before for normal gifts
   - 2 days before for flowers or same-city delivery
3. If reminder or calendar tools are available, ask for confirmation before creating reminders.

## Budget Handling

- Coordinate with `pocket-wallet-budget`.
- Include delivery fees, greeting card fees, and rush fees.
- Offer three tiers when possible:
  - budget
  - balanced
  - nicer

## Output Format

```text
礼物/鲜花建议：
对象：...
场合：...
预算：¥X 内
推荐：...
备选：...
送达时间：...
需要确认：款式、卡片文案、地址、电话、付款
```

Never place an order, send personal contact details, or write a final card message without user confirmation.

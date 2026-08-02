---
name: pocket-wallet-budget
description: Manage a small reserved wallet for household purchases with budget checks, spending rules, and confirmation steps.
---

# Pocket Wallet Budget

Use this skill when the user wants to set aside part of their money as a small wallet for daily-life purchases, check whether a planned purchase fits the wallet, or decide how much to reserve for routine supplies, period care, gifts, or flowers.

## Core Behavior

- Treat the wallet as a bounded spending pool, not as the user's full balance.
- Before recommending any purchase, identify:
  - current wallet balance, if known
  - purchase purpose
  - target date or deadline
  - hard budget limit
  - whether the user wants cheapest, balanced, or premium options
- If the wallet balance is unknown, ask the user for the amount they want to allocate or use a clearly labeled estimate.
- Never claim a purchase has been made unless an actual purchase tool confirms it.
- Never make payment, place an order, or send recipient details without explicit user confirmation for the exact item, price, delivery address, and timing.
- Prefer practical, repeatable choices over impulse purchases.

## Wallet Rules

Maintain these virtual buckets when useful:

- `daily-supplies`: supermarket and household consumables
- `period-care`: pads, liners, tampons, pain relief, heat patches, wipes
- `gifts-flowers`: birthday, holiday, family, friend, and relationship gifts
- `buffer`: unassigned reserve for price changes, delivery fees, and urgent needs

Recommended allocation when the user has no preference:

- 50% daily supplies
- 20% period care
- 25% gifts and flowers
- 5% buffer

Adjust this split when the user has upcoming birthdays, holidays, travel, menstrual cycle needs, or a low wallet balance.

## Spending Decision

For each purchase request:

1. Convert the request into a short shopping objective.
2. Estimate the minimum viable spend and a comfortable spend.
3. Check the matching bucket and total wallet.
4. Recommend one of:
   - `buy now`
   - `buy cheaper version`
   - `wait`
   - `ask user for approval to exceed budget`
5. Explain the tradeoff in one or two short sentences.

## Output Format

When giving a wallet recommendation, use:

```text
钱包建议：买 / 换便宜款 / 等一等
预算：¥X 内
理由：...
需要确认：商品、价格、地址、时间
```

Use the user's local currency when known. If the user does not specify a currency, use CNY by default for Chinese-language conversations.

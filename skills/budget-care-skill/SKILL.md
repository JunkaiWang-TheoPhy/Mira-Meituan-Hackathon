# budget-care-skill

Mira uses this skill to make recommendations feel like household management
instead of pure commerce. It records planned spending categories, warns before
budget pressure, and keeps sensitive or money-moving actions behind policy
gates.

## Trigger Events

- `budget_limit_warning`
- `birthday_gift_due`

## Tool Surface

- `checkBudget(category)`
- `recordPlannedSpend(category, amount)`
- `summarizeLifeBudget()`
- `proposeLowerCostAlternative(proposal)`

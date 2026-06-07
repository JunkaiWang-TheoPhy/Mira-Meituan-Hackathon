# Data Safety and Policy

Mira is intentionally conservative. A proactive butler is useful only if it does
not overstep.

## Hard Rules

- Demo uses fictional profiles only.
- No real health data is collected.
- No medical diagnosis is made.
- No real Meituan order is placed.
- Money-moving actions require user confirmation.
- Health-adjacent or sensitive context requires user confirmation.
- Location and budget are mock fields in the demo.
- Budget overrun requires a second review path.

## Sensitive Wording

Do not say:

> 我检测到你来例假了。

Say:

> 你现在可能不太舒服。我按你常用清单配了一个补给包，要我帮你买过来吗？

## Policy Statuses

| Status | Meaning |
| --- | --- |
| `confirmation_required` | User must confirm before mock order or reservation. |
| `budget_review_required` | Proposal exceeds the event budget. |
| `advisory_only` | Mira can only advise; no order action is allowed. |
| `approved_for_mock_execution` | Demo-only path where policy permits execution. |

## Demo Scope

This repository is an engineering demo of the runtime, not an official Meituan
integration. The bridge and mock service are designed so a future real adapter
could replace the mock API without changing the OpenClaw-facing tool surface.

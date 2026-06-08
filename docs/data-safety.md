# Data Safety and Redaction

Mira is intentionally conservative. A proactive butler is useful only if it can
explain the action, wait for confirmation, and avoid exposing private data.

## Submission-Level Redaction

- No personal names in public-facing docs.
- No local absolute paths in CLI output, summary JSON, or reports.
- No real coordinates; mock location uses `demo_area` and `geo_bucket`.
- No real addresses; mock address uses a public demo zone label.
- No real order IDs; generated files use `demo-order-public-*`.
- No real platform API calls, credentials, tokens, or user identifiers.

## Demo Scope

- Fictional profile only.
- Public mock location bucket only.
- Public mock budget only.
- Public mock POI, inventory, ETA, and order only.
- No medical diagnosis.
- No real order or reservation.

## Policy Gate

| Status | Meaning |
| --- | --- |
| `confirmation_required` | User must confirm before mock order or reservation. |
| `budget_review_required` | Proposal exceeds the event budget. |
| `advisory_only` | Mira can only advise; no order action is allowed. |
| `approved_for_mock_execution` | Demo-only path where policy permits execution. |

## Sensitive Wording

Do not say:

> 我检测到你来例假了。

Say:

> 你现在可能不太舒服。我按你常用清单配了一个补给包，要我帮你买过来吗？

## Non-Official Statement

This repository is a hackathon mock demo. It is not an official platform
integration, does not call real APIs, and does not create real orders. The
bridge is shaped so a future approved adapter could replace the mock service
without changing the OpenClaw-facing tool surface.

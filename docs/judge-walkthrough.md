# Judge Walkthrough

Use this path if you have three minutes to evaluate the repository.

## 1. Product Read

Open [SUBMISSION.md](./SUBMISSION.md). The important claim is:

> Mira turns state into a confirmable local-life action, not a generic search.

## 2. Architecture Read

Open [architecture-for-judges.md](./architecture-for-judges.md). Look for the
six-stage loop:

```text
state -> event -> skill -> policy -> confirmation -> mock fulfillment
```

## 3. Run the Main Demo

```bash
npm run demo:retail
```

Expected output includes:

```text
Skill selected：instant-retail-skill
Policy：confirmation_required
Demo order created
Budget updated
Summary: runtime/demo-runs/<timestamp>-instant-retail/summary.json
```

## 4. Open the Console

Open [../web/mira_console/index.html](../web/mira_console/index.html).

The console has six blocks:

- 状态
- 事件
- Skill
- Policy
- 预算
- 履约

## 5. Check Safety

Open [data-safety.md](./data-safety.md). This is a public mock demo: no real API,
no real order, no real health data, no real coordinates.

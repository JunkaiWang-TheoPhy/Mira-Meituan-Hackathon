# Mira: OpenClaw-Style Local-Life Butler

Mira is a roadshow-ready local-life Agent demo. It turns multi-device context
into confirmable life actions: instant retail, dining, mobility,
entertainment, and budget care.

This repository is a non-official hackathon mock demo. It does not call real
platform APIs, place real orders, or collect real health, identity, or location
data. All user profiles, areas, inventory, budgets, orders, and ETAs are public
mock seeds.

Primary demo:

```bash
npm run demo:retail
```

All scenarios:

```bash
npm run demo
```

Tests:

```bash
python3 -m unittest discover -s tests
node --check web/mira_console/app.js
```

# Mira: OpenClaw-Based Local-Life Private Butler

Mira is a proactive local-life butler, not a search chatbot. It converts watch,
glasses, phone, calendar, location, weather, memory, and budget signals into
confirmable local-life actions: dining, instant retail, mobility,
entertainment, and budget care.

Core line:

> Mira understands you, OpenClaw schedules the skills, and Meituan-style local
> fulfillment gets things done.

Run the primary instant-retail demo:

```bash
python3 scripts/run_instant_retail_demo.py
```

Run tests:

```bash
python3 -m unittest discover -s tests
```

This repository is mock-only. It does not call real Meituan APIs, collect real
health data, or place real orders.

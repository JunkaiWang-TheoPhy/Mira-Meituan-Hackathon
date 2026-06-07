# Mira Life Bridge

This bridge adapts the Mira Light local bridge idea to the Meituan hackathon:
OpenClaw sees high-level life tools, while mock POI, inventory, delivery, order,
budget, and policy details stay behind one local loopback API.

Default local URL:

```text
http://127.0.0.1:9793
```

Health endpoint:

```text
GET /health
```

High-level endpoints:

```text
POST /v1/mira-life/trigger-event
POST /v1/mira-life/propose-action
POST /v1/mira-life/confirm-action
POST /v1/mira-life/cancel-action
POST /v1/mira-life/check-budget
POST /v1/mira-life/place-mock-order
POST /v1/mira-life/track-fulfillment
GET  /v1/mira-life/bundles
```

If `MIRA_LIFE_BRIDGE_TOKEN` is set, every `/v1/...` call must include:

```text
Authorization: Bearer $MIRA_LIFE_BRIDGE_TOKEN
```

Start locally:

```bash
bash tools/mira_life_bridge/start_bridge.sh
```

Trigger the main demo event:

```bash
curl http://127.0.0.1:9793/v1/mira-life/trigger-event \
  -H "Content-Type: application/json" \
  -d @config/demo_event_period_care_needed.json
```

The bridge is mock-only by design. It never creates a real Meituan order.

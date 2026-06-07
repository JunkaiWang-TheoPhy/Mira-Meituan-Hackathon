#!/usr/bin/env python3
"""Emit a mock calendar state used by the Mira heartbeat demo."""

import json

print(json.dumps({
    "source": "calendar",
    "current_state": "overtime_after_meetings",
    "next_morning": {
        "time": "08:00",
        "title": "跨区会议",
        "commute_risk": "high"
    }
}, ensure_ascii=False, indent=2))

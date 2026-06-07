#!/usr/bin/env python3
"""Emit a mock watch state used by the Mira heartbeat demo."""

import json

print(json.dumps({
    "source": "watch",
    "heart_state": "low_energy",
    "activity": "long_sedentary_session",
    "confidence": 0.82
}, ensure_ascii=False, indent=2))

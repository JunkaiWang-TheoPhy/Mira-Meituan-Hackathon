#!/usr/bin/env python3
"""Emit a mock location state used by the Mira heartbeat demo."""

import json

print(json.dumps({
    "source": "phone",
    "location_label": "公司附近",
    "weather": "rain",
    "mobility_state": "still_at_office"
}, ensure_ascii=False, indent=2))

#!/usr/bin/env python3
"""Emit a mock location state used by the Mira heartbeat demo."""

import json

print(json.dumps({
    "source": "phone",
    "location_label": "演示区域A",
    "demo_area": "zone_a",
    "geo_bucket": "mock-city-center",
    "weather": "rain",
    "mobility_state": "still_at_office"
}, ensure_ascii=False, indent=2))

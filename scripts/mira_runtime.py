#!/usr/bin/env python3
"""Minimal Mira heartbeat runtime wrapper."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.life_event_router import route_life_event


def heartbeat(event_file: Path) -> dict:
    event = json.loads(event_file.read_text(encoding="utf-8"))
    return route_life_event(event, root=ROOT)


if __name__ == "__main__":
    print(json.dumps(heartbeat(ROOT / "config" / "demo_event_period_care_needed.json"), ensure_ascii=False, indent=2))

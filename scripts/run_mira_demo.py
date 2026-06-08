#!/usr/bin/env python3
"""Run the core Mira local-life demos: retail, dining, and mobility."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.life_event_router import route_life_event
from scripts.run_instant_retail_demo import run_demo as run_retail_demo


def _public_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.name


def main() -> None:
    retail = run_retail_demo(confirm=True, root=ROOT)
    scenarios = [retail["summary"]]
    for filename in ["demo_event_meal_risk_detected.json", "demo_event_commute_risk.json"]:
        event = json.loads((ROOT / "config" / filename).read_text(encoding="utf-8"))
        scenarios.append({
            "demo": event["event_type"],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "event": event,
            "route": route_life_event(event, root=ROOT),
            "order": None
        })

    out_dir = ROOT / "runtime" / "demo-runs" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ-core")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "summary.json"
    out_path.write_text(
        json.dumps(
            {
                "output_path": _public_path(out_path),
                "scenarios": scenarios
            },
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    print("Mira core demo scenarios")
    for scenario in scenarios:
        print(f"- {scenario['demo']}: {scenario['route']['mira_line']}")
    print(f"Summary: {_public_path(out_path)}")


if __name__ == "__main__":
    main()

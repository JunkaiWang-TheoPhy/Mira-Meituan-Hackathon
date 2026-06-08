#!/usr/bin/env python3
"""Generate a short daily-life report from the latest demo run."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def public_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.name


def latest_summary() -> Path:
    summaries = sorted((ROOT / "runtime" / "demo-runs").glob("*/summary.json"))
    if not summaries:
        raise SystemExit("No demo summaries found. Run npm run demo:retail first.")
    return summaries[-1]


def main() -> None:
    source = latest_summary()
    payload = json.loads(source.read_text(encoding="utf-8"))
    scenarios = payload.get("scenarios") or [payload]

    lines = [
        "# Mira Life Report",
        "",
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        f"Source: {public_path(source)}",
        "",
        "## 今天 Mira 为你做了什么",
        ""
    ]
    for scenario in scenarios:
        route = scenario["route"]
        proposal = route["proposal"]
        lines.extend([
            f"- 事件：`{route['event_type']}`",
            f"  - Skill：`{route['selected_skill']}`",
            f"  - 建议：{route['mira_line']}",
            f"  - 预算变化：{proposal.get('budget_before')} -> {proposal.get('budget_after')}",
            f"  - Policy：`{route['policy_decision']['status']}`"
        ])

    out = ROOT / "runtime" / "reports" / f"life-report-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(public_path(out))


if __name__ == "__main__":
    main()

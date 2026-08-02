#!/usr/bin/env python3
"""Run the 90-second Mira instant-retail demo in deterministic mock mode."""

from __future__ import annotations

from datetime import datetime, timezone
import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.life_event_router import route_life_event
from scripts.mock_meituan_service import MockMeituanService


def _timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _public_path(path: Path, root: Path = ROOT) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.name


def run_demo(*, confirm: bool = True, root: Path = ROOT) -> dict:
    event_path = root / "config" / "demo_event_period_care_needed.json"
    event = json.loads(event_path.read_text(encoding="utf-8"))
    routed = route_life_event(event, root=root)

    order = None
    if confirm:
        service = MockMeituanService(root)
        order = service.confirm_mock_order(routed["proposal"], root / "runtime" / "mock-orders")
        routed["trace"].extend(["user_confirmed_action", "mock_order_created", "budget_updated"])
    else:
        routed["trace"].append("user_confirmation_skipped")

    run_dir = root / "runtime" / "demo-runs" / f"{_timestamp()}-instant-retail"
    run_dir.mkdir(parents=True, exist_ok=True)
    summary = {
        "demo": "instant_retail",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "output_path": _public_path(run_dir / "summary.json", root),
        "event": event,
        "route": routed,
        "order": order,
        "judge_readout": [
            "[20:47:03] Heartbeat triggered",
            "[20:47:04] 状态：晚间加班 / 长时间未离开 / 天气下雨",
            "[20:47:05] Memory：用户常用应急补给包",
            f"[20:47:06] Skill selected：{routed['selected_skill']}",
            f"[20:47:06] Fulfillment skill：{routed['fulfillment_skill']}",
            "[20:47:07] 库存匹配：附近便利店有货",
            f"[20:47:08] ETA：{routed['proposal']['eta_minutes']}min",
            f"[20:47:09] Policy：{routed['policy_decision']['status']}",
            "[20:47:15] 用户确认" if confirm else "[20:47:15] 等待用户确认",
            "[20:47:16] Demo order created" if confirm else "[20:47:16] No order created",
            "[20:47:17] Budget updated" if confirm else "[20:47:17] Budget unchanged"
        ]
    }
    (run_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    return {"summary": summary, "summary_path": str(run_dir / "summary.json")}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-confirm", action="store_true", help="stop after proposal instead of mock confirmation")
    args = parser.parse_args()
    result = run_demo(confirm=not args.no_confirm)
    summary = result["summary"]
    print("Mira instant-retail demo")
    print(summary["route"]["mira_line"])
    print()
    for line in summary["judge_readout"]:
        print(line)
    if summary["order"]:
        print(f"\nMock order: {summary['order']['order_id']}")
    print(f"Summary: {_public_path(Path(result['summary_path']))}")


if __name__ == "__main__":
    main()

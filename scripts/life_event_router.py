#!/usr/bin/env python3
"""Route Mira life events into OpenClaw-style local-life skills."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.mock_meituan_service import MockMeituanService


EVENT_TO_SKILL = {
    "meal_risk_detected": "dining-skill",
    "instant_retail_need_detected": "instant-retail-skill",
    "period_care_needed": "period-care-restock",
    "calendar_commute_risk": "schedule-mobility-skill",
    "weekend_low_energy": "entertainment-skill",
    "weekend_high_energy": "entertainment-skill",
    "birthday_gift_due": "gifts-flowers-planner",
    "budget_limit_warning": "pocket-wallet-budget",
    "daily_supplies_low": "supermarket-daily-supplies",
}

FULFILLMENT_SKILL = {
    "period-care-restock": "instant-retail-skill",
    "supermarket-daily-supplies": "instant-retail-skill",
    "dining-skill": "dining-skill",
    "instant-retail-skill": "instant-retail-skill",
    "schedule-mobility-skill": "schedule-mobility-skill",
    "gifts-flowers-planner": "instant-retail-skill",
}


def _policy_for(event: dict[str, Any], proposal: dict[str, Any]) -> dict[str, Any]:
    policy = event["policy"]
    if not policy.get("can_place_order", False):
        return {
            "status": "advisory_only",
            "reason": "policy_can_place_order_false",
            "requires_confirmation": False
        }

    total_price = float(proposal.get("total_price", 0.0))
    max_budget = float(policy.get("max_budget", 0.0))
    if total_price > max_budget > 0:
        return {
            "status": "budget_review_required",
            "reason": "proposal_exceeds_event_budget",
            "requires_confirmation": True,
            "max_budget": max_budget,
            "total_price": total_price
        }

    if policy.get("requires_confirmation", True):
        return {
            "status": "confirmation_required",
            "reason": "money_or_sensitive_context",
            "requires_confirmation": True
        }

    return {
        "status": "approved_for_mock_execution",
        "reason": "policy_allows_order_without_extra_gate",
        "requires_confirmation": False
    }


def _mobility_proposal(event: dict[str, Any]) -> dict[str, Any]:
    context = event.get("context", {})
    preferences = context.get("user_preferences", {})
    pickup_time = preferences.get("preferred_pickup_time", "07:10")
    budget_remaining = float(context.get("budget_remaining", 0.0))
    total_price = 58.0
    return {
        "kind": "ride_reservation_preview",
        "title": "明早会议出行安排",
        "pickup_time": pickup_time,
        "estimated_commute_minutes": 45,
        "departure_buffer_minutes": preferences.get("departure_buffer_minutes", 15),
        "eta_minutes": 6,
        "total_price": total_price,
        "budget_before": budget_remaining,
        "budget_after": round(budget_remaining - total_price, 2),
        "category": "mobility",
        "requires_confirmation": True
    }


def _entertainment_proposal(event: dict[str, Any]) -> dict[str, Any]:
    context = event.get("context", {})
    low_energy = event["event_type"] == "weekend_low_energy"
    title = "安静咖啡馆与居家观影" if low_energy else "展览与 Livehouse 备选"
    return {
        "kind": "entertainment_recommendation",
        "title": title,
        "total_price": 0.0,
        "budget_before": context.get("budget_remaining"),
        "budget_after": context.get("budget_remaining"),
        "category": "entertainment",
        "requires_confirmation": False
    }


def _budget_proposal(event: dict[str, Any]) -> dict[str, Any]:
    remaining = float(event.get("context", {}).get("budget_remaining", 0.0))
    return {
        "kind": "budget_advisory",
        "title": "生活预算提醒",
        "total_price": 0.0,
        "budget_before": remaining,
        "budget_after": remaining,
        "category": "budget",
        "requires_confirmation": False,
        "remaining": remaining
    }


def _gift_proposal(event: dict[str, Any]) -> dict[str, Any]:
    context = event.get("context", {})
    remaining = float(context.get("budget_remaining", 0.0))
    total_price = min(128.0, remaining if remaining else 128.0)
    return {
        "kind": "gift_flowers_plan",
        "title": "生日礼物与鲜花提醒",
        "recipient_group": context.get("recipient_group", "family"),
        "occasion": context.get("occasion", "birthday"),
        "deadline": context.get("deadline", "本周内"),
        "tiers": [
            {"name": "budget", "estimate": 68.0, "idea": "实用小礼物 + 简短卡片"},
            {"name": "balanced", "estimate": 128.0, "idea": "鲜花 + 轻量礼物"},
            {"name": "nicer", "estimate": 158.0, "idea": "花束 + 偏好礼物"}
        ],
        "eta_minutes": 120,
        "total_price": total_price,
        "budget_before": remaining,
        "budget_after": round(remaining - total_price, 2),
        "category": "gifts_flowers",
        "requires_confirmation": True
    }


def _daily_supplies_proposal(event: dict[str, Any]) -> dict[str, Any]:
    context = event.get("context", {})
    remaining = float(context.get("budget_remaining", 0.0))
    max_budget = float(event.get("policy", {}).get("max_budget", 90.0))
    items = [
        {"name": "纸巾", "quantity": 1, "price": 18.0, "priority": "must-buy"},
        {"name": "垃圾袋", "quantity": 1, "price": 12.0, "priority": "must-buy"},
        {"name": "洗手液", "quantity": 1, "price": 16.0, "priority": "good-to-have"},
        {"name": "早餐牛奶", "quantity": 1, "price": 24.0, "priority": "good-to-have"}
    ]
    selected: list[dict[str, Any]] = []
    total = 0.0
    for item in items:
        next_total = total + item["price"] * item["quantity"]
        if next_total <= max_budget or item["priority"] == "must-buy":
            selected.append(item)
            total = next_total
    return {
        "kind": "daily_supplies_plan",
        "title": "日用品补货清单",
        "items": selected,
        "eta_minutes": 35,
        "total_price": round(total, 2),
        "budget_before": remaining,
        "budget_after": round(remaining - total, 2),
        "category": "daily_supplies",
        "address_label": context.get("location_label", "演示区域A"),
        "requires_confirmation": True
    }


def _mira_line(event_type: str, proposal: dict[str, Any], policy_decision: dict[str, Any]) -> str:
    if event_type in {"period_care_needed", "instant_retail_need_detected"}:
        return (
            "你现在可能不太舒服。我按你常用清单配了一个补给包，"
            f"附近门店有货，预计 {proposal['eta_minutes']} 分钟到。要我帮你买过来吗？"
        )
    if event_type == "meal_risk_detected":
        return (
            "你今天午饭吃得少，现在又加班到这个点了。我避开了你最近吃腻的重口味，"
            f"给你选了一份{proposal['title']}，{proposal['eta_minutes']} 分钟到。要我下单吗？"
        )
    if event_type == "calendar_commute_risk":
        return (
            "明早 8 点的会离你比较远，早高峰可能要 45 分钟。"
            f"我建议 {proposal['pickup_time']} 出发，要我帮你预约车吗？"
        )
    if event_type == "budget_limit_warning":
        return f"你本周生活预算只剩 {proposal['remaining']:.0f} 元，我会把后续建议控制在必要支出内。"
    if event_type == "birthday_gift_due":
        return (
            f"{proposal['deadline']}有一个生日提醒。我准备了三档礼物/鲜花方案，"
            f"平衡档约 {proposal['total_price']:.0f} 元，需要你确认对象、卡片和送达时间。"
        )
    if event_type == "daily_supplies_low":
        return (
            f"你常用日用品快不够了。我按钱包预算整理了{proposal['title']}，"
            f"预计 {proposal['eta_minutes']} 分钟送达，要我按这个清单下单吗？"
        )
    return f"我为你准备了一个生活安排：{proposal['title']}。"


def route_life_event(event: dict[str, Any], *, root: Path | str | None = None) -> dict[str, Any]:
    root_path = Path(root) if root else ROOT
    event_type = event["event_type"]
    selected_skill = EVENT_TO_SKILL.get(event_type)
    if not selected_skill:
        raise ValueError(f"unsupported event_type: {event_type}")

    service = MockMeituanService(root_path)
    fulfillment_skill = FULFILLMENT_SKILL.get(selected_skill)

    if selected_skill == "period-care-restock":
        proposal = service.build_instant_retail_proposal(event)
        proposal["kind"] = "period_care_restock_plan"
        proposal["planning_skill"] = selected_skill
        proposal["fulfillment_skill"] = fulfillment_skill
    elif selected_skill == "instant-retail-skill":
        proposal = service.build_instant_retail_proposal(event)
    elif selected_skill == "dining-skill":
        proposal = service.build_dining_proposal(event)
    elif selected_skill == "schedule-mobility-skill":
        proposal = _mobility_proposal(event)
    elif selected_skill == "entertainment-skill":
        proposal = _entertainment_proposal(event)
    elif selected_skill == "budget-care-skill":
        proposal = _budget_proposal(event)
    elif selected_skill == "pocket-wallet-budget":
        proposal = _budget_proposal(event)
    elif selected_skill == "gifts-flowers-planner":
        proposal = _gift_proposal(event)
    elif selected_skill == "supermarket-daily-supplies":
        proposal = _daily_supplies_proposal(event)
    else:
        raise ValueError(f"unsupported skill: {selected_skill}")

    policy_decision = _policy_for(event, proposal)
    return {
        "schema_version": "1.0.0",
        "event_type": event_type,
        "selected_skill": selected_skill,
        "fulfillment_skill": fulfillment_skill,
        "confidence": event["confidence"],
        "proposal": proposal,
        "policy_decision": policy_decision,
        "mira_line": _mira_line(event_type, proposal, policy_decision),
        "memory_writeback": {
            "type": "life_preference_or_budget_trace",
            "category": proposal.get("category"),
            "budget_after": proposal.get("budget_after"),
            "mock_only": True
        },
        "trace": [
            "heartbeat_triggered",
            "life_event_extracted",
            f"skill_selected:{selected_skill}",
            f"fulfillment_skill:{fulfillment_skill}" if fulfillment_skill else "fulfillment_skill:none",
            f"policy:{policy_decision['status']}",
            "await_user_confirmation" if policy_decision.get("requires_confirmation") else "advisory_ready"
        ]
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Route a Mira life event JSON file.")
    parser.add_argument("event_file", type=Path)
    args = parser.parse_args()
    event = json.loads(args.event_file.read_text(encoding="utf-8"))
    print(json.dumps(route_life_event(event), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

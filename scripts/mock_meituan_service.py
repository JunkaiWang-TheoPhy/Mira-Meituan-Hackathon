#!/usr/bin/env python3
"""Mock Meituan local-life service used by Mira demos.

The mock intentionally models the platform capabilities that matter to the
hackathon story: POI, inventory, ETA, order preview, confirmation, and tracking.
It does not call real Meituan APIs or use real personal data.
"""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any
from itertools import count


ROOT = Path(__file__).resolve().parents[1]
_ORDER_COUNTER = count(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


class MockMeituanService:
    def __init__(self, root: Path | str | None = None):
        self.root = Path(root) if root else ROOT
        self.config = self.root / "config"
        self.profile = load_json(self.config / "mira_user_profile.mock.json")
        self.budget = load_json(self.config / "mira_budget.mock.json")
        self.poi = load_json(self.config / "meituan_poi.mock.json")
        self.inventory = load_json(self.config / "meituan_inventory.mock.json")
        self.delivery = load_json(self.config / "meituan_delivery.mock.json")

    def find_poi(self, poi_id: str) -> dict[str, Any]:
        for poi in self.poi:
            if poi["poi_id"] == poi_id:
                return poi
        raise KeyError(f"unknown poi_id: {poi_id}")

    def search_retail_inventory(self, names: list[str], location_label: str) -> list[dict[str, Any]]:
        retail_store_ids = {
            poi["poi_id"]
            for poi in self.poi
            if poi["category"] == "instant_retail"
            and poi["location_label"] == location_label
            and poi["open_now"]
        }
        wanted = set(names)
        return [
            item
            for item in self.inventory
            if item["store_id"] in retail_store_ids
            and item["stock"] > 0
            and (item["name"] in wanted or "usual_care_item" in item.get("tags", []))
        ]

    def build_instant_retail_proposal(self, event: dict[str, Any]) -> dict[str, Any]:
        context = event.get("context", {})
        preferences = context.get("user_preferences") or self.profile["preferences"]
        location_label = context.get("location_label") or self.profile["location_label"]
        usual_items = preferences.get("usual_care_items") or self.profile["preferences"]["usual_care_items"]
        candidates = self.search_retail_inventory(usual_items, location_label)

        # Keep the proposal small and confirmable: one familiar care pack, not a
        # shopping cart full of guesses.
        selected: list[dict[str, Any]] = []
        selected_names = set()
        for name in usual_items:
            match = next((item for item in candidates if item["name"] == name), None)
            if match and name not in selected_names:
                selected.append({**match, "quantity": 1})
                selected_names.add(name)

        if not selected:
            raise RuntimeError("no retail inventory matched the user care kit")

        store_id = selected[0]["store_id"]
        store = self.find_poi(store_id)
        eta_minutes = self.delivery[store_id]["eta_minutes"]
        total_price = round(sum(item["price"] * item["quantity"] for item in selected), 2)
        budget_remaining = float(context.get("budget_remaining", self.budget["budget_remaining"]))

        return {
            "kind": "instant_retail_order_preview",
            "title": "常用舒缓补给包",
            "items": [
                {
                    "sku_id": item["sku_id"],
                    "name": item["name"],
                    "quantity": item["quantity"],
                    "price": item["price"],
                    "store": store["name"],
                    "store_id": store_id
                }
                for item in selected
            ],
            "eta_minutes": eta_minutes,
            "total_price": total_price,
            "budget_before": budget_remaining,
            "budget_after": round(budget_remaining - total_price, 2),
            "category": "health_emergency",
            "address_label": location_label,
            "requires_confirmation": True,
            "privacy_note": "mock profile only; no real health data or real order"
        }

    def build_dining_proposal(self, event: dict[str, Any]) -> dict[str, Any]:
        context = event.get("context", {})
        location_label = context.get("location_label") or self.profile["location_label"]
        candidates = [
            item
            for item in self.inventory
            if item["category"] == "meal"
            and self.find_poi(item["store_id"])["location_label"] == location_label
        ]
        selected = next((item for item in candidates if "not_spicy" in item.get("tags", [])), candidates[0])
        store = self.find_poi(selected["store_id"])
        eta_minutes = self.delivery[selected["store_id"]]["eta_minutes"]
        budget_remaining = float(context.get("budget_remaining", self.budget["budget_remaining"]))
        total_price = selected["price"]
        return {
            "kind": "dining_order_preview",
            "title": selected["name"],
            "items": [
                {
                    "sku_id": selected["sku_id"],
                    "name": selected["name"],
                    "quantity": 1,
                    "price": selected["price"],
                    "store": store["name"],
                    "store_id": selected["store_id"]
                }
            ],
            "eta_minutes": eta_minutes,
            "total_price": total_price,
            "budget_before": budget_remaining,
            "budget_after": round(budget_remaining - total_price, 2),
            "category": "food",
            "address_label": location_label,
            "requires_confirmation": True
        }

    def create_retail_order_preview(
        self,
        *,
        items: list[dict[str, Any]],
        address_label: str,
        category: str = "instant_retail"
    ) -> dict[str, Any]:
        if not items:
            raise ValueError("items cannot be empty")
        store_id = items[0]["store_id"]
        total_price = round(sum(item["price"] * item.get("quantity", 1) for item in items), 2)
        return {
            "kind": "instant_retail_order_preview",
            "preview_id": f"demo-preview-{next(_ORDER_COUNTER):03d}",
            "items": items,
            "eta_minutes": self.delivery[store_id]["eta_minutes"],
            "total_price": total_price,
            "category": category,
            "address_label": address_label,
            "requires_confirmation": True
        }

    def confirm_mock_order(self, preview: dict[str, Any], output_dir: Path | None = None) -> dict[str, Any]:
        output_dir = output_dir or (self.root / "runtime" / "mock-orders")
        output_dir.mkdir(parents=True, exist_ok=True)
        order_id = f"demo-order-public-{next(_ORDER_COUNTER):03d}"
        order = {
            "order_id": order_id,
            "status": "mock_order_created",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "items": preview["items"],
            "eta_minutes": preview["eta_minutes"],
            "total_price": preview["total_price"],
            "category": preview.get("category", "instant_retail"),
            "address_label": preview.get("address_label", "演示区域A"),
            "tracking": self.track_delivery(order_id, preview["eta_minutes"])
        }
        (output_dir / f"{order_id}.json").write_text(
            json.dumps(order, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        return order

    def track_delivery(self, order_id: str, eta_minutes: int) -> dict[str, Any]:
        return {
            "order_id": order_id,
            "state": "rider_assigned",
            "eta_minutes": eta_minutes,
            "message": f"Mock rider assigned; ETA {eta_minutes} minutes."
        }


if __name__ == "__main__":
    service = MockMeituanService()
    event = load_json(ROOT / "config" / "demo_event_period_care_needed.json")
    print(json.dumps(service.build_instant_retail_proposal(event), ensure_ascii=False, indent=2))

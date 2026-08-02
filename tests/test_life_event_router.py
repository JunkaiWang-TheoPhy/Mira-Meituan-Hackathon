import json
import unittest
from pathlib import Path

from scripts.life_event_router import route_life_event


ROOT = Path(__file__).resolve().parents[1]


class LifeEventRouterTest(unittest.TestCase):
    def test_instant_retail_event_requires_confirmation_and_preserves_budget(self):
        event = json.loads((ROOT / "config" / "demo_event_period_care_needed.json").read_text())

        result = route_life_event(event, root=ROOT)

        self.assertEqual(result["selected_skill"], "period-care-restock")
        self.assertEqual(result["fulfillment_skill"], "instant-retail-skill")
        self.assertEqual(result["policy_decision"]["status"], "confirmation_required")
        self.assertTrue(result["proposal"]["requires_confirmation"])
        self.assertLess(result["proposal"]["total_price"], event["policy"]["max_budget"])
        self.assertIn("28", result["mira_line"])

    def test_budget_limit_warning_routes_to_budget_skill(self):
        event = {
            "schema_version": "1.0.0",
            "event_type": "budget_limit_warning",
            "timestamp": "2026-06-07T20:47:00+08:00",
            "source": {"phone": True, "meituan_mock": True},
            "confidence": 0.9,
            "context": {"budget_remaining": 48.0, "time_of_day": "evening"},
            "policy": {
                "requires_confirmation": False,
                "max_budget": 0,
                "privacy_level": "public_demo",
                "can_place_order": False
            }
        }

        result = route_life_event(event, root=ROOT)

        self.assertEqual(result["selected_skill"], "pocket-wallet-budget")
        self.assertEqual(result["policy_decision"]["status"], "advisory_only")
        self.assertIn("预算", result["mira_line"])

    def test_zip_skills_route_to_planning_skills(self):
        cases = {
            "demo_event_period_care_needed.json": ("period-care-restock", "instant-retail-skill"),
            "demo_event_birthday_gift_due.json": ("gifts-flowers-planner", "instant-retail-skill"),
            "demo_event_budget_limit_warning.json": ("pocket-wallet-budget", None),
            "demo_event_daily_supplies_low.json": ("supermarket-daily-supplies", "instant-retail-skill"),
        }
        for filename, expected in cases.items():
            with self.subTest(filename=filename):
                event = json.loads((ROOT / "config" / filename).read_text())
                result = route_life_event(event, root=ROOT)
                self.assertEqual(result["selected_skill"], expected[0])
                self.assertEqual(result["fulfillment_skill"], expected[1])


if __name__ == "__main__":
    unittest.main()

import tempfile
import unittest
from pathlib import Path

from scripts.mock_meituan_service import MockMeituanService


ROOT = Path(__file__).resolve().parents[1]


class MockMeituanServiceTest(unittest.TestCase):
    def test_create_order_records_mock_order(self):
        service = MockMeituanService(ROOT)
        preview = service.create_retail_order_preview(
            items=[
                {
                    "sku_id": "sku-warmer-001",
                    "name": "暖宝宝",
                    "quantity": 1,
                    "price": 12.9,
                    "store_id": "poi-familymart-001"
                }
            ],
            address_label="演示区域A",
            category="health_emergency"
        )

        with tempfile.TemporaryDirectory() as tmp:
            order = service.confirm_mock_order(preview, output_dir=Path(tmp))
            order_path = Path(tmp) / f"{order['order_id']}.json"

            self.assertEqual(order["status"], "mock_order_created")
            self.assertTrue(order_path.exists())
            self.assertEqual(order["eta_minutes"], preview["eta_minutes"])


if __name__ == "__main__":
    unittest.main()

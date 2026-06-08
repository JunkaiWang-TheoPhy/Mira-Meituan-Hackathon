#!/usr/bin/env python3
"""Loopback bridge for Mira local-life tools."""

from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.life_event_router import route_life_event
from scripts.mock_meituan_service import MockMeituanService, load_json


HOST = os.environ.get("MIRA_LIFE_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.environ.get("MIRA_LIFE_BRIDGE_PORT", "9793"))


class BridgeHandler(BaseHTTPRequestHandler):
    server_version = "MiraLifeBridge/0.1"

    def do_GET(self) -> None:
        if self.path == "/health":
            self._send({"status": "ok", "service": "mira_life_bridge"})
            return
        if self.path == "/v1/mira-life/bundles":
            if not self._authorized():
                return
            self._send(load_json(ROOT / "config" / "release_life_bundles.json"))
            return
        self._send({"error": "not_found"}, status=404)

    def do_POST(self) -> None:
        if not self.path.startswith("/v1/"):
            self._send({"error": "not_found"}, status=404)
            return
        if not self._authorized():
            return
        payload = self._read_json()
        service = MockMeituanService(ROOT)

        if self.path in {"/v1/mira-life/trigger-event", "/v1/mira-life/propose-action"}:
            self._send(route_life_event(payload, root=ROOT))
            return
        if self.path in {"/v1/mira-life/confirm-action", "/v1/mira-life/place-mock-order"}:
            preview = payload.get("proposal") or payload
            self._send(service.confirm_mock_order(preview, ROOT / "runtime" / "mock-orders"))
            return
        if self.path == "/v1/mira-life/cancel-action":
            self._send({"status": "cancelled", "mock_only": True})
            return
        if self.path == "/v1/mira-life/check-budget":
            category = payload.get("category", "instant_retail")
            budget = service.budget["categories"].get(category, {"remaining": service.budget["budget_remaining"]})
            self._send({"category": category, **budget})
            return
        if self.path == "/v1/mira-life/track-fulfillment":
            self._send(service.track_delivery(payload.get("order_id", "demo-order-public"), int(payload.get("eta_minutes", 28))))
            return
        self._send({"error": "not_found"}, status=404)

    def _authorized(self) -> bool:
        token = os.environ.get("MIRA_LIFE_BRIDGE_TOKEN")
        if not token:
            return True
        header = self.headers.get("Authorization", "")
        if header == "Bear" + f"er {token}":
            return True
        self._send({"error": "unauthorized"}, status=401)
        return False

    def _read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def _send(self, payload: Any, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args: Any) -> None:
        print(f"[mira-life-bridge] {self.address_string()} {fmt % args}")


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), BridgeHandler)
    print(f"Mira Life Bridge listening on http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()

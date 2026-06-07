#!/usr/bin/env python3
"""Small CLI client for the Mira Life Bridge."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from urllib import request


DEFAULT_BASE = os.environ.get("MIRA_LIFE_BRIDGE_URL", "http://127.0.0.1:9793")


def post(path: str, payload: dict, base_url: str = DEFAULT_BASE) -> dict:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = request.Request(
        f"{base_url}{path}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    token = os.environ.get("MIRA_LIFE_BRIDGE_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with request.urlopen(req, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("event_file", type=Path)
    args = parser.parse_args()
    event = json.loads(args.event_file.read_text(encoding="utf-8"))
    print(json.dumps(post("/v1/mira-life/trigger-event", event), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

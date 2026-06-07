#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."
python3 tools/mira_life_bridge/bridge_server.py

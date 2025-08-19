#!/usr/bin/env bash
set -euo pipefail
echo "[prepare] Creating network and volume (via compose) and building images..."
docker compose build
echo "[prepare] Done."


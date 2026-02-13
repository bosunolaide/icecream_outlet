#!/usr/bin/env bash
set -euo pipefail

echo "[beat] Waiting for dependent services..."
python scripts/wait_for_tcp.py

echo "[beat] Starting Celery beat..."
exec celery -A icecream_outlet beat --loglevel=info

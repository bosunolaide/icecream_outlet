#!/usr/bin/env bash
set -euo pipefail

echo "[worker] Waiting for dependent services..."
python scripts/wait_for_tcp.py

echo "[worker] Starting Celery worker + beat..."
exec celery -A icecream_outlet worker -B --loglevel=info

#!/usr/bin/env bash
set -euo pipefail

echo "[worker] Waiting for dependent services..."
python scripts/wait_for_tcp.py

# Memory-friendly defaults for small instances
CELERY_CONCURRENCY="${CELERY_CONCURRENCY:-1}"
CELERY_PREFETCH_MULTIPLIER="${CELERY_PREFETCH_MULTIPLIER:-1}"

echo "[worker] Starting Celery worker (concurrency=$CELERY_CONCURRENCY, prefetch=$CELERY_PREFETCH_MULTIPLIER)..."
exec celery -A icecream_outlet worker   --loglevel=info   --concurrency="$CELERY_CONCURRENCY"   --prefetch-multiplier="$CELERY_PREFETCH_MULTIPLIER"

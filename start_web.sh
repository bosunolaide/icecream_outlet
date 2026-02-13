#!/usr/bin/env bash
set -euo pipefail

echo "[web] Waiting for dependent services..."
python scripts/wait_for_tcp.py

echo "[web] Running migrations (default/Postgres)..."
python manage.py migrate --database=default

echo "[web] Running migrations (analytics/MySQL)..."
python manage.py migrate --database=analytics

echo "[web] Collecting static files..."
python manage.py collectstatic --noinput

echo "[web] Starting Gunicorn..."
exec gunicorn icecream_outlet.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers ${WEB_CONCURRENCY:-2}

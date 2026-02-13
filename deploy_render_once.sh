#!/usr/bin/env bash
set -euo pipefail

echo "1) Validate render.yaml"
render blueprints validate ./render.yaml

echo "2) Push to GitHub (required for Blueprint deploy)"
git status --porcelain
echo "If you haven't pushed yet, do: git add . && git commit -m 'Add Render blueprint' && git push"

echo "3) Create the Blueprint in Render Dashboard"
echo "In Render: New +  -> Blueprint -> select this repo -> Deploy Blueprint"

echo "4) After first deploy, run migrations as a one-off job (Dashboard -> icecream-web -> Shell):"
cat <<'EOF'
python manage.py migrate --database=default
python manage.py migrate --database=analytics
python manage.py collectstatic --noinput
EOF

echo "5) Optional: create admin user"
echo "python manage.py createsuperuser"

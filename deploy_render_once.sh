#!/usr/bin/env bash
set -euo pipefail

echo "1) Validate render.yaml"
render blueprints validate ./render.yaml

echo "2) Ensure scripts are executable (Linux/macOS/WSL)"
chmod +x start_web.sh start_worker.sh || true

echo "3) Push to GitHub (Render Blueprints deploy from repo)"
git status --porcelain
echo "If you have uncommitted changes: git add . && git commit -m 'Render deploy fixes' && git push"

echo "4) Deploy via Render Dashboard"
echo "Render -> New + -> Blueprint -> select this repo -> Deploy Blueprint"

echo "5) After first deploy: create an admin user (optional)"
cat <<'EOF'
# In Render dashboard -> icecream-web -> Shell:
python manage.py createsuperuser
EOF

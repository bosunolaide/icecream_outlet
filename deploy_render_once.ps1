# Deploy Ice Cream Outlet (Render) - Windows PowerShell helper
# Usage (PowerShell):
#   Set-ExecutionPolicy -Scope Process Bypass
#   .\deploy_render_once.ps1
#
# This script validates render.yaml and reminds you of the correct Render steps.
# Render Blueprints deploy from GitHub repos, so push first.

$ErrorActionPreference = "Stop"

Write-Host "1) Validating render.yaml..." -ForegroundColor Cyan
render blueprints validate ./render.yaml

Write-Host "`n2) Git status (Render deploys from GitHub)..." -ForegroundColor Cyan
git status

Write-Host "`n3) If you have changes, run:" -ForegroundColor Yellow
Write-Host "   git add ."
Write-Host "   git commit -m `"Render deploy fixes`""
Write-Host "   git push"

Write-Host "`n4) Deploy in Render Dashboard:" -ForegroundColor Cyan
Write-Host "   Render -> New + -> Blueprint -> select this repo -> Deploy Blueprint"

Write-Host "`n5) Post-deploy (optional): create superuser" -ForegroundColor Cyan
Write-Host "   Render dashboard -> icecream-web -> Shell:"
Write-Host "   python manage.py createsuperuser"

Write-Host "`nDone." -ForegroundColor Green

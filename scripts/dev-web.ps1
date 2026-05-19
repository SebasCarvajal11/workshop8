# API (8000) + frontend Vite (5173)
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

Start-Process -NoNewWindow -FilePath "$root\.venv\Scripts\python.exe" -ArgumentList "-m", "pricing_expert.api.runner"
Start-Sleep -Seconds 2
Set-Location "$root\web"
pnpm dev

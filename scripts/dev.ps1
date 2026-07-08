# DevOps Knowledge Copilot — dev commands (Windows)
# Industry teams use Makefile or scripts like this instead of remembering long commands.

param(
    [Parameter(Position = 0)]
    [ValidateSet("help", "demo", "infra", "up", "down", "api", "test", "ask", "index", "ui-local")]
    [string]$Command = "help"
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

function Ensure-Venv {
    if (-not (Test-Path ".venv\Scripts\Activate.ps1")) {
        Write-Host "Create venv first: py -3 -m venv .venv" -ForegroundColor Yellow
        exit 1
    }
}

switch ($Command) {
    "help" {
        Write-Host @"
Portfolio demo commands (all free, local):

  .\scripts\dev.ps1 demo      Start Qdrant + show interview demo steps
  .\scripts\dev.ps1 api       API — run in terminal 1
  .\scripts\dev.ps1 ui-local  UI — run in terminal 2 (http://localhost:8080)
  .\scripts\dev.ps1 ask       CLI chat (simplest demo, no browser)
  .\scripts\dev.ps1 test      pytest
  .\scripts\dev.ps1 infra     Qdrant only
  .\scripts\dev.ps1 up        Full Docker stack (optional)
  .\scripts\dev.ps1 down      Stop containers

Interview guide: docs/PORTFOLIO.md
"@
    }
    "demo" {
        docker compose up -d qdrant
        Write-Host ""
        Write-Host "=== Portfolio demo (free, local) ===" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "1. Keep Ollama running (system tray)"
        Write-Host "2. Terminal 1:  .\scripts\dev.ps1 api"
        Write-Host "3. Terminal 2:  .\scripts\dev.ps1 ui-local"
        Write-Host "4. Browser:     http://localhost:8080"
        Write-Host ""
        Write-Host "Simplest (no UI):  python scripts/06_ask.py -i" -ForegroundColor Yellow
        Write-Host ""
    }
    "infra" {
        docker compose up -d qdrant
        Write-Host "Qdrant: http://localhost:6333/dashboard"
    }
    "up" {
        docker compose up -d --build
        Write-Host "UI:  http://localhost:8080"
        Write-Host "API: http://localhost:8000/docs"
    }
    "down" {
        docker compose down
    }
    "api" {
        Ensure-Venv
        .\.venv\Scripts\Activate.ps1
        uvicorn src.api.main:app --reload
    }
    "test" {
        Ensure-Venv
        .\.venv\Scripts\Activate.ps1
        pytest tests/ -q
    }
    "index" {
        Ensure-Venv
        .\.venv\Scripts\Activate.ps1
        python scripts/02_ingest.py
        python scripts/03_chunk.py
        python scripts/04_index.py
    }
    "ask" {
        Ensure-Venv
        .\.venv\Scripts\Activate.ps1
        python scripts/06_ask.py -i
    }
    "ui-local" {
        Write-Host "Start API first: .\scripts\dev.ps1 api"
        Write-Host "UI: http://localhost:8080  (Ctrl+C to stop)"
        python -m http.server 8080 --directory docs
    }
}

# DevOps Knowledge Copilot — dev commands (Windows)
# Industry teams use Makefile or scripts like this instead of remembering long commands.

param(
    [Parameter(Position = 0)]
    [ValidateSet("help", "infra", "up", "down", "api", "test", "ask", "index", "ui-local")]
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
Standard commands (industry-style dev workflow):

  .\scripts\dev.ps1 infra      Start Qdrant only
  .\scripts\dev.ps1 up         Full stack: Qdrant + API + UI (Docker)
  .\scripts\dev.ps1 down       Stop all containers
  .\scripts\dev.ps1 api        API with hot reload (local Python)
  .\scripts\dev.ps1 test       Run pytest (same as CI)
  .\scripts\dev.ps1 index      Run ingest + chunk + index (02-04)
  .\scripts\dev.ps1 ask        Interactive RAG CLI
  .\scripts\dev.ps1 ui-local   Open static UI at http://localhost:8080

Docs: docs/OPERATIONS.md
"@
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

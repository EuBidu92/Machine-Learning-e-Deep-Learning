$ErrorActionPreference = "Stop"

Write-Host "Criando ambiente virtual..."
if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

Write-Host "Ativando ambiente virtual..."
& ".\.venv\Scripts\Activate.ps1"

Write-Host "Atualizando pip e instalando dependencias..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Arquivo .env criado a partir do exemplo. Edite-o com suas credenciais."
} else {
    Write-Host "Arquivo .env ja existe; nao foi alterado."
}

Write-Host "Concluido. Edite .env e execute: python -m uvicorn main:app --reload"

# [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$ErrorActionPreference = "Stop"

# --- Gerenciamento do MongoDB ---
$mongoService = Get-Service -Name "MongoDB"
if ($mongoService.Status -ne "Running") {
    Start-Service -Name "MongoDB"
}

if ($mongoService.Status -eq "Stopped") {
    Restart-Service -Name "MongoDB"
}
Get-Service -Name "MongoDB"

# --- Checando se ffmpeg está instalado ---
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
    Write-Host "Installing ffmpeg..."
    winget install ffmpeg
    Write-Warning "FFmpeg foi instalado. Pode ser necessário reiniciar o terminal para aplicar o PATH."
}

# --- Validação de Arquivos Críticos ---
if (-not (Test-Path "./flask_backend/permalink-googleDrive-pibiti6-nervo.json")) {
    Write-Error "permalink-googleDrive-pibiti6-nervo.json file not found in FLASK directory"
    exit 1
}

if (-not (Test-Path "./env.csv")) {
    Write-Error "env.csv file not found"
    exit 1
}

# --- Configuração do MSYS2 / Pango (Geração de PDF) ---
if (-not (Test-Path "C:\msys64")) {
    Write-Host "MSYS2 not found. Downloading installer..."
    $msys2InstallerUrl = "https://github.com/msys2/msys2-installer/releases/download/2025-02-21/msys2-x86_64-20250221.exe"
    $installerPath = "$env:TEMP\msys2-installer.exe"
    Invoke-WebRequest -Uri $msys2InstallerUrl -OutFile $installerPath

    Write-Host "Installing MSYS2 with default options..."
    Start-Process -FilePath $installerPath -ArgumentList "/S" -Wait
}

if (-not ($env:Path -split ';' | ForEach-Object { $_.Trim() } | Where-Object { $_ -eq "C:\msys64\mingw64\bin" })) {
    Write-Error "C:\msys64\mingw64\bin was not added to PATH on Windows. Exiting."
    exit 1
}

& "C:\msys64\usr\bin\bash.exe" -l -c "pacman -Qs pango"
if ($LASTEXITCODE -ne 0) {
    Write-Host "MSYS packages not found. Installing with MSYS2..."
    
    & "C:\msys64\usr\bin\bash.exe" -l -c "pacman -S --noconfirm mingw-w64-ucrt-x86_64-toolchain"
    if ($LASTEXITCODE -ne 0) { Write-Error "Error installing mingw-w64-ucrt-x86_64-toolchain"; exit 1 }
    
    & "C:\msys64\usr\bin\bash.exe" -l -c "pacman -S --noconfirm mingw-w64-ucrt-x86_64-python-gobject"
    if ($LASTEXITCODE -ne 0) { Write-Error "Error installing mingw-w64-ucrt-x86_64-gtk3"; exit 1 }
    
    & "C:\msys64\usr\bin\bash.exe" -l -c "pacman -S --noconfirm mingw-w64-x86_64-pango"
    if ($LASTEXITCODE -ne 0) { Write-Error "Error installing mingw-w64-x86_64-pango"; exit 1 }
}
else {
    Write-Host "MSYS packages already installed. Skipping installation."
}

# --- Frontend Node.js / Vite ---
if (-not (Test-Path "./vite-project/node_modules/")) {
    Write-Host "Installing packages into Vite Project..."
    Set-Location -Path "vite-project"
    npm install
    npm install -g vite
    Set-Location -Path ".."
}

Write-Host "Starting Node Frontend Server"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location 'vite-project'; npm run dev"

# --- Backend Python com UV + pyproject.toml ---
$backendDir = "flask_backend"
$venvPath = "$backendDir/.venv"

# 1. Garante que o UV está instalado via winget
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "uv não encontrado. Instalando via winget..."
    winget install astral-sh.uv
    # Atualiza o PATH na sessão atual do PowerShell
    $env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User")
}

# 2. Cria e sincroniza o ambiente virtual baseado no pyproject.toml
if (-not (Test-Path $venvPath)) {
    Write-Host "Criando ambiente virtual e instalando dependências com uv..."
    # Entra na pasta do backend para o uv ler o pyproject.toml corretamente
    Set-Location -Path $backendDir
    
    # Cria o venv e instala/sincroniza as dependências do pyproject.toml de uma vez só
    uv venv
    uv sync
    
    Set-Location -Path ".."
}

# 3. Inicia o Flask chamando o interpretador do .venv localizado dentro de flask_backend
Write-Host "Starting Flask Backend com UV"
$pythonVenvPath = "./$venvPath/Scripts/python.exe"

Start-Process -FilePath $pythonVenvPath -ArgumentList "server.py" -WorkingDirectory $backendDir
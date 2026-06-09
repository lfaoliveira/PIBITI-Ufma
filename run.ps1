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

# if (-not (Test-Path "./env")) {
#     Write-Error ".env  not found"
#     exit 1
# }

# --- Configuração do MSYS2 / Pango (Geração de PDF) ---
if (-not (Test-Path "C:\msys64")) {
    Write-Host "MSYS2 not found. Downloading installer..."
    $msys2InstallerUrl = "https://github.com/msys2/msys2-installer/releases/download/2025-02-21/msys2-x86_64-20250221.exe"
    $installerPath = "$env:TEMP\msys2-installer.exe"
    Invoke-WebRequest -Uri $msys2InstallerUrl -OutFile $installerPath

    Write-Host "Installing MSYS2 with default options..."
    Start-Process -FilePath $installerPath -ArgumentList "/S" -Wait
    # Adiciona os caminhos do MSYS2 ao PATH da sessão atual após instalação
    $env:Path += ";C:\\msys64\\mingw64\\bin;C:\\msys64\\ucrt64\\bin;C:\\msys64\\usr\\bin"}

# Verifica se o caminho do MSYS2 está acessível via diferentes variantes de caminho
$msysPaths = @(
    "C:\msys64\mingw64\bin",
    "C:\msys64\ucrt64\bin",
    "C:\msys64\usr\bin"
)

$msysPathFound = $false
foreach ($path in $msysPaths) {
    if ($env:Path -split ';' | ForEach-Object { $_.Trim() } | Where-Object { $_ -eq $path }) {
        $msysPathFound = $true
        break
    }
}

if (-not $msysPathFound) {
    Write-Error "Nenhum dos caminhos do MSYS2 foi encontrado no PATH: C:\\msys64\\mingw64\\bin, C:\\msys64\\ucrt64\\bin, C:\\msys64\\usr\\bin. Verifique a instalação e o PATH."
    exit 1
}

# --- Validação do MSYS2 ---
# Tenta localizar comandos essenciais dentro do ambiente MSYS2
Write-Host "Validando ambiente MSYS2..."
$msysCheck = & C:\msys64\usr\bin\bash.exe -l -c "pacman -Qs pango-view && pacman -Qs gcc"
if ($LASTEXITCODE -ne 0) {
    Write-Error "Comandos essenciais nao encontrados no ambiente MSYS2. Saida: $msysCheck"
    exit 1
}

# --- Verificação e instalação de pacotes MSYS2 ---
Write-Host "MSYS2 validado com sucesso."

# Verifica e instala pacotes essenciais do MSYS2
$msysPackages = @(
    "mingw-w64-ucrt-x86_64-toolchain",  # Compilador GCC e ferramentas de compilação
    "mingw-w64-ucrt-x86_64-python-gobject",  # Para integração Python/GTK
    "mingw-w64-ucrt-x86_64-pango"  # Para geração de PDF com suporte a texto
)

Write-Host "Verificando e instalando pacotes do MSYS2..."

# Garante que o ambiente MSYS2 está acessível
if (-not (Test-Path "C:\\msys64\\usr\\bin\\bash.exe")) {
    Write-Error "Bash do MSYS2 não encontrado em C:\\msys64\\usr\\bin\\bash.exe"
    exit 1
}

# Atualiza o banco do pacman e os pacotes base (pode demorar na primeira vez)
Write-Host "Atualizando pacman e pacotes base (pacman -Syu)..."
& "C:\\msys64\\usr\\bin\\bash.exe" -l -c "pacman -Syu --noconfirm --needed"
if ($LASTEXITCODE -ne 0) {
    Write-Warning "pacman -Syu retornou erro. Tentando novamente uma vez."
    & "C:\\msys64\\usr\\bin\\bash.exe" -l -c "pacman -Syu --noconfirm --needed"
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Falha ao atualizar pacman/pacotes base. Verifique a instalação do MSYS2.";
        exit 1
    }
}

foreach ($package in $msysPackages) {
    Write-Host "Checando pacote: $package"
    & "C:\\msys64\\usr\\bin\\bash.exe" -l -c "pacman -Qi $package >/dev/null 2>&1"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Instalando pacote: $package"
        & "C:\\msys64\\usr\\bin\\bash.exe" -l -c "pacman -S --noconfirm $package"
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Erro ao instalar o pacote $package"
            exit 1
        }
        Write-Host "Pacote $package instalado com sucesso."
    } else {
        Write-Host "Pacote $package já está instalado."
    }
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
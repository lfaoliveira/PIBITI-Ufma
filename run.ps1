$mongoService = Get-Service -Name "MongoDB"
if ($mongoService.Status -eq "Stopped") {
    Restart-Service -Name "MongoDB"
}
# checando se ffmpeg esta instalado
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
    Write-Host "Installing ffmpeg..."
    winget install ffmpeg
    Restart-Computer
}

Get-Service -Name "MongoDB"

if (-not (Test-Path "./FLASK/permalink-googleDrive-pibiti6-nervo.json")) {
    Write-Error "permalink-googleDrive-pibiti6-nervo.json file not found in FLASK directory"
    exit 1
}

<# This part is for pdf generation #>
# Install MSYS2 if not already installed
if (-not (Test-Path "C:\msys64")) {
    Write-Host "MSYS2 not found. Downloading installer..."
    $msys2InstallerUrl = "https://github.com/msys2/msys2-installer/releases/download/2025-02-21/msys2-x86_64-20250221.exe"
    $installerPath = "$env:TEMP\msys2-installer.exe"
    Invoke-WebRequest -Uri $msys2InstallerUrl -OutFile $installerPath

    Write-Host "Installing MSYS2 with default options..."
    Start-Process -FilePath $installerPath -ArgumentList "/S" -Wait
}
if (-not ($env:Path -like "*C:\msys64\mingw64\bin*")) {
    Write-Error "C:\msys64\mingw64\bin was not added to PATH on Windows. Exiting."
    exit 1
}

# checking Pango
&  "C:\msys64\usr\bin\bash.exe" -l -c "pacman -Qs pango"
if ($LASTEXITCODE -ne 0) {
    Write-Host "MSYS packages not found. Installing with MSYS2..."
    
    & "C:\msys64\usr\bin\bash.exe" -l -c "pacman -S --noconfirm mingw-w64-ucrt-x86_64-toolchain"
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Error installing mingw-w64-ucrt-x86_64-toolchain"
        exit 1
    }
    
    & "C:\msys64\usr\bin\bash.exe" -l -c "pacman -S --noconfirm mingw-w64-ucrt-x86_64-python-gobject"
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Error installing mingw-w64-ucrt-x86_64-gtk3"
        exit 1
    }
    & "C:\msys64\usr\bin\bash.exe" -l -c "pacman -S --noconfirm mingw-w64-x86_64-pango"
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Error installing mingw-w64-x86_64-pango"
        exit 1
    }

    <# & "C:\msys64\usr\bin\bash.exe" -l -c "pacman -S --noconfirm mingw-w64-x86_64-fontconfig"
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Error installing mingw-w64-x86_64-fontconfig"
        exit 1
    } #>
    

} else {
    Write-Host "MSYS packages already installed. Skipping installation."
}


#Check if node packages are installed
if (-not (Test-Path "./vite-project/node_modules/")) {
    Write-Host "Installing packages into $PWD"
    Set-Location -Path "vite-project"
    npm install
    npm install -g vite
    Set-Location -Path ".."
}
Write-Host "Starting Node Frontend Server"
#Start Node+Vite+Vue server
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location 'vite-project'; npm run dev"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Node server failed to start with exit code: $LASTEXITCODE"
}

$nomeConda = "env-pibiti"
# Activate conda environment if it doesnt exist
if (-not (Test-Path "./$nomeConda")) {
    conda env create --prefix "./$nomeConda" --file ./conda.yml
}

Write-Host "Starting Flask Backend"
conda activate "./$nomeConda"
if (-not (Test-Path "./env.csv")) {
    Write-Error "env.csv file not found"
    exit 1
}
# Start Flask server
Start-Process -FilePath "python" -ArgumentList "server.py" -WorkingDirectory "FLASK" -NoNewWindow

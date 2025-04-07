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

$nomeConda = "env-pibiti"
# Activate conda environment if it doesnt exist
if (-not (Test-Path "./$nomeConda")) {
    conda env create --prefix "./$nomeConda" --file ./conda.yml
}
<# conda init#>
Write-Host "Starting Flask Backend"
conda activate "./$nomeConda"
if (-not (Test-Path "./env.csv")) {
    Write-Error "env.csv file not found"
    exit 1
}
# Start Flask server
Start-Process -FilePath "python" -ArgumentList "server.py" -WorkingDirectory "FLASK"


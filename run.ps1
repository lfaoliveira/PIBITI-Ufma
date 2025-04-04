$mongoService = Get-Service -Name "MongoDB"
if ($mongoService.Status -eq "Stopped") {
    Restart-Service -Name "MongoDB"
}

Get-Service -Name "MongoDB"

#Start Node+Vite+Vue server
Start-Process -FilePath "npm" -ArgumentList "run dev" -WorkingDirectory "vite-project"

# Activate conda environment if it doesnt exist
if (-not (Test-Path "./.conda/")) {
    conda env create --prefix env-pibiti --file conda.yml
}
conda activate ./env-pibiti
if (-not (Test-Path "./env.csv")) {
    Write-Error "env.csv file not found"
    exit 1
}
# Start Flask server
Start-Process -FilePath "python" -ArgumentList "server.py" -WorkingDirectory "FLASK"


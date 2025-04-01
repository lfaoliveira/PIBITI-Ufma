$mongoService = Get-Service -Name "MongoDB"
if ($mongoService.Status -eq "Stopped") {
    Restart-Service -Name "MongoDB"
}

Get-Service -Name "MongoDB"

#Start Node+Vite+Vue server
Start-Process -FilePath "npm" -ArgumentList "run dev" -WorkingDirectory "vite-project"

# Activate conda environment from root directory
conda activate ".\.conda"
# Start Flask server
Start-Process -FilePath "python" -ArgumentList "server.py" -WorkingDirectory "FLASK"


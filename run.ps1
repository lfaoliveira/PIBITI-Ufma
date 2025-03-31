# MongoDB
$mongoService = Get-Service -Name "MongoDB"
if ($mongoService.Status -eq "Stopped") {
    Restart-Service -Name "MongoDB"
}
# Activate conda environment from root directory
$secretKey = Read-Host -Prompt "Digite chave secreta do servidor (Ver google drive)"
$env:SECRET_KEY = $secretKey

Get-Service -Name "MongoDB"

#Start Node+Vite+Vue server
Start-Process -FilePath "npm" -ArgumentList "run dev" -WorkingDirectory "vite-project"

# Start Flask server
conda activate ".\.conda"
Start-Process -FilePath "python" -ArgumentList "server.py" -WorkingDirectory "FLASK"


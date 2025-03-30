# MongoDB
$mongoService = Get-Service -Name "MongoDB"
if ($mongoService.Status -eq "Stopped") {
    Restart-Service -Name "MongoDB"
}

Get-Service -Name "MongoDB"
#Start Node server
Set-Location -Path "vite-project"
Start-Process "npm" -ArgumentList "run dev"
# Start Flask server
Set-Location -Path "..\FLASK"
& conda activate .
Start-Process "python" -ArgumentList "server.py"
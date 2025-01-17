#Start Node server
Set-Location -Path "vite-project"
Start-Process "npm" -ArgumentList "run dev"
# Start Flask server
Set-Location -Path "..\FLASK"
Start-Process "python" -ArgumentList "server.py"
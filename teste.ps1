# 1. Ensure TLS 1.2
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$ErrorActionPreference = "Stop"
# Run PowerShell as Administrator and execute the script


<# if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    # Relaunch the script with elevated privileges
    Start-Process powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    # Exit the current non-elevated session
    exit
} 
 #>
# ----------------------------------------
# Variables: adjust versions or paths here
# ----------------------------------------
$serverVersion  = '8.0.6'
$installDir     = "C:\Program Files\MongoDB\Server\$serverVersion"
$serverUrl = "https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-$serverVersion-signed.msi"
$serverMsi      = Join-Path $env:TEMP "mongodb-server.msi"
$serviceName    = 'MongoDB'
$configFile     = Join-Path $installDir 'bin\mongod.cfg'
$logFile        = Join-Path $env:TEMP 'mongodb-install.log'

# 3. Ensure the install directory and bin subdirectory exist
if (-Not (Test-Path $installDir)) {
    New-Item -ItemType Directory -Path $installDir -Force | Out-Null
    Write-Output "Created install directory at $installDir"
}
$binDir = Join-Path $installDir 'bin'
if (-Not (Test-Path $binDir)) {
    New-Item -ItemType Directory -Path $binDir -Force | Out-Null
    Write-Output "Created bin directory at $binDir"
}
# 4. Try BitsTransfer first (more reliable)

if (-Not (Test-Path $serverMsi)) {
    Start-BitsTransfer -Source $serverUrl -Destination $serverMsi -ErrorAction Stop
    Write-Host "Downloaded MongoDB Server via BITS"
}

Start-Process -FilePath 'msiexec.exe' `
  -ArgumentList "/i `"$serverMsi`" /qn INSTALLLOCATION=`"$installDir`" ADDLOCAL=All /l*v `"$logFile`"" `
  -Wait
Write-Output "Installed MongoDB Server binaries to $installDir"

# ----------------------------------------
# 5. Create the mongod.cfg if missing
# ----------------------------------------
if (-Not (Test-Path $configFile)) {
  @"
systemLog:
  destination: file
  path: "$installDir\data\log\mongod.log"
storage:
  dbPath: "$installDir\data\db"
net:
  bindIp: 127.0.0.1
  port: 27017
"@ | Out-File -FilePath $configFile -Encoding UTF8
  Write-Output "Created default config at $configFile"
}

# -ErrorAction SilentlyContinue
$mongoService = Get-Service -Name $serviceName

if ($mongoService ) {
    if ((Get-Service -Name $serviceName).Status -eq 'Running') {
        Stop-Service -Name $serviceName -Force
        Write-Output "Stopped running service '$serviceName'"
    }
  sc.exe delete $serviceName
}
# Create service to run under NetworkService
sc.exe create $serviceName `
  binPath= "\"$installDir\bin\mongod.exe\" --config \"$configFile\" --service" `
  DisplayName= "MongoDB Database" `
  start= auto `
  obj= "NT AUTHORITY\NetworkService"
Write-Output "Configured `$serviceName` to run as NT AUTHORITY\NetworkService"
# :contentReference[oaicite:11]{index=11}

# ----------------------------------------
# 7. Start the MongoDB service
# ----------------------------------------
Start-Service -Name $serviceName
Write-Output "Started MongoDB service '$serviceName' under NetworkService"
# :contentReference[oaicite:12]{index=12}

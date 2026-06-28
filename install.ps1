# Folder Sorter CLI installer script for Windows (Production Binary-Only).

$ErrorActionPreference = "Stop"

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "      Installing Folder Sorter CLI...              " -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

# Fetch latest release details from GitHub API
Write-Host "Fetching latest release information..."
$ApiUrl = "https://api.github.com/repos/Debanjan110d/Folder-Sorter/releases/latest"

try {
    # Set TLS 1.2
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    $ReleaseInfo = Invoke-RestMethod -Uri $ApiUrl -UseBasicParsing
    $Tag = $ReleaseInfo.tag_name
} catch {
    # Fallback default version
    $Tag = "v1.0.0"
    Write-Host "Warning: Could not parse tag from GitHub API. Defaulting to $Tag." -ForegroundColor Yellow
}

$AssetUrl = "https://github.com/Debanjan110d/Folder-Sorter/releases/download/$Tag/folder-sorter-windows.zip"
Write-Host "Latest release tag found: $Tag"
Write-Host "Downloading prebuilt binary from: $AssetUrl"

$INSTALL_DIR = "$env:LOCALAPPDATA\FolderSorter"
$BIN_DIR = "$INSTALL_DIR\bin"

# Create target directories
if (!(Test-Path $BIN_DIR)) {
    New-Item -ItemType Directory -Path $BIN_DIR | Out-Null
}

# Download to temp zip
$TempZip = [System.IO.Path]::GetTempFileName() + ".zip"
try {
    Invoke-WebRequest -Uri $AssetUrl -OutFile $TempZip -UseBasicParsing
} catch {
    Write-Host "Error: Failed to download release asset from GitHub." -ForegroundColor Red
    Write-Host "Please verify that a release exists at: https://github.com/Debanjan110d/Folder-Sorter/releases" -ForegroundColor Red
    if (Test-Path $TempZip) { Remove-Item $TempZip }
    exit 1
}

# Extract binary
Write-Host "Extracting binary..."
try {
    Expand-Archive -Path $TempZip -DestinationPath $BIN_DIR -Force
} finally {
    if (Test-Path $TempZip) { Remove-Item $TempZip }
}

# Modify User PATH Environment Variable
Write-Host "Configuring Environment PATH variables..."
$UserPath = [Environment]::GetEnvironmentVariable("PATH", [EnvironmentVariableTarget]::User)
$PathSplit = $UserPath -split ';'
$IsAlreadyInPath = $false

foreach ($Path in $PathSplit) {
    if ($Path.Trim().TrimEnd('\') -eq $BIN_DIR.Trim().TrimEnd('\')) {
        $IsAlreadyInPath = $true
        break
    }
}

if (!$IsAlreadyInPath) {
    Write-Host "Adding $BIN_DIR to User PATH environment..." -ForegroundColor Yellow
    $NewUserPath = $UserPath
    if (!$NewUserPath.EndsWith(';')) {
        $NewUserPath += ";"
    }
    $NewUserPath += $BIN_DIR
    [Environment]::SetEnvironmentVariable("PATH", $NewUserPath, [EnvironmentVariableTarget]::User)
    
    # Update current session environment PATH
    $env:PATH += ";$BIN_DIR"
}

# Install shell completions for powershell
Write-Host "Setting up PowerShell command autocompletions..."
try {
    & "$BIN_DIR\folder-sorter.exe" --install-completion powershell
} catch {
    # Fail-safe
}

Write-Host ""
Write-Host "Successfully installed Folder Sorter!" -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Cyan

# Verify & Run diagnostics
Write-Host "Running diagnostics check..."
& "$BIN_DIR\folder-sorter.exe" doctor

if (!$IsAlreadyInPath) {
    Write-Host ""
    Write-Host "IMPORTANT: We have added folder-sorter to your environment PATH." -ForegroundColor Yellow
    Write-Host "Please close and reopen your current terminal/PowerShell window to use 'folder-sorter' globally." -ForegroundColor Yellow
}

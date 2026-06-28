# Folder Sorter CLI installer script for Windows.

$ErrorActionPreference = "Stop"

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "      Installing Folder Sorter CLI...              " -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

# Check for Python
$PythonCmd = $null
if (Get-Command "python" -ErrorAction SilentlyContinue) {
    $PythonCmd = "python"
} elseif (Get-Command "py" -ErrorAction SilentlyContinue) {
    $PythonCmd = "py"
}

if ($null -eq $PythonCmd) {
    Write-Host "Error: Python 3 is required but was not found on your system." -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher from python.org and try again." -ForegroundColor Red
    exit 1
}

# Verify Python Version
$PyVerString = & $PythonCmd -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
Write-Host "Found Python $PyVerString..."

$INSTALL_DIR = "$HOME\.folder-sorter"
$BIN_DIR = "$INSTALL_DIR\bin"

Write-Host "Creating environment directory at $INSTALL_DIR..."
if (!(Test-Path $INSTALL_DIR)) {
    New-Item -ItemType Directory -Path $INSTALL_DIR | Out-Null
}

# Create Virtualenv
Write-Host "Creating python virtual environment..."
& $PythonCmd -m venv "$INSTALL_DIR\venv"

# Resolve Source Path
if (Test-Path ".\pyproject.toml") {
    Write-Host "Installing from local repository folder..."
    $SRC_PATH = (Get-Item ".").FullName
} else {
    Write-Host "Downloading Folder Sorter source from GitHub..."
    $SRC_PATH = "$INSTALL_DIR\src"
    if (Test-Path $SRC_PATH) {
        Remove-Item -Recurse -Force $SRC_PATH
    }
    if (!(Get-Command "git" -ErrorAction SilentlyContinue)) {
        Write-Host "Error: Git is required to clone the source code repository." -ForegroundColor Red
        exit 1
    }
    & git clone https://github.com/Debanjan110d/Folder-Sorter.git $SRC_PATH
}

# Upgrade pip and install
Write-Host "Installing package dependencies..."
& "$INSTALL_DIR\venv\Scripts\pip.exe" install --upgrade pip --quiet
& "$INSTALL_DIR\venv\Scripts\pip.exe" install $SRC_PATH --quiet

# Register wrapper script
Write-Host "Registering folder-sorter executable commands..."
if (!(Test-Path $BIN_DIR)) {
    New-Item -ItemType Directory -Path $BIN_DIR | Out-Null
}

$WrapperContent = @"
@echo off
"$INSTALL_DIR\venv\Scripts\folder-sorter.exe" %*
"@
Set-Content -Path "$BIN_DIR\folder-sorter.cmd" -Value $WrapperContent

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
    & "$BIN_DIR\folder-sorter.cmd" --install-completion powershell
} catch {
    # Fail-safe
}

Write-Host ""
Write-Host "Successfully installed Folder Sorter!" -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Cyan

# Verify & Run diagnostics
Write-Host "Running diagnostics check..."
& "$BIN_DIR\folder-sorter.cmd" doctor

if (!$IsAlreadyInPath) {
    Write-Host ""
    Write-Host "IMPORTANT: We have added folder-sorter to your environment PATH." -ForegroundColor Yellow
    Write-Host "Please close and reopen your current terminal/PowerShell window to use 'folder-sorter' globally." -ForegroundColor Yellow
}

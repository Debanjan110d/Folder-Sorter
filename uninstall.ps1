# Folder Sorter CLI uninstaller script for Windows.

$ErrorActionPreference = "Stop"

Write-Host "====================================================" -ForegroundColor Yellow
Write-Host "      Uninstalling Folder Sorter CLI...            " -ForegroundColor Yellow
Write-Host "====================================================" -ForegroundColor Yellow

$INSTALL_DIR = "$env:LOCALAPPDATA\FolderSorter"

# Remove installation directory
if (Test-Path $INSTALL_DIR) {
    Write-Host "Removing installation files at $INSTALL_DIR..."
    Remove-Item -Recurse -Force $INSTALL_DIR
} else {
    Write-Host "Installation directory $INSTALL_DIR not found. Skipping folder removal."
}

# Remove path from User PATH variable
Write-Host "Cleaning up Environment PATH variable..."
$UserPath = [Environment]::GetEnvironmentVariable("PATH", [EnvironmentVariableTarget]::User)
$PathSplit = $UserPath -split ';'
$NewPaths = @()
$Found = $false

foreach ($Path in $PathSplit) {
    $Trimmed = $Path.Trim().TrimEnd('\')
    if ($Trimmed -eq $INSTALL_DIR.Trim().TrimEnd('\')) {
        $Found = $true
    } elseif ($Trimmed -ne "") {
        $NewPaths += $Path
    }
}

if ($Found) {
    $NewUserPath = $NewPaths -join ';'
    [Environment]::SetEnvironmentVariable("PATH", $NewUserPath, [EnvironmentVariableTarget]::User)
    Write-Host "Removed $INSTALL_DIR from User PATH variable." -ForegroundColor Green
} else {
    Write-Host "No PATH entry found for $INSTALL_DIR."
}

Write-Host ""
Write-Host "Uninstall complete. Folder Sorter has been removed." -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Yellow

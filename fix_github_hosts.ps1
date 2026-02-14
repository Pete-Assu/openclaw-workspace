# Fix GitHub hosts file
# Run this script as Administrator to fix GitHub connectivity

$hostsPath = "C:\Windows\System32\drivers\etc\hosts"
$backupPath = "$hostsPath.backup.$(Get-Date -Format 'yyyyMMdd_HHmmss')"

Write-Host "=" * 60
Write-Host "GitHub Hosts File Fix"
Write-Host "=" * 60

# Check if running as administrator
$currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object System.Security.Principal.WindowsPrincipal($currentUser)
$isAdmin = $principal.IsInRole([System.Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "[ERROR] Please run this script as Administrator!" -ForegroundColor Red
    Write-Host "[INFO] Right-click PowerShell -> Run as Administrator" -ForegroundColor Yellow
    exit 1
}

Write-Host "[OK] Running as Administrator" -ForegroundColor Green

# Backup current hosts file
if (Test-Path $hostsPath) {
    Copy-Item $hostsPath $backupPath
    Write-Host "[BACKUP] Created: $backupPath" -ForegroundColor Cyan
}

# Read hosts file
$content = Get-Content $hostsPath -Raw

# GitHub domains to remove
$githubDomains = @(
    "github.dev",
    "api.github.com",
    "github.githubassets.com",
    "support-assets.githubassets.com",
    "education.github.com",
    "resources.githubassets.com",
    "uploads.github.com",
    "archiveprogram.github.com",
    "raw.github.com",
    "githubusercontent.com",
    "raw.githubusercontent.com",
    "camo.githubusercontent.com",
    "cloud.githubusercontent.com",
    "avatars.githubusercontent.com",
    "avatars0.githubusercontent.com",
    "avatars1.githubusercontent.com",
    "avatars2.githubusercontent.com",
    "avatars3.githubusercontent.com",
    "user-images.githubusercontent.com",
    "objects.githubusercontent.com",
    "private-user-images.githubusercontent.com",
    "github.com",
    "pages.github.com",
    "gist.github.com",
    "githubapp.com",
    "github.io",
    "www.github.io"
)

# Count lines to remove
$originalLines = $content -split "`n" | Where-Object { $_ -match "github" }
$count = ($originalLines | Measure-Object).Count

if ($count -eq 0) {
    Write-Host "[INFO] No GitHub entries found in hosts file" -ForegroundColor Yellow
    exit 0
}

Write-Host "[INFO] Found $count GitHub entries to remove" -ForegroundColor Yellow

# Remove GitHub entries (lines containing any GitHub domain)
$newContent = $content
foreach ($domain in $githubDomains) {
    $newContent = $newContent -replace ".*$domain.*`n?", ""
}

# Clean up multiple blank lines
$newContent = $newContent -replace "`n{3,}", "`n`n"
$newContent = $newContent.Trim()

# Write new content
Set-Content -Path $hostsPath -Value $newContent -Encoding UTF8

Write-Host "[OK] Removed $count GitHub entries" -ForegroundColor Green
Write-Host "[OK] Hosts file updated" -ForegroundColor Green

# Verify
Write-Host "`n[VERIFY] Testing DNS resolution..."
$test = [System.Net.Dns]::GetHostAddresses("github.com")
Write-Host "[OK] github.com resolves to: $($test[0].IPAddressToString)" -ForegroundColor Green

Write-Host "`n" + "=" * 60
Write-Host "GitHub connectivity should now work!" -ForegroundColor Green
Write-Host "=" * 60

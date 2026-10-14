param([Parameter(Mandatory=$true)][string]$Zip)
$ErrorActionPreference = 'Stop'
$source = (Resolve-Path $Zip).Path
$dest = Join-Path $env:USERPROFILE '.codex\skills\periplus'
$tmp = Join-Path ([System.IO.Path]::GetTempPath()) ('periplus-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $tmp -Force | Out-Null
try {
    Expand-Archive -LiteralPath $source -DestinationPath $tmp -Force
    $src = Join-Path $tmp 'periplus'
    if (-not (Test-Path (Join-Path $src 'SKILL.md'))) { throw 'Invalid ZIP: missing periplus/SKILL.md' }
    New-Item -ItemType Directory -Path (Split-Path $dest) -Force | Out-Null
    if (Test-Path $dest) {
        $backup = $dest + '.backup-' + (Get-Date -Format 'yyyyMMdd-HHmmss')
        Move-Item $dest $backup
        Write-Host "Previous version backed up to $backup"
    }
    Copy-Item -LiteralPath $src -Destination $dest -Recurse
    if (-not (Test-Path (Join-Path $dest 'SKILL.md'))) { throw 'Installation integrity check failed' }
    $installedVersion = (Get-Content -LiteralPath (Join-Path $dest 'VERSION') -Raw).Trim()
    Write-Host "Installed Periplus $installedVersion to $dest" -ForegroundColor Green
    Write-Host 'Restart Codex. Then invoke $periplus with travel inputs.'
} finally {
    if (Test-Path $tmp) { Remove-Item $tmp -Force -Recurse }
}

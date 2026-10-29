Write-Host "=== 1. PROCESSES WITH WINDOWS ==="
Get-Process | ForEach-Object {
    if ($_.MainWindowTitle) {
        [PSCustomObject]@{
            ProcessName = $_.ProcessName
            Title = $_.MainWindowTitle
        }
    }
} | Format-Table -AutoSize

Write-Host "=== 2. OFFICE UNSAVED & AUTORECOVER ==="
$dirs = @(
    "$env:LOCALAPPDATA\Microsoft\Office\UnsavedFiles",
    "$env:APPDATA\Microsoft\Word"
)
foreach ($d in $dirs) {
    if (Test-Path $d) {
        Write-Host "Dir: $d"
        Get-ChildItem -Path $d -Filter "*.*" -ErrorAction SilentlyContinue |
            Sort-Object LastWriteTime -Descending |
            Select-Object -First 10 LastWriteTime, Length, Name |
            Format-Table -AutoSize
    }
}

Write-Host "=== 3. RECENT FILES IN WINDOWS ==="
$recent = "$env:APPDATA\Microsoft\Windows\Recent"
if (Test-Path $recent) {
    Get-ChildItem -Path $recent -File -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 15 LastWriteTime, Name |
        Format-Table -AutoSize
}


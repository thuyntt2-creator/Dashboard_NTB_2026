Write-Host "=== 1. CHECK OFFICE AUTORECOVER & UNSAVED ==="
$paths = @(
    "$env:APPDATA\Microsoft\Word",
    "$env:LOCALAPPDATA\Microsoft\Office\UnsavedFiles",
    "$env:APPDATA\Microsoft\Excel",
    "$env:LOCALAPPDATA\Temp"
)

foreach ($p in $paths) {
    if (Test-Path $p) {
        Write-Host "--- Scanning: $p ---"
        Get-ChildItem -Path $p -Recurse -File -ErrorAction SilentlyContinue | 
            Where-Object { $_.LastWriteTime -gt (Get-Date).AddDays(-2) } |
            Sort-Object LastWriteTime -Descending |
            Select-Object -First 10 LastWriteTime, Length, FullName |
            Format-Table -AutoSize
    }
}

Write-Host "=== 2. WINDOWS RECENT ITEMS ==="
$recent = "$env:APPDATA\Microsoft\Windows\Recent"
if (Test-Path $recent) {
    Get-ChildItem -Path $recent -File -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 25 LastWriteTime, Name |
        Format-Table -AutoSize
}

Write-Host "=== 3. RUNNING PROCESSES (Office / Editors / Browsers) ==="
Get-Process | Where-Object { $_.MainWindowTitle -ne "" } | 
    Select-Object ProcessName, Id, MainWindowTitle | 
    Format-Table -AutoSize

Write-Host "=== 4. VS CODE / ANTIGRAVITY BACKUPS ==="
$editorBackups = @(
    "$env:APPDATA\Code\Backups",
    "$env:APPDATA\Antigravity\Backups",
    "$env:USERPROFILE\.gemini\antigravity"
)
foreach ($eb in $editorBackups) {
    if (Test-Path $eb) {
        Write-Host "--- Editor backup: $eb ---"
        Get-ChildItem -Path $eb -Recurse -File -ErrorAction SilentlyContinue |
            Where-Object { $_.LastWriteTime -gt (Get-Date).AddDays(-2) } |
            Sort-Object LastWriteTime -Descending |
            Select-Object -First 10 LastWriteTime, Length, FullName |
            Format-Table -AutoSize
    }
}

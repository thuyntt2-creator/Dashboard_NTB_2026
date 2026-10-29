$target = Get-ChildItem "recovered_docs\FILE_KHOI_PHUC" -Filter "*TO_N*.doc" | Select-Object -First 1
Write-Host "Target: $($target.FullName)"
$bytes = [System.IO.File]::ReadAllBytes($target.FullName)

$unicodeText = [System.Text.Encoding]::Unicode.GetString($bytes)
$matches = [regex]::Matches($unicodeText, '[\p{L}\p{N}\s,\.\-\:\(\)\/\%\+\=]{8,}')
Write-Host "=== TEXT EXTRACT FROM BÀI TOÁN 1 (UNICODE) ==="
$count = 0
foreach ($m in $matches) {
    $t = $m.Value.Trim()
    if ($t.Length -gt 10) {
        Write-Host "-> $t"
        $count++
        if ($count -ge 15) { break }
    }
}


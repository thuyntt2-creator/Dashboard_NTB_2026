$path = "c:\Users\lap4all\Desktop\New folder\recovered_docs\BAI TOAN 1((Unsaved-312870380708660752)).asd"
$bytes = [System.IO.File]::ReadAllBytes($path)

# Try UTF-16LE (standard Word text encoding in binary doc stream)
$unicodeText = [System.Text.Encoding]::Unicode.GetString($bytes)
$matches = [regex]::Matches($unicodeText, '[\p{L}\p{N}\s,\.\-\:\(\)\/\%\+\=]{8,}')
Write-Host "=== TEXT EXTRACT FROM BAI TOAN 1 (UNICODE) ==="
$count = 0
foreach ($m in $matches) {
    $t = $m.Value.Trim()
    if ($t.Length -gt 10 -and $t -notmatch '^[a-zA-Z0-9_\.]+$') {
        Write-Host "-> $t"
        $count++
        if ($count -ge 10) { break }
    }
}


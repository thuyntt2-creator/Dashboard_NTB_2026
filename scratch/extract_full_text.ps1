$src = Get-ChildItem "recovered_docs\FILE_KHOI_PHUC" -Filter "*TO_N*.doc" | Select-Object -First 1
$bytes = [System.IO.File]::ReadAllBytes($src.FullName)

# Word OLE compound files store text in 16-bit Unicode (UTF-16LE)
$text = [System.Text.Encoding]::Unicode.GetString($bytes)

# Extract contiguous readable text fragments
$cleanParagraphs = @()
$matches = [regex]::Matches($text, '[\p{L}\p{N}\s,\.\-\:\(\)\/\%\+\=\?\!\@\#\$\^\&\*\"\''\<\>]{5,}')
foreach ($m in $matches) {
    $val = $m.Value.Trim()
    # Filter out binary junk or single words
    if ($val.Length -gt 10 -and $val -notmatch '^[0-9a-fA-F\s]+$' -and $val -notmatch '^[a-zA-Z0-9_\.]+$') {
        $cleanParagraphs += $val
    }
}

$fullExtracted = $cleanParagraphs -join "`r`n`r`n"
Write-Host "Total extracted paragraphs: $($cleanParagraphs.Count)"

$outTxt = "c:\Users\lap4all\Desktop\New folder\recovered_docs\BAI_TOAN_1_NOI_DUNG_KHOI_PHUC.txt"
[System.IO.File]::WriteAllText($outTxt, $fullExtracted, [System.Text.Encoding]::UTF8)

$outDesktop = "C:\Users\lap4all\Desktop\BAI_NOP_CAPACITY_GHN\BAI_TOAN_1_NOI_DUNG_KHOI_PHUC.txt"
[System.IO.File]::WriteAllText($outDesktop, $fullExtracted, [System.Text.Encoding]::UTF8)

$outDeskDirect = "C:\Users\lap4all\Desktop\BAI_TOAN_1_NOI_DUNG_KHOI_PHUC.txt"
[System.IO.File]::WriteAllText($outDeskDirect, $fullExtracted, [System.Text.Encoding]::UTF8)

Write-Host "Saved text file to Desktop!"
Write-Host "--- SAMPLE TEXT ---"
$cleanParagraphs | Select-Object -First 10 | ForEach-Object { Write-Host $_ }


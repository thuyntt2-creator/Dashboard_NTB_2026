$path = "recovered_docs\BAI TOAN 1((Unsaved-312870380708660752)).asd"
$bytes = [System.IO.File]::ReadAllBytes($path)
$header = [System.BitConverter]::ToString($bytes, 0, 16)
Write-Host "Header: $header"

# Check if it starts with PK (50-4B-03-04) -> it's a docx (zip)!
if ($bytes[0] -eq 0x50 -and $bytes[1] -eq 0x4B) {
    Write-Host "It is a ZIP/DOCX format!"
    Copy-Item $path "recovered_docs\BAI_TOAN_1_Recovered.docx" -Force
    Write-Host "Saved as recovered_docs\BAI_TOAN_1_Recovered.docx"
}
# Check if it starts with D0-CF-11-E0 -> OLE compound document (old doc or ASD container)
elseif ($bytes[0] -eq 0xD0 -and $bytes[1] -eq 0xCF) {
    Write-Host "It is an OLE compound document format!"
} else {
    Write-Host "Unknown header format"
}

# Let's extract printable UTF-8 or Unicode strings to inspect the document title / text
$text = [System.Text.Encoding]::UTF8.GetString($bytes)
$matches = [regex]::Matches($text, '[\p{L}\p{N}\s,\.\-\:\(\)\/\%\+\=]{10,}')
Write-Host "Extracted text sample (first 10 paragraphs):"
$count = 0
foreach ($m in $matches) {
    $val = $m.Value.Trim()
    if ($val.Length -gt 15) {
        Write-Host "[$count] $val"
        $count++
        if ($count -ge 15) { break }
    }
}


$file = Get-ChildItem -LiteralPath "C:\Users\lap4all\Desktop\New folder\recovered_docs" | Where-Object { $_.Name -like "*BAI TOAN 1*" }
Write-Host "Found file: $($file.FullName)"
$bytes = [System.IO.File]::ReadAllBytes($file.FullName)
$header = [System.BitConverter]::ToString($bytes, 0, 16)
Write-Host "Header: $header"

if ($bytes[0] -eq 0x50 -and $bytes[1] -eq 0x4B) {
    Write-Host "Format: ZIP/DOCX"
    Copy-Item -LiteralPath $file.FullName "recovered_docs\BAI_TOAN_1_Recovered.docx" -Force
} elseif ($bytes[0] -eq 0xD0 -and $bytes[1] -eq 0xCF) {
    Write-Host "Format: OLE Compound Document (DOC or ASD)"
    Copy-Item -LiteralPath $file.FullName "recovered_docs\BAI_TOAN_1_Recovered.doc" -Force
} else {
    Write-Host "Format: Raw / ASD"
}

# Also let's check AM Thuy
$file2 = Get-ChildItem -LiteralPath "C:\Users\lap4all\Desktop\New folder\recovered_docs" | Where-Object { $_.Name -like "*Th*y*" }
Write-Host "Found file 2: $($file2.FullName)"
$bytes2 = [System.IO.File]::ReadAllBytes($file2.FullName)
$header2 = [System.BitConverter]::ToString($bytes2, 0, 16)
Write-Host "Header 2: $header2"
if ($bytes2[0] -eq 0x50 -and $bytes2[1] -eq 0x4B) {
    Copy-Item -LiteralPath $file2.FullName "recovered_docs\AM_Thuy_Recovered.docx" -Force
} elseif ($bytes2[0] -eq 0xD0 -and $bytes2[1] -eq 0xCF) {
    Copy-Item -LiteralPath $file2.FullName "recovered_docs\AM_Thuy_Recovered.doc" -Force
}


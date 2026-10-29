$folder = "C:\Users\lap4all\Desktop\New folder\recovered_docs"
$files = Get-ChildItem -LiteralPath $folder -File
foreach ($f in $files) {
    Write-Host "File: $($f.Name) | Length: $($f.Length)"
    $bytes = [System.IO.File]::ReadAllBytes($f.FullName)
    $hex = [System.BitConverter]::ToString($bytes, 0, 8)
    Write-Host "Header: $hex"
    if ($bytes[0] -eq 0x50 -and $bytes[1] -eq 0x4B) {
        $outDocx = Join-Path $folder ($f.BaseName + ".docx")
        Copy-Item -LiteralPath $f.FullName -Destination $outDocx -Force
        Write-Host "-> Saved as DOCX: $outDocx"
    } elseif ($bytes[0] -eq 0xD0 -and $bytes[1] -eq 0xCF) {
        $outDoc = Join-Path $folder ($f.BaseName + ".doc")
        Copy-Item -LiteralPath $f.FullName -Destination $outDoc -Force
        Write-Host "-> Saved as DOC (OLE): $outDoc"
    }
}


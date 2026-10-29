$dest = "c:\Users\lap4all\Desktop\New folder\recovered_docs\FILE_KHOI_PHUC"
New-Item -ItemType Directory -Force -Path $dest | Out-Null

$allAsd = Get-ChildItem -Path "c:\Users\lap4all\Desktop\New folder\recovered_docs" -Filter "*.asd" -Recurse

foreach ($f in $allAsd) {
    Write-Host "Processing: $($f.FullName)"
    $cleanName = $f.BaseName -replace '[^a-zA-Z0-9_\-\.\s]', '_'
    $targetDoc = Join-Path $dest ($cleanName + ".doc")
    Copy-Item -LiteralPath $f.FullName -Destination $targetDoc -Force
    Write-Host "-> Created: $targetDoc"
}

# Also let's copy to Desktop\BAI_NOP_CAPACITY_GHN so user can find it right away
$desktopFolder = "C:\Users\lap4all\Desktop\BAI_NOP_CAPACITY_GHN"
if (Test-Path $desktopFolder) {
    $targetInDesktop = Join-Path $desktopFolder "BAI_TOAN_1_KHOI_PHUC.doc"
    $source = Get-ChildItem -Path "c:\Users\lap4all\Desktop\New folder\recovered_docs" -Filter "*BAI TOAN 1*.asd" -Recurse | Select-Object -First 1
    if ($source) {
        Copy-Item -LiteralPath $source.FullName -Destination $targetInDesktop -Force
        Write-Host "-> Copied to Desktop folder: $targetInDesktop"
    }
}


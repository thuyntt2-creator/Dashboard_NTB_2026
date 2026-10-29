Add-Type -AssemblyName System.IO.Compression.FileSystem
$p = "C:\Users\lap4all\Desktop\BAI_NOP_CAPACITY_GHN\BAI_GIANG_TUNG_BUOC_TINH_TOAN.docx"
$zip = [System.IO.Compression.ZipFile]::OpenRead($p)
$entry = $zip.GetEntry("word/document.xml")
$reader = New-Object System.IO.StreamReader($entry.Open())
$xml = $reader.ReadToEnd()
$reader.Close()
$zip.Dispose()

$matches = [regex]::Matches($xml, '(?<=<w:t[^>]*>).*?(?=</w:t>)')
$allText = ($matches | ForEach-Object { $_.Value }) -join ' '
Write-Host "Length: $($allText.Length)"
Write-Host "Preview:"
Write-Host ($allText.Substring(0, [Math]::Min(300, $allText.Length)))


Add-Type -AssemblyName System.IO.Compression.FileSystem
$p = "C:\Users\lap4all\Desktop\BAI_NOP_CAPACITY_GHN\BAI_GIANG_TUNG_BUOC_TINH_TOAN.docx"
$zip = [System.IO.Compression.ZipFile]::OpenRead($p)
$entry = $zip.GetEntry("word/document.xml")
$reader = New-Object System.IO.StreamReader($entry.Open())
$xml = $reader.ReadToEnd()
$reader.Close()
$zip.Dispose()

$docXml = [xml]$xml
$t = $docXml.InnerText
Write-Host "BAI_GIANG_TUNG_BUOC_TINH_TOAN.docx text preview:"
Write-Host ($t.Substring(0, [Math]::Min(300, $t.Length)))


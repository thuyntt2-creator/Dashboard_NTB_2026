Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [System.IO.Compression.ZipFile]::OpenRead("c:\Users\lap4all\Desktop\New folder\recovered_docs\BAI_TOAN_1_DON_TAO_VA_DON_VE.docx")
$entry = $zip.GetEntry("word/document.xml")
$stream = $entry.Open()
$reader = New-Object System.IO.StreamReader($stream)
$xml = $reader.ReadToEnd()
$reader.Close()
$zip.Dispose()

$docXml = [xml]$xml
$text = $docXml.InnerText
Write-Host "Length of text: $($text.Length)"
Write-Host "Preview text:"
Write-Host ($text.Substring(0, [Math]::Min(500, $text.Length)))


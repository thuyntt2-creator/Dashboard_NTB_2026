try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    
    $folder = "C:\Users\lap4all\AppData\Local\Microsoft\Office\UnsavedFiles"
    $files = Get-ChildItem -LiteralPath $folder -Filter "*.asd"
    
    foreach ($f in $files) {
        Write-Host "Trying to convert: $($f.Name)"
        try {
            $doc = $word.Documents.Open($f.FullName)
            $cleanName = ($f.BaseName -replace '[^a-zA-Z0-9_\-\.\s]', '_').Trim()
            $outPath = "C:\Users\lap4all\Desktop\BAI_NOP_CAPACITY_GHN\$cleanName.docx"
            $doc.SaveAs2($outPath, 12)
            $doc.Close()
            Write-Host "-> CONVERTED TO DOCX: $outPath (Paragraphs: $($doc.Paragraphs.Count))"
        } catch {
            Write-Host "-> Word Open failed: $($_.Exception.Message)"
        }
    }
    
    $word.Quit()
} catch {
    Write-Host "Error: $($_.Exception.Message)"
    if ($word) { $word.Quit() }
}


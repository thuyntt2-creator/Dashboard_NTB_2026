$desktopFolder = "C:\Users\lap4all\Desktop\BAI_NOP_CAPACITY_GHN"
if (Test-Path $desktopFolder) {
    Write-Host "Folder exists: $desktopFolder"
    Get-ChildItem -Path $desktopFolder -File | 
        Sort-Object LastWriteTime -Descending |
        Select-Object LastWriteTime, Length, Name |
        Format-Table -AutoSize
} else {
    Write-Host "Folder does not exist"
}


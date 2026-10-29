$sh = New-Object -ComObject WScript.Shell
$lnkPath = "$env:APPDATA\Microsoft\Windows\Recent\BAI TOAN 1((Unsaved-312870380708660752)).asd.lnk"
if (Test-Path $lnkPath) {
    $target = $sh.CreateShortcut($lnkPath).TargetPath
    Write-Host "Target Path: $target"
} else {
    Write-Host "Lnk not found"
}

# Also let's check other recent links from 12:31 - 12:32
Get-ChildItem "$env:APPDATA\Microsoft\Windows\Recent\*.lnk" | 
    Where-Object { $_.LastWriteTime -gt (Get-Date).AddMinutes(-30) } |
    ForEach-Object {
        $t = $sh.CreateShortcut($_.FullName).TargetPath
        Write-Host "$($_.Name) -> $t"
    }


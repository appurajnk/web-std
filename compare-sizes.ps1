Write-Host '================================================================='
Write-Host 'BEFORE COMPRESSION (Original files in originals_backup):'
Write-Host '================================================================='

$before = Get-ChildItem 'D:\personal\web\originals_backup\*.jpg' | Sort-Object Name | ForEach-Object {
    [PSCustomObject]@{
        Name = $_.Name
        'Size (MB)' = [math]::Round($_.Length/1MB, 2)
        'Size (KB)' = [math]::Round($_.Length/1KB, 2)
        Bytes = $_.Length
    }
}

$before | Format-Table -AutoSize
$totalBefore = ($before | Measure-Object -Property Bytes -Sum).Sum
Write-Host "Total before: $([math]::Round($totalBefore/1MB,2)) MB ($([math]::Round($totalBefore/1KB,2)) KB)`n"

Write-Host '================================================================='
Write-Host 'AFTER COMPRESSION (Current files):'
Write-Host '================================================================='

$after = Get-ChildItem 'D:\personal\web\*.jpg' | Sort-Object Name | ForEach-Object {
    [PSCustomObject]@{
        Name = $_.Name
        'Size (MB)' = [math]::Round($_.Length/1MB, 2)
        'Size (KB)' = [math]::Round($_.Length/1KB, 2)
        Bytes = $_.Length
    }
}

$after | Format-Table -AutoSize
$totalAfter = ($after | Measure-Object -Property Bytes -Sum).Sum
Write-Host "Total after: $([math]::Round($totalAfter/1MB,2)) MB ($([math]::Round($totalAfter/1KB,2)) KB)`n"

Write-Host '================================================================='
Write-Host 'COMPARISON (File by File):'
Write-Host '================================================================='

for($i = 0; $i -lt $before.Count; $i++) {
    $reduction = [math]::Round((1 - $after[$i].Bytes / $before[$i].Bytes) * 100, 1)
    Write-Host "$($before[$i].Name): $($before[$i].'Size (MB)') MB -> $($after[$i].'Size (MB)') MB (Reduced by $reduction%)"
}

$totalReduction = [math]::Round((1 - $totalAfter / $totalBefore) * 100, 1)
$spaceSaved = [math]::Round(($totalBefore - $totalAfter)/1MB, 2)

Write-Host "`n================================================================="
Write-Host 'SUMMARY:'
Write-Host '================================================================='
Write-Host "Total size before: $([math]::Round($totalBefore/1MB,2)) MB"
Write-Host "Total size after:  $([math]::Round($totalAfter/1MB,2)) MB"
Write-Host "Space saved:       $spaceSaved MB"
Write-Host "Total reduction:   $totalReduction%"
Write-Host '================================================================='
Write-Host "`nCompression settings used:"
Write-Host "  - Quality: 85"
Write-Host "  - Engine: MozJPEG"
Write-Host "  - Progressive: Yes (better for web loading)"
Write-Host "  - Original files backed up to: originals_backup\"
Write-Host '================================================================='

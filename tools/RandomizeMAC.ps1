if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Start-Process -FilePath 'pwsh' -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    return
}
$adapter = Get-NetAdapter | Where-Object { $_.Status -eq 'Up' -and ($_.Name -match 'Ethernet|Wi-Fi') } | Select-Object -First 1
if ($null -eq $adapter) {
    Write-Output "No suitable network adapter found."
    return
}
$originalMac = $adapter.MacAddress.ToUpper()
$macBytes = 6..1 | ForEach-Object { Get-Random -Minimum 0 -Maximum 256 }
$macBytes[0] = $macBytes[0] -band 0xFE -bor 0x02
$macAddress = ($macBytes | ForEach-Object { "{0:X2}" -f $_ }) -join '-'
$regPath = "HKLM:\SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}"
$netConfigs = Get-ChildItem -Path $regPath
Clear-Host
foreach ($key in $netConfigs) {
    $driverDesc = (Get-ItemProperty -Path $key.PSPath).DriverDesc
    if ($driverDesc -eq $adapter.InterfaceDescription) {
        Set-ItemProperty -Path $key.PSPath -Name "NetworkAddress" -Value $macAddress
        Write-Output "$($adapter.Name) : $originalMac -> $macAddress"
        Restart-NetAdapter -Name $adapter.Name -Confirm:$false
        break
    }
}
pause

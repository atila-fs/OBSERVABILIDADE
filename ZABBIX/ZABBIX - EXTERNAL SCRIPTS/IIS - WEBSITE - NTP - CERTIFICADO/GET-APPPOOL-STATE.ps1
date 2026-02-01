param ([string] $name = 0)
Import-Module WebAdministration
$apppoolState = Get-WebAppPoolState -name "$name"
If ($apppoolState.value -eq "Started") { Write-Output (1) } Else { Write-Output (0) }
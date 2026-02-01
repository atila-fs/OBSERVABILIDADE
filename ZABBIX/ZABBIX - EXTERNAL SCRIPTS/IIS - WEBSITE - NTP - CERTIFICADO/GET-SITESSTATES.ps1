param ([string] $name = 0)
Import-Module WebAdministration
$siteState = Get-WebsiteState -name "$name"
If ($siteState.value -eq "Started") { Write-Output (1) } Else { Write-Output (0) }
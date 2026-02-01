Param(
  [string]$thumb
)

$hoje = Get-Date

$c = Get-ChildItem -Path cert:\LocalMachine\My\$thumb

$expiringdays = $c.NotAfter - $hoje

echo $expiringdays.Days







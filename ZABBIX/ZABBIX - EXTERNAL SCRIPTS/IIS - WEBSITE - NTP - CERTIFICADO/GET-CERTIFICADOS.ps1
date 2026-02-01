echo '{"data": ['

$string = '';
$certificados = Get-ChildItem -Path cert:\LocalMachine\My

foreach($c in $certificados)
{
    $cn = $c.Subject | % {$_.split(",")} | select -first 1 | % {$_.split("=")} | select -last 1

    $string += '{"{#THUMB}": "' + $c.Thumbprint + '", "{#SUBJECT}": "' + $cn + '"},'; 
    
}
echo $string.TrimEnd(',');

echo ']}'





#-ExpiringInDays 0 | Format-List -Property Thumbprint,NotAfter,Subject


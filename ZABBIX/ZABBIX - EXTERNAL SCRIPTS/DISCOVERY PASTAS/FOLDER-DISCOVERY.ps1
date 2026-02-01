# Caminho do diretório a ser monitorado
$directoryPath = "E:\Event_Viewers"

# Lista todas as pastas no diretório
$folders = Get-ChildItem -Path $directoryPath -Directory

# Inicializa uma string para armazenar os resultados formatados
$resultText = ""

# Itera sobre cada pasta
foreach ($folder in $folders) {
    $folderName = $folder.Name
    $folderPath = $folder.FullName
    $folderSizeBytes = (Get-ChildItem -Path $folderPath -Recurse | Measure-Object -Property Length -Sum).Sum
    $folderSizeGB = [math]::Round($folderSizeBytes / 1GB, 2)

    # Obtém a data da última alteração da pasta
    $lastChange = $folder.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss")

    # Formata a saída para cada pasta
    $folderInfo = @"
Last Change: $lastChange
Folder Name: $folderName
Folder Size: $folderSizeGB GB`n

"@

    # Adiciona a informação da pasta à string de resultados
    $resultText += $folderInfo
}

# Exibe a saída formatada na saída padrão
Write-Host $resultText

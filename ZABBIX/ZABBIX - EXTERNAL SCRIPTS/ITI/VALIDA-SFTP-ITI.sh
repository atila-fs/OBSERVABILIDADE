#!/usr/bin/expect -f

# Limpa o arquivo de logs 
# echo > /var/log/relatorio-iti/safewebrfb

# Define variáveis
set timeout -1
set sftp_key "<caminho>"
set sftp_user "<usuario>"
set sftp_host "<host>"
set passphrase "<senha>"
set output_file "<caminho>"

# Inicia o script para capturar a saída
set script_cmd "script -q -c"

# Conecta no SFTP e captura a saída no arquivo
spawn $script_cmd "sftp -i $sftp_key -oPort=22 $sftp_user@$sftp_host" > $output_file

# Espera pela solicitação da passphrase
expect "Enter passphrase for key '$sftp_key':"
send "$passphrase\r"

# Espera pelo prompt do SFTP
expect "sftp>"

# Executa os comandos no SFTP
send "cd <caminho>\r"
send "ls\r"
send "exit\r"

# Espera pela saída
expect eof
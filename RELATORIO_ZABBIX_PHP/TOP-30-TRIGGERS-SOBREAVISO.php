<?php

// Conectar ao banco MySQL
$con = mysqli_connect("<ip_banco_zabbix>", "<user>", "<pass>", "<database>");
if (!$con) {
  die('Could not connect: ' . mysqli_connect_error());
}

// Obter timestamps atuais e da última semana
$current_time = time();
$week_ago_time = $current_time - 604800; // uma semana atrás

// Query para buscar as 30 triggers mais ativas no período 19h - 08h da última semana
$result = mysqli_query($con, "
SELECT COUNT(DISTINCT e.eventid) AS cnt_event, h.host, t.description, t.priority
FROM events e
JOIN triggers t ON t.triggerid = e.objectid
JOIN functions f ON t.triggerid = f.triggerid
JOIN items i ON i.itemid = f.itemid
JOIN hosts h ON h.hostid = i.hostid
WHERE t.priority > 3
  AND e.clock > $week_ago_time
  AND (
       FROM_UNIXTIME(e.clock, '%H') >= 19
       OR FROM_UNIXTIME(e.clock, '%H') < 8
  )
GROUP BY h.host, t.triggerid, t.description, t.priority
ORDER BY cnt_event DESC, h.host, t.description, t.triggerid
LIMIT 30
");

// Criar a mensagem em HTML para o e-mail
$mail_message = '
<html>
<head>
  <style type="text/css">
    table {border-collapse:collapse;}
    th {background-color:#8BB381;}
    table, th, td {border: 1px solid black;}
  </style>
</head>
<body>
Top 30 triggers sobreaviso (19h - 08h) na última semana: ' . date("Y-m-d H:i", $week_ago_time) . ' até ' . date("Y-m-d H:i", $current_time) . '<br><br>
<table>
<tr>
  <th>Quantidade de alarmes</th>
  <th>Host</th>
  <th>Problema</th>
  <th>Criticidade</th>
</tr>';

// Preencher a tabela com os resultados
while ($row = mysqli_fetch_array($result)) {
  $row['description'] = str_replace("{HOSTNAME}", $row['host'], $row['description']);
  $mail_message .= '<tr>
        <td align="center">' . $row['cnt_event'] . '</td>
        <td>' . $row['host'] . '</td>
        <td>' . $row['description'] . '</td>
        <td align="center">' . $row['priority'] . '</td>
    </tr>';
}

$mail_message .= '
</table>
</body>
</html>';

// Fechar a conexão com o banco
mysqli_close($con);

// Configurar cabeçalhos do e-mail
$headers = "MIME-Version: 1.0\r\n";
$headers .= "Content-type: text/html; charset=utf-8\r\n";
$headers .= "From: Zabbix Administrator\r\n";

// Enviar o e-mail
$to = '[EMAIL_ADDRESS]';
mail($to, 'Top 30 triggers sobreaviso (19h - 08h)' . date("Y-m-d H:i", $week_ago_time) . ' - ' . date("Y-m-d H:i", $current_time), $mail_message, $headers);

?>
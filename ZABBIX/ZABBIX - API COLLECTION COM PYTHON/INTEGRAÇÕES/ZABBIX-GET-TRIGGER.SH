#!/bin/bash

# Variáveis de acesso à API do Zabbix
ZABBIX_URL="http://<ip_zabbix>/zabbix/api_jsonrpc.php"
ZABBIX_USER="<user>"
ZABBIX_PASS="<pass>"

# Headers
HEADERS="Content-Type: application/json"

# Autenticação na API do Zabbix
AUTH_TOKEN=$(curl -s -X POST -H "$HEADERS" \
  --data "{
    \"jsonrpc\": \"2.0\",
    \"method\": \"user.login\",
    \"params\": { \"user\": \"$ZABBIX_USER\", \"password\": \"$ZABBIX_PASS\" },
    \"id\": 1
  }" \
  "$ZABBIX_URL" | jq -r .result)

# Verifica se a autenticação foi bem-sucedida
if [[ "$AUTH_TOKEN" == "null" || -z "$AUTH_TOKEN" ]]; then
  echo "Erro: Falha na autenticação no Zabbix."
  exit 1
fi

# Busca a última trigger do tipo HIGH
LAST_HIGH_TRIGGER=$(curl -s -X POST -H "$HEADERS" \
  --data "{
    \"jsonrpc\": \"2.0\",
    \"method\": \"trigger.get\",
    \"params\": {
      \"output\": [\"triggerid\", \"description\", \"priority\"],
      \"filter\": {\"priority\": 4},
      \"sortfield\": \"lastchange\",
      \"sortorder\": \"DESC\",
      \"limit\": 1
    },
    \"auth\": \"$AUTH_TOKEN\",
    \"id\": 1
  }" \
  "$ZABBIX_URL" | jq '.result[0]')

# Exibe a última trigger HIGH
if [[ "$LAST_HIGH_TRIGGER" == "null" || -z "$LAST_HIGH_TRIGGER" ]]; then
  echo "Nenhuma trigger HIGH encontrada."
else
  echo "Última Trigger HIGH:"
  echo "$LAST_HIGH_TRIGGER" | jq
fi

# Logout na API do Zabbix
curl -s -X POST -H "$HEADERS" \
  --data "{
    \"jsonrpc\": \"2.0\",
    \"method\": \"user.logout\",
    \"params\": [],
    \"auth\": \"$AUTH_TOKEN\",
    \"id\": 1
  }" \
  "$ZABBIX_URL" > /dev/null

#!/bin/bash

# Variáveis de acesso à API do Zabbix
ZABBIX_URL="http://<ip_zabbix>/zabbix/api_jsonrpc.php"
ZABBIX_USER="<user>"
ZABBIX_PASS="<pass>"

# Variáveis de acesso ao Azure DevOps
ORG_URL="<URL>"
PROJECT="<PROJETO>"
WORKITEM_TYPE="<TIPO_DE_WORKITEM>"
API_VERSION="7.1"
PAT_TOKEN="<TOKEN>"

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

if [[ "$AUTH_TOKEN" == "null" || -z "$AUTH_TOKEN" ]]; then
  echo "Erro: Falha na autenticação no Zabbix." >> /var/log/zabbix-devops.log
  exit 1
fi

# Busca a última trigger HIGH (4) ou DISASTER (5)
LAST_TRIGGER=$(curl -s -X POST -H "$HEADERS" \
  --data "{
    \"jsonrpc\": \"2.0\",
    \"method\": \"trigger.get\",
    \"params\": {
      \"output\": [\"triggerid\", \"description\", \"priority\"],
      \"filter\": {\"priority\": [4, 5]},
      \"sortfield\": \"lastchange\",
      \"group\": \"PROD\",
      \"selectHosts\": [\"host\", \"name\"],
      \"sortorder\": \"DESC\",
      \"limit\": 1
    },
    \"auth\": \"$AUTH_TOKEN\",
    \"id\": 1
  }" \
  "$ZABBIX_URL" | jq '.result[0]') > /dev/null

if [[ "$LAST_TRIGGER" == "null" || -z "$LAST_TRIGGER" ]]; then
  echo "Nenhuma trigger HIGH ou DISASTER encontrada." >> /var/log/zabbix-devops.log
  exit 0
fi

# Extrai os campos necessários
TRIGGER_DESC=$(echo "$LAST_TRIGGER" | jq -r '.description')
HOSTNAME=$(echo "$LAST_TRIGGER" | jq -r '.hosts[0].host')

# Verifica se encontrou um hostname válido
if [[ "$HOSTNAME" == "null" || -z "$HOSTNAME" ]]; then
  echo "Erro: Hostname não encontrado na trigger." >> /var/log/zabbix-devops.log
  exit 1
fi

# Codifica o token PAT em Base64
AUTH_HEADER="Basic $(echo -n ":$PAT_TOKEN" | base64 | tr -d '\n')"

# Cria o card no Azure DevOps
JSON_DATA="[
  {
    \"op\": \"add\",
    \"path\": \"/fields/System.Title\",
    \"value\": \"Alerta Zabbix - $HOSTNAME\"
  },
  {
    \"op\": \"add\",
    \"path\": \"/fields/System.Description\",
    \"value\": \"$TRIGGER_DESC\"
  }
]"

RESPONSE=$(curl -s -X POST \
  -H "Content-Type: application/json-patch+json" \
  -H "Authorization: $AUTH_HEADER" \
  --data "$JSON_DATA" \
  "$ORG_URL/$PROJECT/_apis/wit/workitems/\$$WORKITEM_TYPE?api-version=$API_VERSION" | jq)

echo "Card criado no Azure DevOps:" >> /var/log/zabbix-devops.log
echo "$RESPONSE" | jq >> /var/log/zabbix-devops.log

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

#!/bin/bash
set -euxo pipefail

# =========================
# VARIÁVEIS DO ZABBIX
# =========================
HOST_NAME="${1:-{HOST.NAME}}"
EVENT_ID="${2:-{EVENT.ID}}"

# Sanitização
HOST_NAME="${HOST_NAME//\}/}"
HOST_NAME="${HOST_NAME//\'/}"
EVENT_ID=$(echo "$EVENT_ID" | tr -cd '0-9')

# =========================
# AZURE DEVOPS CONFIG
# =========================
AZURE_ORG="<ORG>"
AZURE_PROJECT="<PROJECT>"
AZURE_WORK_ITEM_TYPE="<WORK_ITEM_TYPE>"
AZURE_PAT="<PAT>"
API_VERSION="7.0"

# =========================
# ZABBIX CONFIG
# =========================
ZABBIX_API_URL="http://zbx.<ORG>.com.br/api_jsonrpc.php"
ZABBIX_API_TOKEN="<TOKEN>"

# =========================
# Validação EVENT_ID
# =========================
if [[ -z "$EVENT_ID" ]]; then
    echo "❌ EVENT_ID inválido"
    exit 1
fi

# =========================
# Buscar trigger do evento
# =========================
EVENT_JSON=$(curl -s -X POST -H "Content-Type: application/json" -d "{
    \"jsonrpc\": \"2.0\",
    \"method\": \"event.get\",
    \"params\": {
        \"eventids\": [\"$EVENT_ID\"],
        \"output\": [\"eventid\",\"objectid\"],
        \"selectRelatedObject\": [\"description\"]
    },
    \"auth\": \"$ZABBIX_API_TOKEN\",
    \"id\": 1
}" "$ZABBIX_API_URL")

TRIGGER_ID=$(echo "$EVENT_JSON" | jq -r '.result[0].objectid // empty')
TRIGGER_NAME=$(echo "$EVENT_JSON" | jq -r '.result[0].relatedObject.description // empty')

if [[ -z "$TRIGGER_ID" ]]; then
    echo "❌ Trigger não encontrada para o evento $EVENT_ID"
    exit 1
fi

# =========================
# TITLE e DESCRIPTION
# =========================
TITLE="[Zabbix][EventID:$EVENT_ID] $HOST_NAME - $TRIGGER_NAME"

ZABBIX_EVENT_URL="https://zbx.safeweb.com.br/zabbix/tr_events.php?triggerid=$TRIGGER_ID&eventid=$EVENT_ID"

DESCRIPTION="Host: $HOST_NAME
Trigger: $TRIGGER_NAME
EventID: $EVENT_ID

Link do evento no Zabbix:
$ZABBIX_EVENT_URL"

# =========================
# Azure DevOps URL / Auth
# =========================
PROJECT_ENC=$(jq -nr --arg v "$AZURE_PROJECT" '$v|@uri')
TYPE_ENC=$(jq -nr --arg v "$AZURE_WORK_ITEM_TYPE" '$v|@uri')

AZURE_URL="https://dev.azure.com/$AZURE_ORG/$PROJECT_ENC/_apis/wit/workitems/\$$TYPE_ENC?api-version=$API_VERSION"
AUTH_HEADER=$(printf ":%s" "$AZURE_PAT" | base64 | tr -d '\n')

# =========================
# Verificar duplicidade
# =========================
WIQL=$(jq -n --arg eid "$EVENT_ID" '{
  "query": "SELECT [System.Id] FROM WorkItems WHERE [System.Title] CONTAINS \"EventID:'"$EVENT_ID"'\" AND [System.State] <> \"Closed\""
}')

EXISTING_WI_ID=$(curl -s -X POST \
  "https://dev.azure.com/$AZURE_ORG/$PROJECT_ENC/_apis/wit/wiql?api-version=$API_VERSION" \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic $AUTH_HEADER" \
  --data "$WIQL" | jq -r '.workItems[0].id // empty')

if [[ -n "$EXISTING_WI_ID" ]]; then
    MESSAGE="ℹ️ Chamado já existente para EventID:$EVENT_ID
🔁 Azure DevOps Work Item ID: $EXISTING_WI_ID"

    jq -n --arg eid "$EVENT_ID" --arg msg "$MESSAGE" '{
        "jsonrpc": "2.0",
        "method": "event.acknowledge",
        "params": {
            "eventids": [$eid],
            "action": 4,
            "message": $msg
        },
        "auth": "'"$ZABBIX_API_TOKEN"'",
        "id": 1
    }' | curl -s -X POST -H "Content-Type: application/json" -d @- "$ZABBIX_API_URL"

    echo -e "$MESSAGE"
    exit 0
fi

# =========================
# Payload Azure DevOps
# =========================
DATA=$(jq -n --arg title "$TITLE" --arg description "$DESCRIPTION" '[
    { "op": "add", "path": "/fields/System.Title", "value": $title },
    { "op": "add", "path": "/fields/System.Description", "value": $description },
    { "op": "add", "path": "/fields/System.State", "value": "Parado" },
    { "op": "add", "path": "/fields/System.AreaPath", "value": "Infraestrutura - TI" }
]')

# =========================
# Criar Work Item
# =========================
RESPONSE=$(curl -sS -X POST "$AZURE_URL" \
    -H "Content-Type: application/json-patch+json" \
    -H "Accept: application/json" \
    -H "Authorization: Basic $AUTH_HEADER" \
    --data-binary "$DATA" \
    -w "\n%{http_code}")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')
DEVOPS_URL=$(echo "$BODY" | jq -r '._links.html.href // empty')

if [[ "$HTTP_CODE" == "200" || "$HTTP_CODE" == "201" ]]; then
    MESSAGE="✅ Work Item criado com sucesso
🔗 Azure DevOps: $DEVOPS_URL"
else
    MESSAGE="❌ Erro ao criar Work Item (HTTP $HTTP_CODE)
$BODY"
fi

# =========================
# Registrar comentário no Zabbix
# =========================
jq -n --arg eid "$EVENT_ID" --arg msg "$MESSAGE" '{
    "jsonrpc": "2.0",
    "method": "event.acknowledge",
    "params": {
        "eventids": [$eid],
        "action": 4,
        "message": $msg
    },
    "auth": "'"$ZABBIX_API_TOKEN"'",
    "id": 1
}' | curl -s -X POST -H "Content-Type: application/json" -d @- "$ZABBIX_API_URL"
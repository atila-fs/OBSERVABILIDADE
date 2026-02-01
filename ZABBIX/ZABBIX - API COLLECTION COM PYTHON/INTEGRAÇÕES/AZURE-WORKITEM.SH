#!/bin/bash

# Variáveis
ORG_URL="<URL>"
PROJECT="<PROJETO>"
WORKITEM_TYPE="<TIPO_DE_WORKITEM>"
API_VERSION="7.1"
PAT_TOKEN="<TOKEN>"

# Codifica o token PAT em Base64
AUTH_HEADER="Basic $(echo -n ":$PAT_TOKEN" | base64 | tr -d '\n')"

# Body da requisição
JSON_DATA='[
  {
    "op": "add",
    "path": "/fields/System.Title",
    "value": "Atila TESTE"
  },
  {
    "op": "add",
    "path": "/fields/System.Description",
    "value": "Atila TESTE"
  }
]'

# Executa a requisição CURL
curl -v -X POST \
  -H "Content-Type: application/json-patch+json" \
  -H "Authorization: $AUTH_HEADER" \
  --data "$JSON_DATA" \
  "$ORG_URL/$PROJECT/_apis/wit/workitems/\$$WORKITEM_TYPE?api-version=$API_VERSION" | jq

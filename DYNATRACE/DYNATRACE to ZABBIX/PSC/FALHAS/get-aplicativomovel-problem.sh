#!/bin/bash
set -o pipefail

API_URL="https://<enviroment>/api/v2/problems"
API_TOKEN="<token>"

PROBLEM_SELECTOR='status("open")'
ENTITY_SELECTOR='entityId("SERVICE-F265A926E28B601")'
FROM='now-30d'
TITLE_MATCH='Failure rate increase'

resp_and_code="$(
  curl -sS -w $'\n%{http_code}' --get \
    -H "Authorization: Api-Token ${API_TOKEN}" \
    -H "Accept: application/json" \
    --data-urlencode "problemSelector=${PROBLEM_SELECTOR}" \
    --data-urlencode "entitySelector=${ENTITY_SELECTOR}" \
    --data-urlencode "from=${FROM}" \
    "${API_URL}"
)"

body="$(printf '%s\n' "$resp_and_code" | sed '$d')"
code="$(printf '%s\n' "$resp_and_code" | tail -n1)"

if [[ "$code" != "200" ]]; then
  echo "HTTP=$code" >&2
  echo "$body" >&2
  echo "666"
  exit 0
fi

count="$(
  jq -r --arg t "$TITLE_MATCH" '
    [ ((.problems // [])[]) | select((.title? // "") | contains($t)) ] | length
  ' <<<"$body" 2>/dev/null
)"

[[ -n "$count" ]] && echo "$count" || echo "666"
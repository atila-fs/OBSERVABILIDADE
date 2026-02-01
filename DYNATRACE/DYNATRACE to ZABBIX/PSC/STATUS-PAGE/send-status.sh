#!/bin/bash
set -euo pipefail

URL="http://[IP_ADDRESS]/"
TO="[EMAIL_ADDRESS]"
FROM="[EMAIL_ADDRESS]"
SUBJECT="[SAFEID] Health Check - $(date +%F)"
TMP="/tmp/safeid_status_$$.html"

curl -fsS "$URL" -o "$TMP"

{
  echo "From: $FROM"
  echo "To: $TO"
  echo "Subject: $SUBJECT"
  echo "MIME-Version: 1.0"
  echo "Content-Type: text/html; charset=UTF-8"
  echo
  cat "$TMP"
} | /usr/sbin/sendmail -t

rm -f "$TMP"


# 0 7 * * * /opt/scripts/dynatrace/psc/status-page/send-status.sh >/var/log/safeid_status_mail.log 2>&1
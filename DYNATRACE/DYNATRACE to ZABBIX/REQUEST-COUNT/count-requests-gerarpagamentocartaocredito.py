from datetime import datetime, timedelta, timezone

DYNATRACE_ENV = "<enviroment>"
DYNATRACE_API_TOKEN = "<token>"
ENDPOINT_NAME = "<endpoint>"

now = datetime.now(timezone.utc)
to_time = now.replace(microsecond=0).isoformat().replace("+00:00", "Z")
from_time = (now - timedelta(minutes=10)).replace(microsecond=0).isoformat().replace("+00:00", "Z")

import requests
url = f"https://{DYNATRACE_ENV}/api/v2/metrics/query"
headers = {"Authorization": f"Api-Token {DYNATRACE_API_TOKEN}"}
params = {
    "metricSelector": "builtin:service.keyRequest.count.total",
    "entitySelector": f'type(SERVICE_METHOD),entityName.equals("{ENDPOINT_NAME}")',
    "from": from_time,
    "to": to_time
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    results = data.get("result", [])
    if results and "data" in results[0] and results[0]["data"]:
        datapoints = results[0]["data"][0]
        valores = [v for v in datapoints.get("values", []) if v is not None]
        print(int(sum(valores)))
    else:
        print(0)
else:
    print(0)
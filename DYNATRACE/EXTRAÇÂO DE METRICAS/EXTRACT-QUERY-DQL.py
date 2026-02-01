import requests
from datetime import datetime

DT_ENV = "<enviroment>"
API_TOKEN = "<token>"

query = 'builtin:service.requestCount.server:filter(eq("dt.entity.service","SERVICE-C7CF3B2FBB0FAA6F")):splitBy():value'

url = f"{DT_ENV}/api/v2/metrics/query"
params = {
    "metricSelector": query,
    "from": "now-1h",
    "to": "now",
    "resolution": "Inf"
}

headers = {"Authorization": f"Api-Token {API_TOKEN}"}

resp = requests.get(url, headers=headers, params=params)

if resp.status_code == 200:
    data = resp.json()
    print("==== Dados extraídos ====")

    for result in data.get("result", []):
        for serie in result.get("data", []):
            timestamps = serie.get("timestamps", [])
            values = serie.get("values", [])
            
            for ts, val in zip(timestamps, values):
                dt = datetime.fromtimestamp(ts / 1000)
                print(f"{dt.strftime('%Y-%m-%d %H:%M:%S')} -> {val} requisições")

else:
    print(f"Erro {resp.status_code}: {resp.text}")
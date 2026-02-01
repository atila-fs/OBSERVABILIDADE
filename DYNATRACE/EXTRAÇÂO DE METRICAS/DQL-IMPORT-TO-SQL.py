import os
import json
import requests
from datetime import datetime, timezone
import psycopg2
from psycopg2.extras import execute_values

DT_ENV = "<enviroment>"
API_TOKEN = "<token>"
SERVICE_ID = "<service_id>"

agora = datetime.now()
data_formatada = agora.strftime("%Y-%m-%d %H:%M:%S")

query = f'builtin:service.requestCount.server:filter(eq("dt.entity.service","{SERVICE_ID}")):splitBy():value'

FROM = "now-1h"
TO = "now"
RESOLUTION = "1h"

PG_CONN = "host=127.0.0.1 dbname=dynatrace user=dyna password=Safeweb828"

def fetch_dynatrace():
    url = f"{DT_ENV}/api/v2/metrics/query"
    params = {
        "metricSelector": query,
        "from": FROM,
        "to": TO,
        "resolution": RESOLUTION
    }
    headers = {"Authorization": f"Api-Token {API_TOKEN}"}
    r = requests.get(url, headers=headers, params=params, timeout=60)
    r.raise_for_status()
    return r.json()

def payload_to_rows(payload):
    rows = []
    resolution = payload.get("resolution", RESOLUTION)
    for res in payload.get("result", []):
        raw_metric_id = res.get("metricId", "")
        metric_id = raw_metric_id.split(":filter(")[0] if ":filter(" in raw_metric_id else raw_metric_id

        for serie in res.get("data", []):
            ts_list = serie.get("timestamps", []) or []
            val_list = serie.get("values", []) or []
            dimmap = serie.get("dimensionMap", {}) or {}
            dims_json = json.dumps(dimmap) if dimmap else None

            for ts_ms, val in zip(ts_list, val_list):
                ts = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc)
                rows.append((
                    ts,
                    metric_id,
                    SERVICE_ID,
                    float(val),
                    resolution,
                    dims_json
                ))
    return rows

UPSERT_SQL = """
INSERT INTO dt_metrics (ts, metric_id, service_id, value, resolution, dims)
VALUES %s
ON CONFLICT (metric_id, service_id, ts) DO UPDATE
SET value = EXCLUDED.value,
    resolution = EXCLUDED.resolution,
    dims = COALESCE(EXCLUDED.dims, dt_metrics.dims);
"""

def upsert_rows(conn_str, rows):
    if not rows:
        print("Nenhum dado para inserir.")
        return 0
    with psycopg2.connect(conn_str) as conn:
        with conn.cursor() as cur:
            execute_values(cur, UPSERT_SQL, rows, page_size=1000)
        conn.commit()
    return len(rows)

if __name__ == "__main__":
    try:
        payload = fetch_dynatrace()
        rows = payload_to_rows(payload)
        n = upsert_rows(PG_CONN, rows)
        print(f"[{data_formatada}] Inseridos/atualizados {n} ponto(s).")
    except requests.HTTPError as e:
        print(f"[Dynatrace] HTTP {e.response.status_code}: {e.response.text}")
    except Exception as e:
        print(f"Erro: {e}")
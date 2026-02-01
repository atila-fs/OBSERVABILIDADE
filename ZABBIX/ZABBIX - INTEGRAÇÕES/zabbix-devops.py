import os
import json
import requests
import urllib3
import base64
from datetime import datetime, timezone

# Configurações do Zabbix
ZABBIX_URL = "http://[IP_ADDRESS]/zabbix/api_jsonrpc.php"
ZABBIX_TOKEN = "<token>"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configurações do Azure DevOps
ORG_URL = "https://dev.azure.com/<ORG>"
PROJECT = "<PROJECT>"
WORKITEM_TYPE = "<WORK_ITEM_TYPE>"
API_VERSION = "7.1"
PAT_TOKEN = "<PAT>"
AUTH_HEADER = {
    "Authorization": f"Basic {base64.b64encode(f':{PAT_TOKEN}'.encode()).decode()}",
    "Content-Type": "application/json-patch+json"
}

# Arquivos
TIMESTAMP_FILE = "/var/log/zabbix_last_timestamp.txt"
LOG_FILE = "/var/log/zabbix-devops.log"

def log(message):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{datetime.now()} - {message}\n")

def is_host_in_maintenance(hostid):
    payload = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": ["hostid", "name", "maintenance_status"],
            "hostids": [hostid]
        },
        "auth": ZABBIX_TOKEN,
        "id": 1
    }
    try:
        response = requests.post(ZABBIX_URL, json=payload, timeout=10, verify=False)
        response.raise_for_status()
        host = response.json()["result"][0]
        return str(host.get("maintenance_status", "0")) == "1"
    except Exception as e:
        log(f"Erro ao verificar manutenção do host {hostid}: {e}")
        return False

def get_recent_triggers(last_timestamp):
    payload = {
        "jsonrpc": "2.0",
        "method": "trigger.get",
        "params": {
            "output": ["triggerid", "description", "priority", "lastchange", "state", "value"],
            "filter": {"priority": [4, 5]},
            "group": "PROD",
            "selectHosts": ["host", "name", "hostid"],
            "sortfield": "lastchange",
            "sortorder": "DESC"
        },
        "auth": ZABBIX_TOKEN,
        "id": 1
    }

    try:
        response = requests.post(ZABBIX_URL, json=payload, timeout=10, verify=False)
        response.raise_for_status()
        triggers = response.json().get("result", [])
        filtered_triggers = []
        for t in triggers:
            try:
                if int(t.get("lastchange", 0)) <= last_timestamp:
                    continue
                if str(t.get("value", "0")) != "1":  # Ativo
                    continue
                host = t["hosts"][0]
                hostid = host["hostid"]
                hostname = host["host"]
                if is_host_in_maintenance(hostid):
                    log(f"Ignorado: Host '{hostname}' está em manutenção.")
                    continue
                filtered_triggers.append(t)
            except Exception as e:
                log(f"Erro ao processar trigger: {e}")
        log(f"{len(filtered_triggers)} triggers válidas encontradas.")
        return filtered_triggers
    except requests.RequestException as e:
        log(f"Erro ao obter triggers do Zabbix: {e}")
        return []

def get_current_sprint():
    url = f"{ORG_URL}/{PROJECT}/_apis/work/teamsettings/iterations?$timeframe=current&api-version={API_VERSION}"
    try:
        response = requests.get(url, headers=AUTH_HEADER, timeout=10)
        response.raise_for_status()
        iterations = response.json().get("value", [])
        if iterations:
            return iterations[0]["path"]
        return None
    except requests.RequestException as e:
        log(f"Erro ao obter Sprint atual: {e}")
        return None

def create_devops_card(hostname, description, alert_date):
    user_email = "lucas.bereta@safeweb.com.br"
    sprint_path = get_current_sprint()
    json_data = [
        {"op": "add", "path": "/fields/System.Title", "value": f"{hostname} - {description}"},
        {"op": "add", "path": "/fields/System.Description", "value": description},
        {"op": "add", "path": "/fields/Custom.AlertDate", "value": alert_date},
        {"op": "add", "path": "/fields/System.AssignedTo", "value": user_email}
    ]
    if sprint_path:
        json_data.append({"op": "add", "path": "/fields/System.IterationPath", "value": sprint_path})
    try:
        url = f"{ORG_URL}/{PROJECT}/_apis/wit/workitems/%24{WORKITEM_TYPE}?api-version={API_VERSION}"
        response = requests.post(url, headers=AUTH_HEADER, json=json_data, timeout=10)
        response.raise_for_status()
        log(f"Card criado: {response.text}")
        return response.json().get("id")
    except requests.RequestException as e:
        log(f"Erro ao criar card no Azure DevOps: {e}")
        return None
    except json.JSONDecodeError:
        log("Erro: Resposta inválida do Azure DevOps.")
        return None

# Carrega timestamp
last_timestamp = 0
if os.path.exists(TIMESTAMP_FILE):
    try:
        with open(TIMESTAMP_FILE, "r") as file:
            last_timestamp = int(file.read().strip())
    except ValueError:
        log("Aviso: Timestamp inválido. Reiniciando com 0.")
else:
    last_timestamp = int(datetime.now(timezone.utc).timestamp())
    with open(TIMESTAMP_FILE, "w") as file:
        file.write(str(last_timestamp))
    log("Arquivo de timestamp criado. Execução inicial ignorada.")
    exit(0)

# Processa triggers
triggers = get_recent_triggers(last_timestamp)
if not triggers:
    log("Nenhuma trigger nova válida.")
    exit(0)

new_timestamp = last_timestamp
for trigger in triggers:
    hostname = trigger["hosts"][0]["host"]
    description = trigger["description"]
    lastchange = int(trigger["lastchange"])
    alert_date = datetime.fromtimestamp(lastchange, tz=timezone.utc).isoformat()
    card_id = create_devops_card(hostname, description, alert_date)

    if card_id:
        log(f"Card criado com sucesso: ID {card_id}")
    else:
        log("Falha ao criar card no Azure DevOps.")

    new_timestamp = max(new_timestamp, lastchange)

# Salva novo timestamp
try:
    with open(TIMESTAMP_FILE, "w") as file:
        file.write(str(new_timestamp))
    log(f"Novo timestamp salvo: {new_timestamp}")
except IOError as e:
    log(f"Erro ao salvar timestamp: {e}")

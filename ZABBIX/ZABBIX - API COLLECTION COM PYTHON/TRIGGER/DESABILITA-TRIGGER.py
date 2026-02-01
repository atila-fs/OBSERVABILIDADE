import requests

# Configurações do Zabbix
ZABBIX_URL = 'http://[IP_ADDRESS]/zabbix/api_jsonrpc.php'
ZABBIX_USER = 'zabbix_api'
ZABBIX_PASSWORD = '<senha>'

# Autenticação na API do Zabbix
def authenticate():
    payload = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": ZABBIX_USER,
            "password": ZABBIX_PASSWORD
        },
        "id": 1,
        "auth": None
    }
    response = requests.post(ZABBIX_URL, json=payload)
    result = response.json()
    return result.get("result")

# Buscar triggers com severidade DISASTER (5) e desabilitadas (0)
def get_disabled_disaster_triggers(auth_token):
    payload = {
        "jsonrpc": "2.0",
        "method": "trigger.get",
        "params": {
            "output": ["triggerid", "description", "status"],
            "filter": {
                "priority": 5,  # Severidade DISASTER
                "status": 1     # Triggers desabilitadas (1)
            }
        },
        "auth": auth_token,
        "id": 2
    }
    response = requests.post(ZABBIX_URL, json=payload)
    result = response.json()
    return result.get("result", [])

# Habilitar triggers pelo triggerid
def enable_triggers(auth_token, trigger_ids):
    if not trigger_ids:
        print("Nenhuma trigger para habilitar.")
        return

    payload = {
        "jsonrpc": "2.0",
        "method": "trigger.update",
        "params": [{"triggerid": tid, "status": 0} for tid in trigger_ids],  # 0 = habilitado
        "auth": auth_token,
        "id": 3
    }
    response = requests.post(ZABBIX_URL, json=payload)
    result = response.json()

    if "result" in result:
        print(f"{len(trigger_ids)} triggers foram habilitadas com sucesso!")
    else:
        print("Erro ao habilitar triggers:", result)

# Fluxo principal
if __name__ == "__main__":
    auth_token = authenticate()
    if not auth_token:
        print("Erro ao autenticar no Zabbix.")
        exit()

    triggers = get_disabled_disaster_triggers(auth_token)

    if not triggers:
        print("Nenhuma trigger DISASTER desabilitada encontrada.")
    else:
        trigger_ids = [t["triggerid"] for t in triggers]
        print(f"Encontradas {len(trigger_ids)} triggers desabilitadas. Habilitando...")
        enable_triggers(auth_token, trigger_ids)
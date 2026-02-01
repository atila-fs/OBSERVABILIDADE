import requests
import json
from datetime import datetime, timedelta

# Configurações da API do Zabbix
ZABBIX_URL = 'http://[IP_ADDRESS]/zabbix/api_jsonrpc.php'
ZABBIX_USER = 'zabbix_api'
ZABBIX_PASSWORD = '<senha>'

# Função para autenticar na API do Zabbix
def zabbix_login():
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
    return response.json()["result"]

# Função para buscar triggers do tipo HIGH alteradas nas últimas 6 horas
def get_high_triggers(auth_token):
    time_from = int((datetime.now() - timedelta(hours=6)).timestamp())
    payload = {
        "jsonrpc": "2.0",
        "method": "trigger.get",
        "params": {
            "output": ["triggerid", "description", "priority", "lastchange"],
            "filter": {
                "priority": 4,  # Prioridade 4 = HIGH
                "value": 1      # Triggers com estado PROBLEM (1)
            },
            "sortfield": "lastchange",
            "sortorder": "DESC",
            "lastChangeSince": time_from
        },
        "auth": auth_token,
        "id": 1
    }
    response = requests.post(ZABBIX_URL, json=payload)
    return response.json()["result"]

# Função principal
def main():
    auth_token = zabbix_login()
    triggers = get_high_triggers(auth_token)
    
    if triggers:
        print("Triggers do tipo HIGH alteradas nas últimas horas:")
        for trigger in triggers:
            lastchange = datetime.fromtimestamp(int(trigger["lastchange"])).strftime("%Y-%m-%d %H:%M:%S")
            print(f"ID: {trigger['triggerid']}, Descrição: {trigger['description']}, Última alteração: {lastchange}")
    else:
        print("Nenhuma trigger do tipo HIGH alterada nas últimas 24 horas.")

if __name__ == "__main__":
    main()
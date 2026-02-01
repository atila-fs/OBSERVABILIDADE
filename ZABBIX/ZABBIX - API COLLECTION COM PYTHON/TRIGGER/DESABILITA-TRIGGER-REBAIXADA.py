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

# Função para buscar triggers alteradas nas últimas horas
def get_high_triggers(auth_token):
    # Calcula o timestamp de horas atrás (OBS: Definir a quantidade de horas na variavel "hours")
    time_from = int((datetime.now() - timedelta(hours=3)).timestamp())
    payload = {
        "jsonrpc": "2.0",
        "method": "trigger.get",
        "params": {
            "output": ["triggerid", "description", "priority", "lastchange"],
            "filter": {
                "priority": 4,  # Prioridade 5 = Disaster / Prioridade 4 = High / Prioridade 3 = Average
                "value": 1      # Triggers com status PROBLEM (1)
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

# Função para desabilitar uma trigger
def disable_trigger(auth_token, trigger_id):
    payload = {
        "jsonrpc": "2.0",
        "method": "trigger.update",
        "params": {
            "triggerid": trigger_id,
            "status": 1  # 1 = Desabilitar a trigger / 2 = Habilitar a trigger
        },
        "auth": auth_token,
        "id": 1
    }
    response = requests.post(ZABBIX_URL, json=payload)
    return response.json()

# Função principal
def main():
    # Autentica na API do Zabbix
    auth_token = zabbix_login()

    # Busca as triggers alteradas nas últimas  horas
    triggers = get_high_triggers(auth_token)

    # Verifica se há triggers para desabilitar
    if triggers:
        print(f"Triggers alteradas nas últimas horas:")
        for trigger in triggers:
            lastchange = datetime.fromtimestamp(int(trigger["lastchange"])).strftime("%Y-%m-%d %H:%M:%S")
            print(f"ID: {trigger['triggerid']}, Descrição: {trigger['description']}, Última alteração: {lastchange}")
            
            # Desabilita a trigger
            result = disable_trigger(auth_token, trigger["triggerid"])
            if "error" in result:
                print(f"Erro ao desabilitar a trigger {trigger['triggerid']}: {result['error']['data']}")
            else:
                print(f"Trigger {trigger['triggerid']} desabilitada com sucesso.")
    else:
        print("Nenhuma trigger alterada nas últimas horas.")

if __name__ == "__main__":
    main()

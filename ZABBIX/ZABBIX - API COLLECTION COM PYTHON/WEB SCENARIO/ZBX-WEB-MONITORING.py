# Importa as Bibliotecas
import requests
import json

debug = True

# Variaveis para logar na API
username = 'zabbix_api'
password = '<senha>'
url = 'http://[IP_ADDRESS]/zabbix/api_jsonrpc.php'
headers = {'Content-Type': 'application/json'}

# Função que solicita a API do Zabbix os parametros para login


def make_request(method, params, auth_token=None):
    if debug:
        print('Fazendo solicitação: ' + method)
        print('Parâmetros da solicitação: ' + str(params))

    data = {
        'jsonrpc': '2.0',
        'method': method,
        'params': params,
        'auth': auth_token,
        'id': 1
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)
    response_json = response.json()

    if debug:
        print('Resposta da solicitação: ' + str(response_json))

    return response_json


if debug:
    print('Autenticando usuário: ' + username)

# Faz uma solicitação de autenticação a API do Zabbix
auth_params = {
    'user': username,
    'password': password
}
auth_request = make_request('user.login', auth_params)

if debug:
    print('Token de autenticação: ' + auth_request['result'])

auth_token = auth_request['result']

# Configurações do cenário web 01
host_id = "11759"
scenario_name = "PSBIO WORKER ENDPOINT PORT 30003"
update_interval = 180
attempts = 3
steps = [
    {
        "name": "PSBIO WORKER ENDPOINT PORT 30003",
        "url": "http://[IP_ADDRESS]:30003/swagger/index.html",
        "timeout": 15,
        "status_codes": "200",
        "headers": [
            {"name": "User-Agent", "value": "Internet Explorer 11"}
        ],
        "no": 1
    }
]

# Criação do cenário web 01
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "httptest.create",
    "params": {
        "name": scenario_name,
        "hostid": host_id,
        "delay": update_interval,
        "retries": attempts,
        "steps": steps
    },
    "auth": auth_token,
    "id": 1
}

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar cenário web: {response_json['error']['data']}")
else:
    scenario_id = response_json["result"]["httptestids"][0]
    print(f"Cenário web criado com sucesso com o ID {scenario_id}")

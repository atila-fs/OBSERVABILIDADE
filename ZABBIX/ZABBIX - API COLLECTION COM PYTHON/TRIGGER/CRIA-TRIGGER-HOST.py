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

# Definindo as informações da trigger 01
trigger1 = {
    'description': 'PSBIO WORKER ENDPOINT PORT 30003 INDISPONIVEL',
    'expression': 'last(/HOST-NAME/web.test.fail[PSBIO WORKER ENDPOINT PORT 30003])=1',
    'priority': 4,
    'status': 0
}

# Criando a trigger 01
data1 = {
    'jsonrpc': '2.0',
    'method': 'trigger.create',
    'params': trigger1,
    'auth': auth_token,
    'id': 1
}

# Definindo as informações da trigger 02
trigger2 = {
    'description': 'PSBIO WORKER ENDPOINT PORT 30004 INDISPONIVEL',
    'expression': 'last(/HOST-NAME/web.test.fail[PSBIO WORKER ENDPOINT PORT 30004])=1',
    'priority': 4,
    'status': 0
}

# Criando a trigger 02
data2 = {
    'jsonrpc': '2.0',
    'method': 'trigger.create',
    'params': trigger2,
    'auth': auth_token,
    'id': 1
}

response1 = requests.post(url, headers=headers, data=json.dumps(data1))
response2 = requests.post(url, headers=headers, data=json.dumps(data2))

response_json = response1.json()
if 'error' in response_json:
    print(f"Erro ao criar a trigger: {response_json['error']['data']}")
else:
    trigger_id = response_json["result"]["triggerids"][0]
    print(f"Trigger criada com sucesso com o ID: {trigger_id}")

response_json = response2.json()
if 'error' in response_json:
    print(f"Erro ao criar a trigger: {response_json['error']['data']}")
else:
    trigger_id = response_json["result"]["triggerids"][0]
    print(f"Trigger criada com sucesso com o ID: {trigger_id}")

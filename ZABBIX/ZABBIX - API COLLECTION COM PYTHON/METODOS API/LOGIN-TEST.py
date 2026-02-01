# IMPORTA OS METODOS NECESSÁRIOS E SUAS RESPECTIVAS BIBLIOTECAS
import requests
import json
import os

# ATIVA OU DESATIVA O MODO DEBUG
debug = True

# CARREGAR VARIÁVEIS DO ARQUIVO JSON
config_path = os.path.join(r'C:\Users\atila.silva.ECDS\Desktop\Visual Studio\Api Zabbix', 'config.json')
with open(config_path, 'r') as file:
    config = json.load(file)

# VARIÁVEIS DE CONFIGURAÇÃO
username = config['username']
password = config['password']
url = config['url']

# CRIA O PAYLOAD
def payload(username, password):
    return {
        'jsonrpc': '2.0',
        'method': 'user.login',
        'params': {
            'user': username,
            'password': password
        },
        'id': 1,
        'auth': None
    }

headers = {'Content-Type': 'application/json'}

# AUTENTICA O USUÁRIO
response = requests.post(url, headers=headers, data=json.dumps(payload(username, password)))
auth_request = response.json()

# VALIDA A AUTENTICAÇÃO
if 'result' in auth_request:
    print('Token de autenticação: ' + auth_request['result'])
else:
    print('Autenticação Falhou:')
    if 'error' in auth_request:
        print('Code:', auth_request['error'].get('code', 'N/A'))
        print('Message:', auth_request['error'].get('message', 'N/A'))
        print('Data:', auth_request['error'].get('data', 'N/A'))
    else:
        print('Erro desconhecido.')
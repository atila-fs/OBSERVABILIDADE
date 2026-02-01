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

# Lista de informações das triggers
triggers_info = [
    {
        'description': '<Server_01> - Desabilitado no pool',
        'expression': 'find(/FORTIADC SNMP/SS_VS01,#1,"regexp","Disable")>=1)<>0',
        'priority': 3,
        'status': 0
    },
    {
        'description': '<Server_02> - Desabilitado no pool',
        'expression': 'find(/FORTIADC SNMP/SS_VS02,#1,"regexp","Disable")>=1)<>0',
        'priority': 3,
        'status': 0
    },
    {
        'description': '<Server_03> - Desabilitado no pool',
        'expression': 'find(/FORTIADC SNMP/SS_VS03,#1,"regexp","Disable")>=1)<>0',
        'priority': 3,
        'status': 0
    },
    {
        'description': '<Server_04> - Desabilitado no pool',
        'expression': 'find(/FORTIADC SNMP/SS_VS04,#1,"regexp","Disable")>=1)<>0',
        'priority': 3,
        'status': 0
    },
    {
        'description': '<Server_05> - Desabilitado no pool',
        'expression': 'find(/FORTIADC SNMP/SS_VS05,#1,"regexp","Disable")>=1)<>0',
        'priority': 3,
        'status': 0
    },
    {
        'description': '<Server_06> - Desabilitado no pool',
        'expression': 'find(/FORTIADC SNMP/SS_VS06,#1,"regexp","Disable")>=1)<>0',
        'priority': 3,
        'status': 0
    },
    {
        'description': '<Server_07> - Desabilitado no pool',
        'expression': 'find(/FORTIADC SNMP/SS_VS07,#1,"regexp","Disable")>=1)<>0',
        'priority': 3,
        'status': 0
    },
    {
        'description': '<Server_08> - Desabilitado no pool',
        'expression': 'find(/FORTIADC SNMP/SS_VS08,#1,"regexp","Disable")>=1)<>0',
        'priority': 3,
        'status': 0
    },
    {
        'description': '<Server_09> - Desabilitado no pool',
        'expression': 'find(/FORTIADC SNMP/SS_VS09,#1,"regexp","Disable")>=1)<>0',
        'priority': 3,
        'status': 0
    },
    {
        'description': '<Server_10> - Desabilitado no pool',
        'expression': 'find(/FORTIADC SNMP/SS_VS10,#1,"regexp","Disable")>=1)<>0',
        'priority': 3,
        'status': 0
    },
    {
        'description': '<Server_11> - Desabilitado no pool',
        'expression': 'find(/FORTIADC SNMP/SS_VS11,#1,"regexp","Disable")>=1)<>0',
        'priority': 3,
        'status': 0
    }
]

# Criando as triggers no template
for trigger_info in triggers_info:
    # Criando a trigger
    data = {
        'jsonrpc': '2.0',
        'method': 'trigger.create',
        'params': trigger_info,
        'auth': auth_token,
        'id': 1
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_json = response.json()

    if 'error' in response_json:
        print(f"Erro ao criar a trigger: {response_json['error']['data']}")
    else:
        trigger_id = response_json["result"]["triggerids"][0]
        print(f"Trigger criada com sucesso com o ID {trigger_id}")
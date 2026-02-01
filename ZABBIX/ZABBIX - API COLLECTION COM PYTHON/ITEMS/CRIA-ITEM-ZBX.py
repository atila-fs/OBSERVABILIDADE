# Importa as Bibliotecas
import requests
import json

debug = True

# Variáveis para logar na API
username = 'zabbix_api'
password = '<senha>'
url = 'http://[IP_ADDRESS]/zabbix/api_jsonrpc.php'
headers = {'Content-Type': 'application/json'}

# Função que solicita a API do Zabbix os parâmetros para login
def make_request(method, params, auth_token=None):
    if debug:
        print(f'Fazendo solicitação: {method}')
        print(f'Parâmetros da solicitação: {json.dumps(params, indent=2)}')

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
        print(f'Resposta da solicitação: {json.dumps(response_json, indent=2)}')

    return response_json

if debug:
    print(f'Autenticando usuário: {username}')

# Faz uma solicitação de autenticação à API do Zabbix
auth_params = {
    'user': username,
    'password': password
}
auth_request = make_request('user.login', auth_params)

if 'result' not in auth_request:
    print(f"Erro ao autenticar: {auth_request.get('error', {}).get('data', 'Erro desconhecido')}")
    exit(1)

if debug:
    print(f'Token de autenticação: {auth_request["result"]}')

auth_token = auth_request['result']

# ID do template onde o item será criado
template_id = "12104"  

# Configurações do item SNMP Agent
item_name = "[Status] POOL_D-N3P-PSS-WEB01"
key = "HS_VS01"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.1"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_D-N3P-PSS-WEB02"
key = "HS_VS02"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.2"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_Q-N3P-PSS-WEB01"
key = "HS_VS03"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.3"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_Q-N3P-PSS-WEB02"
key = "HS_VS04"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.4"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-N4-PSS-SEC01"
key = "HS_VS05"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.5"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-N4-PSS-SEC02"
key = "HS_VS06"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.6"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-N4-PSS-SEC03"
key = "HS_VS07"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.7"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-N4-PSS-SEC04"
key = "HS_VS08"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.8"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-N4-PSS-SEC05"
key = "HS_VS09"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.9"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-N4-PSS-SEC06"
key = "HS_VS10"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.10"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-N4-PSS-SEAC01"
key = "HS_VS11"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.11"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-N4-PSS-SEAC02"
key = "HS_VS12"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.12"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-N4-PSS-SGC01"
key = "HS_VS13"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.13"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-N4-PSS-SGC02"
key = "HS_VS14"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.14"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_PSBIO-WORKERS01"
key = "HS_VS15"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.15"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_PSBIO-WORKERS02"
key = "HS_VS16"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.16"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_PSBIO-WORKERS03"
key = "HS_VS17"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.17"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_H-N3P-PSS-SEC01"
key = "HS_VS18"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.18"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_H-N3P-PSS-SEC02"
key = "HS_VS19"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.19"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-NTP01"
key = "HS_VS20"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.20"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-NTP02"
key = "HS_VS21"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.21"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_D-N3P-INF-LAB01"
key = "HS_VS22"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.22"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_D-N3P-INF-LAB02"
key = "HS_VS23"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.23"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-LB-BE-SFW01"
key = "HS_VS24"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.24"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-LB-BE-SFW02"
key = "HS_VS25"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.25"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-LB-BE-CND01"
key = "HS_VS26"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.26"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-LB-BE-CND02"
key = "HS_VS27"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.27"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-LB-BE-LNK01"
key = "HS_VS28"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.28"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-LB-BE-LNK02"
key = "HS_VS29"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.29"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-LB-BE-SMP01"
key = "HS_VS30"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.30"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-LB-BE-SMP02"
key = "HS_VS31"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.31"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-LB-BE-CNS01"
key = "HS_VS32"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.32"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-LB-BE-CNS02"
key = "HS_VS33"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.33"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-LB-BE-DCC01"
key = "HS_VS34"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.34"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-LB-BE-DCC02"
key = "HS_VS35"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.35"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-LB-BE-RDI01"
key = "HS_VS36"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.36"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-LB-BE-RDI02"
key = "HS_VS37"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.37"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-LB-BE-CRR01"
key = "HS_VS38"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.38"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-LB-BE-CRR02"
key = "HS_VS39"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.39"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-LB-BE-CRT01"
key = "HS_VS40"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.40"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-LB-BE-CRT02"
key = "HS_VS41"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.41"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-N4-RFBv2-SRV01"
key = "HS_VS42"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.42"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-N4-RFBv2-SRV02"
key = "HS_VS43"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.43"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-N4-RFBv5-SRV01"
key = "HS_VS44"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.44"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-N4-RFBv5-SRV02"
key = "HS_VS45"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.45"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-N4-RFCD-HSM01"
key = "HS_VS46"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.46"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-N4-RFCD-HSM02"
key = "HS_VS47"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.47"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-N4-RFBCD-SRV01"
key = "HS_VS48"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.48"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_P-N4-RFBCD-SRV02"
key = "HS_VS49"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.49"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_H-N3P-SFW-BKE01"
key = "HS_VS50"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.50"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_H-N3P-SFW-BKE02"
key = "HS_VS51"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.51"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_H-N3P-CND-BKE01"
key = "HS_VS52"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.52"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_H-N3P-CND-BKE02"
key = "HS_VS53"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.53"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_C-N3P-PSS-RDS01"
key = "HS_VS54"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.54"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] POOL_C-N3P-PSS-RDS02"
key = "HS_VS55"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.55"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] P-N4-PSS-SEC07"
key = "HS_VS56"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.56"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")

# Configurações do item SNMP Agent
item_name = "[Status] H-N3P-PSS-SEC02"
key = "HS_VS57"
item_type = 2  
value_type = 3  
snmp_oid = "1.3.6.1.4.1.12356.112.8.1.3.1.3.57"  

# Criação do item SNMP Agent no template
headers = {"Content-Type": "application/json-rpc"}
data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": item_name,
        "key_": key,
        "type": item_type,
        "hostid": template_id,  
        "value_type": value_type,
        "snmp_oid": snmp_oid,
        "delay": "30s", 

    },
    "auth": auth_token,
    "id": 1
}

if debug:
    print('Enviando solicitação para criar item SNMP Agent...')

response = requests.post(url, headers=headers, data=json.dumps(data))

response_json = response.json()
if 'error' in response_json:
    print(f"Erro ao criar item SNMP Agent: {response_json['error']['data']}")
else:
    item_id = response_json["result"]["itemids"][0]
    print(f"Item SNMP Agent criado com sucesso com o ID {item_id}")
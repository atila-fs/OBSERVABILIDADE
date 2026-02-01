# Importa as Bibliotecas 
import requests
import json

debug = True

# Trecho do script que vai ser responsavel por logar na API (função que conecta na API e printa os steps de login)
username = 'zabbix_api'
password = '<senha>'
url = 'http://[IP_ADDRESS]/zabbix/api_jsonrpc.php'
headers = {'Content-Type': 'application/json'}

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

auth_params = {
    'user': username,
    'password': password
}
auth_request = make_request('user.login', auth_params)

if debug:
    print('Token de autenticação: ' + auth_request['result'])

auth_token = auth_request['result']

# Trecho do código no qual começa a criar os itens SNMP no template da Huawei (função que "seta" os parametros de requisição para API)

# Função de requisição 01
def zabbix_create_item1(item_key, item_name, template_id, snmp_oid):
    item_payload = {
        'jsonrpc': '2.0',
        'method': 'item.create',
        'params': {
            'name': item_name,
            'key_': item_key,
            'hostid': template_id,
            'type': 20,
            'value_type': 3,
            'delay': 300,
            'history': 604800,
            'trends': 604800,
            'units': "%",
            'interfaceid': "1",
            'applications': ["SNMPv2"],
            'snmp_community': 'safeweb_snmp',
            'snmp_oid': snmp_oid,
        },
        'auth': auth_token,
        'id': 1,
    }

    headers = {
        'Content-Type': 'application/json-rpc'
    }

    response = requests.post(url, data=json.dumps(item_payload), headers=headers)
    result = json.loads(response.text)

    if 'error' in result:
        raise Exception(result['error']['data'])

    return result['result']['itemids'][0]

# Conjunto de variaveis que definem o item a ser criado (item 01)
item_key = 'cpu.usage.ipu'
item_name = 'CPU Usage (IPU)'
template_id = 11637
snmp_oid = '1.3.6.1.4.1.2011.5.25.31.1.1.1.1.5.16842753'

item_id = zabbix_create_item1(item_key, item_name, template_id, snmp_oid)

print("Item criado com sucesso. ID do item:", item_id)

# Função de requisição 02
def zabbix_create_item2(item_key, item_name, template_id, snmp_oid):
    item_payload = {
        'jsonrpc': '2.0',
        'method': 'item.create',
        'params': {
            'name': item_name,
            'key_': item_key,
            'hostid': template_id,
            'type': 20,
            'value_type': 3,
            'delay': 300,
            'history': 604800,
            'trends': 604800,
            'units': "%",
            'interfaceid': "1",
            'applications': ["SNMPv2"],
            'snmp_community': 'safeweb_snmp',
            'snmp_oid': snmp_oid,
        },
        'auth': auth_token,
        'id': 1,
    }

    headers = {
        'Content-Type': 'application/json-rpc'
    }

    response = requests.post(url, data=json.dumps(item_payload), headers=headers)
    result = json.loads(response.text)

    if 'error' in result:
        raise Exception(result['error']['data'])

    return result['result']['itemids'][0]

# Conjunto de variaveis que definem o item a ser criado (item 02)
item_key = 'cpu.avg.ipu'
item_name = 'CPU Average Usage (IPU)'
template_id = 11637
snmp_oid = '1.3.6.1.4.1.2011.5.25.31.1.1.1.1.35.16842753'

item_id = zabbix_create_item2(item_key, item_name, template_id, snmp_oid)

print("Item criado com sucesso. ID do item:", item_id)

# Função de requisição 03
def zabbix_create_item3(item_key, item_name, template_id, snmp_oid):
    item_payload = {
        'jsonrpc': '2.0',
        'method': 'item.create',
        'params': {
            'name': item_name,
            'key_': item_key,
            'hostid': template_id,
            'type': 20,
            'value_type': 3,
            'delay': 300,
            'history': 604800,
            'trends': 604800,
            'interfaceid': "1",
            'applications': ["SNMPv2"],
            'snmp_community': 'safeweb_snmp',
            'snmp_oid': snmp_oid,
        },
        'auth': auth_token,
        'id': 1,
    }

    headers = {
        'Content-Type': 'application/json-rpc'
    }

    response = requests.post(url, data=json.dumps(item_payload), headers=headers)
    result = json.loads(response.text)

    if 'error' in result:
        raise Exception(result['error']['data'])

    return result['result']['itemids'][0]

# Conjunto de variaveis que definem o item a ser criado (item 03)
item_key = 'cpu.type.ipu'
item_name = 'CPU Type (IPU)'
template_id = 11637
snmp_oid = '1.3.6.1.4.1.2011.5.25.31.1.1.1.1.30.16842753'

item_id = zabbix_create_item3(item_key, item_name, template_id, snmp_oid)

print("Item criado com sucesso. ID do item:", item_id)

# Função de requisição 04
def zabbix_create_item4(item_key, item_name, template_id, snmp_oid):
    item_payload = {
        'jsonrpc': '2.0',
        'method': 'item.create',
        'params': {
            'name': item_name,
            'key_': item_key,
            'hostid': template_id,
            'type': 20,
            'value_type': 3,
            'delay': 300,
            'history': 604800,
            'trends': 604800,
            'units': "%",
            'interfaceid': "1",
            'applications': ["SNMPv2"],
            'snmp_community': 'safeweb_snmp',
            'snmp_oid': snmp_oid,
        },
        'auth': auth_token,
        'id': 1,
    }

    headers = {
        'Content-Type': 'application/json-rpc'
    }

    response = requests.post(url, data=json.dumps(item_payload), headers=headers)
    result = json.loads(response.text)

    if 'error' in result:
        raise Exception(result['error']['data'])

    return result['result']['itemids'][0]

# Conjunto de variaveis que definem o item a ser criado (item 04)
item_key = 'cpu.threshold.ipu'
item_name = 'CPU Threshold (IPU)'
template_id = 11637
snmp_oid = '1.3.6.1.4.1.2011.5.25.31.1.1.1.1.6.16842753'

item_id = zabbix_create_item4(item_key, item_name, template_id, snmp_oid)

print("Item criado com sucesso. ID do item:", item_id)

# Função de requisição 05
def zabbix_create_item5(item_key, item_name, template_id, snmp_oid):
    item_payload = {
        'jsonrpc': '2.0',
        'method': 'item.create',
        'params': {
            'name': item_name,
            'key_': item_key,
            'hostid': template_id,
            'type': 20,
            'value_type': 3,
            'delay': 300,
            'history': 604800,
            'trends': 604800,
            'units': "%",
            'interfaceid': "1",
            'applications': ["SNMPv2"],
            'snmp_community': 'safeweb_snmp',
            'snmp_oid': snmp_oid,
        },
        'auth': auth_token,
        'id': 1,
    }

    headers = {
        'Content-Type': 'application/json-rpc'
    }

    response = requests.post(url, data=json.dumps(item_payload), headers=headers)
    result = json.loads(response.text)

    if 'error' in result:
        raise Exception(result['error']['data'])

    return result['result']['itemids'][0]

# Conjunto de variaveis que definem o item a ser criado (item 05)
item_key = 'memory.usage.ipu'
item_name = 'Memory Usage (IPU)'
template_id = 11637
snmp_oid = '1.3.6.1.4.1.2011.5.25.31.1.1.1.1.7.16842753'

item_id = zabbix_create_item5(item_key, item_name, template_id, snmp_oid)

print("Item criado com sucesso. ID do item:", item_id)

# Função de requisição 06
def zabbix_create_item6(item_key, item_name, template_id, snmp_oid):
    item_payload = {
        'jsonrpc': '2.0',
        'method': 'item.create',
        'params': {
            'name': item_name,
            'key_': item_key,
            'hostid': template_id,
            'type': 20,
            'value_type': 3,
            'delay': 300,
            'history': 604800,
            'trends': 604800,
            'interfaceid': "1",
            'applications': ["SNMPv2"],
            'snmp_community': 'safeweb_snmp',
            'snmp_oid': snmp_oid,
        },
        'auth': auth_token,
        'id': 1,
    }

    headers = {
        'Content-Type': 'application/json-rpc'
    }

    response = requests.post(url, data=json.dumps(item_payload), headers=headers)
    result = json.loads(response.text)

    if 'error' in result:
        raise Exception(result['error']['data'])

    return result['result']['itemids'][0]

# Conjunto de variaveis que definem o item a ser criado (item 06)
item_key = 'memory.type.ipu'
item_name = 'Memory Type (IPU)'
template_id = 11637
snmp_oid = '1.3.6.1.4.1.2011.5.25.31.1.1.1.1.31.16842753'

item_id = zabbix_create_item6(item_key, item_name, template_id, snmp_oid)

print("Item criado com sucesso. ID do item:", item_id)

# Função de requisição 07
def zabbix_create_item7(item_key, item_name, template_id, snmp_oid):
    item_payload = {
        'jsonrpc': '2.0',
        'method': 'item.create',
        'params': {
            'name': item_name,
            'key_': item_key,
            'hostid': template_id,
            'type': 20,
            'value_type': 3,
            'delay': 300,
            'history': 604800,
            'trends': 604800,
            'units': "%",
            'interfaceid': "1",
            'applications': ["SNMPv2"],
            'snmp_community': 'safeweb_snmp',
            'snmp_oid': snmp_oid,
        },
        'auth': auth_token,
        'id': 1,
    }

    headers = {
        'Content-Type': 'application/json-rpc'
    }

    response = requests.post(url, data=json.dumps(item_payload), headers=headers)
    result = json.loads(response.text)

    if 'error' in result:
        raise Exception(result['error']['data'])

    return result['result']['itemids'][0]

# Conjunto de variaveis que definem o item a ser criado (item 07)
item_key = 'memory.average.ipu'
item_name = 'Memory Average Usage (IPU)'
template_id = 11637
snmp_oid = '1.3.6.1.4.1.2011.5.25.31.1.1.1.1.36.16842753'

item_id = zabbix_create_item7(item_key, item_name, template_id, snmp_oid)

print("Item criado com sucesso. ID do item:", item_id)

# Função de requisição 08
def zabbix_create_item8(item_key, item_name, template_id, snmp_oid):
    item_payload = {
        'jsonrpc': '2.0',
        'method': 'item.create',
        'params': {
            'name': item_name,
            'key_': item_key,
            'hostid': template_id,
            'type': 20,
            'value_type': 3,
            'delay': 300,
            'history': 604800,
            'trends': 604800,
            'units': "%",
            'interfaceid': "1",
            'applications': ["SNMPv2"],
            'snmp_community': 'safeweb_snmp',
            'snmp_oid': snmp_oid,
        },
        'auth': auth_token,
        'id': 1,
    }

    headers = {
        'Content-Type': 'application/json-rpc'
    }

    response = requests.post(url, data=json.dumps(item_payload), headers=headers)
    result = json.loads(response.text)

    if 'error' in result:
        raise Exception(result['error']['data'])

    return result['result']['itemids'][0]

# Conjunto de variaveis que definem o item a ser criado (item 08)
item_key = 'memory.threshold.ipu'
item_name = 'Memory Threshold (IPU)'
template_id = 11637
snmp_oid = '1.3.6.1.4.1.2011.5.25.31.1.1.1.1.8.16842753'

item_id = zabbix_create_item8(item_key, item_name, template_id, snmp_oid)

print("Item criado com sucesso. ID do item:", item_id)


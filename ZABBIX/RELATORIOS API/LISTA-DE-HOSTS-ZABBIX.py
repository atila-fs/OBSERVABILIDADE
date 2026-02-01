# Importa as Bibliotecas
import requests
import json
import csv

debug = True

# Loga na API
username = '<user>'
password = '<pass>'
url = 'http://<ip_zabbix>/zabbix/api_jsonrpc.php'
headers = {'Content-Type': 'application/json'}

# Função que solicita a API do Zabbix os parametros
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

# Faz uma solicitação para obter uma lista de todos os hosts monitorados no Zabbix
host_params = {
    'output': ['host'],
    'monitored_hosts': True,
}
host_request = make_request('host.get', host_params, auth_token)
host_list = host_request['result']

if debug:
    print('Lista de hosts monitorados: ' + str(host_list))

# Imprime uma lista de todos os hosts monitorados na tela
for host in host_list:
    print(host['host'])

# Salva tudo em um arquivo CSV chamado "hosts.csv"
with open('hosts.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Host'])

    for host in host_list:
        writer.writerow([host['host']])
        print(host['host'], 'hosts.csv')

#
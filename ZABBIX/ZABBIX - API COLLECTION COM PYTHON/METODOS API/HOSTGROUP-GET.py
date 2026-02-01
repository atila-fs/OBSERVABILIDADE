# IMPORTA OS METODOS NECESSÁRIOS E SUAS RESPECTIVAS BIBLIOTECAS
import requests
import json
import os

# ATIVA OU DESATIVA O MODO DEBUG
debug = False

############################################################################################################################################################################
    ######################################## INICIO DA PARTE DO CÓDIGO RESPONSAVÉL POR: PEGAR O TOKEN / AUTENTICAR / LOGAR #########################################
############################################################################################################################################################################

# CARREGAR VARIÁVEIS DO ARQUIVO JSON
config_path = os.path.join(r'C:\Users\atila.silva.ECDS\Desktop\Visual Studio\Api Zabbix', 'config.json')
with open(config_path, 'r') as file:
    config = json.load(file)

# VARIÁVEIS DE CONFIGURAÇÃO
username = config['username']
password = config['password']
url = config['url']

headers = {'Content-Type': 'application/json'}

# FUNÇÃO QUE SOLICITA A API DO ZABBIX O BEARER TOKEN 
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

# AUTENTICAN O USUÁRIO
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

############################################################################################################################################################################
    ######################################## FIM DA PARTE DO CÓDIGO RESPONSAVÉL POR: PEGAR O TOKEN / AUTENTICAR / LOGAR #########################################
############################################################################################################################################################################


############################################################################################################################################################################
    ############################ INICIO DA PARTE DO CÓDIGO RESPONSAVÉL POR: UTILIZAR OS METÓDOS DA API DO ZABBIX E RECEBER AS INFORMAÇÕES #############################
############################################################################################################################################################################

# PARAMETROS DO METODO DA API UTILIZADO

api_params = {
        "filter": {
        "name": {
        "value": ""
      }
    }       
},

# FAZ A REQUISIÇÃO APONTANDO O METODO + OS PARAMETROS + O BEARER TOKEN
api_request = make_request('hostgroup.get', api_params, auth_token)

# VERIFICA A RESPOSTA IMPRIME O RESULTADO / TRATA OS POSSÍVEIS ERROS E IMPRIME OS MESMOS
if 'result' in api_request:
    result_list = api_request['result']
    if debug:
        print(json.dumps(result_list, indent=4))  # Imprime todos os resultados em formato JSON para debug
    else:
        for host in result_list:
            print(f"Nome: {host['name']}")
            print(f"UUID: {host['uuid']}")
            print(f"GROUP ID: {host['groupid']}")
            print('----')
else:
    print('Erro na solicitação: ' + str(api_request))
    if 'error' in api_request:
        print('Detalhes do erro: ' + str(api_request['error']))

############################################################################################################################################################################
    ############################## FIM DA PARTE DO CÓDIGO RESPONSAVÉL POR: UTILIZAR OS METÓDOS DA API DO ZABBIX E RECEBER AS INFORMAÇÕES ###############################
############################################################################################################################################################################
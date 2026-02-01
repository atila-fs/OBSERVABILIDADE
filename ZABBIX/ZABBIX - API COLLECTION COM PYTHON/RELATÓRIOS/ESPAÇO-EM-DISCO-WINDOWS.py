############################################################################################################################################################################
    ################################################################### BLOCO DE CONFIGURAÇÃO ##########################################################################
############################################################################################################################################################################

# IMPORTA OS METODOS NECESSÁRIOS E SUAS RESPECTIVAS BIBLIOTECAS
import requests
import json
import os

# ATIVA OU DESATIVA O MODO DEBUG
debug = True

# ATIVA OU DESATIVA A GRAVAÇÃO EM ARQUIVO
write_to_file = False
output_file_path = 'windows_servers_zbx_report.txt'

############################################################################################################################################################################
    ####################################################### CAMPO DE FUNÇÕES PARA TRABALHAR A SAIDA DOS DADOS ##########################################################
############################################################################################################################################################################

# FUNÇÃO PARA TRABALHAR A AMOSTRAGEM DOS DADOS DE BYTES PARA GIGABYTES
def bytes_to_gb(bytes_value):
    return bytes_value / (1024 ** 3)

# FUNÇÃO PARA ESCREVER SAÍDA EM ARQUIVO
def write_output_to_file(output):
    with open(output_file_path, 'w') as file:
        file.write(output)

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

# AUTENTICANDO O USUÁRIO
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

# Função para obter dados de `item.get` com base em uma chave específica
def get_item_data(key):
    api_params = {
        "output": "extend",
        "groupids": "93",      # PARA BUSCAR O DADO DE OUTROS HOSTSGROUPS ESPECIFICOS BASTA ALTERAR ESSE CAMPO COM O ID DO RESPECTIVO HOST GROUP (OBS: PARA PEGAR O ID DO HOSTGROUP É POSSIVEL FAZER COM O SCRIPT DO METODO hosgroup_get.py )
        "search": {
            "key_": key,
        },
        "sortfield": "name"
    }
    return make_request('item.get', api_params, auth_token)

# Função para obter detalhes dos hosts
def get_host_details(hostids):
    host_params = {
        "output": ["hostid", "name"],
        "hostids": list(hostids)
    }
    host_request = make_request('host.get', host_params, auth_token)
    return {host['hostid']: host['name'] for host in host_request['result']}

# Discos para coletar informações
discos = [f"{chr(drive)}:" for drive in range(ord('C'), ord('U'))]

# Dicionários para armazenar dados dos discos
total_data = {}
used_data = {}

# Coletar dados de cada disco
for disco in discos:
    total_key = f"vfs.fs.size[{disco},total]"
    used_key = f"vfs.fs.size[{disco},free]"
    
    total_data[disco] = get_item_data(total_key)
    used_data[disco] = get_item_data(used_key)

# Verifica a resposta e imprime o resultado / trata os possíveis erros
output = ""
data_dict = {}

# Coleta todos os hostids
hostids = set()
for disco in discos:
    if 'result' in total_data[disco]:
        hostids.update({item['hostid'] for item in total_data[disco]['result']})

hostnames = get_host_details(hostids)

# Consolida os dados
for disco in discos:
    if 'result' in total_data[disco] and 'result' in used_data[disco]:
        total_items = total_data[disco]['result']
        used_items = used_data[disco]['result']
        
        for item in total_items:
            hostid = item['hostid']
            if hostid not in data_dict:
                data_dict[hostid] = {}
            if disco not in data_dict[hostid]:
                data_dict[hostid][disco] = {}
            data_dict[hostid][disco]['total'] = item.get("lastvalue")
        
        for item in used_items:
            hostid = item['hostid']
            if hostid in data_dict and disco in data_dict[hostid]:
                data_dict[hostid][disco]['used'] = item.get("lastvalue")

# Gera a saída
for hostid, discos in data_dict.items():
    hostname = hostnames.get(hostid, "Unknown")
    output += f"Hostname: {hostname}\n"
    for disco, values in discos.items():
        total_gb = bytes_to_gb(float(values.get('total', 0)))
        used_gb = bytes_to_gb(float(values.get('used', 0)))
        free_gb = total_gb - used_gb
        
        output += f"Disco: {disco}\n"
        output += f"  Espaco Total: {total_gb:.2f} GB\n"
        output += f"  Espaco Utilizado: {used_gb:.2f} GB\n"
        output += f"  Espaco Livre: {free_gb:.2f} GB\n"
        output += '----\n'
    output += '====\n'

############################################################################################################################################################################
    ############################## FIM DA PARTE DO CÓDIGO RESPONSAVÉL POR: UTILIZAR OS METÓDOS DA API DO ZABBIX E RECEBER AS INFORMAÇÕES ###############################
############################################################################################################################################################################

# IMPRIME OU GRAVA A SAÍDA
if write_to_file:
    write_output_to_file(output)
else:
    print(output)
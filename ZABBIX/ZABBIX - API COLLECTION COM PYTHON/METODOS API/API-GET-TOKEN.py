import requests
import urllib3

# Desabilitar os avisos de verificação do certificado SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = 'https://[IP_ADDRESS]/oauth2/token'
client_id = 'atila'
client_secret = '<senha>'
id_token = '116ac4e3-4db8-a910-0534-b54ee060a764'

data = {
    'grant_type': 'urn:ietf:params:oauth:grant-type:token-exchange',
    'subject_token': id_token,
    'subject_token_type': 'urn:ietf:params:oauth:token-type:id_token',
}

try:
    response = requests.post(url, verify=False, data=data, auth=(client_id, client_secret))
    response.raise_for_status()  # Verifica se ocorreu um erro HTTP

    if response.status_code == 200:
        access_token = response.json()['access_token']
    else:
        print('Erro:', response.text)
except Exception as e:
    print('Erro durante a solicitação:', str(e))


    storageapi
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = 'https://<pure_ip>/api/2.23/alerts'
access_token = '<token>'

headers = {
    'Authorization': f'Bearer {access_token}'
}

params = {
    'limit': 10,  # Número máximo de alertas retornados
    'filter': 'severity >= warning',  # Filtra alertas com severidade igual ou superior a "warning"
    'sort': 'created-at',  # Ordena os alertas por data de criação
    'total_item_count': True  # Inclui o total_item_count na resposta
}

try:
    response = requests.get(url, verify=False, headers=headers, params=params)
    response.raise_for_status()  # Verifica se ocorreu um erro HTTP

    if response.status_code == 200:
        alerts = response.json()['items']
        total_count = response.json()['total_item_count']
        
        print('Total de alertas:', total_count)
        print('Lista de alertas:')
        for alert in alerts:
            print('ID:', alert['id'])
            print('Severidade:', alert['severity'])
            print('Descrição:', alert['description'])
            print('---')
    else:
        print('Erro:', response.text)
except Exception as e:
    print('Erro durante a solicitação:', str(e))

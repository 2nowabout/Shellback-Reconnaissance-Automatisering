import requests


def send_message_post(url, data):
    url = 'http://localhost:8002/' + url
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print('JSON data was successfully sent to the REST API.')
    else:
        print('Failed to send JSON data to the REST API.')


def send_message_get(url):
    ip = requests.get('https://checkip.amazonaws.com').text.strip()
    url = 'http://localhost:8002/' + url + ip
    response = requests.get(url)
    if response.status_code == 200:
        print('get was successfully sent to the REST API.')
    else:
        print('Failed to send to the REST API.')

import json
import requests
def sendMessage(data):
    url = 'http://example.com/api/endpoint'
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print('JSON data was successfully sent to the REST API.')
    else:
        print('Failed to send JSON data to the REST API.')
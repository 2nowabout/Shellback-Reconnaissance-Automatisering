import json
import os

import requests
from dotenv import load_dotenv

baseurl = ''
company_name = ''

def send_message_post(url, data):
    setup()
    url = baseurl + url
    json_object = json.load(data)
    addcompany = {"companyname":company_name}
    json_object.update(addcompany)
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print('JSON data was successfully sent to the REST API.')
    else:
        print('Failed to send JSON data to the REST API.')


def send_message_get(url):
    setup()
    ip = requests.get('https://checkip.amazonaws.com').text.strip()
    url = baseurl + url + ip
    response = requests.get(url)
    if response.status_code == 200:
        print('get was successfully sent to the REST API.')
    else:
        print('Failed to send to the REST API.')

def setup():
    global baseurl
    global company_name
    load_dotenv()
    baseurl = os.getenv("BASE_URL")
    company_name = os.getenv("COMPANY_NAME")



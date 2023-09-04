import json
import os

import requests
from dotenv import load_dotenv

baseurl = ''
token = ''

def send_message_post(url, data):
    setup()
    url = baseurl + url
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print('JSON data was successfully sent to the REST API.')
    else:
        print('Failed to send JSON data to the REST API.')
        raise ConnectionError


def send_message_get(url):
    setup()
    ip = requests.get('https://checkip.amazonaws.com').text.strip()
    url = baseurl + url + ip
    response = requests.get(url)
    if response.status_code == 200:
        print('get was successfully sent to the REST API.')
    else:
        print('Failed to send to the REST API.')
        raise ConnectionError

def setup():
    global baseurl
    global token
    load_dotenv()
    baseurl = os.getenv("BASE_URL")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    credentials = {
        "username": username,
        "password": password
    }

    # Define the authentication endpoint
    auth_endpoint = f"{baseurl}/login"  # Replace with the actual authentication endpoint

    try:
        # Send a POST request to authenticate and receive a token
        response = requests.post(auth_endpoint, json=credentials)

        if response.status_code == 200:
            # Authentication successful, extract the token from the response JSON
            token = response.json().get("token")

            if token:
                print(f"Authentication successful. Received token: {token}")
            else:
                print("Token not found in the response.")
        else:
            print(f"Authentication failed with status code {response.status_code}: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")





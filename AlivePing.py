import json
import time

import requests

from Sender import send_message_post

ip = requests.get('https://checkip.amazonaws.com').text.strip()
print(ip)
json = json.loads('{"ipadress": "' + ip + '"}')
while 1:
    try:
        send_message_post("/alive", json)
    except Exception as e:
        print(e)
    time.sleep(5)

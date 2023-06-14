import time

import requests

from Sender import send_message_post

while 1:
    ip = requests.get('https://checkip.amazonaws.com').text.strip()
    print(ip)
    send_message_post("alive", '{"ipadress": "' + ip + '"}')
    time.sleep(60)

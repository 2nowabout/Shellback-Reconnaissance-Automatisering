import requests
import json

from Sender import send_message_post

ip = requests.get('https://checkip.amazonaws.com').text.strip()

print('{"type":5,"ipadress":"' + ip + '","value":"communication test"}')
json = json.loads('{"type":5,"ipadress":"' + ip + '","value":"communication test"}')

result = None
while result is None:
    try:
        result = send_message_post("addNotification", json)
    except Exception as e:
        print(e)
        pass

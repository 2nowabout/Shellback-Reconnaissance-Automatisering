import requests
import json

from Sender import send_message_post

ip = requests.get('https://checkip.amazonaws.com').text.strip()

print('{"type":5,"ipadress":"' + ip + '","value":"communication test"}')
json = json.loads('{"type":5,"ipadress":"' + ip + '","value":"communication test"}')


send_message_post("addNotification", json)

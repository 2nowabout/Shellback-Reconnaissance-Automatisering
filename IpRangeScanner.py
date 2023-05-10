import os
import socket
import json
from Sender import sendMessagePost
import requests


def count_lines(filename):
    with open(filename, 'r') as file:
        line_count = sum(1 for line in file)
    return line_count


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("8.8.8.8", 80))
tosplit = sock.getsockname()
ipadress = tosplit[0]
HOST = ipadress
sock.close()

array_of_ip = HOST.split(".")
print(array_of_ip)
ip = array_of_ip[0] + "."
ip = ip + array_of_ip[1] + "."
ip = ip + array_of_ip[2] + "."
ip = ip + "0/24"
os.system(
    "nmap -sn " + ip + " | awk '/Nmap scan/{gsub(/[()]/,\"\",$NF); print $NF > \"Resources/ipHack/ipAdressesToScan\"}'")

amountOfIps = count_lines("Resources/ipHack/ipAdressesToScan")
ip = requests.get('https://checkip.amazonaws.com').text.strip()
json = json.loads(
    '{"type":5,"ipadress":"' + ip + '","value":"ip range scan complete, "' + str(amountOfIps) + 'ips found"}')
sendMessagePost("addNotification", json)

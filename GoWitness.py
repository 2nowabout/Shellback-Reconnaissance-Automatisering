import os
import socket


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
ip = ip + "0" + "."
ip = ip + "0/24"

os.system("gowitness scan --cidr " + ip + " --threads 10")
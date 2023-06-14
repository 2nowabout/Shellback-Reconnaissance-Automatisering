import os
import time
import socket

from Sender import send_message_post

while 1:
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    send_message_post("alive", '{"ipadress": ' +IPAddr + '}')
    time.sleep(60)

import os
import time

from Sender import sendMessagePost

while 1:
    sendMessagePost("alive", '{"alive": true}')
    #stream = os.popen('nmap -p <port_number> 176.57.189.22')
    time.sleep(60)

import os
import time

from Sender import sendMessage

while 1:
    sendMessage('{"alive": true}')
    #stream = os.popen('nmap -p <port_number> 176.57.189.22')
    #time.sleep(60)

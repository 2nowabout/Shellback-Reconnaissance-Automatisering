import os
import time

from Sender import send_message_post

while 1:
    send_message_post("alive", '{"alive": true}')
    time.sleep(60)

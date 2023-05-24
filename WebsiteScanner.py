import os
import time
import threading
import shutil
import sys
import requests
import json

from Sender import send_message_post


# -------------------------------------Thread definition----------------------------------------------------------------

class my_thread(threading.Thread):  # thread definition updated in python 3.0
    def __init__(self, thread_id, threadName, ip):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.threadName = threadName
        self.ip = ip

    def run(self):
        print("Starting " + self.threadName)
        move_file(self.threadName, self.ip)
        print("Exiting " + self.threadName)


# ----------------------------------------------------------------------------------------------------------------------


approvedstart = False
threads = []
automated = False


# ---------------------------------------------Methodes------------------------------------------------------------------

def move_file(threadName, ip):  # scan def for threads to run
    print(threadName + " works")
    adjustedx = ip.replace("/", "_")  # cant write a file with a / in the name
    os.system(
        "sudo nikto -o " + adjustedx + ".txt -Format txt -Tuning x 6 -Option USERAGENT=Mozilla -h " + ip + " -ssl -C all")  # nikto scan on ip, Tuning 6 enables all except DOS scans
    shutil.copy(adjustedx + ".txt", 'Results/WebScanner/')  # copy file to the right place
    if os.path.exists(adjustedx + ".txt"):  # checking after copy if everything is oke
        os.remove(adjustedx + ".txt")  # deleting old file in the wrong location


def runscan():
    import json
    threadnumber = 1
    f = open("Resources/websiteScanner/ipToScan")  # reading file with ips in it to use
    f1 = f.readlines()
    if f1.__len__() > 0:
        for x in f1:
            while threading.active_count() > 4:  # dont go above 4 threads at the same time
                print("Website scanner max threads achived, waiting for space\n")
                time.sleep(10)
            thread = my_thread(1, "Thread-" + str(threadnumber), x)  # creating thread
            thread.start()
            threads.append(thread)  # add to pool
            threadnumber += 1

    ip = requests.get('https://checkip.amazonaws.com').text.strip()
    json = json.loads('{"type":5,"ipadress":"' + ip + '","value":"SMB scanning complete"}')
    send_message_post("addNotification", json)


# ----------------------------------------------------------------------------------------------------------------------


runscan()

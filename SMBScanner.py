import os
import threading
import time
import requests
import json

from Sender import send_message_post

# -------------------------------------Thread definition----------------------------------------------------------------

class my_thread(threading.Thread):  # thread definition updated in python 3.0
    def __init__(self, thread_id, name, adress, version):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.adress = adress
        self.version = version

    def run(self):
        print("Starting SMB " + self.name)
        if self.version == 1:
            run_smb_protocol_scan(self.adress)  #run_scan uitvoeren als main methode
        elif self.version == 2:
            run_smb2_scan(self.adress)
        print("Exiting SMB " + self.name)


# ----------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------Methodes------------------------------------------------------------------

def run_smb_protocol_scan(adress):  # scan def for threads to run
    stream = os.popen(
        'sudo nmap --script=smb-protocols -p 137,139,445 ' + adress)  # --script vulscan is a custom script that connects vuln databases to check
    output = stream.read()
    adressfordocument = adress.replace(".", "_")
    adressfordocument = str(adressfordocument) + "-Protocols"
    t = open("Results/SMBScan/" + adressfordocument + ".txt", "w+")  # make a text file with the name of the adress
    t.write(output)  # fill the text file
    t.close()

def run_smb2_scan(adress):  # scan def for threads to run
    stream = os.popen(
        'sudo nmap --script=smb2-security-mode -p 137,139,445 ' + adress)  # --script vulscan is a custom script that connects vuln databases to check
    output = stream.read()
    adressfordocument = adress.replace(".", "_")
    adressfordocument = str(adressfordocument) + "-SMB2"
    t = open("Results/SMBScan/" + adressfordocument + ".txt", "w+")  # make a text file with the name of the adress
    t.write(output)  # fill the text file
    t.close()

# ----------------------------------------------------------------------------------------------------------------------

# -------------------------------------------Normal code----------------------------------------------------------------

f = open("Resources/ipHack/ipAdressesToScan")  # get ip adresses from file
threads = []
threadnumber = 1
f1 = f.readlines()

for x in f1:
    while threading.active_count() > 10:  # dont go above 10 threads at the same time
        print("SMB Scanner max threads achived, waiting for space")
        time.sleep(10)
    thread = my_thread(1, "Thread-" + str(threadnumber), x, 1)  # creating thread
    threadnumber += 1
    thread2 = my_thread(1, "Thread-" + str(threadnumber), x, 1)
    thread.start()   # starten van thread. hier word de def run uitgevoerd van de thread
    thread2.start()
    threads.append(thread)  # add to pool
    threads.append(thread2)
    threadnumber += 1

f.close()
f1.clear()

ip = requests.get('https://checkip.amazonaws.com').text.strip()
json = json.loads('{"type":5,"ipadress":"' + ip + '","value":"SMB scanning complete"}')
send_message_post("/addNotification", json)
import os
import threading
import time
import json
import sys

import requests

from Sender import sendMessagePost

# -------------------------------------Thread definition----------------------------------------------------------------

class myThread(threading.Thread):  # thread definition updated in python 3.0
    def __init__(self, threadID, name, adress, version):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.adress = adress
        self.version = version

    def run(self):
        print("Starting NMAP " + self.name)
        run_scan(self.adress, self.name, self.version)  #run_scan uitvoeren als main methode
        print("Exiting NMAP " + self.name)


# ----------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------Methodes------------------------------------------------------------------

def run_scan(adress, threadName, version):  # scan def for threads to run
    stream = os.popen(
        'nmap -sV --script=vulscan/vulscan.nse --script-args vulscandb=cve.csv -T2 -v -Pn -A ' + adress)  # --script vulscan is a custom script that connects vuln databases to check
    output = stream.read()
    adressfordocument = adress.replace(".", "_")
    adressfordocument = str(adressfordocument)
    t = open("Results/NetworkScan/" + adressfordocument + ".txt", "w+")  # make a text file with the name of the adress
    t.write(output)  # fill the text file
    t.close()


# ----------------------------------------------------------------------------------------------------------------------

# -------------------------------------------Normal code----------------------------------------------------------------

f = open("Resources/ipHack/ipAdressesToScan")  # get ip adresses from file
threads = []
threadnumber = 1
f1 = f.readlines()
version = 0

#for setting in settings:
#    if setting[0] != "#":    # skippen door alle lijnen van het document dat begint met een # voor comments
#        if setting.__contains__("scansetting="):    # zoeken naar de juiste scansetting in de file
#            version = int(setting.split("=")[1])

for x in f1:
    while threading.active_count() > 10:  # dont go above 10 threads at the same time
        print("Network scanner max threads achived, waiting for space\n")
        time.sleep(10)
    thread = myThread(1, "Thread-" + str(threadnumber), x, version)  # creating thread
    thread.start()   # starten van thread. hier word de def run uitgevoerd van de thread
    threads.append(thread)  # add to pool
    threadnumber += 1

f.close()
f1.clear()

ip = requests.get('https://checkip.amazonaws.com').text.strip()
json = json.loads('{"type":5,"ipadress":"' + ip + '","value":"nmap vulscan complete"}')
sendMessagePost("addNotification", json)


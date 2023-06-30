import os
import re
import threading
import time
import json
from bs4 import BeautifulSoup

import requests

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
        print("Starting NMAP " + self.name)
        run_scan(self.adress)  #run_scan uitvoeren als main methode
        print("Exiting NMAP " + self.name)


# ----------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------Methodes------------------------------------------------------------------

def get_cve_score(cve_id):
    url = f"https://nvd.nist.gov/vuln/detail/{cve_id}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    cvss_link = soup.find("a", id="Cvss2CalculatorAnchor")
    try:
        cvss_score = cvss_link.text.strip().split()[0]
    except:
        return 0
    return cvss_score

def extract_cve_ids(scan_report):
    cve_ids = re.findall(r"\[CVE-\d+-\d+\]", scan_report)
    return cve_ids

def run_scan(adress):  # scan def for threads to run
    stream = os.popen(
        'nmap -sV --script=vulscan/vulscan.nse --script-args vulscandb=cve.csv -T2 -v -Pn -A ' + adress)  # --script vulscan is a custom script that connects vuln databases to check
    output = stream.read()
    cve_ids = extract_cve_ids(output)
    ip = requests.get('https://checkip.amazonaws.com').text.strip()
    for cve_id in cve_ids:
        score = get_cve_score(cve_id)
        if score == 0:
            continue
        jsonstring = ""
        if float(score) < 4.0:
            jsonstring = '{ "type":1,"ipadress":"' + ip + '","value":"CVE found, CVE Score: ' + score + '"}'
        elif 3.9 < float(score) < 7.0:
            jsonstring = '{ "type":2,"ipadress":"' + ip + '","value":"CVE found, CVE Score: ' + score + '"}'
        elif 6.9 < float(score) < 9.0:
            jsonstring = '{ "type":3,"ipadress":"' + ip + '","value":"CVE found, CVE Score: ' + score + '"}'
        elif 8.9 < float(score):
            jsonstring = '{ "type":4,"ipadress":"' + ip + '","value":"CVE found, CVE Score: ' + score + '"}'
        json = json.loads(jsonstring)
        send_message_post("addNotification", json)
        print(f"CVE ID: {cve_id}, Score: {score}")
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

for x in f1:
    while threading.active_count() > 10:  # dont go above 10 threads at the same time
        print("Network scanner max threads achived, waiting for space")
        time.sleep(10)
    thread = my_thread(1, "Thread-" + str(threadnumber), x, version)  # creating thread
    thread.start()   # starten van thread. hier word de def run uitgevoerd van de thread
    threads.append(thread)  # add to pool
    threadnumber += 1

f.close()
f1.clear()

ip = requests.get('https://checkip.amazonaws.com').text.strip()
json = json.loads('{"type":5,"ipadress":"' + ip + '","value":"nmap vulscan complete"}')
send_message_post("addNotification", json)


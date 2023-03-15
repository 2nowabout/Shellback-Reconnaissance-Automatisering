import os
import time
import threading
import shutil
import sys


# -------------------------------------Thread definition----------------------------------------------------------------

class myThread(threading.Thread):  # thread definition updated in python 3.0
    def __init__(self, threadID, threadName, ip):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.threadName = threadName
        self.ip = ip

    def run(self):
        print("Starting " + self.threadName)
        crack_password(self.threadName, self.ip)
        print("Exiting " + self.threadName)


# ----------------------------------------------------------------------------------------------------------------------


approvedstart = False
threads = []
automated = False


# ---------------------------------------------Methodes------------------------------------------------------------------

def crack_password(threadName, ip):  # scan def for threads to run
    print(threadName + " works")
    adjustedx = ip.replace("/", "_") # cant write a file with a / in the name
    os.system("sudo nikto -o " + adjustedx + ".txt -Format txt -Tuning x 6 -Option USERAGENT=Mozilla -h " + ip + " -ssl -C all") # nikto scan on ip, Tuning 6 enables all except DOS scans
    shutil.copy(adjustedx + ".txt", 'Results/WebScanner/') # copy file to the right place
    if os.path.exists(adjustedx + ".txt"): # checking after copy if everything is oke
        os.remove(adjustedx + ".txt") # deleting old file in the wrong location

def runScan():
    threadnumber = 1
    f = open("Resources/websiteScanner/ipToScan")  # reading file with ips in it to use
    f1 = f.readlines()
    for x in f1:
        while threading.activeCount() > 4:  # dont go above 4 threads at the same time
            print("max threads achived, waiting for space")
            time.sleep(10)
        thread = myThread(1, "Thread-" + str(threadnumber), x)  # creating thread
        thread.start()
        threads.append(thread)  # add to pool
        threadnumber += 1
# ----------------------------------------------------------------------------------------------------------------------




if(sys.argv[1] == "1"):
    automated = True
if not automated:
    print("Website scanner activated!")
    print("Before starting make sure you put the ip in the specific folder!")
    print("this scan can take around an hour per ip so hold tight!")
    start = input("are you ready? (yes/no): ")
    start = start.lower()
    if start == "yes":
        approvedstart = True
    if approvedstart:
        runScan()
elif automated:
    runScan()


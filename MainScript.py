import os
import threading
import time
import sys
import socket
import json

PORT = 8192
HOST = ''
data = []
BUFFER_SIZE = 1

# -------------------------------------Thread definition----------------------------------------------------------------

class myThread(threading.Thread):  # thread definition updated in python 3.0
    def __init__(self, threadID, name, command):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.command = command

    def run(self):
        print("Starting " + self.name)
        run_scan(self.command)
        print("Exiting " + self.name)


def listToString(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        if ele != ";":
            str1 += ele

    # return string
    return str1


def server_socket():
    HOST = ''
    while HOST == '':
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        tosplit = sock.getsockname()
        ipadress = tosplit[0]
        HOST = ipadress
        sock.close()
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        soc.bind((HOST, PORT))
    except socket.error as message:
        print('Bind failed. Error Code : '
              + str(message[0]) + ' Message '
              + message[1])
        sys.exit()
    soc.listen(3)

    while 1:  # Accept connections from multiple clients
        conn, addr = soc.accept()
        while 1:  # Accept multiple messages from each client
            buffer = conn.recv(BUFFER_SIZE)
            buffer = buffer.decode()
            if buffer == ";":
                conn.close()
                print(listToString(data))
                break
            elif buffer:
                data.append(buffer)
            else:
                break



def execute_command(command):
    try:
        json_object = json.load(command)
    except:
        print("command was not a json file")
        return

    match json_object["command"]:
        case "start":
            automated_scan()
        case "update_settings":
            settings = json_object["settings"]
            settings

# ---------------------------------------------Methodes------------------------------------------------------------------

def clear():
    os.system("clear")

def run_scan(command):  # scan def for threads to run
    os.system(command)


def automated_scan():
    #Gathering information first:
    os.system("sudo python3 IpRangeScanner.py")




    threads = []
    threadnumber = 1
    stillWorking = True
    commands = []
    commands.append("sudo python3 NetworkScanner.py 1")
    commands.append("sudo python3 WebsiteScanner.py 1")
    for i in commands:
        thread = myThread(threadnumber, "Thread-" + str(threadnumber), i)  # creating thread
        thread.start()
        threads.append(thread)  # add to pool
        threadnumber = threadnumber + 1

    while stillWorking:
        alive = False
        # clear()
        # whatThread = 0
        # for i in threads:
        #     whatThread = whatThread + 1
        #     if i.is_alive():
        #         alive = True
        #         print("thread " + str(whatThread) + " is Working...")
        #     elif not i.is_alive():
        #         print("thread " + str(whatThread) + " is Done")
        if not alive:
            stillWorking = False

# ----------------------------------------------------------------------------------------------------------------------


server_socket()


# if fullanswer == "yes":
#     PasswordCracking = True
#     NetworkScanner = True
#     WebsiteScanner = True
#     print("DONT FORGET TO FILL AUTOMATIONSETTINGS FILE FOR THIS:")
#     fullatomation = input("Enable full automation? yes/no (make sure the full automation file is filled)")
#     if fullatomation == "yes":
#         FullAutomation = True
#         runtester = input("do you want to check the input files if everything is correct? yes/no")
#         if (runtester == "yes"):
#             os.system("python3 FileTester.py")
#             pause = input("if everything is correct press enter, otherwise cancel and adjust settings")
#
# if FullAutomation:
#     automated_scan()
#
# if not FullAutomation:
#     start_all_scan_normal(PasswordCracking, NetworkScanner, WebsiteScanner)

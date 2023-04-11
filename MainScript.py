import json
import os
import socket
import sys
import threading

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


# ---------------------------------------------Methodes------------------------------------------------------------------


def execute_command(command):
    # remove all the extra parameters from the socket connection and only work with json file
    foundbegin = False
    execute = ""
    for i in command:
        if (i == "{"):
            foundbegin = True
        if (foundbegin):
            execute += i

    # load string to json
    try:
        json_object = json.loads(execute)
    except:
        print("command was not a json file")
        return

    # read command from json and execute appropriately
    match json_object["command"]:
        case "start":
            automated_scan()
        case "update_settings":
            settings = json_object["settings"]
            update_settings(settings)
        case _:
            return

def update_settings(json):
    websiteadresses = json["websites"]
    f = open("Resources/websiteScanner" + "ipToScan" + ".txt", "w+")
    f.write(json.dumps(websiteadresses))



def listToString(s):
    # initialize an empty string
    str1 = ""
    s = s.decode('utf-8')
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

    message = ''
    while 1:  # Accept connections from multiple clients
        conn, addr = soc.accept()
        while 1:  # Accept multiple messages from each client
            # buffer = conn.recv(BUFFER_SIZE)
            # buffer = buffer.decode()
            data = conn.recv(1024)
            if not data:
                conn.close()
                data.clear()
                buffer = ""
                break
            else:
                execute_command(listToString(data))
                conn.send(b'''HTTP/1.0 200 OK
Content-Type: text/plain

Connection successful

''')
                conn.close()


def clear():
    os.system("clear")


def run_scan(command):  # scan def for threads to run
    os.system(command)


def automated_scan():
    # Gathering information first:
    print("executing ip range scan")
    os.system("sudo python3 IpRangeScanner.py")
    print("scan done")
    threads = []
    threadnumber = 1
    stillWorking = True
    commands = []
    commands.append("sudo python3 NetworkScanner.py")
    commands.append("sudo python3 SMBScanner.py")
    commands.append("sudo python3 WebsiteScanner.py")
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
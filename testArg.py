import sys

print("number of arguments: ", len(sys.argv))
print("argument List: ", str(sys.argv))
if(sys.argv[1] == "1"):
    print("1 DETECTED")

test = "scansetting=1"
print(test.split("=")[1])

commands = []
commands.append("sudo python3 PasswordCracker.py 1")
commands.append("sudo python3 NetworkScanner.py 1")
commands.append("sudo python3 WebsiteScanner.py 1")
for i in commands:
    print(i)
print("Tester started")

f = open("Resources/ipHack/ipAdressesToScan")
f1 = f.readlines()
count = 0
for x in f1:
    count = count + 1
print("ipadresses found to scan: " + str(count))

f2 = open("Resources/passwordCrack/Usernames")
f2f = f2.readlines()
count2 = 0
for x in f2f:
    count2 = count2 + 1
print("usernames found to test: " + str(count2))

f3 = open("Resources/websiteScanner/ipToScan")
f3f = f3.readlines()
count3 = 0
for x in f3f:
    count3 = count3 + 1
print("Websites found to scan: " + str(count3))

print("Settings:")
settingsfull = open("Resources/fullAutomated/automationSettings")
settings = settingsfull.readlines()
for setting in settings:
    if setting[0] != "#":
        print(setting)


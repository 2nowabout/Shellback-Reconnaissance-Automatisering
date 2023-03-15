
import random
import os


again = True
os.system("main.py")
while again is True:

    print("Welcome to Geuss the number!")
    suceeded = False
    while suceeded is False:
        try:
            number = input("How hard would you like the game to be? (1-10)")
            int(number)
            suceeded = True
        except:
            print("thats not an int, try again-")
    difficulty = int(number) * 10
    numbertogeuss = random.randint(1, int(difficulty))
    gotit = False
    while gotit is False:
        answer = input("what is your geuss?")
        if(int(answer) == numbertogeuss):
            print("Correct! good job!")
            gotit = True
        else:
            print("Incorrect!")
            if(int(answer) > numbertogeuss):
                print("the number is smaller!")
            else:
                print("the number is bigger!")
    againanswer = input("Want to true again? (yes/no)")
    if(againanswer == "yes"):
        again = True
    else:
        again = False

print("See you next time!")



#This is a guess number game
import random

yourName = input('Hello, what is your name? ')
print('Well, '+yourName+', I am thinking of a number between 1 and 20. ')
secretNumber = random.randint(1, 20)

while True:
    print('Take a guess')
    yourNumber = int(input())

    if (yourNumber==secretNumber) :
        print('Good guess, great job!')
        break
    elif (yourNumber>secretNumber) :
        print('Your guess is too high')
    else : 
        print('Your guess is too low')





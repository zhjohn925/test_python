import random
yourName = input("Hello, what is your name?")
print("Well, "+yourName+", I am thinking of a number between 1 and 20. ")
secret = random.randint(1, 20)

while True:
  print('Take a guess')
  yourNumber = int( input() ) 
  if (yourNumber == secret):
     print('Good guess, great job!')
     break
  elif (yourNumber > secret):
     print('your guess is too high')
  else :
     print('your guess is too low') 

#+-random-------------------------------------+
#|   functions      10           20           |
#|   1. randint(small_number, large_number)   |
#|   2.  ......                               | 
#+--------------------------------------------+
#input("string")
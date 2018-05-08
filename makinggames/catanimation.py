import pygame, sys
from pygame.locals import *

# https://www.pygame.org/docs/

pygame.init()

#frames per second
#By calling .tick() below, setting it to a lower value would make 
#the program run slower; setting it to a higher value would make 
#the program run faster.
FPS = 30  

#.time.Clock() object can help us make sure the program
#runs at a certain maximum FPS; this Clock object will 
#ensure that our game programs don't run too fast by putting
#in small pauses on each iteration of the game loop.
#If we did not have these pauses, our game program would run 
#as fast as the computer could run it. 
#A call to the tick() method of a Clock object in the game loop
#can make sure the game runs at the same speed no matter how fast
#of a computer it runs on.
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((400,300), 0, 32)
pygame.display.set_caption('Animation')

WHITE = (255, 255, 255)
#catImg is a Surface object
catImg = pygame.image.load('cat.png')
catx = 10
caty = 10
direction = 'right'

while True:
   DISPLAYSURF.fill(WHITE)
   if direction == 'right':
      catx += 5
      if catx==280:
         direction = 'down'
   elif direction == 'down':
      caty += 5
      if caty == 220:
         direction = 'left'
   elif direction == 'left':
      catx -= 5
      if catx == 10:
         direction = 'up'
   elif direction == 'up':
      caty -= 5
      if caty == 10:
         direction = 'right'
  
   #.blit() copies catImg (a Surface object) into 
   #DISPLAYSURF (it is also a Surface object) with top left
   #corner at (catx, caty)
   DISPLAYSURF.blit(catImg, (catx, caty))
   
   for event in pygame.event.get():
      if event.type == QUIT:
         pygame.quit()
         sys.exit()
         
   pygame.display.update()
   
   #This method should be called once per frame. It will compute 
   #how many milliseconds have passed since the previous call.
   #If you pass the optional framerate argument the function will delay
   #to keep the game running slower than the given ticks per second. 
   #This can be used to help limit the runtime speed of a game. 
   #By calling Clock.tick(40) once per frame, the program will never run 
   #at more than 40 frames per second.
   fpsClock.tick(FPS)
   
          
   
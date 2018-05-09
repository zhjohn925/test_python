import pygame, sys, random
from pygame.locals import *

# https://www.pygame.org/docs/

def terminate():
   pygame.quit()
   sys.exit()
   
def checkForQuit():
   for event in pygame.event.get(QUIT):
      terminate()
   for event in pygame.event.get(KEYUP):
      if event.key == K_ESCAPE:
         terminate()
   #place other events at the end of the event queue      
   pygame.event.post(event)

#return a board with titles in the solved state
#for example, if BOARDWIDTH=BOARDHEIGHT=3,
#then board=[[1,4,7],[2,5,8],[3,6,None]]
def getStartingBoard():
   counter = 1
   board = []
   for x in range(BOARDWIDTH):
      column = []
      for y in range(BOARDHEIGHT):
         column.append(counter)
         counter += BOARDWIDTH
      board.append(column)
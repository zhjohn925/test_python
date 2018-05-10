import pygame, sys
from pygame.locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400,300))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BORDERCOLOR = (99,99,99)

while True:
   DISPLAYSURF.fill(BLUE)
   
   pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (20, 20, 100, 100), 4)
   
   for event in pygame.event.get():
      if event.type == QUIT:
         pygame.quit()
         sys.exit()
   pygame.display.update()



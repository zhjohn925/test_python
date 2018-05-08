import pygame, sys
from pygame.locals import *

# https://www.pygame.org/docs/

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400,300))
pygame.display.set_caption('Hello World!')

WHITE = (255, 255, 255)
GREEN = (0,  255, 0)
BLUE = (0, 0, 128)

fontObj = pygame.font.Font('freesansbold.ttf', 32)

#.render() returns a Surface object
#True (antialias argument), if True the characters will have smooth edges.
#GREEN is font color; BLUE is background color;
#if no background color is specified, the text will be transparent.
textSurfaceObj = fontObj.render('Hello world!', True, GREEN)  #, BLUE)

#Surface.get_rect() returns a Rect object
textRectObj = textSurfaceObj.get_rect()
#Set Rect member variable (center)
textRectObj.center = (200, 150)

while True:
   DISPLAYSURF.fill(WHITE)
   
   #the second parameter is dest in .blit()
   #which is textRectObj in here.
   #Dest can either be pair of coordinates representing the upper left corner
   #of the source. A Rect can also be passed as the destination and the topleft 
   #corner of the rectangle will be used as the position for the blit. 
   #The size of the destination rectangle does not effect the blit.
   DISPLAYSURF.blit(textSurfaceObj, textRectObj)
   
   for event in pygame.event.get():
      if event.type == QUIT:
         pygame.quit()
         sys.exit()
   pygame.display.update()
   
   
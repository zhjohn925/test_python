import pygame, sys, random
from pygame.locals import *

# https://www.pygame.org/docs/

BOARDWIDTH = 4
BOARDHEIGHT = 4

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def main():
   global FPSCLOCK
   pygame.init()


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
    board = []
    for x in range(BOARDWIDTH):
       column = []
       counter = x+1
       for y in range(BOARDHEIGHT):
          column.append(counter)
          counter += BOARDWIDTH
       board.append(column)
    #the last one as blank   
    board[BOARDWIDTH-1][BOARDHEIGHT-1] = None
    return board

#return which tile is blank (None)
def getBlankPosition(board):
	for x in range(BOARDWIDTH):
		for y in range(BOARDHEIGHT):
			if (board[x][y]==None):
				return(x,y)

def makeMove(board, move):
	x, y = getBlankPosition(board)
	if move==UP:
		board[x][y] = board[x][y+1]
		board[x][y+1] = None
	elif move==DOWN:
		board[x][y] = board[x][y-1]
		board[x][y-1] = None
	elif move==LEFT:
		board[x][y] = board[x+1][y]
		board[x+1][y] = None
	elif move==RIGHT:
		board[x][y] = board[x-1][y]
		board[x-1][y] = None					 	



if __name__ == '__main__':
	main()

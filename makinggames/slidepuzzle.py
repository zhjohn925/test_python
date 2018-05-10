# Slide Puzzle
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Creative Commons BY-NC-SA 3.0 US

import pygame, sys, random
from pygame.locals import *

# https://www.pygame.org/docs/

BOARDWIDTH = 4
BOARDHEIGHT = 4
TILESIZE = 80
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 30
BLANK = None

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRIGHTBLUE = (0, 50, 255)
DARKTURQUOISE = (3, 54, 73)
GREEN = (0, 204, 0)

BGCOLOR = DARKTURQUOISE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20
BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, \
           RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Slide Puzzle')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    # return Surface, Rectangle covering the surface
    RESET_SURF, RESET_RECT = makeText('Reset', TEXTCOLOR, TILECOLOR, WINDOWWIDTH-120, WINDOWHEIGHT-90)
    NEW_SURF, NEW_RECT = makeText('New Game', TEXTCOLOR, TILECOLOR, WINDOWWIDTH-120, WINDOWHEIGHT-60)
    SOLVE_SURF, SOLVE_RECT = makeText('Solve', TEXTCOLOR, TILECOLOR, WINDOWWIDTH-120, WINDOWHEIGHT-30)
    mainBoard, solutionSeq = generateNewPuzzle(80)
    SOLVEDBOARD = getStartingBoard()
    allMoves = []
    while True: 
        slideTo = None
        msg = ''
        if mainBoard == SOLVEDBOARD:     
            msg = 'Solved!'
        # one more effect for this call:    
        # I noticed the tile can be not alligned after animation. drawBoard() here 
        # re-draw the board make the tiles align up again    
        drawBoard(mainBoard, msg)
        checkForQuit()
        # event handling loop
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                tileX, tileY = getTileClicked(mainBoard, event.pos[0], event.pos[1])
                if (tileX, tileY) == (None, None):
                    # check if the user clicked on an option button 
                    if RESET_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, allMoves)
                        allMoves = []
                    elif NEW_RECT.collidepoint(event.pos):
                        mainBoard, solutionSeq = generateNewPuzzle(80)
                        allMoves = []
                    elif SOLVE_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, solutionSeq+allMoves)
                        solutionSeq = []
                        allMoves = []
                else:
                    # check if the user clicked on the tile next to blank
                    blankX, blankY = getBlankTile(mainBoard)
                    if tileX==blankX+1 and tileY==blankY:
                        slideTo = LEFT
                    elif tileX==blankX-1 and tileY==blankY:
                        slideTo = RIGHT
                    elif tileX==blankX and tileY==blankY+1:
                        slideTo = UP
                    elif tileX==blankX and tileY==blankY-1:
                        slideTo = DOWN        
            elif event.type == KEYUP:
                # check if the user pressed a key to slide the tile
                if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
                    slideTo = LEFT
                elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                    slideTo = RIGHT
                elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                    slideTo = UP
                elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
                    slideTo = DOWN
        if slideTo:
            slideAnimation(mainBoard, slideTo, 'Click tile or press arrow keys to slide.', 8)
            makeMove(mainBoard, slideTo)
            # save the slide, to restore back if asked
            allMoves.append(slideTo)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


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

# return blank (None) tile
def getBlankTile(board):
	for x in range(BOARDWIDTH):
		for y in range(BOARDHEIGHT):
			if (board[x][y]==None):
				return(x,y)

# Update the tiles in board after moving ie. switch the moving tile with the Blank tile
# This function does not check if the move is valid
def makeMove(board, moveTile):
	x, y = getBlankTile(board)        # (0,0) +---------------------------------> x
	if moveTile==UP:                  #       |  (x,y)BLANK        (x,y)TILE 
		board[x][y] = board[x][y+1]   #       |          ---MoveUP-->  
		board[x][y+1] = None          #       |  (x,y+1)TILE       (x,y+1)BLANK   
	elif moveTile==DOWN:              #       y
		board[x][y] = board[x][y-1]
		board[x][y-1] = None
	elif moveTile==LEFT:
		board[x][y] = board[x+1][y]
		board[x+1][y] = None
	elif moveTile==RIGHT:
		board[x][y] = board[x-1][y]
		board[x-1][y] = None					 	

#  3 x 3 matrix (x has width, y has height)
#
#  board = [[1,4,7],[2,5,8],[3,6,None]]
#  
#  when blank in the first column (x=0), move RIGHT is invalid (no way to move Tile to the right);
#  when blank in the last column (x=2), move LEFT is invalid (no way to move Tile to the left)
#
#        x0   x1   x2    
#      +----+----+----+---- x
#  y0  |  1    2    3   //when blank in this row (y=0), move DOWN is invalid (no way to move down)       
#      +----+----+----+ 
#  y1  |  4    5    6
#      +----+----+----+
#  y2  |  7    8    9   //when blank in this row (y=2), move UP is invalid (no way to move up)
#      +----+----+----+
#      |
#      y
#  
def isValidMove(board, moveTile):
    x, y = getBlankTile(board)
    return (moveTile==UP and y != len(board[0])-1) or \
           (moveTile==DOWN and y != 0) or \
           (moveTile==LEFT and x != len(board)-1) or \
           (moveTile==RIGHT and x != 0)


# return a valid move but not repeated from the last move
def getRandomMove(board, lastMove=None):
    validMoves = [UP, DOWN, LEFT, RIGHT]
    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board,UP):
        validMoves.remove(UP)
    if lastMove == LEFT or not isValidMove(board,RIGHT):
        validMoves.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board,LEFT):
        validMoves.remove(LEFT)            
    return random.choice(validMoves)


# return left top coordinate of the given tile
# (tileX, tileY) of the first tile is (0, 0) 
def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX*TILESIZE) + (tileX-1)
    top = YMARGIN + (tileY*TILESIZE) + (tileY-1)
    return (left, top)  #tuple

# x,y is pixel coordinates
# returns tile being clicked
def getTileClicked(board, x, y):
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x,y):
                return (tileX, tileY)
    return (None, None)


def drawTile(tileX, tileY, number, adjx=0, adjy=0):
    left, top = getLeftTopOfTile(tileX, tileY)
    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left+adjx,top+adjy, TILESIZE, TILESIZE))
    # draw text (number) on a new Surface
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    # returns a new rectanle covering the entire Surface (textSurf)
    textRect = textSurf.get_rect()
    # set the rectanle center coordinates
    textRect.center = left+int(TILESIZE/2)+adjx, top+int(TILESIZE/2)+adjy
    # blit (copy) the text Surface to DISPLAYSURF at the textRect position
    DISPLAYSURF.blit(textSurf, textRect)

def makeText(text, color, bgcolor, top, left):
    # draw text on a new Surface (textSurf)
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    # returns a new rectanle covering the entire Surface (textSurf)
    textRect = textSurf.get_rect()
    # set the rectangle top left position
    textRect.topleft = (top, left)
    return (textSurf, textRect)

def drawBoard(board, message):
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        #draw the message
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            if board[tileX][tileY]:
                drawTile(tileX, tileY, board[tileX][tileY])
    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    # draw a rectangle frame (width=4) around the tiles
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left-5,top-5,width+11,height+11), 4)
    # .blit(source, dest): draw (copy) the Surface into the Rectangle 
    # area in DISPLAYSURF 
    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)            

def slideAnimation(board, direction, message, speed):
    blankX, blankY = getBlankTile(board)
    # The tile in (moveX, moveY) will be moved in the specified direction
    if (direction==UP):         #  +--------------> x
        moveX = blankX          #  |  blank   (y)   
        moveY = blankY+1        #  |  move_up (y+1)    
    elif (direction==DOWN):     #  y
        moveX = blankX
        moveY = blankY-1
    elif (direction==LEFT):
        moveX = blankX+1
        moveY = blankY
    elif (direction==RIGHT):
        moveX = blankX-1
        moveY = blankY
    # prepare the base surface
    drawBoard(board, message)
    # create a new copy of Surface
    baseSurf = DISPLAYSURF.copy()
    # draw a blank space over the moving tile on the baseSurf Surface
    # now there are two blank tiles back-to-back in this new Surface
    moveLeft, moveTop = getLeftTopOfTile(moveX, moveY)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))

    # animate the tile sliding over
    for i in range(0, TILESIZE, speed):
        checkForQuit()
        # put the Surface copy back to DISPLAYSURF
        DISPLAYSURF.blit(baseSurf, (0,0))
        if direction == UP:
            drawTile(moveX, moveY, board[moveX][moveY], 0, -i)
        if direction == DOWN:
            drawTile(moveX, moveY, board[moveX][moveY], 0, i)
        if direction == LEFT:
            drawTile(moveX, moveY, board[moveX][moveY], -i, 0)
        if direction == RIGHT:
            drawTile(moveX, moveY, board[moveX][moveY], i, 0)   
        pygame.display.update()
        FPSCLOCK.tick(FPS) 

def generateNewPuzzle(numSlides):
    sequence = []
    # create board matrix (BOARDWIDTH * BOARDHEIGHT) of tiles 
    # with number; one tile with None (blank)
    board = getStartingBoard()
    # draw solved board (ie. tiles in the right number order)
    drawBoard(board, '')
    # update portions of the screen for software displays
    # no argument means the entire screen
    pygame.display.update()
    # pause 500 milliseconds for effect
    pygame.time.wait(500)
    lastMove = None
    for i in range(numSlides):
        # return valid and not repeated move
        move = getRandomMove(board, lastMove)
        slideAnimation(board, move, 'Generating new puzzle ...', int(TILESIZE/3))
        # update the tiles in board with moving
        makeMove(board, move)
        sequence.append(move)
        lastMove = move
    return (board, sequence)


def resetAnimation(board, allMoves):
    # gets a copy of the list
    revAllMoves = allMoves[:]
    revAllMoves.reverse()
    for move in revAllMoves:
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == LEFT:
            oppositeMove = RIGHT
        elif move == RIGHT:
            oppositeMove = LEFT
        slideAnimation(board, oppositeMove, '', int(TILESIZE/2))
        # update the tiles in board with moving
        makeMove(board, oppositeMove)    


if __name__ == '__main__':
	main()

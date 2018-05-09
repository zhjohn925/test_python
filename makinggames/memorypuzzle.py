# Memory Puzzle
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys
from pygame.locals import *

FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 640 # size of window's width in pixels
WINDOWHEIGHT = 480 # size of windows' height in pixels
REVEALSPEED = 8 # speed boxes' sliding reveals and covers
BOXSIZE = 40 # size of box height & width in pixels
GAPSIZE = 10 # size of gap between boxes in pixels
BOARDWIDTH = 6 #10 # number of columns of icons
BOARDHEIGHT = 7 # number of rows of icons
assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined."


def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    pygame.display.set_caption('Memory Game')

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None # stores the (x, y) of the first box clicked.

    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(mainBoard)

    while True: # main game loop
        mouseClicked = False
        DISPLAYSURF.fill(BGCOLOR) # drawing the window
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mousex, mousey)

        if boxx != None and boxy != None:

            # The mouse is currently over a box.
            if not revealedBoxes[boxx][boxy]:
               drawHighlightBox(boxx, boxy)

            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                revealedBoxes[boxx][boxy] = True # set the box as "revealed"
                if firstSelection == None: # the current box was the first box clicked
                    firstSelection = (boxx, boxy)
                else: # the current box was the second box clicked
                    # Check if there is a match between the two icons.
                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)

                    if icon1shape != icon2shape or icon1color != icon2color:
                        # Icons don't match. Re-cover up both selections.
                        pygame.time.wait(1000) # 1000 milliseconds = 1 sec
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection [1]] = False
                        revealedBoxes[boxx][boxy] = False
                    elif hasWon(revealedBoxes): # check if all pairs found
                        gameWonAnimation(mainBoard)
                        pygame.time.wait(2000)

                        # Reset the board
                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False)

                        # Show the fully unrevealed board for a second.
                        drawBoard(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        # Replay the start game animation.
                        startGameAnimation(mainBoard)           
                    firstSelection = None # reset firstSelection variable

        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)


#############################################################
# [BOARDWIDTH * BOARDHEIGHT] matrix with element = val
#############################################################
def generateRevealedBoxesData(val):
   res = []
   for i in range(BOARDWIDTH):
      res.append([val]*BOARDHEIGHT)
   return res
   
#############################################################   
# Place icons into the board with all possible shapes, and
# two copies of each shape
#############################################################
def getRandomizedBoard():
   #filled with various shapes with colors 
   #with random order
   icons = []
   for color in ALLCOLORS:
      for shape in ALLSHAPES:
         icons.append((shape, color))   
   random.shuffle(icons) 
   #number of icons are needed to place into the board
   numOfIcons = int(BOARDWIDTH * BOARDHEIGHT/2)
   #throw away the extra shapes, and make two copies of each shape
   icons = icons[:numOfIcons] * 2
   #randomize the order
   random.shuffle(icons)
   
   #place the icons into the board
   board = []
   for x in range(BOARDWIDTH):
      column = []
      for y in range(BOARDHEIGHT):
         column.append(icons[0])
         del icons[0]
      board.append(column)
   return board      
   
########################################################################
#Split theList into a group of lists with size of groupSize (or less)
########################################################################
def splitIntoGroupOf(groupSize, theList):
   res = []
   #class range(start, stop[, step])
   for i in range(0, len(theList), groupSize):
      res.append(theList[i : i+groupSize])
   return res 
   
########################################################################
#Calculate left top pixel coordinates of the given box in the board
#col, row indicates the box's column & row in the board
########################################################################
def leftTopCoordinatesOfBox(col, row):
   leftX = col * (BOXSIZE+GAPSIZE) + XMARGIN
   topY  = row * (BOXSIZE+GAPSIZE) + YMARGIN
   return (leftX, topY)  #tuple


########################################################################
#get box column and row indice in the board per the given coordinates
########################################################################
def getBoxAtPixel(x, y):
   for col in range(BOARDWIDTH):
      for row in range(BOARDHEIGHT):
         left, top = leftTopCoordinatesOfBox(col, row)
         boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
         if boxRect.collidepoint(x, y):
            return (col, row)
   return (None, None)
   
########################################################################
#draw icon
########################################################################
def drawIcon(shape, color, col, row):
   quarter = int(BOXSIZE * 0.25)
   half = int(BOXSIZE * 0.5)
   left, top = leftTopCoordinatesOfBox(col, row)
   if shape == DONUT:
      pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
      pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
   elif shape == SQUARE:
      pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
   elif shape == DIAMOND:
      pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))
   elif shape == LINES:
      for i in range(0, BOXSIZE, 4):
         pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
         pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))
   elif shape == OVAL:
      pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))
      

#######################################################
#shape value and color
#x, y indicates row & column in the board matrix
#######################################################
def getShapeAndColor(board, x, y):
   #shape value for x, y is stored in board[x][y][0]
   #shape value for x, y is stored in board[x][y][1]
   return board[x][y][0], board[x][y][1]

#######################################################################
#boxes contains list of box row & col in the board matrix  
#coverage is length (in x) to cover up the box
#######################################################################
def drawBoxCovers(board, boxes, coverage):
   for box in boxes:
      #box is a list of row & col
      left,top = leftTopCoordinatesOfBox(box[0], box[1])
      #draw background in this box
      pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
      shape, color = getShapeAndColor(board, box[0], box[1])
      drawIcon(shape, color, box[0], box[1])  
      if coverage > 0:
         pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
         
   pygame.display.update()
   FPSCLOCK.tick(FPS)    
      
#######################################################################
#Do the box reveal animation
####################################################################### 
def revealBoxesAnimation(board, boxesToReveal):
   for coverage in range (BOXSIZE, (-REVEALSPEED)-1, -REVEALSPEED):
      drawBoxCovers(board, boxesToReveal, coverage)
      
#######################################################################
#Do the box cover animation
####################################################################### 
def coverBoxesAnimation(board, boxesToCover):
   for coverage in range (0, BOXSIZE+REVEALSPEED, REVEALSPEED):
      drawBoxCovers(board, boxesToCover, coverage)
      

def drawBoard(board, revealed):
   # Draws all of the boxes in their covered or revealed state.
   for boxx in range(BOARDWIDTH):
      for boxy in range(BOARDHEIGHT):
         left, top = leftTopCoordinatesOfBox(boxx, boxy)
         if not revealed[boxx][boxy]:
            # Draw a covered box.
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
         else:
            # Draw the (revealed) icon.
            shape, color = getShapeAndColor(board, boxx, boxy)
            drawIcon(shape, color, boxx, boxy)


def drawHighlightBox(boxx, boxy):
   left, top = leftTopCoordinatesOfBox(boxx, boxy)
   pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


def startGameAnimation(board):
   #set BOXWIDTH*BOXHEIGHT matrix with all elements are False
   coveredBoxes = generateRevealedBoxesData(True)
   #hold list of (col, row) in the board
   boxes = []
   for x in range(BOARDWIDTH):
      for y in range(BOARDHEIGHT):
         boxes.append((x, y))
   random.shuffle(boxes)
   #split (col, row) into group with max of 8 elements
   boxGroups = splitIntoGroupOf(8, boxes)
   #draw the board with all boxes covered
   drawBoard(board, coveredBoxes)
   #reveal then cover up the boxes in the board
   for boxGroup in boxGroups:
      #reveal 8 boxes 
      revealBoxesAnimation(board, boxGroup)
      #cover up the same 8 boxes
      coverBoxesAnimation(board, boxGroup)
      

def gameWonAnimation(board):
   coveredBoxes = generateRevealedBoxesData(True)
   color1 = LIGHTCOLOR
   color2 = BGCOLOR
   for i in range (13):
      #swap the colors
      color1, color2 = color2, color1
      DISPLAYSURF.fill(color1)
      drawBoard(board, coveredBoxes)
      pygame.display.update()
      pygame.time.wait(300)
      
   
#returns True if all the boxes have been revealed.      
def hasWon(revealedBoxes):
   for i in revealedBoxes:
      if False in i: 
         return False
   return True
   

if __name__ == '__main__':
   main()
   
         
   
   
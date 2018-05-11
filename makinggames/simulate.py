# Simulate (a Simon clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame

import pygame, sys, time, random
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FLASHSPEED = 500  # in milliseconds
FLASHDELAY = 200  # in milliseconds
BUTTONSIZE = 200
BUTTONGAPSIZE = 20
TIMEOUT = 4 # seconds before game over if no button is pushed

#                R    G    B
WHITE        =  (255, 255, 255)
BLACK        =  (0,   0,   0  )
BRIGHTRED    =  (255, 0,   0  )
RED          =  (155, 0,   0  )
BRIGHTGREEN  =  (0,   255, 0  )
GREEN        =  (0,   155, 0  )
BRIGHTBLUE   =  (0,   0,   255)
BLUE         =  (0,   0,   155)
BRIGHTYELLOW =  (255, 255, 0  )
YELLOW       =  (155, 155, 0  )
DARKGRAY     =  (40,  40,  40 )
bgColor = BLACK

XMARGIN = int((WINDOWWIDTH - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)

# Rect objects for each of the four buttons
YELLOWRECT = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
BLUERECT   = pygame.Rect(XMARGIN+BUTTONSIZE+BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
REDRECT    = pygame.Rect(XMARGIN, YMARGIN+BUTTONSIZE+BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
GREENRECT  = pygame.Rect(XMARGIN+BUTTONSIZE+BUTTONGAPSIZE, YMARGIN+BUTTONSIZE+BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BEEP1, BEEP2, BEEP3, BEEP4
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Simulate')

    BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
    infoSurf = BASICFONT.render('Match the pattern by clicking on the button or using the Q,W,A,S keys', 1, DARKGRAY)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, WINDOWHEIGHT-25)
    #load the sound files
    BEEP1 = pygame.mixer.Sound('beep1.ogg')
    BEEP2 = pygame.mixer.Sound('beep2.ogg')
    BEEP3 = pygame.mixer.Sound('beep3.ogg')
    BEEP4 = pygame.mixer.Sound('beep4.ogg')

    pattern = []        # stores the pattern for colors
    currentStep = 0     # the color the player must push next
    lastClickTime = 0   # timestamp of the player's last button push
    score = 0
    # when False, the pattern is playing.
    # when True, waiting for the player to click a colored button
    waitingForInput = False  

    while True:
        clickedButton = None
        DISPLAYSURF.fill(bgColor)
        drawButtons()
        # display score
        scoreSurf = BASICFONT.render('Score: '+str(score), 1, WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH-100, 10)
        DISPLAYSURF.blit(scoreSurf, scoreRect)
        # display info 
        DISPLAYSURF.blit(infoSurf, infoRect)

        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mouseX, mouseY = event.pos
                clickedButton = getButtonClicked(mouseX, mouseY)
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    clickedButton = YELLOW
                elif event.key == K_w:
                    clickedButton = BLUE
                elif event.key == K_a:
                    clickedButton = RED
                elif event.key == K_s:
                    clickedButton = GREEN

        if not waitingForInput:
            pygame.display.update()
            pygame.time.wait(1000)
            pattern.append(random.choice((YELLOW, BLUE, RED, GREEN)))
            for button in pattern:
                flashButtonAnimation(button)
                pygame.time.wait(FLASHDELAY)
            waitingForInput = True
        else:
            # wait for the player to enter buttons
            if clickedButton and clickedButton==pattern[currentStep]:
                # pushed the correct button
                flashButtonAnimation(clickedButton)
                currentStep += 1
                lastClickTime = time.time()

                if currentStep == len(pattern):
                    # the last button in the pattern was pushed
                    changeBackgroundAnimation()
                    score += 1
                    waitingForInput = False
                    currentStep = 0
            elif (clickedButton and clickedButton!=pattern[currentStep]) or \
                 (currentStep!=0 and time.time()-TIMEOUT>lastClickTime):
                 # push the incorrect button, or has timed out
                 gameOverAnimation()
                 # reset the variables for the new game
                 pattern = []
                 currentStep = 0
                 waitingForInput = False
                 score = 0
                 pygame.time.wait(1000)
                 changeBackgroundAnimation()

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
        #place back other KEYUP events at the end of the event queue      
        pygame.event.post(event)


def flashButtonAnimation(color, speed=50):
    if color == YELLOW:
        sound = BEEP1
        flashColor = BRIGHTYELLOW
        rectangle = YELLOWRECT
    elif color == BLUE:
        sound = BEEP2
        flashColor = BRIGHTBLUE
        rectangle = BLUERECT
    elif color == RED:
        sound = BEEP3
        flashColor = BRIGHTRED
        rectangle = REDRECT
    elif color == GREEN:
        sound = BEEP4
        flashColor = BRIGHTGREEN
        rectangle = GREENRECT
    # store the original surface    
    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface((BUTTONSIZE, BUTTONSIZE))
    # return Surface in a format suited for quick blitting to the given
    # format with per pixel alpha
    flashSurf = flashSurf.convert_alpha()
    r, g, b = flashColor
    sound.play()
    for start, end, step in ((0, 255, 1),(255, 0, -1)):
        for alpha in range(start, end, speed*step):
            checkForQuit()
            # retrieve the original surface
            DISPLAYSURF.blit(origSurf, (0,0))
            # animation with various alpha
            flashSurf.fill((r,g,b,alpha))
            DISPLAYSURF.blit(flashSurf, rectangle.topleft)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
    # retrieve the original surface        
    DISPLAYSURF.blit(origSurf, (0,0))

def drawButtons():
    # rect(Surface, color, Rect, width=0) -> Rect
    pygame.draw.rect(DISPLAYSURF, YELLOW, YELLOWRECT)
    pygame.draw.rect(DISPLAYSURF, BLUE, BLUERECT)
    pygame.draw.rect(DISPLAYSURF, RED, REDRECT)
    pygame.draw.rect(DISPLAYSURF, GREEN, GREENRECT)

def changeBackgroundAnimation(speed=40):
    global bgColor
    # pick a random color
    newBgColor = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    newBgSurf = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
    # return Surface in a format suited for quick blitting to the given
    # format with per pixel alpha
    newBgSurf = newBgSurf.convert_alpha()
    r, g, b = newBgColor
    for alpha in range(0, 255, speed):
        checkForQuit()
        DISPLAYSURF.fill(bgColor)
        newBgSurf.fill((r,g,b,alpha))
        DISPLAYSURF.blit(newBgSurf, (0, 0))
        # redraw the buttons on the top
        drawButtons()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    # bgColor is a global variable    
    bgColor = newBgColor    

def gameOverAnimation(color=WHITE, speed=50):
    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface(DISPLAYSURF.get_size())
    flashSurf = flashSurf.convert_alpha()
    # play all four beeps at the same time roughly
    BEEP1.play()
    BEEP2.play()
    BEEP3.play()
    BEEP4.play()
    r, g, b = color
    for i in range(3):
        for start, end, step in ((0, 255, 1),(255, 0, -1)):
            for alpha in range (start, end, speed*step):
                checkForQuit()
                flashSurf.fill((r,g,b,alpha))
                DISPLAYSURF.blit(origSurf, (0,0))
                DISPLAYSURF.blit(flashSurf, (0,0))
                drawButtons()
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def getButtonClicked(x, y):
    if YELLOWRECT.collidepoint((x,y)):
        return YELLOW
    elif BLUERECT.collidepoint((x,y)):
        return BLUE
    elif REDRECT.collidepoint((x,y)):
        return RED
    elif GREENRECT.collidepoint((x,y)):
        return GREEN
    return None

if __name__ == '__main__':
    main()


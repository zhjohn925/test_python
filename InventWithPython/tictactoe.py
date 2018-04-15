#Tic-Tac-Toe

import random

#Board:
#  7  8  9
#  4  5  6
#  1  2  3

winMatrix = [[7,8,9],[4,5,6],[1,2,3],
             [7,4,1],[8,5,2],[9,6,3],
             [7,5,3],[9,5,1]
            ]
allowedMoves = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

def drawBoard(board):
    #board is a list of 10 strings, ignore index 0
    print(board[7]+'|'+board[8]+'|'+board[9])
    print('-+-+-')
    print(board[4]+'|'+board[5]+'|'+board[6])
    print('-+-+-')
    print(board[1]+'|'+board[2]+'|'+board[3])
    print('-+-+-')

#return pair of letters in a list
#the first is the player's letter, 
#the second is the computer's letter.
def inputPlayerLetter():
    letter = ''
    while not (letter=='X' or letter=='O'):
        print('Do you want to be X or O?')
        letter = input().upper()
    if letter == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


def whoGoesFirst():
    if random.randint(0,1)==0:
        return 'computer'
    else:
        return 'player'
    

#letter is 'X' or 'O'
#move is a number(which grid) in the board
def makeMove(board, letter, move):
    board[move] = letter
    
#check if the letter is connected to be 3 
#in the board
def isWinner(board, letter):
    for row in winMatrix:
        win = True
        for n in row:
            if (board[n]!=letter):
                win = False
                break
        if win:
            break
    return win

def getBoardCopy(board):
    boardCopy = []
    for i in board:
        boardCopy.append(i)
    return boardCopy

def isSpaceFree(board, move):
    return board[move]==' '

#Player select move (1-9) and the move has free space 
#in the board
def getPlayerMove(board):
    move = ' '
    while move not in allowedMoves or not isSpaceFree(board, int(move)):
        print('What is your next move? (1-9)')
        move = input()
    return int(move)          
        
def chooseRandomMoveFromList(board, movesList):
    possibleMoves = []
    for move in movesList:
        if isSpaceFree(board, move):
            possibleMoves.append(move)
    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None
    
def getComputerMove(board, computerLetter):
    if computerLetter == 'X':
        playerLetter = 'O'
    else:
        playerLetter = 'X'
        
    #check if any move can win the game
    for move in range(1, 10):
        boardCopy = getBoardCopy(board)
        if isSpaceFree(boardCopy, move):
            makeMove(boardCopy, computerLetter, move)
            if isWinner(boardCopy, computerLetter):
                return move
            
    #check if any move can block the player to win
    for move in range(1, 10):
        boardCopy = getBoardCopy(board)
        if isSpaceFree(boardCopy, move):
            makeMove(boardCopy, playerLetter, move)
            if isWinner(boardCopy, playerLetter):
                return move      
    
    #try to take one of the free corners
    move = chooseRandomMoveFromList(board, [1,3,7,9])
    if move != None:
        return move
    
    #try to take the center if it is free
    if isSpaceFree(board, 5):
        return 5
    
    #move on one of the sides
    move = chooseRandomMoveFromList(board, [2,4,6,8])
    return move

def isBoardFull(board):
    for move in range(1, 10):
        if isSpaceFree(board, move):
            return False
    return True

print('Welcome to Tic-Tac-Toe!')
    
while True:
    #reset the board
    theBoard = [' ']*10
    playerLetter, computerLetter = inputPlayerLetter()
    turn = whoGoesFirst()
    print('The '+turn+' will go first.')
    gameIsPlaying = True
    while gameIsPlaying:
        if turn == 'player':
            #player's turn
            drawBoard(theBoard)
            move = getPlayerMove(theBoard)
            makeMove(theBoard, playerLetter, move)
            if isWinner(theBoard, playerLetter):
                drawBoard(theBoard)
                print('Hooray! You have won the game!')
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('The game is a tie!')
                    break
                else:
                    turn = 'computer'
        else:
            #computer's turn
            move = getComputerMove(theBoard, computerLetter)
            makeMove(theBoard, computerLetter, move)
            if isWinner(theBoard, computerLetter):
                drawBoard(theBoard)
                print('The computer has beaten you! You lose.')
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('The game is a tie!')
                    break
                else:
                    turn = 'player'
    
    print('Do you want to play again ? (yes or no)')
    if not input().lower().startswith('y'):
        break
        
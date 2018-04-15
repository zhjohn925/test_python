import random
HANGMAN_PICS = ['''
  +---+
      |
      |
      |
     ===''', '''
  +---+
  O   |
      |
      |
     ===''', '''  
  +---+
  O   |
  |   |
      |
     ===''', '''  
  +---+
  O   |
 /|   |
      |
     ===''', '''  
  +---+
  O   |
 /|\  |
      |
     ===''', '''  
  +---+
  O   |
 /|\  |
 /    |
     ===''', ''' 
  +---+
  O   |
 /|\  |
 / \  |
     ===''', '''  
  +---+
 [O   |
 /|\  |
 / \  |
     ===''', '''       
  +---+
 [O]  |
 /|\  |
 / \  |
     ===''']

#define as dictionary data type
words = {'Colors':'red orange yellow green blue indigo violet white black brown'.split(), 'Shapes':'square triangle rectangle circle ellipse rhombus trapezoid chevron pentagon hexagon septagon octagon'.split(), 'Fruits':'apple orange lemon lime pear watermelon grape grapefruit cherry banana cantaloupe mango strawberry tomato'.split(), 'Animals':'bat bear beaver cat cougar crab deer dog donkey duck eagle fish frog goat leech lion lizard monkey moose mouse otter owl panda python rabbit rat shark sheep skunk squid tiger turkey turtle weasel whale wolf wombat zebra'.split()}

#pick a random word from the list
#to be secret word
def getRandomWord(wordDict):
    keys = list(wordDict.keys())
    key = random.choice(keys)
    wordIdx = random.randint(0, len(wordDict[key])-1)
    return [wordDict[key][wordIdx], key]

def displayBoard(missedLetters, correctLetters, secretWord):
    #print hang man
    print(HANGMAN_PICS[len(missedLetters)])
    print()
    #print missed letters
    print('Missed letters:', end=' ')
    for letter in missedLetters:
        print(letter, end=' ')
    print()
    #print correct letters
    blanks = '_'*len(secretWord)
    for i in range(len(secretWord)):
        if (secretWord[i] in correctLetters):
            blanks = blanks[:i]+secretWord[i]+blanks[i+1:]
    for letter in blanks:
        print(letter, end=' ')
    print()
    
def getGuess(alreadyGuessed):
    while True:
        guess = input('Guess a letter.')
        guess = guess.lower()
        if (len(guess) != 1):
            print('Please enter a single letter.')
        elif guess in alreadyGuessed:
            print('You have already guessed that letter. Choose again.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a LETTER.')
        else: 
            return guess

def playAgain():
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')

print('H A N G M A N')

#select difficulty
difficulty = 'X'
while difficulty not in 'EMH':
    print('Enter difficulty: E-Easy,M-Medium,H-Hard')
    difficulty = input().upper()
if difficulty=='M':
    del HANGMAN_PICS[8]
    del HANGMAN_PICS[7]
if difficulty=='H':
    del HANGMAN_PICS[8]
    del HANGMAN_PICS[7]
    del HANGMAN_PICS[5]
    del HANGMAN_PICS[3]

missedLetters = ''
correctLetters = ''
secretWord, category = getRandomWord(words)
gameIsDone = False

while True:
    print('The secret word is in the category: '+category)
    displayBoard(missedLetters, correctLetters, secretWord)
    #Let the player take the guess
    guess = getGuess(missedLetters+correctLetters)
    if (guess in secretWord):
        correctLetters = correctLetters + guess
        #check if the player has won
        foundAllLetters = True
        for i in range(len(secretWord)):
            if secretWord[i] not in correctLetters:
                foundAllLetters = False
                break
        if foundAllLetters:
            print('Yes! The secret word is "'+secretWord+'"! You have won!')
            gameIsDone = True
    else:
        missedLetters = missedLetters + guess
        #check if player has guessed too many times and lost
        if (len(missedLetters)==len(HANGMAN_PICS)-1):
            displayBoard(missedLetters, correctLetters, secretWord)
            print('You have run out of guesses!\nAfter '+str(len(missedLetters))+' missed guesses and '+str(len(correctLetters))+' correct guesses, the word was "'+secretWord+'"')
            gameIsDone = True
    
    if gameIsDone:
        if playAgain():
            missedLetters = ''
            correctLetters = ''
            gameIsDone = False
            secretWord, category = getRandomWord(words)
        else:
            break
        

    
    
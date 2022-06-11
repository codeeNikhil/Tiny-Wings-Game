from ast import Global
from pickle import GLOBAL

import random
from re import X  # generate random nmber
import sys
from turtle import Screen, width
#from pip import main     # for exit the program
import pygame
from pygame.locals import *  # basic imports

# global variables for requirements
def scorehighget():
    with open("C:\\codee\\python\\PROJECT_FLAPPY\\highscore.txt","r") as f:
           p=int(f.read())
           return p
    

FPS = 32
LEVEL=2.5
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT)) 
GROUNDY = SCREENHEIGHT*0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'C:\\codee\\python\\PROJECT_FLAPPY\\bird1.png'
BACKGROUND = 'C:\\codee\\python\\PROJECT_FLAPPY\\background.png'
BACKGROUNDSCORE = 'C:\\codee\\python\\PROJECT_FLAPPY\\backgroundscore.png'
PIPE = 'C:\\codee\\python\\PROJECT_FLAPPY\\pipe.png'
SCORE='C:\\codee\\python\\PROJECT_FLAPPY\\score.png'



def welcomeScreen():  # it shows main screen to the use for start the game if he press up game will start . press esc for exit

    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():  # get the value of touch
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.QUIT()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0)) 
                SCREEN.blit(GAME_SPRITES['player'], (120, 230))
                SCREEN.blit(GAME_SPRITES['message'], (0, 0))
                high=scorehighget()
                
                    
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def scoreput(score):
        myD = [int(x) for x in list(str(score))]
        width = 0
        SCREEN.blit(GAME_SPRITES['backgroundscore'], (0, 0))
        SCREEN.blit(GAME_SPRITES['messagescore'], (0, 0))

        print("your score is",score)
        p=scorehighget()
        if p<score:
           with open("C:\\codee\\python\\PROJECT_FLAPPY\\highscore.txt","w")as f:
               f.write(str(score))               
               SCREEN.blit(GAME_SPRITES['score'], (0, 0))

        

       
        for digit in myD:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myD:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.15))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        for event in pygame.event.get():     
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
               return 0
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                mainGame()
            
            

            




def mainGame():
    score = 0
    GAME_SOUNDS['background'].play()
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0
    
        

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe(0)
    newPipe2 = getRandomPipe(0)

    # my List of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 # velocity while flapping
    playerFlapped = False # It is true only when the bird is flapping


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()
        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) # This function will return true if the player is crashed
        
              
        if crashTest:
            result=1
            while result ==1:
                result =scoreput(score)
            global LEVEL
            LEVEL=2.5  
            return     

        #check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
               # print(f"Your score is {score}") 
                GAME_SOUNDS['point'].play()


        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe(score)
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0)) 
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.85))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperPipe, lowerPipe):
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipe:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipe:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
            
    return False

def getRandomPipe(score):
    global LEVEL
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    if score >4 and score%7 is 0:
        print("upgrade")
        LEVEL=LEVEL+0.3
        offset = SCREENHEIGHT/LEVEL
        print('value of level is',LEVEL)
        
    else:
        offset = SCREENHEIGHT/LEVEL
        print('value of level is',LEVEL)
            
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe
# main function where game will start
if __name__ == "__main__":
    pygame.init()  # initialize all game mouldule
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('FlapPy BiRd game')
    GAME_SPRITES['numbers'] = (
        pygame.image.load(
            'C:\\codee\\python\\PROJECT_FLAPPY\\0.png').convert_alpha(),
        pygame.image.load(
            'C:\\codee\\python\\PROJECT_FLAPPY\\1.png').convert_alpha(),
        pygame.image.load(
            'C:\\codee\\python\\PROJECT_FLAPPY\\2.png').convert_alpha(),
        pygame.image.load(
            'C:\\codee\\python\\PROJECT_FLAPPY\\3.png').convert_alpha(),
        pygame.image.load(
            'C:\\codee\\python\\PROJECT_FLAPPY\\4.png').convert_alpha(),
        pygame.image.load(
            'C:\\codee\\python\\PROJECT_FLAPPY\\5.png').convert_alpha(),
        pygame.image.load(
            'C:\\codee\\python\\PROJECT_FLAPPY\\6.png').convert_alpha(),
        pygame.image.load(
            'C:\\codee\\python\\PROJECT_FLAPPY\\7.png').convert_alpha(),
        pygame.image.load(
            'C:\\codee\\python\\PROJECT_FLAPPY\\8.png').convert_alpha(),
        pygame.image.load(
            'C:\\codee\\python\\PROJECT_FLAPPY\\9.png').convert_alpha(),
    )
GAME_SPRITES['message'] = pygame.image.load(
    'C:\\codee\\python\\PROJECT_FLAPPY\\message.png').convert_alpha()

GAME_SPRITES['messagescore'] = pygame.image.load(
    'C:\\codee\\python\\PROJECT_FLAPPY\\messagescore.png').convert_alpha()
GAME_SPRITES['base'] = pygame.image.load(
    'C:\\codee\\python\\PROJECT_FLAPPY\\base.png').convert_alpha()
GAME_SPRITES['pipe'] = (
    pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
    pygame.image.load(PIPE).convert_alpha()
)

GAME_SOUNDS['die'] = pygame.mixer.Sound(
    'C:\\codee\\python\\PROJECT_FLAPPY\\die.wav')
GAME_SOUNDS['hit'] = pygame.mixer.Sound(
    'C:\\codee\\python\\PROJECT_FLAPPY\\hit.wav')
GAME_SOUNDS['point'] = pygame.mixer.Sound(
    'C:\\codee\\python\\PROJECT_FLAPPY\\point.wav')
GAME_SOUNDS['swoosh'] = pygame.mixer.Sound(
    'C:\\codee\\python\\PROJECT_FLAPPY\\swoosh.wav')
GAME_SOUNDS['wing'] = pygame.mixer.Sound(
    'C:\\codee\\python\\PROJECT_FLAPPY\\wing.wav')
GAME_SOUNDS['background'] = pygame.mixer.Sound(
    'C:\\codee\\python\\PROJECT_FLAPPY\\background.mp3')

GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
GAME_SPRITES['backgroundscore'] = pygame.image.load(BACKGROUNDSCORE).convert()
GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
GAME_SPRITES['score'] = pygame.image.load(SCORE).convert_alpha()

while True:
    welcomeScreen()
    mainGame()

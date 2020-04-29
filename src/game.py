import pygame, sys
from pygame.locals import *
from gameStates import *
from GameStateManager import *

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
gray = (100,100,100)
white = (255,255,255)

menu_music = '.\\bin\\GOT.mp3'
in_game_music = '.\\bin\\war.mp3'
rule_music ='.\\bin\\Halo.mp3'
pausing_music = '.\\bin\\GOT.mp3'

click = False

FPS = 30
displayWidth = 1200
displayHeight = 716   #1 extra pixel to see the last line

pygame.init()
FPSCLOCK = pygame.time.Clock()
GAMEDISPLAY = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Lu Zhan QI")

def play(music):
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1)

def stop_music():
    pygame.mixer.music.stop()

gsm = GameStateManager()

mainMenu = MainMenu(displayWidth,displayHeight,gsm)
instruction = Instruction(displayWidth,displayHeight,gsm)
inGame = None
pause = Pause(displayWidth,displayHeight,gsm)
gameOver = None

gameStates = {"MainMenu": mainMenu, 
              "Instruction": instruction, 
              "InGame": inGame,
              "Pause": pause,
              "GameOver": gameOver}

def update(event, gsm, gameStates):
    if gsm.currentGameState == "InGame" and gameStates[gsm.currentGameState] == None:
        gameStates[gsm.currentGameState] = InGame(100,55,12,5,gsm)
    gameStates[gsm.currentGameState].update(event)

        
def draw(GAMEDISPLAY, gsm, gameStates):
    if gsm.currentGameState == "InGame" and gameStates[gsm.currentGameState] == None:
        return
    gameStates[gsm.currentGameState].draw(GAMEDISPLAY)

run = True
while run:

    #Lock Framerate
    FPSCLOCK.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        print(gameStates)
        if gameStates["InGame"] and gsm.currentGameState == "MainMenu":
            dump = gameStates["InGame"]
            gameStates["InGame"] = None
            del dump
        update(event, gsm, gameStates)
        draw(GAMEDISPLAY, gsm, gameStates)

    pygame.display.update()

pygame.quit()

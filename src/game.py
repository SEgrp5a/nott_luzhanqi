import pygame, sys
from pygame.locals import *
from gameStates import *
from GameStateManager import *
from jukebox import *

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
gray = (100,100,100)
white = (255,255,255)

#BGM
BGM = {"MainMenu": '.\\bin\\GOT.mp3',
       "Instruction": '.\\bin\\Halo.mp3',
       "InGame": '.\\bin\\war.mp3',
       "Pause": '.\\bin\\GOT.mp3',
       "GameOver": None}

FPS = 30
displayWidth = 1200
displayHeight = 716   #1 extra pixel to see the last line

pygame.init()
FPSCLOCK = pygame.time.Clock()
GAMEDISPLAY = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Lu Zhan QI")

gsm = GameStateManager()
jukebox = JukeBox()

mainMenu = MainMenu(displayWidth,displayHeight,gsm)
instruction = Instruction(displayWidth,displayHeight,gsm)
inGame = None
pause = Pause(displayWidth,displayHeight,gsm)
gameOver = None

#Game State
gameStates = {"MainMenu": mainMenu,
              "Instruction": instruction,
              "InGame": inGame,
              "Pause": pause,
              "GameOver": gameOver}

#BGM
BGM = {"MainMenu": '.\\bin\\GOT.mp3',
       "Instruction": '.\\bin\\Halo.mp3',
       "InGame": '.\\bin\\war.mp3',
       "Pause": '.\\bin\\GOT.mp3',
       "GameOver": None}

def update(event, gsm, gameStates):
    if gsm.currentGameState == "InGame" and gameStates[gsm.currentGameState] == None:
        gameStates[gsm.currentGameState] = InGame(100,55,12,5,gsm)
    gameStates[gsm.currentGameState].update(event)


def draw(GAMEDISPLAY, gsm, gameStates):
    if gsm.currentGameState == "InGame" and gameStates[gsm.currentGameState] == None:
        return
    gameStates[gsm.currentGameState].draw(GAMEDISPLAY)

run = True
gsm.setState("MainMenu")
while run:

    #Lock Framerate
    FPSCLOCK.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if gameStates["InGame"] and gsm.currentGameState == "MainMenu":
            dump = gameStates["InGame"]
            gameStates["InGame"] = None
            del dump
        update(event, gsm, gameStates)
        draw(GAMEDISPLAY, gsm, gameStates)
        jukebox.play(BGM[gsm.currentGameState])

    pygame.display.update()

pygame.quit()

def gameOver_page(playerResult):
    play(gameOver_music)
    running = True
    while running:
        titleImage = pygame.image.load(".\\bin\\gameover.jpg")
        titleImage = pygame.transform.scale(titleImage,(displayWidth,displayHeight))
        GAMEDISPLAY.blit(titleImage,(0,0))

        write_text(displayWidth/2,50,'GAME OVER',red,60)

        if playerResult:
            write_text(displayWidth/2,150,'CONGRADULATIONS YOU WON',red,60)

        else:
            write_text(displayWidth/2,150,'YOU LOST THE WAR',red,60)

        mx, my = pygame.mouse.get_pos()

        restart_button = pygame.Rect(displayWidth-310,displayHeight-80,200,60)
        pygame.draw.rect(GAMEDISPLAY,red,restart_button)
        write_text(displayWidth-210,displayHeight-50,'PLAY AGAIN',white,25)

        exit_button = pygame.Rect(120,displayHeight-80,200,60)
        pygame.draw.rect(GAMEDISPLAY,red,exit_button)
        write_text(220,displayHeight-50,'EXIT GAME',white,25)

        if restart_button.collidepoint((mx, my)):
            if click:
                stop_music()
                running = False
        if exit_button.collidepoint((mx, my)):
            if click:
                print('EXIT')
                pygame.quit()
                sys.exit()

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        FPSCLOCK.tick(FPS)

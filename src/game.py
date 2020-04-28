import pygame, sys
from pygame.locals import *
from board import Board

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
black = (0,0,0)
white = (255,255,255)

menu_music = '.\\bin\\GOT.mp3'
In_game_music = '.\\bin\\war.mp3'
rule_music ='.\\bin\\Halo.mp3'
pausing_music = '.\\bin\\GOT.mp3'

click = False

FPS = 30
displayWidth = 1200
displayHeight = 716   #1 extra pixel to see the last line

board = Board(100,55,12,5)  #initialise board

pygame.init()
FPSCLOCK = pygame.time.Clock()
GAMEDISPLAY = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Lu Zhan QI")

def play(music):
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1)

def stop_music():
    pygame.mixer.music.stop()

def update(event):
    board.handleEvent(event)

def write_text(x,y,text,textcolor,fontsize):
    titleTextObj = pygame.font.Font(".\\bin\\Becker.ttf", fontsize)
    titleTextSurfaceObj = titleTextObj.render(text, True, textcolor)
    titleTextRectObj = titleTextSurfaceObj.get_rect()
    titleTextRectObj.center = (x, y)
    GAMEDISPLAY.blit(titleTextSurfaceObj, titleTextRectObj)

def writeRules():

    y = 150

    rulesImage = pygame.image.load(".\\bin\\scroll.png")
    rulesImage = pygame.transform.scale(rulesImage,(displayWidth,displayHeight))
    GAMEDISPLAY.blit(rulesImage,(0,0))

    write_text(displayWidth/2,y/2,"RULES:",black,40)

    file = open(".\\bin\\rules.csv", "r")

    for line in file:

        write_text(displayWidth/2, y,line.rstrip(),black,20)

        y += 25

    file.close()

def loadTitleScreen ():
    titleImage = pygame.image.load(".\\bin\\main.png")
    titleImage = pygame.transform.scale(titleImage,(displayWidth,displayHeight))
    GAMEDISPLAY.blit(titleImage,(0,0))

    write_text(300, 50,"Lu Zhan Qi",red,100)

def draw(board):
        GAMEDISPLAY.fill(white)
        board.draw(GAMEDISPLAY)

def main_menu ():
    play(menu_music)
    while True:
        loadTitleScreen()

        mx, my = pygame.mouse.get_pos()

        rule_button = pygame.Rect(displayWidth/2 - 100, displayHeight/2 + 110, 200, 80) 
        pygame.draw.rect(GAMEDISPLAY,red,rule_button)
        write_text(displayWidth/2,displayHeight/2 + 150,'RULES',black,34)

        start_button = pygame.Rect(displayWidth/2 - 100, displayHeight/2 + 10, 200, 80)
        pygame.draw.rect(GAMEDISPLAY,red,start_button)
        write_text(displayWidth/2,displayHeight/2 + 50,'START',black,34)

        if rule_button.collidepoint((mx, my)):
            if click:
                stop_music()
                rule_menu()
                play(menu_music)
        
        if start_button.collidepoint((mx, my)):
            if click:
                stop_music()
                start_page()
                play(menu_music)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def rule_menu():
    play(rule_music)
    running = True
    while running:
        writeRules()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    stop_music()
                    running = False
    
        pygame.display.update()
        FPSCLOCK.tick(FPS)      

def start_page():
    play(In_game_music)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE: #Pause
                    stop_music()
                    pause_page()
                    play(In_game_music)
                if event.key == K_ESCAPE: #Exit Game
                    stop_music()
                    #del board 
                    #board = Board(100,55,12,5) 
                    running = False

        update(event)
        draw(board)

        pygame.display.update()
        FPSCLOCK.tick(FPS) 

def pause_page():
    play(pausing_music)
    running = True
    while running:
        titleImage = pygame.image.load(".\\bin\\war screen.png")
        titleImage = pygame.transform.scale(titleImage,(displayWidth,displayHeight))
        GAMEDISPLAY.blit(titleImage,(0,0))
        write_text(displayWidth/2,40,'PUASED',red,60)
        write_text(displayWidth/2,100,'SPACE BAR - RETURN TO GAME',black,20)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN: 
                if event.key == K_SPACE: #return to game
                    stop_music()
                    running = False 
        pygame.display.update()
        FPSCLOCK.tick(FPS) 

main_menu()
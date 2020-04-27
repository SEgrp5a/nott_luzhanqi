import pygame, sys
from pygame.locals import *
from board import Board

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
black = (0,0,0)
white = (255,255,255)

click = False

FPS = 30
displayWidth = 1200
displayHeight = 716   #1 extra pixel to see the last line

board = Board(100,55,12,5)  #initialise board

pygame.init()
FPSCLOCK = pygame.time.Clock()
GAMEDISPLAY = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Lu Zhan QI")

def update(event):
    board.handleEvent(event)

def button_text (x, y, textColor,text,fontsize):
    startTextObj = pygame.font.Font(".\\bin\\Becker.ttf", fontsize)
    startTextSurfaceObj = startTextObj.render(text, True, textColor)
    startTextRectObj = startTextSurfaceObj.get_rect()
    startTextRectObj.center = (x, y)
    GAMEDISPLAY.blit(startTextSurfaceObj, startTextRectObj)

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

    titleTextObj = pygame.font.Font(".\\bin\\Becker.ttf", 40)
    titleTextSurfaceObj = titleTextObj.render("RULES:", True, black)
    titleTextRectObj = titleTextSurfaceObj.get_rect()
    titleTextRectObj.center = (displayWidth/2, y/2)
    GAMEDISPLAY.blit(titleTextSurfaceObj, titleTextRectObj)

    ruleTextObj = pygame.font.Font(".\\bin\\Becker.ttf", 20)

    file = open(".\\bin\\rules.csv", "r")

    for line in file:

        ruleTextSurfaceObj = ruleTextObj.render(line.rstrip(), True, black)
        ruleTextRectObj = ruleTextSurfaceObj.get_rect()
        ruleTextRectObj.center = (displayWidth/2, y)
        GAMEDISPLAY.blit(ruleTextSurfaceObj, ruleTextRectObj)

        y += 25

    file.close()

def loadTitleScreen ():
    titleImage = pygame.image.load(".\\bin\\main.png")
    titleImage = pygame.transform.scale(titleImage,(displayWidth,displayHeight))
    GAMEDISPLAY.blit(titleImage,(0,0))

    titleTextObj = pygame.font.Font("bin\Becker.ttf", 100)
    titleTextSurfaceObj = titleTextObj.render("Lu Zhan Qi", True, red)
    titleTextRectObj = titleTextSurfaceObj.get_rect()
    titleTextRectObj.center = (300, 50)
    GAMEDISPLAY.blit(titleTextSurfaceObj, titleTextRectObj)

def draw(board):
        GAMEDISPLAY.fill(white)
        board.draw(GAMEDISPLAY)

def main_menu ():
    pygame.mixer.music.load('.\\bin\\GOT.mp3')
    pygame.mixer.music.play(-1)
    while True:
        loadTitleScreen()

        mx, my = pygame.mouse.get_pos()

        rule_button = pygame.Rect(displayWidth/2 - 100, displayHeight/2 + 110, 200, 80) 
        pygame.draw.rect(GAMEDISPLAY,red,rule_button)
        button_text(displayWidth/2,displayHeight/2 + 150,black,'RULES',34)

        start_button = pygame.Rect(displayWidth/2 - 100, displayHeight/2 + 10, 200, 80)
        pygame.draw.rect(GAMEDISPLAY,red,start_button)
        button_text(displayWidth/2,displayHeight/2 + 50,black,'START',34)

        if rule_button.collidepoint((mx, my)):
            if click:
                pygame.mixer.music.stop()
                rule_menu()
        
        if start_button.collidepoint((mx, my)):
            if click:
                pygame.mixer.music.stop()
                start_page()

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
    pygame.mixer.music.load('.\\bin\\Halo.mp3')
    pygame.mixer.music.play(-1)
    running = True
    while running:
        writeRules()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load('.\\bin\\GOT.mp3')
                    pygame.mixer.music.play(-1)
                    running = False
    
        pygame.display.update()
        FPSCLOCK.tick(FPS)      

def start_page():
    pygame.mixer.music.load('.\\bin\\war.mp3')
    pygame.mixer.music.play(-1)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE: #Pause
                    pygame.mixer.music.stop()
                    pause_page()
                if event.key == K_ESCAPE: #Exit Game
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load('.\\bin\\GOT.mp3')
                    pygame.mixer.music.play(-1)
                    #del board 
                    running = False

            update(event)
            draw(board)

        pygame.display.update()
        FPSCLOCK.tick(FPS) 

def pause_page():
    pygame.mixer.music.load('.\\bin\\GOT.mp3')
    pygame.mixer.music.play(-1)

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
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load('.\\bin\\war.mp3')
                    pygame.mixer.music.play(-1)
                    running = False 
        pygame.display.update()
        FPSCLOCK.tick(FPS) 

main_menu()
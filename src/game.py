import pygame, sys
from board import Board

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
black = (0,0,0)
white = (255,255,255)

FPS = 30
pygame.init()
infoObject = pygame.display.Info()

displayWidth = infoObject.current_w

displayHeight =  infoObject.current_h  #1 extra pixel to see the last line

pygame.init()
FPSCLOCK = pygame.time.Clock()
GAMEDISPLAY = pygame.display.set_mode((displayWidth,displayHeight), pygame.RESIZABLE)
pygame.display.set_caption("Lu Zhan QI")
##
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]

###
fullscreen = False
###


#initialise board
w, h = pygame.display.get_surface().get_size()  #access the dimensions of the pygame window //get the surface, then get the size from the surface object.
board = Board(int(w/13.66),int(h/14),13,5)

rankData = {"Field Marshal": 1, "General": 2, "Lieutenant General": 3, "Brigadier": 4, "Colonel": 5, "Major": 6, "Captain": 7, "Platoon Commander": 8, "Engineer": 9, "Landmine": 0, "Grenade": 0, "Flag": "F"}       
            

def draw(board):
    GAMEDISPLAY.fill(white)
    board.draw(GAMEDISPLAY)
    
run = True

while run:
    pygame.time.Clock()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.VIDEORESIZE:
            if not fullscreen:
                GAMEDISPLAY = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE) ###
                w, h = pygame.display.get_surface().get_size()
                board = Board(int(w/13.66),int(h/14),13,5)
        board.handleEvent(event)
        draw(board)
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode(monitor_size,pygame.FULLSCREEN)
                    w, h = pygame.display.get_surface().get_size()   ###
                    board = Board(int(w/13.66),int(h/14),13,5)
                else:
                    screen = pygame.display.set_mode((screen.get_width(),screen.get_height()),pygame.RESIZABLE)
                    w, h = pygame.display.get_surface().get_size()  ###
                    board = Board(int(w/13.66),int(h/14),13,5)
            
    

    pygame.display.update()
    FPSCLOCK.tick(FPS)

pygame.quit()

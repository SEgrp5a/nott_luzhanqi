import pygame
from board import Board

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
black = (0,0,0)
white = (255,255,255)

FPS = 30
displayWidth = 1200
displayHeight = 716   #1 extra pixel to see the last line

pygame.init()
FPSCLOCK = pygame.time.Clock()
GAMEDISPLAY = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Lu Zhan QI")
#initialise board
board = Board(100,55,13,5)

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
        board.handleEvent(event)

    draw(board)

    pygame.display.update()
    FPSCLOCK.tick(FPS)

pygame.quit()
import pygame
from board import Board

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
gray = (100,100,100)
white = (255,255,255)

FPS = 30
displayWidth = 1200
displayHeight = 716   #1 extra pixel to see the last line

board = Board(100,55,12,5)  #initialise board

pygame.init()
FPSCLOCK = pygame.time.Clock()
GAMEDISPLAY = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Lu Zhan QI")
run = True

def update(event):
    board.handleEvent(event)

def draw():
    GAMEDISPLAY.fill(gray)
    board.draw(GAMEDISPLAY)

# Main game loop
while run:

    #Lock Framerate
    FPSCLOCK.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                del board
                board = Board(100,55,12,5)

        update(event)
        draw()

    pygame.display.update()

pygame.quit()
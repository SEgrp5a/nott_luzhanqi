import pygame
from board import Board
#from pieces.brigadier import Brigadier

pygame.init()
white = (255, 255, 255)

gameDisplay = pygame.display.set_mode((1200,716))
pygame.display.set_caption("Testing")
clock = pygame.time.Clock()


######
gameDisplay.fill(white)



image = pygame.image.load("./Art/" + Board.temporary[0].toString() + ".png")
#print(Brigadier.toString())
gameDisplay.blit(image,(745,150))

quitGame = False 

while not quitGame:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitGame = True
            pygame.quit()
            quit()

    pygame.display.update()
    clock.tick(60)
import pygame
from board import Board

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
black = (0,0,0)
white = (255,255,255)

gamePhase=1;

FPS = 30
displayWidth = 1200
displayHeight = 716   #1 extra pixel to see the last line

pygame.init()
FPSCLOCK = pygame.time.Clock()
GAMEDISPLAY = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Lu Zhan QI")
#initialise board
board = Board(100,55,12,5)

rankData = {"Field Marshal": 1, "General": 2, "Lieutenant General": 3, "Brigadier": 4, "Colonel": 5, "Major": 6, "Captain": 7, "Platoon Commander": 8, "Engineer": 9, "Landmine": 0, "Grenade": 0, "Flag": "F"}       
            
def draw(board):
    GAMEDISPLAY.fill(white)
    board.draw(GAMEDISPLAY)
    
run = True

def drawDoneButton(surface):
        #drawing done icon
        textObj = pygame.font.Font("bin\OpenSans.ttf", 18)
        buttonRect = pygame.Rect(1200-115, 716-55, 100, 40)
        pygame.draw.rect(surface, red, buttonRect)
        numTextSurfaceObj = textObj.render("DONE", True, black)
        numTextRectObj = numTextSurfaceObj.get_rect()
        numTextRectObj.center = (buttonRect.left + 50, buttonRect.top + 20)
        surface.blit(numTextSurfaceObj, numTextRectObj)

def setup():
    draw(board)
    drawDoneButton(GAMEDISPLAY)


while run:
    pygame.time.Clock()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        board.handleEvent(event)

        if gamePhase==1:
            setup()
        if gamePhase==2:
            draw(board)

    pygame.display.update()

    mousePos = pygame.mouse.get_pos()
    mouseClicked=pygame.mouse.get_pressed()
    if (1200-115)+100 > mousePos[0] > (1200-115) and (716-55)+40 > mousePos[1] > (716-55):
        if mouseClicked[0]==True:
            board.checkDone()

    FPSCLOCK.tick(FPS)

pygame.quit()
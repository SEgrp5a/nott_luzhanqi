import pygame
from pygame.locals import *
from gameBoard.board import Board

pygame.init()

Board = Board()
Board.accessingPieces()

red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
yellow = (247, 255, 0)
black = (0, 0, 0)

mouseX = 0
mouseY = 0

gamePhase = 0

displayX = 1200
displayY = 716   #1 extra pixel to see the last line

win=pygame.display.set_mode((700,700))

gameDisplay=pygame.display.set_mode((displayX,displayY))
pygame.display.set_caption("LUZHANQI")
gameDisplay.fill(white)

#The "Item" variable is just used to call for drawing Image
def genPieceObject(x, y, item, color, showEnemy, drawShadow):

    if drawShadow == True:

        shadowImage = pygame.image.load("./Art/Piece Shadow.png")
        gameDisplay.blit(shadowImage, (x + 2, y + 2))

    pieceRect = pygame.Rect(x, y, 50, 50)  #50 by 50 because its the size of the icons
    pygame.draw.rect(gameDisplay, color, pieceRect)

    if color != blue or showEnemy == True or alwaysShowEnemy == True:
            
        image = pygame.image.load("./Art/"+ item + ".png")
        gameDisplay.blit(image, (x, y))
        

    return pieceRect

def newPhase():
    global gamePhase
    gamePhase = gamePhase + 1
    print("game phase:", gamePhase)

def setupPhase():

    global pieceData, ready

    gameDisplay.fill(white)
    
    drawBoard()


    #draws text and pieces beside board
    titleTextObj = pygame.font.Font("./Art/OpenSans.ttf", 38)
    titleTextSurfaceObj = titleTextObj.render("PIECES", True, black) 
    titleTextRectObj = titleTextSurfaceObj.get_rect()
    titleTextRectObj.center = (925, 75)
    gameDisplay.blit(titleTextSurfaceObj, titleTextRectObj)

    textObj = pygame.font.Font("./Art/OpenSans.ttf", 18)

    x = 745
    y = 150

    for item in Board.temporary:
        #drawing pieces icon

        textSurfaceObj = textObj.render(item, True, black) #Printing the Name of the Piece
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (x, y)
        gameDisplay.blit(textSurfaceObj, textRectObj)

        numTextSurfaceObj = textObj.render("x" + str(Board.temporary[item].available), True, black) #Printing the number of pieces remaining
        numTextRectObj = numTextSurfaceObj.get_rect()
        numTextRectObj.center = (x, y + 100)
        gameDisplay.blit(numTextSurfaceObj, numTextRectObj)

        if Board.temporary[item].available != 0:

            ready = False
            pieceRect = genPieceObject(x - 25, y + 25, item, yellow, False, False)
            #pieceData[item] = [pieceData[item][0], pieceRect]c


        if x > 1050:

            x = 745
            y += 150

        else:
            x += 120
            

    #dragPiece()


    #drawing done icon

    buttonRect = pygame.Rect(displayX - 115, displayY - 55, 100, 40)
    pygame.draw.rect(gameDisplay, red, buttonRect)

    endPhaseTextSurfaceObj = textObj.render("DONE", True, black)
    endPhaseTextRectObj = endPhaseTextSurfaceObj.get_rect()
    endPhaseTextRectObj.center = (buttonRect.left + 50, buttonRect.top + 20)
    gameDisplay.blit(endPhaseTextSurfaceObj, endPhaseTextRectObj)

    if buttonRect.left < mouseX < buttonRect.right and buttonRect.top < mouseY < buttonRect.bottom and mouseClicked == True:
        pieceData = {"Field Marshal": 1, "General": 1, "Lieutenant General": 2, "Brigadier": 2, "Colonel": 2, "Major": 2, "Captain": 3, "Platoon Commander": 3, "Engineer": 3, "Landmine": 3, "Bomb": 2, "Flag": 1}
        gameDisplay.fill(white)          

def drawBoard():
    y = 0
    x = 0
    width = 100
    height = 55 
    
    Board.draw(gameDisplay,width,height)

def eventHandler():
    global mouseX, mouseY, mouseClicked
    mouseClicked = False

    #runs through game events

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            quit()

        if event.type == MOUSEMOTION:
            mouseX, mouseY = event.pos

        elif event.type == MOUSEBUTTONUP:
            mouseX, mouseY = event.pos
            print(mouseX, mouseY)
            mouseClicked = True 

def loadTitleScreen():

    titleImage = pygame.image.load("./Art/Title Screen.png")
    titleImage = pygame.transform.scale(titleImage,(displayX,displayY))
    gameDisplay.blit(titleImage, (0, 0))

def startButton():

    buttonRect = pygame.Rect(displayX/2 - 100, displayY/2 + 110, 200, 80)
    pygame.draw.rect(gameDisplay, red, buttonRect)

    startTextObj = pygame.font.Font("./Art/Becker.ttf", 34)
    startTextSurfaceObj = startTextObj.render("START", True, black)
    startTextRectObj = startTextSurfaceObj.get_rect()
    startTextRectObj.center = (displayX/2, displayY/2 + 150)
    gameDisplay.blit(startTextSurfaceObj, startTextRectObj)

    return buttonRect

def startGame():

    if buttonRect.left < mouseX < buttonRect.right and buttonRect.top < mouseY < buttonRect.bottom and mouseClicked == True:
        gameDisplay.fill(white)
        newPhase()
        #writeRules()
        #setupPhase()

def writeRules():

    y = 150

    titleTextObj = pygame.font.Font("./Art/Becker.ttf", 38)
    titleTextSurfaceObj = titleTextObj.render("RULES:", True, black)
    titleTextRectObj = titleTextSurfaceObj.get_rect()
    titleTextRectObj.center = (displayX/2, y/2)
    gameDisplay.blit(titleTextSurfaceObj, titleTextRectObj)

    ruleTextObj = pygame.font.Font("./Art/Becker.ttf", 18)

    rulesImage = pygame.image.load("./Art/Rule Screen.png")
    rulesImage = pygame.transform.scale(rulesImage,(displayX,displayY))
    gameDisplay.blit(rulesImage,(0,0))

    file = open("./Art/rules.csv", "r")

    for line in file:

        ruleTextSurfaceObj = ruleTextObj.render(line.rstrip(), True, white)
        ruleTextRectObj = ruleTextSurfaceObj.get_rect()
        ruleTextRectObj.center = (displayX/2, y)
        gameDisplay.blit(ruleTextSurfaceObj, ruleTextRectObj)

        y += 25

    file.close()

    newPhase()

loadTitleScreen()
buttonRect = startButton()
run = True
while run:

    eventHandler()

    if gamePhase == 0:
        startGame()

    elif gamePhase == 1:
        writeRules()

    elif gamePhase == 2:
        if mouseClicked == True:
            gameDisplay.fill(white)
            newPhase()
            
    elif gamePhase == 3:
        setupPhase()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False

    pygame.display.update()
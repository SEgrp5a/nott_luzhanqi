import pygame
import operator
from button import Button
from pieces import *

class Board:
    def __init__(self,width,height,numRow,numCol):
        self.red = pygame.Color(255,0,0)
        self.green = pygame.Color(0,255,0)
        self.blue = pygame.Color(0,0,255)
        self.black = pygame.Color(0,0,0)
        self.pieceData = {"Flag": [1],
                          "Grenade": [2],
                          "Landmine": [3],
                          "Marshal": [1],
                          "General": [1], 
                          "Lieutenant": [2], 
                          "Brigadier": [2],
                          "Colonel": [2], 
                          "Major": [2], 
                          "Captain": [3], 
                          "Commander": [3],
                          "Engineer": [3]}
        self.width = width
        self.height = height
        self.numRow = numRow
        self.numCol = numCol
        self.layout = self.generateLayout()
        #board
        brdImgPath = "bin\\board.png"
        orgBrdImg = pygame.image.load(brdImgPath)
        self.brdImg = pygame.transform.scale(orgBrdImg, (width*numCol, height*numRow))
        #tile
        self.tiles = self.generateTiles()
        #selection pane
        self.selectionPaneTiles = self.generateSelectionPane()
        #holding piece
        self.currentPiece = None
        #moving piece
        self.movingPiece = False

    def generateLayout(self):
        #Initialise the game board
        #Set all as Soldier Station
        layout = [["SS" for i in range(self.numCol)] for j in range(self.numRow)]

        #Setting Camp
        layout[2][1] = "CP"
        layout[2][3] = "CP"
        layout[3][2] = "CP"
        layout[4][1] = "CP"
        layout[4][3] = "CP"
        layout[8][1] = "CP"
        layout[8][3] = "CP"
        layout[9][2] = "CP"
        layout[10][1] = "CP"
        layout[10][3] = "CP"

        #Setting Headquarters
        layout[0][1] = "HQ"
        layout[0][3] = "HQ"
        layout[12][1] = "HQ"
        layout[12][3] = "HQ"

        #Setting Front Line
        layout[6][0] = "FL"
        layout[6][2] = "FL"
        layout[6][4] = "FL"

        #Setting Mountain Border
        layout[6][1] = "MB"
        layout[6][3] = "MB"

        return layout

    def generateTiles(self):
        tiles = [[Button(i * self.width, j * self.height, self.width, self.height, transparent = True) for i in range(self.numCol)] for j in range(self.numRow)]
        return tiles

    def generateSelectionPane(self):
        selectionPaneTiles = [None for i in range(12)]
        #draws text and pieces beside board
        x = 725
        y = 200
        i = 0
        for item in self.pieceData:
            selectionPaneTiles[i] = Button(x, y, 50, 50, color = (255,255,0))
            if item == "Flag":
                selectionPaneTiles[i].setPiece(Flag(0,selectionPaneTiles[i].getPos()))
            elif item == "Grenade":
                selectionPaneTiles[i].setPiece(Grenade(0,selectionPaneTiles[i].getPos()))
            elif item == "Landmine":
                selectionPaneTiles[i].setPiece(Landmine(0,selectionPaneTiles[i].getPos()))
            elif item == "Marshal":
                selectionPaneTiles[i].setPiece(Marshal(0,selectionPaneTiles[i].getPos()))
            elif item == "General":
                selectionPaneTiles[i].setPiece(General(0,selectionPaneTiles[i].getPos()))
            elif item == "Lieutenant":
                selectionPaneTiles[i].setPiece(Lieutenant(0,selectionPaneTiles[i].getPos()))
            elif item == "Brigadier":
                selectionPaneTiles[i].setPiece(Brigadier(0,selectionPaneTiles[i].getPos()))
            elif item == "Colonel":
                selectionPaneTiles[i].setPiece(Colonel(0,selectionPaneTiles[i].getPos()))
            elif item == "Major":
                selectionPaneTiles[i].setPiece(Major(0,selectionPaneTiles[i].getPos()))
            elif item == "Captain":
                selectionPaneTiles[i].setPiece(Captain(0,selectionPaneTiles[i].getPos()))
            elif item == "Commander":
                selectionPaneTiles[i].setPiece(Commander(0,selectionPaneTiles[i].getPos()))
            elif item == "Engineer":
                selectionPaneTiles[i].setPiece(Engineer(0,selectionPaneTiles[i].getPos()))
            selectionPaneTiles[i].setFlag(item)
            i = i + 1
            if x > 1050:
                x = 725
                y += 150
                #go to new line
            else:
                x += 120

        return selectionPaneTiles

    def draw(self,surface):
        #Draw board
        surface.blit(self.brdImg,(0,0))
        #Draw tiles
        for j in range(self.numCol):
            for i in range(self.numRow):
                self.tiles[i][j].draw(surface)

        #Only draw Selection Pane on setup phase
        #Draw Selection Pane
        #Draw Selection Pane Title
        titleTextObj = pygame.font.Font("bin\OpenSans.ttf", 38)
        titleTextSurfaceObj = titleTextObj.render("PIECES", True, self.black)
        titleTextRectObj = titleTextSurfaceObj.get_rect()
        titleTextRectObj.center = (925, 75)
        surface.blit(titleTextSurfaceObj, titleTextRectObj)
        #Draw Selection Pane Tiles
        k = 0
        for item in self.pieceData:
            #Draw piece image
            if (self.pieceData[item][0] == 0):
                self.selectionPaneTiles[k].setPiece(None)
            self.selectionPaneTiles[k].draw(surface)
            #Draw Selection Pane piece's name
            textObj = pygame.font.Font("bin\OpenSans.ttf", 18)
            textSurfaceObj = textObj.render(item, True, self.black)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = tuple(x + y for x, y in zip(self.selectionPaneTiles[k].getPos(), (25,-25)))
            surface.blit(textSurfaceObj, textRectObj)
            #Draw number of piece remaining
            numTextSurfaceObj = textObj.render("x " + str(self.pieceData[item][0]), True, self.black)
            numTextRectObj = numTextSurfaceObj.get_rect()
            numTextRectObj.center = tuple(x + y for x, y in zip(self.selectionPaneTiles[k].getPos(), (25,75)))
            surface.blit(numTextSurfaceObj, numTextRectObj)
            k = k + 1

        if self.currentPiece != None:
            mousePos = pygame.mouse.get_pos()
            cursorImg = pygame.image.load(self.currentPiece.getPath())
            surface.blit(cursorImg, tuple(x + y for x, y in zip(mousePos, (-25,-25))))

    def handleEvent(self, event):
        #handle mouse click
        for j in range(self.numCol):
            for i in range(self.numRow):
                outline = False
                outlineColor = None
                if 'hover' in self.tiles[i][j].handleEvent(event):
                    #if is hovering on button
                    outline = True
                    outlineColor = self.green
                if 'down' in self.tiles[i][j].handleEvent(event):
                    #if button is clicked
                    outline = True
                    outlineColor = self.blue
                if 'click' in self.tiles[i][j].handleEvent(event):
                    #if button is clicked & released
                    if self.currentPiece == None:
                        if self.tiles[i][j].getPiece() != None:
                            #take the piece if the tile already contain a piece
                            self.currentPiece = self.tiles[i][j].getPiece()
                            self.tiles[i][j].setPiece(None)
                            self.movingPiece = True
                    else:
                        if self.tiles[i][j].getPiece() == None:
                            #place the piece if the tile does not contain a piece
                            self.tiles[i][j].setPiece(self.currentPiece)
                            if not self.movingPiece:
                                self.pieceData[self.currentPiece.toString()][0] = self.pieceData[self.currentPiece.toString()][0] - 1
                            self.currentPiece = None
                            self.movingPiece = False
                if 'exit' in self.tiles[i][j].handleEvent(event):
                    #if mouse exited a button
                    outline = False
                self.tiles[i][j].update(self.tiles[i][j].getColor(), outline, outlineColor)

        for k in range(len(self.selectionPaneTiles)):
            outline = False
            outlineColor = None
            if 'hover' in self.selectionPaneTiles[k].handleEvent(event):
                #if is hovering on button
                outline = True
                outlineColor = self.red
            if 'down' in self.selectionPaneTiles[k].handleEvent(event):
                #if button is clicked
                outline = True
                outlineColor = self.black
            if 'click' in self.selectionPaneTiles[k].handleEvent(event):
                #if button is clicked & released
                if self.currentPiece == None:
                    self.currentPiece = self.selectionPaneTiles[k].getPiece()
                else:
                    if self.movingPiece and self.currentPiece.toString() == self.selectionPaneTiles[k].getFlag():
                        self.selectionPaneTiles[k].setPiece(self.currentPiece)
                        self.pieceData[self.currentPiece.toString()][0] = self.pieceData[self.currentPiece.toString()][0] + 1
                        self.currentPiece = None
                        self.movingPiece = False
            if 'exit' in self.selectionPaneTiles[k].handleEvent(event):
                outline = False
            self.selectionPaneTiles[k].update(self.selectionPaneTiles[k].getColor(), outline, outlineColor)
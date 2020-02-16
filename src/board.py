import pygame
import operator
from button import *
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
        self.brdImg = pygame.transform.scale(orgBrdImg, (width * numCol, height * (numRow + 1)))
        #tile
        self.tiles = self.generateTiles()
        #selection pane
        self.selectionPaneTiles = self.generateSelectionPane()
        #holding piece
        self.currentPiece = None
        #moving piece
        self.movingPiece = False
        self.doneButton = self.generateDoneButton()
        self.gamePhase = 1

    def getGamePhase():
        return self.gamePhase

    def generateLayout(self):
        #Set all as Soldier Station
        layout = [["SS" for i in range(self.numCol)] for j in range(self.numRow)]

        #Setting Camp
        layout[2][1] = "CP"
        layout[2][3] = "CP"
        layout[3][2] = "CP"
        layout[4][1] = "CP"
        layout[4][3] = "CP"
        layout[7][1] = "CP"
        layout[7][3] = "CP"
        layout[8][2] = "CP"
        layout[9][1] = "CP"
        layout[9][3] = "CP"

        #Setting Headquarters
        layout[0][1] = "HQ"
        layout[0][3] = "HQ"
        layout[11][1] = "HQ"
        layout[11][3] = "HQ"

        return layout

    def generateTiles(self):
        tiles=[]
        for j in range(self.numRow):
            x=[]
            for i in range(self.numCol):
                if j>=6:
                    x.append(Button(i * self.width, (j + 1) * self.height, self.width, self.height, transparent = True))
                else:
                     x.append(Button(i * self.width, j * self.height, self.width, self.height, transparent = True))
            tiles.append(x)
        return tiles

    def generateSelectionPane(self):
        selectionPaneTiles = [None for _ in range(12)]
        #draws text and pieces beside board
        x = 725
        y = 200
        i = 0
        for item in self.pieceData:
            selectionPaneTiles[i] = SelectionPaneButton(x, y, 50, 50, color = (255,255,0), nPieces = self.pieceData[item][0])
            for j in range(self.pieceData[item][0]):
                selectionPaneTiles[i].addPiece(self.spawnPiece(item, selectionPaneTiles[i].getPos()))
            selectionPaneTiles[i].setFlag(item)
            i = i + 1
            if x > 1050:
                x = 725
                y += 150
                #go to new line
            else:
                x += 120

        return selectionPaneTiles

    def spawnPiece(self, piece, pos):
        spawn = None
        if piece == "Flag":
            spawn = Flag(0, pos)
        elif piece == "Grenade":
            spawn = Grenade(0, pos)
        elif piece == "Landmine":
            spawn = Landmine(0, pos)
        elif piece == "Marshal":
            spawn = Marshal(0, pos)
        elif piece == "General":
            spawn = General(0, pos)
        elif piece == "Lieutenant":
            spawn = Lieutenant(0, pos)
        elif piece == "Brigadier":
            spawn = Brigadier(0, pos)
        elif piece == "Colonel":
            spawn = Colonel(0, pos)
        elif piece == "Major":
            spawn = Major(0, pos)
        elif piece == "Captain":
            spawn = Captain(0, pos)
        elif piece == "Commander":
            spawn = Commander(0, pos)
        elif piece == "Engineer":
            spawn = Engineer(0, pos)

        return spawn

    def generateDoneButton(self):
        return Button(1200 - 115, 716 - 55, 100, 40, self.red, text = "Done")

    def genAiPieces(self):
        for j in range(self.numCol):
            tempY = 11; # -1 for each iteration to simulate mirroring
            for i in range(6):
                self.tiles[i][j].setPiece(self.tiles[tempY][j].getPiece())
                tempY = tempY - 1
        self.gamePhase = 2

    def checkDone(self):
        complete = False
        if self.currentPiece == None:
            for item in self.pieceData:
                if self.pieceData[item][0] == 0:
                    complete = True;
                else:
                    complete = False;
            if complete == True:
                self.genAiPieces()
        return complete

    def draw(self,surface):
        """Draw the entire interface"""
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

        if self.gamePhase==1:
            self.doneButton.draw(surface)

    def checkAvailablePlacement(self,row,col,piece):
        """check if piece placement is vailble"""
        if row < 6:
            #opposite territory
            return False
        if self.layout[row][col] == "CP":
            #cannot be initialise at camps
            return False
        if piece.toString() == "Flag" and self.layout[row][col] != "HQ":
            #flag can only be placed in headquaters
            return False
        if piece.toString() == "Landmine" and not(row == 10 or row == 11):
            #landmine can only be initailse at last 2 rows
            return False
        if piece.toString() == "Grenade" and row == 6:
            #grenade cannot be placed at 1st row
                return False
        return True

    def handleEvent(self, event):
        """handle mouse click"""
        for j in range(self.numCol):
            for i in range(self.numRow):
                outline_tile = False
                outlineColor_tile = None
                if 'hover' in self.tiles[i][j].handleEvent(event):
                    #if is hovering on button
                    outline_tile = True
                    if self.currentPiece != None:
                        if self.checkAvailablePlacement(i,j,self.currentPiece):
                            outlineColor_tile = self.green
                        else:
                            outlineColor_tile = self.red
                    else:
                        outlineColor_tile = self.black
                if 'down' in self.tiles[i][j].handleEvent(event):
                    #if button is clicked
                    outline_tile = True
                    outlineColor_tile = self.blue
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
                            if self.checkAvailablePlacement(i,j,self.currentPiece):
                                self.tiles[i][j].setPiece(self.currentPiece)
                                if not self.movingPiece:
                                    self.pieceData[self.currentPiece.toString()][0] = self.pieceData[self.currentPiece.toString()][0] - 1
                                self.currentPiece = None
                                self.movingPiece = False
                if 'exit' in self.tiles[i][j].handleEvent(event):
                    #if mouse exited a button
                    outline_tile = False
                self.tiles[i][j].update(self.tiles[i][j].getColor(), outline_tile, outlineColor_tile)

        if self.gamePhase == 1:
            for k in range(len(self.selectionPaneTiles)):
                outline_select = False
                outlineColor_select = None
                if 'hover' in self.selectionPaneTiles[k].handleEvent(event):
                    #if is hovering on button
                    outline_select = True
                    outlineColor_select = self.black
                if 'down' in self.selectionPaneTiles[k].handleEvent(event):
                    #if button is clicked
                    outline_select = True
                    outlineColor_select = self.blue
                if 'click' in self.selectionPaneTiles[k].handleEvent(event):
                    #if button is clicked & released
                    if self.currentPiece == None:
                        self.currentPiece = self.selectionPaneTiles[k].getPiece()
                        self.selectionPaneTiles[k].removePiece()
                    else:
                        if self.currentPiece.toString() == self.selectionPaneTiles[k].getFlag():
                            self.selectionPaneTiles[k].addPiece(self.currentPiece)
                            if self.movingPiece:
                                self.pieceData[self.currentPiece.toString()][0] = self.pieceData[self.currentPiece.toString()][0] + 1
                            self.currentPiece = None
                            self.movingPiece = False
                if 'exit' in self.selectionPaneTiles[k].handleEvent(event):
                    outline_select = False
                self.selectionPaneTiles[k].update(self.selectionPaneTiles[k].getColor(), outline_select, outlineColor_select)

        if self.gamePhase == 1:
            outline_done = False
            outlineColor_done = None
            if 'hover' in self.doneButton.handleEvent(event):
                #if is hovering on button
                outline_done = True
                outlineColor_done = self.black
            if 'down' in self.doneButton.handleEvent(event):
                #if button is clicked
                outline_done = True
                outlineColor_done = self.blue
            if 'click' in self.doneButton.handleEvent(event):
                #if button is clicked & released
                self.checkDone()
            if 'exit' in self.doneButton.handleEvent(event):
                outline_done = False
            self.doneButton.update(self.doneButton.getColor(),outline_done,outlineColor_done)

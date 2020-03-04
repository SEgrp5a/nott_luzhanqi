import pygame
import operator
import random
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
        self.pieceRow = None
        self.pieceCol = None
        #moving piece
        self.movingPiece = False
        #done button
        self.doneButton = Button(1200 - 115, 716 - 55, 100, 40, self.red, text = "Done")
        #record game phase
        self.gamePhase = 1

    def getGamePhase():
        return self.gamePhase

    def generateLayout(self):
        #Set all as Soldier Station
        layout = [["SS" for i in range(self.numCol)] for j in range(self.numRow)]

        #Set Railway
        for i in range(1,self.numRow - 1):
            layout[i][0] = "RW"
            layout[i][4] = "RW"
        for j in range(1, self.numCol - 1):
            layout[1][j] = "RW"
            layout[5][j] = "RW"
            layout[6][j] = "RW"
            layout[10][j] = "RW"

        #Set Camp
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

        #Set Headquarters
        layout[0][1] = "HQ"
        layout[0][3] = "HQ"
        layout[11][1] = "HQ"
        layout[11][3] = "HQ"

        return layout

    def generateTiles(self):
        tiles = []
        for j in range(self.numRow):
            x = []
            for i in range(self.numCol):
                if j >= 6:
                    x.append(Button(i * self.width, (j + 1) * self.height, self.width, self.height, transparent = True))
                else:
                     x.append(Button(i * self.width, j * self.height, self.width, self.height, transparent = True))
            tiles.append(x)
        return tiles

    #draws text and pieces beside board
    def generateSelectionPane(self):
        selectionPaneTiles = [None for _ in range(12)]
        x = 725
        y = 200
        i = 0
        for item in self.pieceData:
            selectionPaneTiles[i] = SelectionPaneButton(x, y, 50, 50, color = (255,255,0), nPieces = self.pieceData[item][0])
            for j in range(self.pieceData[item][0]):
                selectionPaneTiles[i].addPiece(self.spawnPiece(0, item, selectionPaneTiles[i].getPos()))
            selectionPaneTiles[i].setFlag(item)
            i = i + 1
            if x > 1050:
                x = 725
                y += 150
                #go to new line
            else:
                x += 120

        return selectionPaneTiles

    def spawnPiece(self, alliance, piece, pos):
        spawn = None
        if piece == "Flag":
            spawn = Flag(alliance, pos)
        elif piece == "Grenade":
            spawn = Grenade(alliance, pos)
        elif piece == "Landmine":
            spawn = Landmine(alliance, pos)
        elif piece == "Marshal":
            spawn = Marshal(alliance, pos)
        elif piece == "General":
            spawn = General(alliance, pos)
        elif piece == "Lieutenant":
            spawn = Lieutenant(alliance, pos)
        elif piece == "Brigadier":
            spawn = Brigadier(alliance, pos)
        elif piece == "Colonel":
            spawn = Colonel(alliance, pos)
        elif piece == "Major":
            spawn = Major(alliance, pos)
        elif piece == "Captain":
            spawn = Captain(alliance, pos)
        elif piece == "Commander":
            spawn = Commander(alliance, pos)
        elif piece == "Engineer":
            spawn = Engineer(alliance, pos)

        return spawn

    def genAiPieces(self):
        for j in range(self.numCol):
            tempY = 11 # -1 for each iteration to simulate mirroring
            for i in range(6):
                if self.tiles[tempY][j].getPiece():
                    self.tiles[i][j].setPiece(self.spawnPiece(1, self.tiles[tempY][j].getPiece().toString(), self.tiles[i][j].getPos()))
                tempY = tempY - 1
        self.gamePhase = 2

    def checkDone(self):
        complete=False
        if self.currentPiece == None:
            for k in self.pieceData:
                if self.pieceData[k][0] == 0:
                    complete=True;
                else:
                    # can do a pop-up to let user know not all pieces are set
                    break
            if complete==True:
                self.genAiPieces()

    #Draw the entire interface
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

        if self.currentPiece:
            mousePos = pygame.mouse.get_pos()
            cursorImg = pygame.image.load(self.currentPiece.getPath())
            surface.blit(cursorImg, tuple(x + y for x, y in zip(mousePos, (-25,-25))))

        if self.gamePhase == 1:
            self.doneButton.draw(surface)

    #check if piece placement is vailble
    def checkAvailablePlacement(self, row, col, piece):
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

    #check if movement is vailable
    def checkAvailableMovement(self, row, col, piece, pieceRow, pieceCol):
        action = None   #action is either "attack" or "move" or None for invalid action
        #pos = (row, col)
        ul = (pieceRow - 1, pieceCol - 1) #upperleft
        up = (pieceRow - 1, pieceCol)     #up
        ur = (pieceRow - 1, pieceCol + 1) #upperright
        lf = (pieceRow, pieceCol - 1)     #left
        og = (pieceRow, pieceCol)         #original
        rg = (pieceRow, pieceCol + 1)     #right
        dl = (pieceRow + 1, pieceCol - 1) #downleft
        dw = (pieceRow + 1, pieceCol)     #down
        dr = (pieceRow + 1, pieceCol + 1) #downright
        if piece.toString() == "Landmine" or piece.toString() == "Flag":
            return False    #landmine and flag cannot be move
        #if no move
        if og == (row, col):
            action = "move"
        #if engineer on railway
        if self.layout[pieceRow][pieceCol] == "RW" and self.layout[row][col] == "RW" and piece.toString() == "Engineer":
            railwayGraph = {}   #will contain adjacent nodes of the pos ({0 : [1, 10], ...})
            index = 0   #label the nodes (key for railwayGraph)
            railwayList = []    #will contain all railway counting up to down, left to right ([(row, col), ...]) (railwayList[vertex] will have result for the location of railway)
            #initialise railwayList
            for j in range(self.numCol):
                for i in range(self.numRow):
                    if self.layout[i][j] == "RW":
                        railwayList.append((i,j))
            #generate the graph of railways
            for j in range(self.numCol):
                for i in range(self.numRow):
                    if self.layout[i][j] == "RW":
                        directions = {"right" : (i, j + 1),
                                      "down" : (i + 1, j),
                                      "left" : (i, j - 1),
                                      "up" : (i - 1, j)}  #save adjacent tiles
                        rw_adj = [] #save adjacent railway tiles
                        for direction in directions:  #loop all 4 directions
                            if directions[direction][0] >= 0 and directions[direction][0] < self.numRow and directions[direction][1] >= 0 and directions[direction][1] < self.numCol and self.layout[directions[direction][0]][directions[direction][1]] == "RW" :   #check if adjacent tiles is railway
                                rw_adj.append(railwayList.index(directions[direction]))
                        if index == 11:
                            if 12 in rw_adj:
                                rw_adj.remove(12)
                        if index == 12:
                            if 11 in rw_adj:
                                rw_adj.remove(11)
                        if index == 19:
                            if 20 in rw_adj:
                                rw_adj.remove(20)
                        if index == 20:
                            if 19 in rw_adj:
                                rw_adj.remove(19)
                        rw_adj.sort()   #sort to improve DFS consistency
                        railwayGraph[index] = rw_adj
                        index = index + 1
            #search for path to dest using DFS
            #DFS algorithm referenced from https://www.koderdojo.com/blog/depth-first-search-in-python-recursive-and-non-recursive-programming
            def DFS(graph, start, dest):
                stack = [start]
                path = []
                while stack:
                    if dest in path:
                        break   #return as soon as a path has been find
                    vertex = stack.pop()
                    if self.tiles[railwayList[vertex][0]][railwayList[vertex][1]].getPiece():
                        if self.tiles[railwayList[vertex][0]][railwayList[vertex][1]].getPiece().getAlliance() != piece.getAlliance():
                            path.append(vertex) #add to path if is opponent piece
                        continue    #don't expand vertices with pieces on them
                    path.append(vertex)
                    for neighbour in graph[vertex]:
                        if neighbour in path:
                            continue    #ignore discovered vertices
                        if neighbour in stack:
                            continue    #ignore discovered vertices
                        stack.append(neighbour)
                return path
            start = railwayList.index((pieceRow, pieceCol)) #get the corresponding vertices
            dest = railwayList.index((row, col))    #get the corresponding vertices
            path = DFS(railwayGraph, start, dest)
            if dest in path:
                if not self.tiles[row][col].getPiece():
                    action = "move"
                elif self.tiles[row][col].getPiece().getAlliance() != piece.getAlliance():
                    action = "attack"
                elif self.tiles[row][col].getPiece().getAlliance() == piece.getAlliance():
                    action = None
            else:
                action = None
        #if on railway
        elif self.layout[pieceRow][pieceCol] == "RW" and self.layout[row][col] == "RW":
            if pieceRow == row:   #check if same horizontal railway
                distance = pieceCol - col
                for hOffset in range(0, abs(distance)):
                    if self.layout[row][pieceCol - (int(distance / abs(distance)) * hOffset)] == "RW":
                        if not self.tiles[row][col].getPiece():
                            if not self.tiles[row][pieceCol - (int(distance / abs(distance)) * hOffset)].getPiece():
                                action = "move"
                            elif self.tiles[row][pieceCol - (int(distance / abs(distance)) * hOffset)].getPiece():
                                action = None
                                break
                        elif self.tiles[row][col].getPiece() and self.tiles[row][col].getPiece().getAlliance() != piece.getAlliance():
                            if not self.tiles[row][pieceCol - (int(distance / abs(distance)) * hOffset)].getPiece():
                                action = "attack"
                            elif self.tiles[pieceRow - (int(distance / abs(distance)) * vOffset)][col].getPiece():
                                action = None
                                break
                    else:
                        action = None
                        break
            elif pieceCol == col and not (col == 1 or col == 3): #check if same vertical railway and not blocked by mountain range
                distance = pieceRow - row
                for vOffset in range(0, abs(distance)):
                    if self.layout[pieceRow - (int(distance / abs(distance)) * vOffset)][col] == "RW":
                        if self.tiles[row][col].getPiece() == None:
                            if not self.tiles[pieceRow - (int(distance / abs(distance)) * vOffset)][col].getPiece():
                                action = "move"
                            elif self.tiles[pieceRow - (int(distance / abs(distance)) * vOffset)][col].getPiece():
                                action = None
                                break
                        elif self.tiles[row][col].getPiece() != None and self.tiles[row][col].getPiece().getAlliance() != piece.getAlliance():
                            if not self.tiles[pieceRow - (int(distance / abs(distance)) * vOffset)][col].getPiece():
                                action = "attack"
                            elif self.tiles[pieceRow - (int(distance / abs(distance)) * vOffset)][col].getPiece():
                                action = None
                                break
                    else:
                        action = None
                        break
        #if currently on camp
        if self.layout[pieceRow][pieceCol] == "CP" and (up == (row, col) or dw == (row, col) or lf == (row, col) or rg == (row, col) or ul == (row, col) or ur == (row, col) or dl == (row, col) or dr == (row, col)):
            if not self.tiles[row][col].getPiece():
                action = "move"
            elif self.tiles[row][col].getPiece().getAlliance() != piece.getAlliance():
                action = "attack"
            elif self.tiles[row][col].getPiece().getAlliance() == piece.getAlliance():
                action = None
        #if moving to camp
        if self.layout[row][col] == "CP" and (up == (row, col) or dw == (row, col) or lf == (row, col) or rg == (row, col) or ul == (row, col) or ur == (row, col) or dl == (row, col) or dr == (row, col)):
            if not self.tiles[row][col].getPiece():
                action = "move"
            else:
                action = None
        #horizontal movement
        if lf == (row, col) or rg == (row, col):
            if not self.tiles[row][col].getPiece():
                action = "move"
            elif self.tiles[row][col].getPiece().getAlliance() != piece.getAlliance():
                action = "attack"
            elif self.tiles[row][col].getPiece().getAlliance() == piece.getAlliance():
                action = None
        #vertical movement
        if up == (row, col) or dw == (row, col):
            if up == (5, 1) or up == (5, 3) or dw == (6, 1) or dw == (6, 3):    #check if not blocked by mountain range
                action == None
            elif not self.tiles[row][col].getPiece():
                action = "move"
            elif self.tiles[row][col].getPiece().getAlliance() != piece.getAlliance():
                action = "attack"
            elif self.tiles[row][col].getPiece().getAlliance() == piece.getAlliance():
                action = None
        return action

    #AI random move
    def AImove(self):
        print('it is now AI turn')
        Turn = True
        randomPiece = None
        while Turn == True:
            rand_row = random.randint(0,11)
            rand_column = random.randint(0,4)

            moves_row = []
            moves_col = []
            randomPiece = self.tiles[rand_row][rand_column].getPiece()

            if randomPiece != None and randomPiece.toString() != 'Flag' and randomPiece.toString() != 'Landmine':
                if randomPiece.getAlliance() == 1:
                    #check all possible moves of that single randomPiece by scanning the whole board
                    for i in range(self.numCol):
                        for j in range(self.numRow):
                            if self.checkAvailableMovement(j,i,randomPiece,rand_row,rand_column) != None:
                                moves_row.append(j)
                                moves_col.append(i)
                    #Now pick a random move from the array moves
                    if len(moves_col) != 0:
                        rand_index = random.randint(0,(len(moves_col)-1))
                        action = self.checkAvailableMovement(moves_row[rand_index],moves_col[rand_index],randomPiece,rand_row,rand_column)
                        if  action == 'move':
                            if moves_col[rand_index] != rand_column and moves_row[rand_index] != rand_row: #Prevent choosing Original Place
                                self.tiles[moves_row[rand_index]][moves_col[rand_index]].setPiece(randomPiece)
                                self.tiles[rand_row][rand_column].setPiece(None)
                                print(randomPiece.toString() + ": Alliance " + str(randomPiece.getAlliance()) + " Moved from "
                                + str(rand_row) + "," + str(rand_column) + " to "
                                + str(moves_row[rand_index]) + "," + str(moves_col[rand_index]) + "\n"
                                )
                                Turn = False
                            else:
                                Turn = True
                        #if that availeble action is 'attack' then attack
                        if action == 'attack':
                            print(randomPiece.toString() + ": Alliance " + str(randomPiece.getAlliance()) + " Attacked from "
                            + str(rand_row) + "," + str(rand_column) + " to "
                            + str(moves_row[rand_index]) + "," + str(moves_col[rand_index]) + "\n"
                            )
                            attackPiece = randomPiece
                            defendPiece = self.tiles[moves_row[rand_index]][moves_col[rand_index]].getPiece()
                            winner = self.referee(attackPiece, defendPiece)   #referee should return either the winning piece or None if draw
                            self.tiles[moves_row[rand_index]][moves_col[rand_index]].setPiece(winner)
                            self.tiles[rand_row][rand_column].setPiece(None)
                            Turn = False
                elif randomPiece.getAlliance() == 0:
                    Turn = True
                else:
                    print('Error Occured: Exception')
                    break

    #handle mouse click
    def handleEvent(self, event):
        #handle event on board tiles
        for j in range(self.numCol):
            for i in range(self.numRow):
                outline_tile = False
                outlineColor_tile = None
                #if is hovering on button
                if 'hover' in self.tiles[i][j].handleEvent(event):
                    outline_tile = True
                    #setup phase
                    if self.gamePhase == 1:
                        if self.currentPiece:
                            if self.checkAvailablePlacement(i,j,self.currentPiece) and not self.tiles[i][j].getPiece():
                                outlineColor_tile = self.green
                            else:
                                outlineColor_tile = self.red
                        else:
                            outlineColor_tile = self.black
                    #play phase
                    if self.gamePhase == 2:
                        if self.currentPiece:
                            if self.checkAvailableMovement(i,j,self.currentPiece,self.pieceRow,self.pieceCol):
                                outlineColor_tile = self.green
                            else:
                                outlineColor_tile = self.red
                        else:
                            outlineColor_tile = self.black
                #if button is clicked
                if 'down' in self.tiles[i][j].handleEvent(event):
                    outline_tile = True
                    outlineColor_tile = self.blue
                    #setup phase
                    if self.gamePhase == 1:
                        #take the piece if the tile already contain a piece
                        if not self.currentPiece:
                            if self.tiles[i][j].getPiece():
                                self.currentPiece = self.tiles[i][j].getPiece()
                                self.tiles[i][j].setPiece(None)
                                self.movingPiece = True
                        #place the piece if the tile does not contain a piece
                        else:
                            if not self.tiles[i][j].getPiece():
                                if self.checkAvailablePlacement(i,j,self.currentPiece):
                                    self.tiles[i][j].setPiece(self.currentPiece)
                                    if not self.movingPiece:
                                        self.pieceData[self.currentPiece.toString()][0] = self.pieceData[self.currentPiece.toString()][0] - 1
                                    self.currentPiece = None
                                    self.movingPiece = False
                    #playing phase
                    elif self.gamePhase == 2:
                        #take the piece if the tile already contain a piece(except for landmine and flag)
                        if self.currentPiece == None:
                            if self.tiles[i][j].getPiece() and self.tiles[i][j].getPiece().toString() != "Landmine" and self.tiles[i][j].getPiece().toString() != "Flag":
                                self.currentPiece = self.tiles[i][j].getPiece()
                                self.pieceRow = i
                                self.pieceCol = j
                                self.tiles[i][j].setPiece(None)
                        else:
                            self.takeAction(self.checkAvailableMovement(i,j,self.currentPiece,self.pieceRow,self.pieceCol), (i,j))
                            #whenever the player's turn is over.. then the AI will take action
                            pygame.time.wait(500)
                            self.AImove()
                #if mouse exited a button
                if 'exit' in self.tiles[i][j].handleEvent(event):
                    outline_tile = False
                self.tiles[i][j].update(self.tiles[i][j].getColor(), outline_tile, outlineColor_tile)
        if self.gamePhase == 2 and self.currentPiece:
            self.tiles[self.pieceRow][self.pieceCol].setOutline(True, self.blue)

        #handle event on selection pane
        if self.gamePhase == 1:
            for k in range(len(self.selectionPaneTiles)):
                outline_select = False
                outlineColor_select = None
                #if is hovering on button
                if 'hover' in self.selectionPaneTiles[k].handleEvent(event):
                    outline_select = True
                    if self.currentPiece:
                        if self.selectionPaneTiles[k].getFlag() == self.currentPiece.toString():
                            outlineColor_select = self.green
                        else:
                            outlineColor_select = self.red
                    else:
                        outlineColor_select = self.black
                #if button is clicked
                if 'down' in self.selectionPaneTiles[k].handleEvent(event):
                    outline_select = True
                    outlineColor_select = self.blue
                #if button is clicked & released
                if 'click' in self.selectionPaneTiles[k].handleEvent(event):
                    if not self.currentPiece:
                        self.currentPiece = self.selectionPaneTiles[k].getPiece()
                        self.selectionPaneTiles[k].removePiece()
                    else:
                        if self.currentPiece.toString() == self.selectionPaneTiles[k].getFlag():
                            self.selectionPaneTiles[k].addPiece(self.currentPiece)
                            if self.movingPiece:
                                self.pieceData[self.currentPiece.toString()][0] = self.pieceData[self.currentPiece.toString()][0] + 1
                            self.currentPiece = None
                            self.movingPiece = False
                #if mouse exited a button
                if 'exit' in self.selectionPaneTiles[k].handleEvent(event):
                    outline_select = False
                self.selectionPaneTiles[k].update(self.selectionPaneTiles[k].getColor(), outline_select, outlineColor_select)

        #handle event on done button
        if self.gamePhase == 1:
            outline_done = False
            outlineColor_done = None
            #if is hovering on button
            if 'hover' in self.doneButton.handleEvent(event):
                outline_done = True
                outlineColor_done = self.black
            #if button is clicked
            if 'down' in self.doneButton.handleEvent(event):
                outline_done = True
                outlineColor_done = self.blue
            #if button is clicked & released
            if 'click' in self.doneButton.handleEvent(event):
                self.checkDone()
                print('You make the first move')
                #Bool variable to check turns
                #aiTurn = False
            #if mouse exited a button
            if 'exit' in self.doneButton.handleEvent(event):
                outline_done = False
            self.doneButton.update(self.doneButton.getColor(),outline_done,outlineColor_done)

    #referee will decide on the result of an attack action
    def referee(self,piece1, piece2):
        winner = None
        loser = None
        #checking alliances
        if piece1.alliance == piece2.alliance:
            print('You can not attack your own piece!\n')
        elif piece1.toString() != "Flag" and piece2.toString() != "Flag":
            #if engineer steps on a landmine
            if piece1.toString() == "Landmine" and piece2.toString() == "Engineer" or piece1.toString() == "Engineer" and piece2.toString() == "Landmine":
                print("Engineer has disarmed the landmine!\n")
                if piece1.toString() == "Engineer":
                    winner = piece1
                    loser = piece2
                else:
                    winner = piece2
                    loser = piece1
            #if Grenade attacks any piece
            elif piece1.toString() == "Grenade" or piece2.toString() == "Grenade":
                print("Both pieces have been taken")
                loser = piece1
            #if Grenade lands on Landmine
            elif piece1.toString() == "Landmine" and piece2.toString() == "Grenade" or piece1.toString() == "Grenade" and piece2.toString() == "Landmine":
                print("Both Landmine and Grenade are GONE!\n")
                loser = piece1
            #every other pieces of different or same rank battling
            elif piece1.rank < piece2.rank:
                print(piece1.toString() + " has taken " + piece2.toString() +"!\n")
                winner = piece1
                loser = piece2
            elif piece2.rank < piece1.rank:
                print(piece2.toString() + " has taken " + piece1.toString() + "!\n")
                winner = piece2
                loser = piece1
            elif piece2.rank == piece1.rank:
                print(piece2.toString() + " and " + piece1.toString() + " have both been taken!\n")
                loser = piece1
                loser.alliance=0
        #if Flag is captured
        elif piece1.toString() == "Flag":
            print(piece2.toString() + " has captured the Flag\n")
        elif piece2.toString() == "Flag":
            print(piece1.toString() + " has captured the Flag\n")

        if loser.alliance == 0  and self.pieceData[loser.toString()][0] == 0:
            k = 0
            for item in self.pieceData:
                if (self.selectionPaneTiles[k].getFlag() == loser.toString()):
                    self.selectionPaneTiles[k].addPiece(loser)
                k=k+1

        if loser.alliance == 0: # only draw my own piece
            self.pieceData[loser.toString()][0]=self.pieceData[loser.toString()][0]+1

        return winner

    #called whenever an action is executed
    def takeAction(self, action, dest):
        replacement = self.currentPiece
        i = dest[0]
        j = dest[1]
        if action:
            if action == "attack":
                attackPiece = self.currentPiece
                defendPiece = self.tiles[i][j].getPiece()
                replacement = self.referee(attackPiece, defendPiece)   #referee should return either the winning piece or None if draw
            self.tiles[i][j].setPiece(replacement)
            self.currentPiece = None
            self.pieceRow = None
            self.pieceCol = None

from AI import *
from pieces import *
from tile import *


class Board:
    def __init__(self, width, height, numRow, numCol):
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.blue = pygame.Color(0, 0, 255)
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
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
        # board
        brdImgPath = "bin\\board.png"
        orgBrdImg = pygame.image.load(brdImgPath)
        self.brdImg = pygame.transform.scale(orgBrdImg, (width * numCol, height * (numRow + 1)))
        # tile
        self.tiles = self.generateTiles()
        # selection pane
        self.selectionPaneTiles = self.generateSelectionPane()
        # holding piece
        self.currentPiece = None
        self.pieceRow = None
        self.pieceCol = None
        # moving piece
        self.movingPiece = False
        # done button
        self.doneButton = Tile(1200 - 115, 716 - 55, 100, 40, self.red, text="Done")
        # Auto player piece setup
        self.plySetup1 = Tile(1200 - 375, 716 - 55, 110, 40, self.green, text="Setup 1")
        self.plySetup2 = Tile(1200 - 245, 716 - 55, 110, 40, self.green, text="Setup 2")
        self.clear = Tile(1200 - 335, 716 - 105, 170, 40, self.green, text="Undo Setup")
        # record game phase
        self.gamePhase = 1
        # AI player
        self.ai = None
        # AI condition
        self.aiMoved = False
        self.aiLastMove = [None, None]  # [start, dest]
        # sound effects
        self.friendFire = '.\\bin\\Friendly Fire.wav'
        self.explosion = '.\\bin\\explosion.wav'
        self.shoot = '.\\bin\\fire.wav'
        self.ticking = '.\\bin\\TickingBomb.wav'
        self.win = None
        # combat log
        self.log = [None, None, None]

    # assign attributes to each tiles
    def generateLayout(self):
        # Set all as Soldier Station
        layout = [["SS" for i in range(self.numCol)] for j in range(self.numRow)]

        # Set Railway
        for i in range(1, self.numRow - 1):
            layout[i][0] = "RW"
            layout[i][4] = "RW"
        for j in range(1, self.numCol - 1):
            layout[1][j] = "RW"
            layout[5][j] = "RW"
            layout[6][j] = "RW"
            layout[10][j] = "RW"

        # Set Camp
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

        # Set Headquarters
        layout[0][1] = "HQ"
        layout[0][3] = "HQ"
        layout[11][1] = "HQ"
        layout[11][3] = "HQ"

        return layout

    # write text
    def write_text(self, x, y, text, textcolor, fontsize, surface):
        if text:
            titleTextObj = pygame.font.Font(".\\bin\\Becker.ttf", fontsize)
            titleTextSurfaceObj = titleTextObj.render(text, True, textcolor)
            titleTextRectObj = titleTextSurfaceObj.get_rect()
            titleTextRectObj.center = (x, y)
            surface.blit(titleTextSurfaceObj, titleTextRectObj)

    # play sound effect
    def play(self, sound):
        sounds = pygame.mixer.Sound(sound)
        pygame.mixer.Sound.play(sounds)
        pygame.mixer_music.set_volume(0.25)

    # create tiles for board
    def generateTiles(self):
        tiles = []
        for j in range(self.numRow):
            x = []
            for i in range(self.numCol):
                if j >= 6:
                    x.append(Tile(i * self.width, (j + 1) * self.height, self.width, self.height, transparent=True))
                else:
                    x.append(Tile(i * self.width, j * self.height, self.width, self.height, transparent=True))
            tiles.append(x)
        return tiles

    # draws text and pieces beside board
    def generateSelectionPane(self):
        selectionPaneTiles = [None for _ in range(12)]
        x = 660
        y = 200
        i = 0
        for item in self.pieceData:
            selectionPaneTiles[i] = SelectionPaneTile(x, y, 50, 50, color=(255, 255, 0), nPieces=self.pieceData[item][0])
            for _ in range(self.pieceData[item][0]):
                selectionPaneTiles[i].addPiece(self.spawnPiece(0, item, selectionPaneTiles[i].getPos()))
            selectionPaneTiles[i].setFlag(item)
            i = i + 1
            if x > 1000:
                x = 660
                y += 150
                # go to new line
            else:
                x += 120

        return selectionPaneTiles

    # spawn an object of the piece at the position
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

    # check if the player setup is complete
    def checkDone(self):
        complete = False
        if self.currentPiece is None:
            for k in self.pieceData:
                if self.pieceData[k][0] == 0:
                    complete = True
                else:
                    break
            if complete:
                self.ai = AI(self)  # initialize AI
                self.ai.placePieces()
                self.gamePhase = 2

    # Draw the entire interface
    def draw(self, surface):
        # Draw board
        surface.blit(self.brdImg, (0, 0))
        # Show Controls
        self.write_text(1200 - 610, 30, '[ESC = PAUSE]', self.white, 23, surface)
        # Show referee log:
        if self.gamePhase == 2:
            self.write_text(1200 - 530, 716 - 50, 'REFEREE LOG:', self.green, 23, surface)
        # Show combat log
        self.write_text(1200 - 200, 716 - 75, self.log[-3], self.white, 20, surface)
        self.write_text(1200 - 200, 716 - 50, self.log[-2], self.white, 20, surface)
        self.write_text(1200 - 200, 716 - 25, self.log[-1], self.white, 20, surface)
        # Draw tiles
        for j in range(self.numCol):
            for i in range(self.numRow):
                self.tiles[i][j].draw(surface)
        # Only draw Selection Pane on setup phase
        # Draw Selection Pane
        # Draw Selection Pane Title
        titleTextObj = pygame.font.Font(".\\bin\\Becker.ttf", 38)
        if self.gamePhase == 1:
            title = "PIECES"
        else:
            title = "DEAD PIECES"
        titleTextSurfaceObj = titleTextObj.render(title, True, self.white)
        titleTextRectObj = titleTextSurfaceObj.get_rect()
        titleTextRectObj.center = (860, 75)
        surface.blit(titleTextSurfaceObj, titleTextRectObj)
        # Draw Selection Pane Tiles
        k = 0
        for item in self.pieceData:
            # Draw piece image
            self.selectionPaneTiles[k].draw(surface)
            # Draw Selection Pane piece's name
            textObj = pygame.font.Font(".\\bin\\Becker.ttf", 18)
            textSurfaceObj = textObj.render(item, True, self.white)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = tuple(x + y for x, y in zip(self.selectionPaneTiles[k].getPos(), (25, -25)))
            surface.blit(textSurfaceObj, textRectObj)
            # Draw number of piece remaining
            numTextSurfaceObj = textObj.render("x " + str(self.pieceData[item][0]), True, self.white)
            numTextRectObj = numTextSurfaceObj.get_rect()
            numTextRectObj.center = tuple(x + y for x, y in zip(self.selectionPaneTiles[k].getPos(), (25, 75)))
            surface.blit(numTextSurfaceObj, numTextRectObj)
            k = k + 1

        if self.currentPiece:
            mousePos = pygame.mouse.get_pos()
            cursorImg = pygame.image.load(self.currentPiece.getPath())
            surface.blit(cursorImg, tuple(x + y for x, y in zip(mousePos, (-25, -25))))

        if self.gamePhase == 1:
            self.doneButton.draw(surface)
            self.plySetup1.draw(surface)
            self.plySetup2.draw(surface)
            self.clear.draw(surface)

    # check if piece placement is valid
    def checkAvailablePlacement(self, row, col, piece):
        if row < 6:
            # opposite territory
            return False
        if self.layout[row][col] == "CP":
            # cannot be initialise at camps
            return False
        if piece.toString() == "Flag" and self.layout[row][col] != "HQ":
            # flag can only be placed in headquarters
            return False
        if piece.toString() == "Landmine" and not (row == 10 or row == 11):
            # landmine can only be initailize at last 2 rows
            return False
        if piece.toString() == "Grenade" and row == 6:
            # grenade cannot be placed at 1st row
            return False
        return True

    # check for game over
    def checkGameOver(self, alliance):
        currentState = {}
        for i in range(self.numRow):
            for j in range(self.numCol):  # check entire board for pieces of the alliance
                if self.tiles[i][j].getPiece() is not None and self.tiles[i][j].getPiece().getAlliance() == alliance:  # get the alliance's piece
                    currentState[self.tiles[i][j].getPiece()] = [(i, j), None]

        for piece in currentState:
            currentRow, currentCol = currentState[piece][0]
            for i in range(self.numRow):
                for j in range(self.numCol):  # check entire board for alliance's piece movement
                    action = self.checkAvailableMovement(i, j, piece, currentRow, currentCol,
                                                         False)  # not checking for engineer to save compute time
                    if action is not None and action != "no move":
                        return False  # not game over
        return True

    # check if movement is vailable
    def checkAvailableMovement(self, row, col, piece, pieceRow, pieceCol, checkEngineer=True):
        action = None  # action is either "attack" or "move" or "no move" or None for invalid action
        # pos = (row, col)
        ul = (pieceRow - 1, pieceCol - 1)  # upperleft
        up = (pieceRow - 1, pieceCol)  # up
        ur = (pieceRow - 1, pieceCol + 1)  # upperright
        lf = (pieceRow, pieceCol - 1)  # left
        og = (pieceRow, pieceCol)  # original
        rg = (pieceRow, pieceCol + 1)  # right
        dl = (pieceRow + 1, pieceCol - 1)  # downleft
        dw = (pieceRow + 1, pieceCol)  # down
        dr = (pieceRow + 1, pieceCol + 1)  # downright
        if piece.toString() == "Landmine" or piece.toString() == "Flag":
            return None  # landmine and flag cannot be move
        # if no move
        elif og == (row, col):
            return "no move"
        # if engineer on railway
        elif checkEngineer and self.layout[pieceRow][pieceCol] == "RW" and self.layout[row][col] == "RW" and piece.toString() == "Engineer":
            railwayGraph = {}  # will contain adjacent nodes of the pos ({0 : [1, 10], ...})
            index = 0  # label the nodes (key for railwayGraph)
            railwayList = []  # will contain all railway counting up to down, left to right ([(row, col), ...]) (railwayList[vertex] will have result for the location of railway)
            # initialise railwayList
            for j in range(self.numCol):
                for i in range(self.numRow):
                    if self.layout[i][j] == "RW":
                        railwayList.append((i, j))
            # generate the graph of railways
            for j in range(self.numCol):
                for i in range(self.numRow):
                    if self.layout[i][j] == "RW":
                        directions = {"right": (i, j + 1),
                                      "down": (i + 1, j),
                                      "left": (i, j - 1),
                                      "up": (i - 1, j)}  # save adjacent tiles
                        rw_adj = []  # save adjacent railway tiles
                        for direction in directions:  # loop all 4 directions
                            if self.numRow > directions[direction][0] >= 0 <= directions[direction][1] < self.numCol and \
                                    self.layout[directions[direction][0]][
                                        directions[direction][1]] == "RW":  # check if adjacent tiles is railway
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
                        rw_adj.sort()  # sort to improve DFS consistency
                        railwayGraph[index] = rw_adj
                        index = index + 1

            # search path to dest using DFS
            def DFS_checkAvailableMovement(graph, start, dest):
                stack = [start]
                path = []
                while stack:
                    if dest in path:
                        break  # return as soon as a path has been find
                    vertex = stack.pop()
                    if self.tiles[railwayList[vertex][0]][railwayList[vertex][1]].getPiece():
                        if self.tiles[railwayList[vertex][0]][railwayList[vertex][1]].getPiece().getAlliance() != piece.getAlliance():
                            path.append(vertex)  # add to path if is opponent piece
                        continue  # don't expand vertices with pieces on them
                    for neighbour in graph[vertex]:
                        if neighbour in path:
                            continue  # ignore discovered vertices
                        if neighbour in stack:
                            continue  # ignore discovered vertices
                        stack.append(neighbour)
                    path.append(vertex)
                return path

            start = railwayList.index((pieceRow, pieceCol))  # get the corresponding vertices
            dest = railwayList.index((row, col))  # get the corresponding vertices
            path = DFS_checkAvailableMovement(railwayGraph, start, dest)
            if dest in path:
                if not self.tiles[row][col].getPiece():
                    action = "move"
                elif self.tiles[row][col].getPiece().getAlliance() != piece.getAlliance():
                    action = "attack"
                elif self.tiles[row][col].getPiece().getAlliance() == piece.getAlliance():
                    action = None
        # if on railway
        elif self.layout[pieceRow][pieceCol] == "RW" and self.layout[row][col] == "RW":
            if pieceRow == row:  # check if same horizontal railway
                distance = pieceCol - col
                for hOffset in range(abs(distance)):
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
                            elif self.tiles[row][pieceCol - (int(distance / abs(distance)) * hOffset)].getPiece():
                                action = None
                                break
                    else:
                        action = None
                        break
            if pieceCol == col and not (col == 1 or col == 3):  # check if same vertical railway and not blocked by mountain range
                distance = pieceRow - row
                for vOffset in range(abs(distance)):
                    if self.layout[pieceRow - (int(distance / abs(distance)) * vOffset)][col] == "RW":
                        if not self.tiles[row][col].getPiece():
                            if not self.tiles[pieceRow - (int(distance / abs(distance)) * vOffset)][col].getPiece():
                                action = "move"
                            elif self.tiles[pieceRow - (int(distance / abs(distance)) * vOffset)][col].getPiece():
                                action = None
                                break
                        elif self.tiles[row][col].getPiece() and self.tiles[row][
                            col].getPiece().getAlliance() != piece.getAlliance():
                            if not self.tiles[pieceRow - (int(distance / abs(distance)) * vOffset)][col].getPiece():
                                action = "attack"
                            elif self.tiles[pieceRow - (int(distance / abs(distance)) * vOffset)][col].getPiece():
                                action = None
                                break
                    else:
                        action = None
                        break
        # if currently on camp
        elif self.layout[pieceRow][pieceCol] == "CP" and (
                up == (row, col) or dw == (row, col) or lf == (row, col) or
                rg == (row, col) or ul == (row, col) or ur == (row, col) or
                dl == (row, col) or dr == (row, col)):
            if not self.tiles[row][col].getPiece():
                action = "move"
            elif self.tiles[row][col].getPiece().getAlliance() != piece.getAlliance():
                action = "attack"
            elif self.tiles[row][col].getPiece().getAlliance() == piece.getAlliance():
                action = None
        # if moving to camp
        elif self.layout[row][col] == "CP" and (
                up == (row, col) or dw == (row, col) or lf == (row, col) or
                rg == (row, col) or ul == (row, col) or ur == (row, col) or
                dl == (row, col) or dr == (row, col)):
            if not self.tiles[row][col].getPiece():
                action = "move"
            else:
                action = None
        # horizontal movement
        elif lf == (row, col) or rg == (row, col):
            if not self.tiles[row][col].getPiece():
                action = "move"
            elif self.tiles[row][col].getPiece().getAlliance() != piece.getAlliance():
                action = "attack"
            elif self.tiles[row][col].getPiece().getAlliance() == piece.getAlliance():
                action = None
        # vertical movement
        elif up == (row, col) or dw == (row, col):
            if up == (5, 1) or up == (5, 3) or dw == (6, 1) or dw == (6, 3):  # check if not blocked by mountain range
                var = action is None
            elif not self.tiles[row][col].getPiece():
                action = "move"
            elif self.tiles[row][col].getPiece().getAlliance() != piece.getAlliance():
                action = "attack"
            elif self.tiles[row][col].getPiece().getAlliance() == piece.getAlliance():
                action = None
        return action

    # handle mouse click
    def handleEvent(self, event):
        # handle event on board tiles
        for j in range(self.numCol):
            for i in range(self.numRow):
                outline_tile = False
                outlineColor_tile = None
                # if is hovering on tile
                if 'hover' in self.tiles[i][j].handleEvent(event):
                    outline_tile = True
                    # setup phase
                    if self.gamePhase == 1:
                        if self.currentPiece:
                            if self.checkAvailablePlacement(i, j, self.currentPiece) and not self.tiles[i][j].getPiece():
                                outlineColor_tile = self.green
                            else:
                                outlineColor_tile = self.red
                        else:
                            outlineColor_tile = self.black
                    # play phase
                    if self.gamePhase == 2:
                        if self.currentPiece:
                            if self.checkAvailableMovement(i, j, self.currentPiece, self.pieceRow, self.pieceCol):
                                outlineColor_tile = self.green
                            else:
                                outlineColor_tile = self.red
                        else:
                            outlineColor_tile = self.black
                # if tile is clicked
                if 'down' in self.tiles[i][j].handleEvent(event):
                    outline_tile = True
                    outlineColor_tile = self.blue
                # if tile is clicked & released
                if 'click' in self.tiles[i][j].handleEvent(event):
                    self.aiMoved = False
                    # setup phase
                    if self.gamePhase == 1:
                        # take the piece if the tile already contain a piece
                        if not self.currentPiece:
                            if self.tiles[i][j].getPiece():
                                self.currentPiece = self.tiles[i][j].getPiece()
                                self.tiles[i][j].setPiece(None)
                                self.movingPiece = True
                        # place the piece if the tile does not contain a piece
                        else:
                            if not self.tiles[i][j].getPiece():
                                if self.checkAvailablePlacement(i, j, self.currentPiece):
                                    self.tiles[i][j].setPiece(self.currentPiece)
                                    if not self.movingPiece:
                                        self.pieceData[self.currentPiece.toString()][0] = \
                                            self.pieceData[self.currentPiece.toString()][0] - 1
                                    self.currentPiece = None
                                    self.movingPiece = False
                    # playing phase
                    elif self.gamePhase == 2:
                        # take the piece if the tile already contain a piece(except for landmine and flag)
                        if not self.currentPiece:
                            if self.tiles[i][j].getPiece() and self.tiles[i][j].getPiece().getAlliance() != 1 and \
                                    self.tiles[i][j].getPiece().toString() != "Landmine" and self.tiles[i][j].getPiece().toString() != "Flag":
                                self.currentPiece = self.tiles[i][j].getPiece()
                                self.pieceRow = i
                                self.pieceCol = j
                                self.tiles[i][j].setPiece(None)
                        else:
                            if self.checkGameOver(0):  # check my available movement before taking an action
                                self.win = False
                                return
                            if self.takeAction(self.currentPiece,
                                               self.checkAvailableMovement(i, j, self.currentPiece, self.pieceRow,
                                                                           self.pieceCol), (i, j)):
                                # whenever the player's turn is over.. then the AI will make move
                                pygame.time.wait(1500)
                                if self.checkGameOver(1):
                                    self.win = True
                                    return
                                start, dest = self.ai.makeMove()
                                self.aiLastMove = [start, dest]
                                self.aiMoved = True
                # if mouse exited a tile
                if 'exit' in self.tiles[i][j].handleEvent(event):
                    outline_tile = False
                self.tiles[i][j].update(self.tiles[i][j].getColor(), outline_tile, outlineColor_tile)

            # Highlight orgin position
            if self.gamePhase == 2 and self.currentPiece:
                self.tiles[self.pieceRow][self.pieceCol].setOutline(True, self.blue)
            # Highlight AI's last move
            if self.aiMoved:
                self.tiles[self.aiLastMove[0][0]][self.aiLastMove[0][1]].setOutline(True, self.blue)
                self.tiles[self.aiLastMove[1][0]][self.aiLastMove[1][1]].setOutline(True, self.blue)

        # handle event on selection pane
        if self.gamePhase == 1:
            for k in range(len(self.selectionPaneTiles)):
                outline_select = False
                outlineColor_select = None
                # if is hovering on tile
                if 'hover' in self.selectionPaneTiles[k].handleEvent(event):
                    outline_select = True
                    if self.currentPiece:
                        if self.selectionPaneTiles[k].getFlag() == self.currentPiece.toString():
                            outlineColor_select = self.green
                        else:
                            outlineColor_select = self.red
                    else:
                        outlineColor_select = self.black
                # if tile is clicked
                if 'down' in self.selectionPaneTiles[k].handleEvent(event):
                    outline_select = True
                    outlineColor_select = self.blue
                # if tile is clicked & released
                if 'click' in self.selectionPaneTiles[k].handleEvent(event):
                    if not self.currentPiece:
                        self.currentPiece = self.selectionPaneTiles[k].getPiece()
                        self.selectionPaneTiles[k].removePiece()
                    else:
                        if self.currentPiece.toString() == self.selectionPaneTiles[k].getFlag():
                            self.selectionPaneTiles[k].addPiece(self.currentPiece)
                            if self.movingPiece:
                                self.pieceData[self.currentPiece.toString()][0] = \
                                    self.pieceData[self.currentPiece.toString()][0] + 1
                            self.currentPiece = None
                            self.movingPiece = False
                # if mouse exited a tile
                if 'exit' in self.selectionPaneTiles[k].handleEvent(event):
                    outline_select = False
                self.selectionPaneTiles[k].update(self.selectionPaneTiles[k].getColor(), outline_select,
                                                  outlineColor_select)

        # handle event on done button
        if self.gamePhase == 1:
            outline_done = False
            outlineColor_done = None
            # if is hovering on button
            if 'hover' in self.doneButton.handleEvent(event):
                outline_done = True
                outlineColor_done = self.black
            # if button is clicked
            if 'down' in self.doneButton.handleEvent(event):
                outline_done = True
                outlineColor_done = self.blue
            # if button is clicked & released
            if 'click' in self.doneButton.handleEvent(event):
                self.checkDone()
            # if mouse exited a button
            if 'exit' in self.doneButton.handleEvent(event):
                outline_done = False
            self.doneButton.update(self.doneButton.getColor(), outline_done, outlineColor_done)

        # handle event on auto piece setup1 for player
        if self.gamePhase == 1:
            outline_done = False
            outlineColor_done = None
            # if is hovering on plySetup1
            if 'hover' in self.plySetup1.handleEvent(event):
                outline_done = True
                outlineColor_done = self.black
            # if plySetup1 is clicked
            if 'down' in self.plySetup1.handleEvent(event):
                outline_done = True
                outlineColor_done = self.blue
            # if plySetup1 is clicked & released
            if 'click' in self.plySetup1.handleEvent(event):
                self.autoSetup1()
            # if mouse exited a plySetup1
            if 'exit' in self.plySetup1.handleEvent(event):
                outline_done = False
            self.plySetup1.update(self.plySetup1.getColor(), outline_done, outlineColor_done)

        # handle event on auto piece setup2 for player
        if self.gamePhase == 1:
            outline_done = False
            outlineColor_done = None
            # if is hovering on plySetup2
            if 'hover' in self.plySetup2.handleEvent(event):
                outline_done = True
                outlineColor_done = self.black
            # if plySetup2 is clicked
            if 'down' in self.plySetup2.handleEvent(event):
                outline_done = True
                outlineColor_done = self.blue
            # if plySetup2 is clicked & released
            if 'click' in self.plySetup2.handleEvent(event):
                self.autoSetup2()
            # if mouse exited a plySetup2
            if 'exit' in self.plySetup2.handleEvent(event):
                outline_done = False
            self.plySetup2.update(self.plySetup2.getColor(), outline_done, outlineColor_done)

        # handle event on clear button
        if self.gamePhase == 1:
            outline_done = False
            outlineColor_done = None
            # if is hovering on Clear
            if 'hover' in self.clear.handleEvent(event):
                outline_done = True
                outlineColor_done = self.black
            # if clear is clicked
            if 'down' in self.clear.handleEvent(event):
                outline_done = True
                outlineColor_done = self.blue
            # if clear is clicked & released
            if 'click' in self.clear.handleEvent(event):
                self.undoSetup()
            # if mouse exited a clear
            if 'exit' in self.clear.handleEvent(event):
                outline_done = False
            self.clear.update(self.clear.getColor(), outline_done, outlineColor_done)

    # referee will decide on the result of an attack action
    def referee(self, attackPiece, defendPiece):
        winner = None  # winner = None when draw
        loser = None  # loser = player piece when draw
        # if none of the pieces are flag
        if attackPiece.toString() != "Flag" and defendPiece.toString() != "Flag":
            # if engineer steps on a landmine
            if attackPiece.toString() == "Landmine" and defendPiece.toString() == "Engineer" or attackPiece.toString() == "Engineer" and defendPiece.toString() == "Landmine":
                if attackPiece.getAlliance() == 0:  # when player disarm a landmine
                    self.play(self.ticking)  # play sound effect
                    self.log.append("Your engineer has disarmed a landmine!")
                if attackPiece.toString() == "Engineer":
                    winner = attackPiece
                    loser = defendPiece
                else:
                    winner = defendPiece
                    loser = attackPiece
            # if Grenade or Landmine attacks any piece
            elif attackPiece.toString() == "Grenade" or attackPiece.toString() == "Landmine" or defendPiece.toString() == "Grenade" or defendPiece.toString() == "Landmine":
                if attackPiece.getAlliance() != 0:
                    self.log.append("Your " + defendPiece.toString() + " and enemy were taken")
                else:
                    self.play(self.shoot)
                    self.log.append("Your " + attackPiece.toString() + " and enemy were taken")
                if attackPiece.getAlliance() == 0 and (
                        attackPiece.toString() == "Landmine" or attackPiece.toString() == "Grenade"):
                    self.play(self.explosion)
                if attackPiece.getAlliance() == 0:
                    loser = attackPiece
                    self.ai.lostPiece = defendPiece
                else:
                    loser = defendPiece
                    self.ai.lostPiece = attackPiece
            # if attacking piece won
            elif attackPiece.getRank() < defendPiece.getRank():
                if attackPiece.getAlliance() == 0:
                    self.play(self.shoot)
                    self.log.append("Your " + attackPiece.toString() + " has taken an enemy piece")
                else:
                    self.log.append("An enemy piece has taken your " + defendPiece.toString())
                winner = attackPiece
                loser = defendPiece
            # if attacking piece lost
            elif defendPiece.getRank() < attackPiece.getRank():
                if attackPiece.getAlliance() == 0:
                    self.play(self.shoot)
                    self.log.append("An enemy piece has taken your " + attackPiece.toString())
                else:
                    self.log.append("Your " + defendPiece.toString() + " has taken an enemy piece")
                winner = defendPiece
                loser = attackPiece
            # if draw
            elif defendPiece.getRank() == attackPiece.getRank():
                if attackPiece.getAlliance() == 0:
                    self.play(self.shoot)
                    self.log.append("Your " + attackPiece.toString() + " and an enemy is taken")
                else:
                    self.log.append("Your " + defendPiece.toString() + " and an enemy is taken")
                if attackPiece.getAlliance() == 0:
                    loser = attackPiece
                    self.ai.lostPiece = defendPiece
                else:
                    loser = defendPiece
                    self.ai.lostPiece = attackPiece
        # if flag is attacked
        else:
            if attackPiece.getAlliance() == 0:
                print("Player has won\n")
                self.win = True
            else:
                print("Computer has won\n")
                self.win = False

            winner = attackPiece
            loser = defendPiece
            return winner, loser

        # add piece's portrait back to selection pane
        if loser.getAlliance() == 0 and self.pieceData[loser.toString()][0] == 0:
            k = 0
            for item in self.pieceData:
                if self.selectionPaneTiles[k].getFlag() == loser.toString():
                    self.selectionPaneTiles[k].addPiece(loser)
                k = k + 1

        if loser.getAlliance() == 0:  # only draw my own piece
            self.pieceData[loser.toString()][0] = self.pieceData[loser.toString()][0] + 1

        return winner, loser

    # called whenever an action is executed
    def takeAction(self, piece, action, dest, prediction=True):
        winner = None
        loser = None
        i = dest[0]
        j = dest[1]
        if action:
            if action == "attack":
                attackPiece = piece
                defendPiece = self.tiles[i][j].getPiece()
                winner, loser = self.referee(attackPiece, defendPiece)  # winner = None, loser = attackPiece if draw
                if self.win:
                    return
                self.tiles[i][j].setPiece(winner)
            else:
                if action == "move" and piece.getAlliance() == 1:
                    self.log.append("The enemy moved")
                self.tiles[i][j].setPiece(piece)
            self.ai.updatePrediction(winner, loser, self.currentPiece, (self.pieceRow, self.pieceCol), dest)
            self.currentPiece = None
            self.pieceRow = None
            self.pieceCol = None
            if action == "no move":
                return False
            else:
                return True
        else:
            return False

    def autoSetup1(self):
        piecePosition = ["Commander", "Commander", "Landmine", "Flag", "Landmine",
                         "Commander", "Engineer", "Captain", "Landmine", "Captain",
                         "Major", None, "Major", None, "Captain",
                         "Brigadier", "Colonel", None, "Brigadier", "Marshal",
                         "Lieutenant", None, "Grenade", None, "Grenade",
                         "General", "Engineer", "Colonel", "Engineer", "Lieutenant"]
        y = 11
        x = 0
        for piece in piecePosition:
            if x < self.numCol:
                self.tiles[y][x].setPiece(self.spawnPiece(0, piece, self.tiles[y][x].getPos))
                x = x + 1
            if x == self.numCol:
                x = 0
                y = y - 1
        for k in range(len(self.selectionPaneTiles)):
            self.selectionPaneTiles[k].removeAll()
        for item in self.pieceData:
            self.pieceData[item] = [0]

    def autoSetup2(self):
        piecePosition = ["Captain", "Flag", "Colonel", "Commander", "Captain",
                         "Landmine", "Landmine", "Landmine", "Major", "Commander",
                         "Captain", None, "Commander", None, "Colonel",
                         "Engineer", "Brigadier", None, "Brigadier", "Engineer",
                         "Grenade", None, "Grenade", None, "Major",
                         "Lieutenant", "Marshal", "General", "Engineer", "Lieutenant"]
        y = 11
        x = 0
        for piece in piecePosition:
            if x < self.numCol:
                self.tiles[y][x].setPiece(self.spawnPiece(0, piece, self.tiles[y][x].getPos))
                x = x + 1
            if x == self.numCol:
                x = 0
                y = y - 1
        for k in range(len(self.selectionPaneTiles)):
            self.selectionPaneTiles[k].removeAll()
        for item in self.pieceData:
            self.pieceData[item] = [0]

    def undoSetup(self):
        y = 11
        x = 0
        for i in range(30):
            if x < self.numCol:
                self.tiles[y][x].setPiece(None)
                x = x + 1
            if x == self.numCol:
                x = 0
                y = y - 1
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
        self.selectionPaneTiles = self.generateSelectionPane()

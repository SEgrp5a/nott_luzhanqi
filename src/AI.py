import pygame
import operator
import numpy.random as rng
from pieces import *

class AI():
    rankData = {"Flag": [0],
                "Grenade": [0],
                "Landmine": [0],
                "Marshal": [1],
                "General": [2],
                "Lieutenant": [3],
                "Brigadier": [4],
                "Colonel": [5],
                "Major": [6],
                "Captain": [7],
                "Commander": [8],
                "Engineer": [9]}

    def __init__(self, board):
        self.brd = board    #get Board reference
        self.currentPiece = None
        self.lostPiece = None   #record what piece is lost this round
        self.prediction = self.getPrediction()
        self.playerDeadPieces = []
        self.moveHeuristic = [[2,1,2,1,2],
                              [2,2,2,2,2],
                              [2,2,1,2,2],
                              [2,1,2,1,2],
                              [2,2,1,2,2],
                              [2,2,2,2,2],
                              [3,3,3,3,3],
                              [3,2,1,2,3],
                              [3,1,2,1,3],
                              [3,2,1,2,3],
                              [4,5,4,5,4],
                              [5,1,5,1,5]] #subject to change
        self.criticalPos = [(0,0),(0,2),(0,4),(1,0),(1,1),(1,2),(1,3),(1,4)] #location with danger of game over
    
    #generate prediction matrix
    def getPrediction(self):
        prediction = {}
        for i in range(int(self.brd.numRow/2),self.brd.numRow):
            for j in range(self.brd.numCol):
                default = ["Marshal", "General", "Lieutenant",
                           "Brigadier", "Colonel", "Major",
                           "Captain", "Commander", "Engineer"]
                playerPiece = self.brd.tiles[i][j].getPiece()
                if playerPiece:
                    prediction[playerPiece] = default
                    if self.brd.layout[i][j] == 'HQ':
                        #add Flag to prediction if at HQ
                        prediction[playerPiece].append('Flag')
                    if i >= 10:
                        #add Landmine to prediction if at last 2 rows
                        prediction[playerPiece].append('Landmine')
                    if i > 6:
                        #add Grenade to prediction if not at 1st row
                        prediction[playerPiece].append('Grenade')
        return prediction

    #update prediction matrix for each move
    def updatePrediction(self, winner, loser, playerPiece, ori, dest):
        #if round lost
        if winner and winner.getAlliance() == 0:
            if loser.toString() == 'Landmine':
                self.prediction[winner] = ['Engineer']
            else:
                for item in self.rankData:
                    if loser.getRank() <= self.rankData[item][0]:
                        if item in self.prediction[winner]:
                            self.prediction[winner].remove(item)
                        #landmine and grenade won't produce a winner
                        if 'Grenade' in self.prediction[winner]:
                            self.prediction[winner].remove('Grenade')
        #if round win
        elif winner and winner.getAlliance() == 1:
            if loser:
                self.playerDeadPieces.append(loser)
            if winner.toString() == 'Engineer':
                self.prediction[loser] = ['Landmine']
            else:
                for item in self.rankData:
                    if winner.getRank() >= self.rankData[item][0]:
                        if item in self.prediction[loser]:
                            self.prediction[loser].remove(item)
        #if round draw
        elif not winner and loser:
            self.playerDeadPieces.append(loser)
            #if lost unit other than landmine & grenade
            if self.lostPiece.toString() != 'Landmine' and self.lostPiece.toString() != 'Grenade':
                for item in self.rankData:
                    if item != self.lostPiece.toString() and item != 'Grenade' and item != 'Landmine':
                        if item in self.prediction[loser]:
                            self.prediction[loser].remove(item)
        #if player piece moved
        if ori != dest and playerPiece:
            #playerPiece won't be flag or landmine if it is moved
            if 'Landmine' in self.prediction[playerPiece]:
                self.prediction[playerPiece].remove('Landmine')
            if 'Flag' in self.prediction[playerPiece]:
                self.prediction[playerPiece].remove('Flag')
            #playerPiece is engineer if can move along corner of RW 
            if ori[0] != dest[0] and ori[1] != dest[1] and (self.brd.layout[ori[0]][ori[1]] != 'CP' and self.brd.layout[dest[0]][dest[1]] != 'CP'):
                self.prediction[playerPiece] = ['Engineer']

        self.lostPiece = None
        self.currentPiece = None
    
    #calculate payoff if piece is attacking
    def calcAttack(self,piece,myRank,enemies): # receives current piece,current piece rank, list of pieces the opponent can be
        willLoseTo = 0
        worth = 0 # for if my piece is grenade
        # If the enemy piece has a chance to be a flag, attack immediately if possible
        if "Flag" in enemies: 
            return 5
        for enemy in enemies:
            enemyRank = self.rankData[str(enemy)]
            if piece.toString() == "Grenade" and enemyRank[0] < 4: # grenade should try to fight pieces with higher power (lieutenant and above)
                worth = worth + 1 # could be a high level piece
            elif myRank > enemyRank[0]:  # rank higher = power lower
                willLoseTo = willLoseTo + 1 # records the pieces it will lose to

        if piece.toString() == "Grenade":
            if (len(enemies) - worth) == 0: # unless I know it is a lieutenant or higher power, i will not attack
                return 1
            else:
                return 0
        else:
            success = 1 - (willLoseTo/len(enemies)) # returns the probability of winning the battle
        if success > 0.8: # if it has a 80% chance of winning
            return success
        else:
            return success-0.5 #lower the success rate to deter the move

    #generate possible moves and calculate its payoff the return as a list
    def generateMoves(self,piece,orgin,checkEngineer):
        moves = []
        (currentRow, currentCol) = orgin

        for i in range(self.brd.numRow):  #i ,j = destination
            for j in range(self.brd.numCol):
                attackPayOff = 0 # incentive to attack
                movePayOff = 0 # incentive to move
                self.brd.tiles[currentRow][currentCol].setPiece(None) # to ignore counting the current place as a dead end
                action = self.brd.checkAvailableMovement(i,j,piece,currentRow,currentCol,checkEngineer) # checks for all available moves in the map
                self.brd.tiles[currentRow][currentCol].setPiece(piece)

                if action != None and action != "no move": # if the piece can move here or attack this piece
                    movePayOff = self.moveHeuristic[i][j]
                    if action == "attack": #if there is a piece on this tile to attack
                        attackPayOff = self.calcAttack(piece, piece.getRank(), self.prediction[self.brd.tiles[i][j].getPiece()]) # calculates the possibility of winning the fight
                        #if the enemy piece is at a critical position which could result in a loss
                        if (i,j) in self.criticalPos:
                            attackPayOff = attackPayOff * 5 #attack to prevent losing the game
                    #calculate payoff
                    payOff = movePayOff + attackPayOff
                    moves.append(((i,j),payOff,action)) #stores the dest, payoff & action of a movable piece

        return moves

    #choose the best move in the current state
    def chooseMove(self):
        currentState = {}  #store the payoff of each move {referenceToPiece: [orgin, [(dest, payOff, action), ...]]}
        for i in range(self.brd.numRow):
            for j in range(self.brd.numCol): # check entire board for AI's piece
                if self.brd.tiles[i][j].getPiece() != None and self.brd.tiles[i][j].getPiece().getAlliance() == 1: # if the piece is AI's piece
                    currentState[self.brd.tiles[i][j].getPiece()] = [(i,j),None]

        #calculate payoff for all possible moves
        for piece in currentState:
            currentState[piece][1] = self.generateMoves(piece,currentState[piece][0],True)

        #for all possibleMoves
        bestMove = (0.0,None,None,None,None) #(Payoff, referenceToPiece, orgin, dest, action)
        for piece in currentState:
            for move in currentState[piece][1]:
                #if move is bad
                if move[1] < 0:
                    continue
                max = move[1] #payoff of move

                #mock next state
                self.brd.tiles[currentState[piece][0][0]][currentState[piece][0][1]].setPiece(None)
                ogPiece = self.brd.tiles[move[0][0]][move[0][1]].getPiece()
                self.brd.tiles[move[0][0]][move[0][1]].setPiece(piece)

                nextState = {}
                for i in range(self.brd.numRow):
                    for j in range(self.brd.numCol): # check entire board for AI's piece
                        if self.brd.tiles[i][j].getPiece() != None and self.brd.tiles[i][j].getPiece().getAlliance() == 1: # if the piece is AI's piece
                            nextState[self.brd.tiles[i][j].getPiece()] = [(i,j),None]

                #calculate payoff for all possible moves
                for temp in nextState:
                    nextState[temp][1] = self.generateMoves(temp,nextState[temp][0],False)

                #get best payoff for all 'attack' moves
                min = 10 #maximum lost by enemy's move
                attackCounter = 0
                for temp in nextState:
                    for temp2 in nextState[temp][1]:
                        if min > temp2[1] and temp2[2] == 'attack': #only calculate min for 'attack' move
                            attackCounter = attackCounter + 1
                            min = temp2[1]
                        ul = (nextState[temp][0][0] - 1, nextState[temp][0][1] - 1) #upperleft
                        up = (nextState[temp][0][0] - 1, nextState[temp][0][1])     #up
                        ur = (nextState[temp][0][0] - 1, nextState[temp][0][1] + 1) #upperright
                        lf = (nextState[temp][0][0], nextState[temp][0][1] - 1)     #left
                        og = (nextState[temp][0][0], nextState[temp][0][1])         #original
                        rg = (nextState[temp][0][0], nextState[temp][0][1] + 1)     #right
                        dl = (nextState[temp][0][0] + 1, nextState[temp][0][1] - 1) #downleft
                        dw = (nextState[temp][0][0] + 1, nextState[temp][0][1])     #down
                        dr = (nextState[temp][0][0] + 1, nextState[temp][0][1] + 1) #downright
                        tempDest = (temp2[0][0],temp2[0][1])
                        # special case for if there is enemy piece in camp
                        if temp2[2] == None and self.brd.layout[temp2[0][0]][temp2[0][1]] == "CP" and (up == tempDest or dw == tempDeat or lf == tempDeat or rg == tempDeat or ul == tempDeat or ur == tempDeat or dl == tempDeat or dr == tempDeat): #check if it is an adjacent camp
                            if self.brd.tiles[temp2[0][0]][temp2[0][1]].getPiece() != None and self.brd.tiles[i][j].getPiece().getAlliance() != 1: # check for piece and its' alliance
                                attackCounter = attackCounter + 1
                                min = self.moveHeuristic[tempDeat[0]][tempDeat[1]] + self.calcAttack(temp,temp.getRank(),self.prediction[self.brd.tiles[temp2[0][0]][temp2[0][1]].getPiece()])

                if attackCounter == 0: #if pieces cannot be attacked next round
                    min = 10

                payoff = (max + min) * ((rng.rand() * 0.1) + 0.95) #added randomness to allow unpredicted moves (range = (0.95, 1.05))
                if bestMove[0] < payoff:
                    bestMove = (payoff, piece, currentState[piece][0], move[0], move[2])
                
                #revert to original state
                self.brd.tiles[currentState[piece][0][0]][currentState[piece][0][1]].setPiece(piece)
                self.brd.tiles[move[0][0]][move[0][1]].setPiece(ogPiece)
         
        return bestMove

    #assign pieces to tiles
    def placePieces(self):
        pieceData = {"Flag": [1],
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
        pieceLayout = [None for _ in range(30)]

        #randomly assign Flag to one of the HQ
        if rng.rand() < 0.5:
            pieceLayout[1] = "Flag"
        else:
            pieceLayout[3] = "Flag"

        #heuristic of landmine change according to position of Flag
        heuristic_landmine = [3 for _ in range(10)]
        if pieceLayout[1] == "Flag":
            heuristic_landmine[1] = -1
            heuristic_landmine[3] = 6
            heuristic_landmine[0] = 5
            heuristic_landmine[2] = 5
        elif pieceLayout[3] == "Flag":
            heuristic_landmine[3] = -1
            heuristic_landmine[1] = 6
            heuristic_landmine[2] = 5
            heuristic_landmine[4] = 5
        #assign landmine
        for i in range(pieceData["Landmine"][0]):
            best = (0,None) #(value,index)
            for j in range(len(heuristic_landmine)):
                heuristicValue = heuristic_landmine[j] * ((rng.rand() * 0.8) + 0.6)
                if heuristicValue > best[0]:
                    best = (heuristicValue, j)
            pieceLayout[best[1]] = "Landmine"
            heuristic_landmine[best[1]] = -1

        #heurictic of grenade
        heuristic_grenade = [3 for _ in range(25)]
        for i in range(5):
            heuristic_grenade[i] = 2
        heuristic_grenade[7] = 5
        for j in range(len(heuristic_grenade)):
            if pieceLayout[j] != None or j == 11 or j == 13 or j == 17 or j == 21 or j == 23:
               heuristic_grenade[j] = -1
        #assign grenade
        for i in range(pieceData["Grenade"][0]):
            best = (0,None)
            for j in range(len(heuristic_grenade)):
                heuristicValue = heuristic_grenade[j] * ((rng.rand() * 0.8) + 0.6)
                if heuristicValue > best[0]:
                    best = (heuristicValue, j)
            pieceLayout[best[1]] = "Grenade"
            heuristic_grenade[best[1]] = -1

        #heuristic for other pieces
        heuristic_pieces = [3 for _ in range(30)]
        for i in range(5):
            heuristic_grenade[i] = 2
        for j in range(5,30):
            if j == 5 or j == 9 or j == 12 or j == 16 or j == 18 or j == 22 or j == 25 or j == 29:
                heuristic_pieces[j] = 4
            elif j == 15 or j == 19:
                heuristic_pieces[j] = 5
            elif j == 7 or j == 27:
                heuristic_pieces[j] = 6
        for k in range(len(heuristic_pieces)):
            if pieceLayout[k] != None or k == 11 or k == 13 or k == 17 or k == 21 or k == 23:
               heuristic_pieces[k] = -1
        #assign pieces
        for piece in pieceData:
            if piece == "Flag" or piece == "Landmine" or piece == "Grenade":
                continue #already assigned
            for i in range(pieceData[piece][0]):
                best = (0,None)
                for j in range(len(heuristic_pieces)):
                    heuristicValue = heuristic_pieces[j] * ((rng.rand() * 1) + 0.5)
                    if heuristicValue > best[0]:
                        best = (heuristicValue, j)
                pieceLayout[best[1]] = piece
                heuristic_pieces[best[1]] = -1

        for x in range(len(pieceLayout)):
            i = int(x / 5)
            j = int(x % 5)
            if pieceLayout[x]:
                self.brd.tiles[i][j].setPiece(self.brd.spawnPiece(1, pieceLayout[x], self.brd.tiles[i][j].getPos()))

    #take action
    def makeMove(self):
        # deciding which piece to move and to where
        payoff, self.currentPiece, orgin, dest, action = self.chooseMove() # returns piece to move, destination of move, current location of piece

        self.brd.tiles[orgin[0]][orgin[1]].setPiece(None)
        self.brd.takeAction(self.currentPiece, (self.brd.checkAvailableMovement(dest[0], dest[1], self.currentPiece, orgin[0], orgin[1], True)), (dest[0],dest[1]))

        return orgin, dest

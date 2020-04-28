import pygame
import operator
import random
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

    def __init__(self, board):
        self.brd = board    #get Board reference
        self.currentPiece = None
        self.lostPiece = None   #record what piece is lost this round
        self.prediction = self.getPrediction()
        self.playerDeadPieces = []
        self.moveHeuristic = [[1,1,1,1,1],
                              [1,1,1,1,1],
                              [1,1,1,1,1],
                              [1,1,1,1,1],
                              [1,1,1,1,1],
                              [1,1,1,1,1],
                              [3,3,3,3,3],
                              [3,2,1,2,3],
                              [3,1,2,1,3],
                              [3,2,1,2,3],
                              [4,5,4,5,4],
                              [5,6,5,6,5]] #subject to change

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
            if ori[0] != dest[0] and ori[1] != dest[1]:
                self.prediction[playerPiece] = ['Engineer']

        self.lostPiece = None
        self.currentPiece = None

        #debug
        for item in self.prediction:
            print(item,end=' : ')
            print(self.prediction[item])
        print(self.playerDeadPieces)

    def calcAttack(self,piece,myRank,enemies): # receives current piece,current piece rank, list of pieces the opponent can be
        willLoseTo = 0
        worth = 0 # for if my piece is grenade
        for enemy in enemies:
            enemyRank = self.rankData[str(enemy)]
            if str(enemy) == "Flag": # If the enemy piece has a chance to be a flag, attack immediately if possible
                return 10
            elif piece.toString() == "Grenade" and enemyRank[0] < 4: # grenade should try to fight pieces with higher power (lieutenant and above)
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
        if success > 0.74: # if it has a 75% chance of winning
            return success
        else:
            return (0 - success) #returns the success rate as a negative value to deter the move

    #generate possible moves and calculate its payoff the return as a list
    def generateMoves(self,piece,orgin,checkEngineer):
        moves = []
        (currentRow, currentCol) = orgin
        attackPayOff = 0 # incentive to attack
        movePayOff = 0 # incentive to move

        for i in range(self.brd.numRow):  #i ,j = destination
            for j in range(self.brd.numCol):
                self.brd.tiles[currentRow][currentCol].setPiece(None) # to ignore counting the current place as a dead end
                action = self.brd.checkAvailableMovement(i,j,piece,currentRow,currentCol,checkEngineer) # checks for all available moves in the map
                self.brd.tiles[currentRow][currentCol].setPiece(piece)

                if action != None and action != "no move": # if the piece can move here or attack this piece
                    movePayOff = self.moveHeuristic[i][j]
                    if action == "attack": #if there is a piece on this tile to attack
                        attackPayOff = self.calcAttack(piece, piece.getRank(), self.prediction[self.brd.tiles[i][j].getPiece()]) # calculates the possibility of winning the fight

                    #calculate payoff
                    payOff = movePayOff + attackPayOff
                    moves.append(((i,j),payOff,action)) #stores the dest, payoff & action of a movable piece

        return moves

    def chooseMove(self):
        currentState = {}  #store the payoff of each move {referenceToPiece: [orgin, [(dest, payOff, action), ...]]}
        for i in range(self.brd.numRow):
            for j in range(self.brd.numCol): # check entire board for AI's piece
                if self.brd.tiles[i][j].getPiece() != None and self.brd.tiles[i][j].getPiece().getAlliance() == 1: # if the piece is AI's piece
                    currentState[self.brd.tiles[i][j].getPiece()] = [(i,j),None]

        #calculate payoff for all possible moves
        for piece in currentState:
            currentState[piece][1] = self.generateMoves(piece,currentState[piece][0],True)

        #debug
        debugMatrix = {}

        #for all possibleMoves
        bestMove = (0.0,None,None,None,None) #(Payoff, referenceToPiece, orgin, dest, action)
        for piece in currentState:
            #debug
            default = [[None for _ in range(5)] for _ in range(12)]
            default[currentState[piece][0][0]][currentState[piece][0][1]] = 0.0
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
                        # special case for if there is enemy piece in camp
                        elif temp2[2] == None and self.brd.layout[temp2[0][0]][temp2[0][1]] == "CP": #check if it is camp
                            if self.brd.tiles[temp2[0][0]][temp2[0][1]].getPiece() != None and self.brd.tiles[i][j].getPiece().getAlliance() != 1: # check for piece and its' alliance
                                    attackCounter = attackCounter + 1
                                    min = temp2[1]

                if attackCounter == 0: #if pieces cannot be attacked next round
                    min = 10

                if bestMove[0] < max + min:
                    bestMove = (max + min, piece, currentState[piece][0], move[0], move[2])
                
                #debug
                default[move[0][0]][move[0][1]] = max + min

                #revert to original state
                self.brd.tiles[currentState[piece][0][0]][currentState[piece][0][1]].setPiece(piece)
                self.brd.tiles[move[0][0]][move[0][1]].setPiece(ogPiece)
            
            #debug
            debugMatrix[piece] = default

        #debug
        for x in debugMatrix:
            print(x)
            for y in debugMatrix[x]:
                print(y)

        return bestMove

    def placePieces(self):
        pieceLayout = [["Commander","Landmine","Major","Flag","Captain"],
                       ["Landmine","Landmine","Engineer","Marshal","Engineer"],
                       ["Grenade",None,"Captain",None,"Colonel"],
                       ["Engineer","Lieutenant",None,"Commander","Lieutenant"],
                       ["Grenade",None,"General",None,"Commander"],
                       ["Brigadier","Colonel","Captain","Major","Brigadier"]]
        for i in range(int(self.brd.numRow/2)):
            for j in range(self.brd.numCol):
                if pieceLayout[i][j]:
                    self.brd.tiles[i][j].setPiece(self.brd.spawnPiece(1, pieceLayout[i][j], self.brd.tiles[i][j].getPos()))

    #take action
    def makeMove(self):
        print('it is now AI turn')
        # deciding which piece to move and to where
        payoff, self.currentPiece, orgin, dest, action = self.chooseMove() # returns piece to move, destination of move, current location of piece

        self.brd.tiles[orgin[0]][orgin[1]].setPiece(None)
        self.brd.takeAction(self.currentPiece, (self.brd.checkAvailableMovement(dest[0], dest[1], self.currentPiece, orgin[0], orgin[1])), (dest[0],dest[1]))

        return orgin, dest

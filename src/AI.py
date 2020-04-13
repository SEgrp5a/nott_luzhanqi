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
        self.prediction = self.genPrediction()
        self.currentPiece = None
        self.playerDeadPieces = []
        self.lostPiece = None   #record what piece is lost this round

    def genPrediction(self):
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
            #piece won't be flag or landmine if it is moved
            if 'Landmine' in self.prediction[playerPiece]:
                self.prediction[playerPiece].remove('Landmine')
            if 'Flag' in self.prediction[playerPiece]:
                self.prediction[playerPiece].remove('Flag')


        self.lostPiece = None
        self.currentPiece = None

        #debug
        for item in self.prediction:
            print(item,end=' : ')
            print(self.prediction[item])
        print(self.playerDeadPieces)

    def calSuccess(self,piece,myRank,enemies): # receives current piece,current piece rank, list of pieces the opponent can be
        willLoseTo=0
        worth=0 # for if my piece is grenade
        for item in enemies:
            enemyRank=self.rankData[item]
            if str(item)=="Flag": # If the enemy piece has a chance to be a flag, attack immediately
                return 1
            elif str(piece)=="Grenade" and enemyRank[0] < 4: # grenade should try to fight pieces with higher power (lieutenant and above)
                worth = worth + 1 # could be a high level piece
            elif myRank > enemyRank[0]:  # rank higher = power lower
                willLoseTo=willLoseTo+1 # records the pieces it will lose to

        if str(piece)=="Grenade":
            if (len(enemies) - worth) == 0: # unless I know it is a lieutenant or higher power, i will not attack
                return 1
            else:
                return 0
        else:
            success=1-(willLoseTo/len(enemies)) # returns the probability of winning the battle

        if success > 0.74: # if it has a 75% chance of winning
            return success
        else:
            return (0-success) #returns the success rate as a negative value to deter the move

    def bestMove(self,key,val):
        valueOfMove={} # dictionary storing the payoff of each move
        currentRow=val[3]
        currentCol=val[4]
        attack=0 # incentive to attack
        move=0 #i ncentive to move

        for i in range(self.brd.numRow):  #i ,j = destination
            for j in range(self.brd.numCol):
                self.brd.tiles[currentRow][currentCol].setPiece(None) # to ignore counting the current place as a dead end
                action=self.brd.checkAvailableMovement(i,j,key,currentRow,currentCol) # checks for all available moves in the map
                self.brd.tiles[currentRow][currentCol].setPiece(key)
                #calculates payoff
                if action != None: # if the piece can move here or attack this piece
                    move=i-currentRow #reverse because start from ai moving downwards , payoff for moving towards the enemy flag

                if action == "attack": #if there is a piece on this tile to attack
                    chosen=self.brd.tiles[i][j].getPiece()
                    attack=self.calSuccess(key,key.getRank(),self.prediction[chosen]) # calculates the possibility of winning the fight
                payOff=move + attack
                valueOfMove[(i,j)]=[payOff]  #stores the payoff at the current destination
                attack=0
                move=0

        bestPayOff=max(valueOfMove.values()) #finds the best payoff, if multiple choices, take first choice
        destination=list(valueOfMove.keys())[list(valueOfMove.values()).index(bestPayOff)] #returns the destination with the best payoff

        return bestPayOff,destination,(currentRow,currentCol)

    def chooseMove(self):
        pieces={} # stores dictionary with pieces AI can move as key
        for i in range(self.brd.numRow):
            for j in range(self.brd.numCol): # check entire board for AI's piece
                if self.brd.tiles[i][j].getPiece() != None and self.brd.tiles[i][j].getPiece().getAlliance() == 1: # if the piece is AI's piece
                    chosen=self.brd.tiles[i][j].getPiece()
                    pieces[chosen]=[0 , 0 , 0 , i , j] # initialization of bestPayOff,destination [][], current position[][]

        for item in pieces:
            pieces.update({item:self.bestMove(item,pieces[item])}) # finds the best move and payoff of the move for each AI's piece

        bestPlay=max(pieces, key=pieces.get) # returns the piece that I should move based on highest payoff

        return bestPlay, pieces[bestPlay][1][0],pieces[bestPlay][1][1],pieces[bestPlay][2][0],pieces[bestPlay][2][1]

    def placePieces(self):
        pieceLayout = [["Commander","Landmine","Major","Flag","Captain"],
                       ["Landmine","Landmine","Engineer","Marshal","Engineer"],
                       ["Grenade",None,"Captain",None,"Colonel"],
                       ["Engineer","Lieutenant",None,"Commander","Lieutenant"],
                       ["Grenade",None,"General",None,"Commander"],
                       ["Brigadier","Colonel","Captain","Major","Brigadier"]]
        for i in range(int(self.brd.numRow/2)):
            for j in range(self.brd.numCol):
                self.brd.tiles[i][j].setPiece(self.brd.spawnPiece(1, pieceLayout[i][j], self.brd.tiles[i][j].getPos()))


    #take action
    def makeMove(self):
        print('it is now AI turn')
        # deciding which piece to move and to where
        self.currentPiece,dest_row,dest_col,ori_row,ori_col=self.chooseMove() # returns piece to move, destination of move, current location of piece
        self.brd.tiles[ori_row][ori_col].setPiece(None) # removes the image of the piece before movement

        if self.brd.takeAction(self.currentPiece,(self.brd.checkAvailableMovement(dest_row,dest_col,self.currentPiece,ori_row,ori_col)), (dest_row,dest_col)):
            self.brd.tiles[dest_row][dest_col].setOutline(True, self.brd.blue)

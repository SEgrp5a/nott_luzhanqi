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

    def calSuccess(self,piece,myRank,enemies):
        willLoseTo=0
        for item in enemies:
            enemyRank=self.rankData[item]
            if myRank < enemyRank[0]:
                willLoseTo=willLoseTo+1

        success=willLoseTo/len(enemies)
        if success > 0.49:
            winRate=success
        else:
            winRate=0-success

        return winRate

    def bestMove(self,key,val):
        valueOfMove={}
        currentRow=val[3]
        currentCol=val[4]
        attack=0
        move=0
        
        actions = []
        for i in range(self.brd.numRow):
            temp = []
            for j in range(self.brd.numCol):
                self.brd.tiles[currentRow][currentCol].setPiece(None)
                temp.append(self.brd.checkAvailableMovement(i,j,key,currentRow,currentCol))
                self.brd.tiles[currentRow][currentCol].setPiece(key)
            actions.append(temp)
        print(actions)

        for i in range(self.brd.numRow):  #i ,j = destination
            for j in range(self.brd.numCol): #row= 12, column = 5
                self.brd.tiles[currentRow][currentCol].setPiece(None)
                action=self.brd.checkAvailableMovement(i,j,key,currentRow,currentCol)
                self.brd.tiles[currentRow][currentCol].setPiece(key)
                #calculates payoff
                if action != None:
                    move=i-currentRow #reverse because start from ai moving downwards , payoff for moving towards the enemy flag     
                
                if action == "attack":
                    chosen=self.brd.tiles[i][j].getPiece()
                    attack=self.calSuccess(key,key.getRank(),self.prediction[chosen]) #my rank, opponents rank
                payOff=move + attack
                valueOfMove[(i,j)]=[payOff]        
                attack=0
                move=0
        
        bestPayOff=max(valueOfMove.values())
        print("sds")
        destination=list(valueOfMove.keys())[list(valueOfMove.values()).index(bestPayOff)]

        return bestPayOff,destination,(currentRow,currentCol)

    def chooseMove(self):
        pieces={}
        for i in range(self.brd.numRow):
            for j in range(self.brd.numCol):
                if self.brd.tiles[i][j].getPiece() != None and self.brd.tiles[i][j].getPiece().getAlliance() == 1:
                    chosen=self.brd.tiles[i][j].getPiece()
                    pieces[chosen]=[0 , 0 , 0 , i , j]  #how to have position  =[bestPayOff,destination,position]
              
        for item in pieces:
            pieces.update({item:self.bestMove(item,pieces[item])})

        bestPlay=max(pieces, key=pieces.get) #what piece i should move
        print(bestPlay)
        print(pieces)
        return bestPlay, pieces[bestPlay][1][0],pieces[bestPlay][1][1],pieces[bestPlay][2][0],pieces[bestPlay][2][1]

    def placePieces(self):
        for j in range(self.brd.numCol):
            tempY = 11 # -1 for each iteration to simulate mirroring
            for i in range(int(self.brd.numRow/2)):
                if self.brd.tiles[tempY][j].getPiece():
                    self.brd.tiles[i][j].setPiece(self.brd.spawnPiece(1, self.brd.tiles[tempY][j].getPiece().toString(), self.brd.tiles[i][j].getPos()))
                tempY = tempY - 1

    #take action
    def makeMove(self):
        print('it is now AI turn')
        self.currentPiece,dest_row,dest_col,ori_row,ori_col=self.chooseMove()
        self.brd.tiles[ori_row][ori_col].setPiece(None)

        if self.brd.takeAction(self.currentPiece,(self.brd.checkAvailableMovement(dest_row,dest_col,self.currentPiece,ori_row,ori_col)), (dest_row,dest_col)):
            self.brd.tiles[dest_row][dest_col].setOutline(True, self.brd.blue)
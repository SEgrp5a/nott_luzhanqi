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


    def calPayOff(self,):
        for j in range(self.numCol):
            for i in range(self.numRow):
                action=self.brd.checkAvailableMovement(i,j,self.currentPiece,self.pieceRow,self.pieceCol)
                

        return payOff

    def bestMove(self,piece):
        valueOfMove={}
        self.calPayOff
        return a,b

    def chooseMove(self):
        pieces={}
        counter = 0
        for i in range(self.brd.numRow):
            for j in range(self.brd.numCol):
                if self.brd.tiles[i][j].getPiece() != None and self.brd.tiles[i][j].getPiece().getAlliance() == 1:
                    chosen=self.brd.tiles[i][j].getPiece()
                    pieces[chosen]=0  #how to have position  =[bestPayOff,position]
                    counter=counter+1
                if counter == 3:
                     break
            if counter == 3:
                break
        for item in pieces:
            pieces.update({item:self.bestMove(item)})

        bestPlay=max(pieces, key=pieces.get)

        #return bestPlay

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
        ai_turn = True
        while ai_turn == True:
            rand_row = random.randint(0,11)
            rand_col = random.randint(0,4)

            moves_row = []
            moves_col = []
            self.currentPiece = self.brd.tiles[rand_row][rand_col].getPiece()

            if self.currentPiece != None and self.currentPiece.getAlliance() == 1 and self.currentPiece.toString() != 'Flag' and self.currentPiece.toString() != 'Landmine':
                self.brd.tiles[rand_row][rand_col].setPiece(None)
                #check all possible moves of the random piece by scanning the whole board
                for i in range(self.brd.numRow):
                    for j in range(self.brd.numCol):
                        action = self.brd.checkAvailableMovement(i,j,self.currentPiece,rand_row,rand_col)
                        if action != None and action != "no move":
                            moves_row.append(i)
                            moves_col.append(j)
                #Now pick a random move from the array moves
                if len(moves_col):
                    rand_index = random.randint(0,(len(moves_col)-1))
                    if self.brd.takeAction(self.currentPiece, (self.brd.checkAvailableMovement(moves_row[rand_index],moves_col[rand_index],self.currentPiece,rand_row,rand_col)), (moves_row[rand_index],moves_col[rand_index])):
                        ai_turn = False
        self.brd.tiles[rand_row][rand_col].setOutline(True, self.brd.blue)
        self.chooseMove()
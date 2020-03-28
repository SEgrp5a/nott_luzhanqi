import pygame
import operator
import random
from pieces import *

class AI():
    def __init__(self, board):
        self.brd = board    #get Board reference
        self.prediction = self.genPrediction()

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


    def placePieces(self):
        for j in range(self.brd.numCol):
            tempY = 11 # -1 for each iteration to simulate mirroring
            for i in range(int(self.brd.numRow/2)):
                if self.brd.tiles[tempY][j].getPiece():
                    self.brd.tiles[i][j].setPiece(self.brd.spawnPiece(1, self.brd.tiles[tempY][j].getPiece().toString(), self.brd.tiles[i][j].getPos()))
                tempY = tempY - 1

    #AI random move
    def makeMove(self):
        print('it is now AI turn')
        ai_turn = True
        randomPiece = None
        while ai_turn == True:
            rand_row = random.randint(0,11)
            rand_col = random.randint(0,4)

            moves_row = []
            moves_col = []
            randomPiece = self.brd.tiles[rand_row][rand_col].getPiece()

            if randomPiece != None and randomPiece.getAlliance() == 1 and randomPiece.toString() != 'Flag' and randomPiece.toString() != 'Landmine':
                self.brd.tiles[rand_row][rand_col].setPiece(None)
                #check all possible moves of that single randomPiece by scanning the whole board
                for i in range(self.brd.numRow):
                    for j in range(self.brd.numCol):
                        action = self.brd.checkAvailableMovement(i,j,randomPiece,rand_row,rand_col)
                        if action != None and action != "no move":
                            moves_row.append(i)
                            moves_col.append(j)
                #Now pick a random move from the array moves
                if len(moves_col):
                    rand_index = random.randint(0,(len(moves_col)-1))
                    if self.brd.takeAction(randomPiece, (self.brd.checkAvailableMovement(moves_row[rand_index],moves_col[rand_index],randomPiece,rand_row,rand_col)), (moves_row[rand_index],moves_col[rand_index])):
                        ai_turn = False
        self.brd.tiles[rand_row][rand_col].setOutline(True, self.brd.blue)
import pygame
from pieces.nullpiece import NullPiece
from pieces.brigadier import Brigadier

class Board:
    temporary = {}


    def __init__(self):
        self.board = self.initialise()

    def initialise(self):
        """Initialise the game board"""
        #Set all as Soldier Station
        board = [["SS" for i in range(13)] for j in range(5)]

        #Setting Camp
        board[1][2] = "CP"
        board[3][2] = "CP"
        board[2][3] = "CP"
        board[1][4] = "CP"
        board[3][4] = "CP"
        board[1][8] = "CP"
        board[3][8] = "CP"
        board[2][9] = "CP"
        board[1][10] = "CP"
        board[3][10] = "CP"

        #Setting Headquarters
        board[1][0] = "HQ"
        board[3][0] = "HQ"
        board[1][12] = "HQ"
        board[3][12] = "HQ"

        #Setting Front Line
        board[0][6] = "FL"
        board[2][6] = "FL"
        board[4][6] = "FL"

        #Setting Mountain Border
        board[1][6] = "MB"
        board[3][6] = "MB"

        return board

    def accessingPieces(self):
        for tile in range(4):
            self.temporary[tile] = NullPiece()

        self.temporary[0] = Brigadier(0,0)
        self.temporary[1] = Captain(0,1)
        self.temporary[2] = Colonel(0,2)
        self.temporary[3] = Commander(0,3)

    def draw(self,surface,width,height):
        for i in range(5):
            for j in range(13):
                if self.board[i][j] == "SS":
                    pygame.draw.rect(surface,(255,0,0),pygame.Rect(i*width,j*height,width,height))
                elif self.board[i][j] == "CP":
                    pygame.draw.rect(surface,(0,255,0),pygame.Rect(i*width,j*height,width,height))
                elif self.board[i][j] == "HQ":
                    pygame.draw.rect(surface,(0,255,255),pygame.Rect(i*width,j*height,width,height))
                elif self.board[i][j] == "FL":
                    pygame.draw.rect(surface,(0,0,255),pygame.Rect(i*width,j*height,width,height))
                elif self.board[i][j] == "MB":
                    pygame.draw.rect(surface,(255,0,255),pygame.Rect(i*width,j*height,width,height))

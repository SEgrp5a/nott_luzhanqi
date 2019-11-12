import pygame
from pieces.allPieces import Brigadier
from pieces.allPieces import Captain
from pieces.allPieces import Colonel
from pieces.allPieces import Commander
from pieces.allPieces import Engineer
from pieces.allPieces import General
from pieces.allPieces import Flag
from pieces.allPieces import Grenade
from pieces.allPieces import Landmine
from pieces.allPieces import Lieutenant
from pieces.allPieces import Major
from pieces.allPieces import Marshal
from pieces.nullpiece import NullPiece

green = (0,255,0)
red = (255,0,0)
neonBlue = (0,255,255)
blue = (0,0,255)
pink = (255,0,255)
white = (255,255,255)

class Board:

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

    def draw(self,surface,width,height):
        
        for i in range(5):
            for j in range(13):
                if self.board[i][j] == "SS":
                    pygame.draw.rect(surface,green,pygame.Rect(i*width,j*height,width,height),1)
                elif self.board[i][j] == "CP":
                    pygame.draw.rect(surface,blue,pygame.Rect(i*width,j*height,width,height),1)
                elif self.board[i][j] == "HQ":
                    pygame.draw.rect(surface,neonBlue,pygame.Rect(i*width,j*height,width,height),1)
                elif self.board[i][j] == "FL":
                    pygame.draw.rect(surface,pink,pygame.Rect(i*width,j*height,width,height),1)
                elif self.board[i][j] == "MB":
                    pygame.draw.rect(surface,red,pygame.Rect(i*width,j*height,width,height),1)

    temporary = {}

    def accessingPieces(self):

        self.temporary["Brigadier"] = Brigadier(0,0)
        self.temporary["Captain"] = Captain(0,1)
        self.temporary["Colonel"] = Colonel(0,2)
        self.temporary["Commander"] = Commander(0,3)
        self.temporary["Engineer"] = Engineer(0,4)
        self.temporary["General"] = General(0,5)
        self.temporary["Flag"] = Flag(0,6)
        self.temporary["Bomb"] = Grenade(0,7)
        self.temporary["Landmine"] = Landmine(0,8)
        self.temporary["Lieutenant"] = Lieutenant(0,9)
        self.temporary["Major"] = Major(0,10)
        self.temporary["Marshal"] = Marshal(0,11)
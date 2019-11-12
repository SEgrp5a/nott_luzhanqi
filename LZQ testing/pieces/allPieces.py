from pieces.piece import Piece

class Brigadier(Piece):

    alliance = None
    position = None
    img = None
    rank = 4
    available = 2

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.img = "./Art/"+ self.toString() +".png"

    def toString(self):
        return "Brigadier"      

    def printPiece(self):
        return self.img

class Captain(Piece):

    alliance = None
    position = None
    img = None
    rank = 7
    available = 3

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.img = "./Art/"+ self.toString() +".png"

    def toString(self):
        return "Captain"      

    def printPiece(self):
        return self.img

class Colonel(Piece):

    alliance = None
    position = None
    img = None
    rank = 5
    available = 2

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.img = "./Art/"+ self.toString() +".png"

    def toString(self):
        return "Colonel"      

    def printPiece(self):
        return self.img

class Commander(Piece):

    alliance = None
    position = None
    img = None
    rank = 8
    available = 3

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.img = "./Art/"+ self.toString() +".png"

    def toString(self):
        return "Commander"     

    def printPiece(self):
        return self.img

class Engineer(Piece):

    alliance = None
    position = None
    img = None
    rank = 9
    available = 3

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.img = "./Art/"+ self.toString() +".png"

    def toString(self):
        return "Engineer"      

    def printPiece(self):
        return self.img

class General(Piece):

    alliance = None
    position = None
    img = None
    rank = 2
    available = 1

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.img = "./Art/"+ self.toString() +".png"

    def toString(self):
        return "General"      

    def printPiece(self):
        return self.img

class Flag(Piece):

    alliance = None
    position = None
    img = None
    taken = None
    available = 1

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.img = "./Art/"+ self.toString() +".png"
        self.taken = False

    def toString(self):
        return "Flag"      

    def printPiece(self):
        return self.img   

class Grenade(Piece):

    alliance = None
    position = None
    img = None
    rank = 0
    available = 2

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.img = "./Art/"+ self.toString() +".png"

    def toString(self):
        return "Bomb"      

    def printPiece(self):
        return self.img  

class Landmine(Piece):

    alliance = None
    position = None
    img = None
    rank = 0
    available = 3

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.img = "./Art/"+ self.toString() +".png"

    def toString(self):
        return "Landmine"      

    def printPiece(self):
        return self.img 

class Lieutenant(Piece):

    alliance = None
    position = None
    img = None
    rank = 3
    available = 2

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.img = "./Art/"+ self.toString() +".png"

    def toString(self):
        return "Lieutenant"      

    def printPiece(self):
        return self.img 

class Major(Piece):

    alliance = None
    position = None
    img = None
    rank = 6
    available = 2

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.img = "./Art/"+ self.toString() +".png"

    def toString(self):
        return "Major"      

    def printPiece(self):
        return self.img

class Marshal(Piece):

    alliance = None
    position = None
    img = None
    rank = 1
    available = 1

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.img = "./Art/"+ self.toString() +".png"

    def toString(self):
        return "Marshal"      

    def printPiece(self):
        return self.img
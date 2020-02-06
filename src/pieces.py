class Piece:

    alliance = None
    position = None
    path = None

    def __init__(self):
        pass
    
    def toString(self):
        return self.__class__.__name__

    def getPath(self):
        return self.path

class NullPiece(Piece):
    pass

class Flag(Piece):

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.path = "bin\\" + self.toString() + ".png"
        self.taken = False

    def istaken(self):
        return self.taken

class Grenade(Piece):

    rank = 0

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.path = "bin\\" + self.toString() + ".png"

class Landmine(Piece):

    rank = 0

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.path = "bin\\" + self.toString() + ".png"
    
class Marshal(Piece):

    rank = 1

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.path = "bin\\" + self.toString() + ".png"

class General(Piece):

    rank = 2

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.path = "bin\\" + self.toString() + ".png"

class Lieutenant(Piece):

    rank = 3

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.path = "bin\\" + self.toString() + ".png"

class Brigadier(Piece):

    rank = 4

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.path = "bin\\" + self.toString() + ".png"

class Colonel(Piece):

    rank = 5

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.path = "bin\\" + self.toString() + ".png"

class Major(Piece):

    rank = 6

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.path = "bin\\" + self.toString() + ".png"

class Captain(Piece):

    rank = 7

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.path = "bin\\" + self.toString() + ".png"

class Commander(Piece):

    rank = 8

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.path = "bin\\" + self.toString() + ".png"

class Engineer(Piece):

    rank = 9

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.path = "bin\\" + self.toString() + ".png"

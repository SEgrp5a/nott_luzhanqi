class Piece:

    alliance = None
    position = None
    path = None
    available = 0

    def __init__(self):
        pass
    
    def toString(self):
        return self.__class__.__name__

    def getAvailable(self):
        return self.available

    def destroy(self):
        if available > 0:
            available = available - 1

    def getPath(self):
        return self.path

class NullPiece(Piece):
    pass

class Flag(Piece):

    available = 1

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.path = "bin\\" + self.toString() + ".png"
        self.taken = False

    def istaken(self):
        return self.taken

class Grenade(Piece):

    rank = 0
    available = 2

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.path = "bin\\" + self.toString() + ".png"

class Landmine(Piece):

    rank = 0
    available = 3

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.path = "bin\\" + self.toString() + ".png"
    
class Marshal(Piece):

    rank = 1
    available = 1

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.path = "bin\\" + self.toString() + ".png"

class General(Piece):

    rank = 2
    available = 1

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.path = "bin\\" + self.toString() + ".png"

class Lieutenant(Piece):

    rank = 3
    available = 2

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.path = "bin\\" + self.toString() + ".png"

class Brigadier(Piece):

    rank = 4
    available = 2

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.path = "bin\\" + self.toString() + ".png"

class Colonel(Piece):

    rank = 5
    available = 2

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.path = "bin\\" + self.toString() + ".png"

class Major(Piece):

    rank = 6
    available = 2

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.path = "bin\\" + self.toString() + ".png"

class Captain(Piece):

    rank = 7
    available = 3

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.path = "bin\\" + self.toString() + ".png"

class Commander(Piece):

    rank = 8
    available = 3

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.path = "bin\\" + self.toString() + ".png"

class Engineer(Piece):

    rank = 9
    available = 3

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
        self.path = "bin\\" + self.toString() + ".png"

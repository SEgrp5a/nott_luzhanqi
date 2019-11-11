from pieces.piece import Piece

class Brigadier(Piece):

    alliance = None
    position = None
    rank = 4
    available = 2

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position

    def toString(self):
        return "Brigadier"        
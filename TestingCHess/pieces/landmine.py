from pieces.piece import Piece

class Landmine(Piece):

    alliance = None
    position = None
    rank = 0
    available = 3

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
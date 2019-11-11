from pieces.piece import Piece

class Lieutenant(Piece):

    alliance = None
    position = None
    rank = 3
    available = 2

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
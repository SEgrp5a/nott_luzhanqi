from pieces.piece import Piece

class Commander(Piece):

    alliance = None
    position = None
    rank = 8
    available = 3

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
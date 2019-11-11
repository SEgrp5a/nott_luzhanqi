from pieces.piece import Piece

class Colonel(Piece):

    alliance = None
    position = None
    rank = 5
    available = 2

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
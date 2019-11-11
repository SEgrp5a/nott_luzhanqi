from pieces.piece import Piece

class Major(Piece):

    alliance = None
    position = None
    rank = 6
    available = 2

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
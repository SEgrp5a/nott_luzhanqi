from pieces.piece import Piece

class Flag(Piece):

    alliance = None
    position = None
    Taken = False
    available = 1

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
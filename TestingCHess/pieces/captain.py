from pieces.piece import Piece

class Captain(Piece):

    alliance = None
    position = None
    rank = 7
    available = 3

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
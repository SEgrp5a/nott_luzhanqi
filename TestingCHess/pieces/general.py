from pieces.piece import Piece

class General(Piece):

    alliance = None
    position = None
    rank = 2
    available = 1

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
from pieces.piece import Piece

class Marshall(Piece):

    alliance = None
    position = None
    rank = 1
    available = 1

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
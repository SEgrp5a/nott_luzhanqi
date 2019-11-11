from pieces.piece import Piece

class Engineer(Piece):

    alliance = None
    position = None
    rank = 9
    available = 3

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
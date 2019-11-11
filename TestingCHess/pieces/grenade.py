from pieces.piece import Piece

class Grenade(Piece):

    alliance = None
    position = None
    rank = 0
    available = 2

    def __init__(self,alliance,position):
        self.alliance = alliance
        self.position = position
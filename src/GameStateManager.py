class GameStateManager():
    def __init__(self):
        self.game_states = ["MainMenu", "Instruction", "InGame", "Pause", "GameOver", "Exit"]

        self.currentGameState = None
        self.prevGameState = None
    
    #set game state
    def setState(self,gameState):
        self.prevGameState = self.currentGameState
        self.currentGameState = gameState
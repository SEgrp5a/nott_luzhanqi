class GameStateManager():
    def __init__(self):
        self.game_states = {"MainMenu": 0, 
                            "Instruction": 1, 
                            "InGame": 2, 
                            "Pause": 3, 
                            "GameOver": 4}
        self.currentGameState = "MainMenu"
        self.prevGameState = None

    def setState(self,gameState):
        self.prevGameState = self.currentGameState
        self.currentGameState = gameState
            
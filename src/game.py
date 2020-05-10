from gameStates import *
from GameStateManager import *
from jukebox import *

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
gray = (100, 100, 100)
white = (255, 255, 255)


# Main game loop
class Game:
    FPS = 30
    displayWidth = 1200
    displayHeight = 716  # 1 extra pixel to see the last line

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    GAMEDISPLAY = pygame.display.set_mode((displayWidth, displayHeight))
    pygame.display.set_caption("Lu Zhan QI")

    gsm = GameStateManager()
    jukebox = Jukebox()

    # Game State
    gameStates = {"MainMenu": MainMenu(displayWidth, displayHeight, gsm),
                  "Instruction": Instruction(displayWidth, displayHeight, gsm),
                  "InGame": None,
                  "Pause": Pause(displayWidth, displayHeight, gsm),
                  "GameOver": None,
                  "Exit": None}

    # BGM
    BGM = {"MainMenu": '.\\bin\\GOT.mp3',
           "Instruction": '.\\bin\\Halo.mp3',
           "InGame": '.\\bin\\war.mp3',
           "Pause": '.\\bin\\GOT.mp3',
           "GameOver": '.\\bin\\GOT.mp3',
           "Exit": None}

    # update board and game states
    def update(event, gsm, gameStates):
        if gsm.currentGameState == "InGame" and gameStates[gsm.currentGameState] is None:
            gameStates[gsm.currentGameState] = InGame(100, 55, 12, 5, gsm)
        result = gameStates[gsm.currentGameState].update(event)
        if gsm.currentGameState == "GameOver" and gameStates[gsm.currentGameState] is None:
            gameStates[gsm.currentGameState] = GameOver(1200, 716, gameStates["InGame"].win, gsm)

    # draw the component of the game states
    def draw(GAMEDISPLAY, gsm, gameStates):
        if gameStates[gsm.currentGameState] is None:
            return
        gameStates[gsm.currentGameState].draw(GAMEDISPLAY)

    running = True
    gsm.setState("MainMenu")
    while running:

        # Lock Framerate
        FPSCLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # dumping unnecessary states to save memory
            if gameStates["InGame"] and gsm.currentGameState == "MainMenu":
                dump = gameStates["InGame"]
                gameStates["InGame"] = None
                dump2 = gameStates["GameOver"]
                gameStates["GameOver"] = None
                del dump
                del dump2

            update(event, gsm, gameStates)
            draw(GAMEDISPLAY, gsm, gameStates)
            jukebox.play(BGM[gsm.currentGameState])
            if gsm.currentGameState == "Exit":
                running = False

        pygame.display.update()

    pygame.quit()

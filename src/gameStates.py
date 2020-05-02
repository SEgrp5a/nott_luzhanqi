import pygame
from tile import *
from board import Board

class GameState():
    #Colour
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)
    yellow = (255,255,0)
    gray = (100,100,100)
    black = (0,0,0)
    white = (255,255,255)

    def __init__(self, gsm):
        self.gsm = gsm
    
    def draw(self):
        pass

    def update(self):
        pass
    
    def write_text(self,x,y,text,textcolor,fontsize,surface):
        titleTextObj = pygame.font.Font(".\\bin\\Becker.ttf", fontsize)
        titleTextSurfaceObj = titleTextObj.render(text, True, textcolor)
        titleTextRectObj = titleTextSurfaceObj.get_rect()
        titleTextRectObj.center = (x, y)
        surface.blit(titleTextSurfaceObj, titleTextRectObj)

class MainMenu(GameState):
    def __init__(self, displayWidth, displayHeight, gsm):
        super().__init__(gsm)
        #Image
        self.titleImage = pygame.image.load(".\\bin\\main.png")
        self.titleImage = pygame.transform.scale(self.titleImage,(displayWidth,displayHeight))
        #Button
        self.start_button = Tile(displayWidth/2 - 100, displayHeight/2 + 10, 200, 80, color = self.red, text = 'START', textColor = self.black)
        self.rule_button = Tile(displayWidth/2 - 100, displayHeight/2 + 110, 200, 80, color = self.red, text = 'RULES', textColor = self.black)

    def draw(self,surface):
        #Show Background
        surface.blit(self.titleImage,(0,0))
        #Write Title
        self.write_text(300, 170, "Lu Zhan Qi", self.red, 100, surface)
        #Draw Button
        self.start_button.draw(surface)
        self.rule_button.draw(surface)
    
    def update(self,event):
        #handle event on start button
        outline_start = False
        outlineColor_start = None
        #if is hovering on button
        if 'hover' in self.start_button.handleEvent(event):
            outline_start = True
            outlineColor_start = self.black
        #if button is clicked
        if 'down' in self.start_button.handleEvent(event):
            outline_start = True
            outlineColor_start = self.blue
        #if button is clicked & released
        if 'click' in self.start_button.handleEvent(event):
            outline_start = True
            #change to game state
            self.gsm.setState("InGame")
        #if mouse exited a button
        if 'exit' in self.start_button.handleEvent(event):
            outline_start = False
        self.start_button.update(self.start_button.getColor(),outline_start,outlineColor_start)

        #handle event on rule button
        outline_rule = False
        outlineColor_rule = None
        #if is hovering on button
        if 'hover' in self.rule_button.handleEvent(event):
            outline_rule = True
            outlineColor_rule = self.black
        #if button is clicked
        if 'down' in self.rule_button.handleEvent(event):
            outline_rule = True
            outlineColor_rule = self.blue
        #if button is clicked & released
        if 'click' in self.rule_button.handleEvent(event):
            outline_rule = True
            #change to rule state
            self.gsm.setState("Instruction")
        #if mouse exited a button
        if 'exit' in self.rule_button.handleEvent(event):
            outline_rule = False
        self.rule_button.update(self.start_button.getColor(),outline_rule,outlineColor_rule)

class Instruction(GameState):
    def __init__(self, displayWidth, displayHeight, gsm):
        super().__init__(gsm)
        self.displayWidth = displayWidth
        #Image
        self.ruleImages = [pygame.image.load(".\\bin\\scroll.png"),pygame.image.load(".\\bin\\rulepage2.png")]
        self.ruleImages = [pygame.transform.scale(ruleImage,(displayWidth,displayHeight)) for ruleImage in self.ruleImages]
        self.currentPage = 0
        self.maxPage = len(self.ruleImages)
        #Button
        self.prev_button = Tile(120, displayHeight-80, 200, 60, color = self.red, text = 'PREVIOUS', textColor = self.black)
        self.next_button = Tile(displayWidth-310, displayHeight-80, 200, 60, color = self.red, text = 'NEXT', textColor = self.black)
        self.menu_button = Tile(displayWidth/2 - 100, displayHeight-80, 200, 60, color = self.red, text = 'MAIN MENU', textColor = self.black)

    def draw(self,surface):
        #Show Background
        surface.blit(self.ruleImages[self.currentPage],(0,0))
        #Write rules
        if self.currentPage == 0:
            y = 150
            self.write_text(self.displayWidth/2, y/2, "RULES:", self.black, 40, surface)
            file = open(".\\bin\\rules.csv", "r")
            for line in file:
                self.write_text(self.displayWidth/2, y, line.rstrip(), self.black, 20, surface)
                #line spacing
                y += 25
            file.close()
        #Draw button
        self.menu_button.draw(surface)
        #draw prev button if not first page
        if self.currentPage != 0:
            self.prev_button.draw(surface)
        #draw next button if not last page
        if self.currentPage != self.maxPage - 1:
            self.next_button.draw(surface)

    def update(self,event):
        #handle event on menu button
        outline_menu = False
        outlineColor_menu = None
        #if is hovering on button
        if 'hover' in self.menu_button.handleEvent(event):
            outline_menu = True
            outlineColor_menu = self.black
        #if button is clicked
        if 'down' in self.menu_button.handleEvent(event):
            outline_menu = True
            outlineColor_menu = self.blue
        #if button is clicked & released
        if 'click' in self.menu_button.handleEvent(event):
            outline_menu = True
            self.currentPage = 0
            #change to menu
            self.gsm.setState("MainMenu")
        #if mouse exited a button
        if 'exit' in self.menu_button.handleEvent(event):
            outline_menu = False
        self.menu_button.update(self.menu_button.getColor(),outline_menu,outlineColor_menu)

        #handle event on prev button if not first page
        if self.currentPage != 0:
            outline_prev = False
            outlineColor_prev = None
            #if is hovering on button
            if 'hover' in self.prev_button.handleEvent(event):
                outline_prev = True
                outlineColor_prev = self.black
            #if button is clicked
            if 'down' in self.prev_button.handleEvent(event):
                outline_prev = True
                outlineColor_prev = self.blue
            #if button is clicked & released
            if 'click' in self.prev_button.handleEvent(event):
                #change page
                self.currentPage = self.currentPage - 1
            #if mouse exited a button
            if 'exit' in self.prev_button.handleEvent(event):
                outline_prev = False
            self.prev_button.update(self.prev_button.getColor(),outline_prev,outlineColor_prev)

        #handle event on next button if not last page
        if self.currentPage != self.maxPage - 1:
            outline_next = False
            outlineColor_next = None
            #if is hovering on button
            if 'hover' in self.next_button.handleEvent(event):
                outline_next = True
                outlineColor_next = self.black
            #if button is clicked
            if 'down' in self.next_button.handleEvent(event):
                outline_next = True
                outlineColor_next = self.blue
            #if button is clicked & released
            if 'click' in self.next_button.handleEvent(event):
                #change page
                self.currentPage = self.currentPage + 1
            #if mouse exited a button
            if 'exit' in self.next_button.handleEvent(event):
                outline_next = False
            self.next_button.update(self.next_button.getColor(),outline_next,outlineColor_next)

class InGame(GameState):
    def __init__(self, width, height, numRow, numCol, gsm):
        super().__init__(gsm)
        self.board = Board(width, height, numRow, numCol)
        self.win = None

    def draw(self,surface):
        surface.fill(self.gray)
        self.board.draw(surface)

    def update(self, event):
        #handle event on board
        self.board.handleEvent(event)
        #check if game is over
        if self.board.win != None:
            self.win = self.board.win
            self.gsm.setState("GameOver")
        #handle keyboard event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                #change to pause state
                self.gsm.setState("Pause")

class Pause(GameState):
    def __init__(self, displayWidth, displayHeight, gsm):
        super().__init__(gsm)
        #Image
        self.pauseImage = pygame.image.load(".\\bin\\war screen.png")
        self.pauseImage = pygame.transform.scale(self.pauseImage,(displayWidth,displayHeight))
        #Button
        self.resume_button = Tile(displayWidth/2 - 100, displayHeight/2 + 10, 200, 80, color = self.red, text = 'RESUME', textColor = self.black)
        self.menu_button = Tile(displayWidth/2 - 100, displayHeight/2 + 110, 200, 80, color = self.red, text = 'MENU', textColor = self.black)

    def draw(self, surface):
        #Show Background
        surface.blit(self.pauseImage,(0,0))
        #Write Title
        self.write_text(300, 170, "PAUSED", self.red, 100, surface)
        #Draw Button
        self.resume_button.draw(surface)
        self.menu_button.draw(surface)

    def update(self, event):
        #handle event on resume button
        outline_resume = False
        outlineColor_resume = None
        #if is hovering on button
        if 'hover' in self.resume_button.handleEvent(event):
            outline_resume = True
            outlineColor_resume = self.black
        #if button is clicked
        if 'down' in self.resume_button.handleEvent(event):
            outline_resume = True
            outlineColor_resume = self.blue
        #if button is clicked & released
        if 'click' in self.resume_button.handleEvent(event):
            outline_resume = True
            #change to game state
            self.gsm.setState("InGame")
        #if mouse exited a button
        if 'exit' in self.resume_button.handleEvent(event):
            outline_resume = False
        self.resume_button.update(self.resume_button.getColor(),outline_resume,outlineColor_resume)

        #handle event on menu button
        outline_menu = False
        outlineColor_menu = None
        #if is hovering on button
        if 'hover' in self.menu_button.handleEvent(event):
            outline_menu = True
            outlineColor_menu = self.black
        #if button is clicked
        if 'down' in self.menu_button.handleEvent(event):
            outline_menu = True
            outlineColor_menu = self.blue
        #if button is clicked & released
        if 'click' in self.menu_button.handleEvent(event):
            outline_menu = True
            #change to main menu state
            self.gsm.setState("MainMenu")
        #if mouse exited a button
        if 'exit' in self.menu_button.handleEvent(event):
            outline_menu = False
        self.menu_button.update(self.menu_button.getColor(),outline_menu,outlineColor_menu)

class GameOver(GameState):
    def __init__(self, displayWidth, displayHeight, win, gsm):
        super().__init__(gsm)
        self.displayWidth = displayWidth
        #Image
        self.gameOverImage = pygame.image.load(".\\bin\\gameover.jpg")
        self.gameOverImage = pygame.transform.scale(self.gameOverImage,(displayWidth,displayHeight))
        #Button
        self.menu_button = Tile(displayWidth/2 - 100, displayHeight/2 + 10, 200, 80, color = self.red, text = 'MENU', textColor = self.black)
        self.exit_button = Tile(displayWidth/2 - 100, displayHeight/2 + 110, 200, 80, color = self.red, text = 'EXIT', textColor = self.black)
        #result
        if win:
            self.result = "CONGRADULATIONS YOU WON"
        else:
            self.result = "YOU LOST THE WAR"

    def draw(self, surface, win = None):
        #Show Background
        surface.blit(self.gameOverImage,(0,0))
        #Write Title
        self.write_text(self.displayWidth/2, 50, "GAME OVER", self.red, 60, surface)
        self.write_text(self.displayWidth/2, 150, self.result, self.red, 60, surface)
        #Draw Button
        self.menu_button.draw(surface)
        self.exit_button.draw(surface)

    def update(self, event):
        #handle event on menu button
        outline_menu = False
        outlineColor_menu = None
        #if is hovering on button
        if 'hover' in self.menu_button.handleEvent(event):
            outline_menu = True
            outlineColor_menu = self.black
        #if button is clicked
        if 'down' in self.menu_button.handleEvent(event):
            outline_menu = True
            outlineColor_menu = self.blue
        #if button is clicked & released
        if 'click' in self.menu_button.handleEvent(event):
            outline_menu = True
            #change to menu state
            self.gsm.setState("MainMenu")
        #if mouse exited a button
        if 'exit' in self.menu_button.handleEvent(event):
            outline_menu = False
        self.menu_button.update(self.menu_button.getColor(),outline_menu,outlineColor_menu)

        #handle event on exit button
        outline_exit = False
        outlineColor_exit = None
        #if is hovering on button
        if 'hover' in self.exit_button.handleEvent(event):
            outline_exit = True
            outlineColor_exit = self.black
        #if button is clicked
        if 'down' in self.exit_button.handleEvent(event):
            outline_exit = True
            outlineColor_exit = self.blue
        #if button is clicked & released
        if 'click' in self.exit_button.handleEvent(event):
            outline_exit = True
            #quit game
            self.gsm.setState("Exit")
        #if mouse exited a button
        if 'exit' in self.exit_button.handleEvent(event):
            outline_exit = False
        self.exit_button.update(self.exit_button.getColor(),outline_exit,outlineColor_exit)
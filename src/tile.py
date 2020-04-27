import pygame
from pieces import *

class Tile():
    def __init__(self, x, y, width, height, color = (255,255,255), transparent = False, outline = False, outlineColor = (0,0,0), text = '', textColor = (0,0,0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.transparent = transparent
        self.outline = outline
        self.outlineColor = outlineColor
        self.text = text
        self.textColor = textColor
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        #record button status
        self.buttonDown = False
        self.buttonPrevDown = False
        self.hovering = False
        self.frameCounter = 0
        #piece is an object of Piece or it's subclasses
        self.piece = None
        #flag is the properties of the tile
        self.flag = None

    #Event handler
    def handleEvent(self,event):
        #if the current event is not a mouse event
        if event.type not in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
            return []
        events = []

        exited = False
        #if mouse entered a button
        if not self.hovering and self.isOver(event.pos):
            self.hovering = True
            events.append('enter')
        #if mouse exited a button
        if self.hovering and not self.isOver(event.pos):
            self.hovering = False
            exited = True

        #if event is happening on a button
        leftMouse = pygame.mouse.get_pressed()[0]
        if self.isOver(event.pos):
            events.append('hover')
            if event.type == pygame.MOUSEBUTTONDOWN and event.type != pygame.MOUSEWHEEL and leftMouse:
                self.buttonDown = True
                self.buttonPrevDown = True
                events.append('down')
            if event.type == pygame.MOUSEBUTTONUP and event.type != pygame.MOUSEWHEEL:
                self.buttonDown = False
                if self.buttonPrevDown:
                    events.append('click')
                    self.frameCounter = self.frameCounter + 1
                    if self.frameCounter == 4:
                        self.frameCounter = 0
                        self.buttonPrevDown = False

        if exited:
            events.append('exit')

        return events

    #check if pos is inside button(including outline)
    def isOver(self, pos):
        if pos[0] >= self.x and pos[0] <= self.x + self.width:
            if pos[1] >= self.y and pos[1] <= self.y + self.height:
                return True
        return False

    def getPos(self):
        return (self.x,self.y)

    def getColor(self):
        return self.color   #color is a tuple of size 3

    def setColor(self,color):
        self.color = color  #color is a tuple of size 3

    def setTransparency(self, transparent):
        self.transparent = transparent  #transparent is a boolean

    #set color of outline
    def setOutline(self,outline,outlineColor = None):
        self.outline = outline
        self.outlineColor = outlineColor

    def getPiece(self):
        return self.piece   #piece is an object of Piece or it's subclasses

    def setPiece(self, piece):
        #set piece to None to remove piece
        self.piece = piece  #piece is an object of Piece or it's subclasses

    def getFlag(self):
        return self.flag

    def setFlag(self, flag):
        self.flag = flag

    #update object properties
    def update(self,color,outline,outlineColor):
        self.setColor(color)
        self.setOutline(outline,outlineColor)

    #Draw the button on the screen
    def draw(self,surface):
        #draw filled rect
        if not self.transparent:
            s = pygame.Surface((self.width,self.height), pygame.SRCALPHA)   # per-pixel alpha
            s.fill(self.getColor())
            surface.blit(s, (self.x, self.y))

            #draw text
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 40)
            text = font.render(self.text, 1, self.textColor)
            #Position the text on the center of the button
            surface.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

        #draw piece
        if self.piece != None:
            if self.piece.getAlliance() == 0:   #if is player piece
                image = pygame.image.load(self.piece.getPath())
            elif self.piece.getAlliance() == 1: #if is AI piece
                #image = pygame.image.load("bin\\Piece Shadow.png")
                image = pygame.image.load(self.piece.getPath()) #debug
            surface.blit(image, (self.x + (self.width / 2 - image.get_width() / 2), self.y + (self.height / 2 - image.get_height() / 2)))

        #draw outline
        if self.outline:
            pygame.draw.rect(surface, self.outlineColor, self.rect, 2)

class SelectionPaneTile(Tile):
    def __init__(self, x, y, width, height, color=(...), transparent=False, outline=False, outlineColor=(...), text='', textColor=(...), nPieces=0):
        self.pieces = []
        self.nPieces = nPieces
        return super().__init__(x, y, width, height, color=color, transparent=transparent, outline=outline, outlineColor=outlineColor, text=text, textColor=textColor)

    def getPiece(self):
        if self.pieces == []:
            return None
        return self.pieces[0]

    def addPiece(self, piece):
        if len(self.pieces) <= self.nPieces and (self.pieces == [] or self.pieces[0].toString() == piece.toString()):
            #only can add when empty or is same piece
            self.pieces.append(piece)

    def removePiece(self):
        if len(self.pieces) > 0:
            self.pieces.pop(0)

    def draw(self, surface):
        super().draw(surface)

        if self.pieces:
            image = pygame.image.load(self.pieces[0].getPath())
            surface.blit(image, (self.x + (self.width / 2 - image.get_width() / 2), self.y + (self.height / 2 - image.get_height() / 2)))

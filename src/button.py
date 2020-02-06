import pygame
from pieces import *

class Button():
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
        #piece is an object of Piece or it's subclasses
        self.piece = None
        #flag is the name of piece the object originally contain (only used in selection pane)
        self.flag = None

    def handleEvent(self,event):
        if event.type not in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
            #if the current event is not a mouse event
            return []
        events = []

        exited = False
        if not self.hovering and self.isOver(event.pos):
            #if mouse entered a button
            self.hovering = True
            events.append('enter')
        if self.hovering and not self.isOver(event.pos):
            #if mouse exited a button
            self.hovering = False
            exited = True

        if self.isOver(event.pos):
            #if event is happening on a button
            events.append('hover')
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.buttonDown = True
                self.buttonPrevDown = True
                events.append('down')
            if event.type == pygame.MOUSEBUTTONUP:
                self.buttonDown = False
                if self.buttonPrevDown:
                    events.append('click')

        if exited:
            events.append('exit')

        return events
    
    def isOver(self, pos):
        #check if pos is inside button(including outline)
        if pos[0] >= self.x and pos[0] <= self.x + self.width:
            if pos[1] >= self.y and pos[1] <= self.y + self.height:
                return True     
        return False

    def getPos(self):
        #get button position
        return (self.x,self.y)

    def getColor(self):
        #get button color
        return self.color

    def setColor(self,color):
        #set color of button
        self.color = color

    def setTransparency(self, transparent):
        #transparent is a boolean
        self.transparent = transparent

    def setOutline(self,outline,outlineColor):
        #set color of outline
        self.outline = outline
        self.outlineColor = outlineColor

    def getPiece(self):
        return self.piece

    def setPiece(self, piece):
        #piece is an object of Piece or it's subclasses
        #set piece to None to remove piece
        self.piece = piece

    def getFlag(self):
        return self.flag

    def setFlag(self, flag):
        self.flag = flag

    def update(self,color,outline,outlineColor):
        self.setColor(color)
        self.setOutline(outline,outlineColor)
        
    def draw(self,surface):
        #Draw the button on the screen
        if not self.transparent:
            #draw filled rect
            s = pygame.Surface((self.width,self.height), pygame.SRCALPHA)   # per-pixel alpha
            s.fill(self.getColor())
            surface.blit(s, (self.x, self.y))
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 12)
            text = font.render(self.text, 1, self.textColor)
            #Position the text on the center of the button
            surface.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

        if self.piece != None:
            image = pygame.image.load(self.piece.getPath())
            surface.blit(image, (self.x + (self.width / 2 - image.get_width() / 2), self.y + (self.height / 2 - image.get_height() / 2)))

        if self.outline:
            pygame.draw.rect(surface, self.outlineColor, self.rect, 2)   #draw outline
           

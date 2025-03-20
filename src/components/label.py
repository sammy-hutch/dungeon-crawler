import pygame
from data.config import FONT_FOLDER

fonts = {}

anti_alias = True

class Label:
    def __init__(self, font, text, size=32, colour=(255, 255, 255)):
        from core.engine import engine
        global labels
        self.colour = colour
        if font in fonts:
            self.font = fonts[font]
        else:
            self.font = pygame.font.Font(FONT_FOLDER + "/" + font, size)
    
        self.set_text(text)
        engine.ui_drawables.append(self)
    
    def set_text(self, text):
        self.text = text
        self.surface = self.font.render(self.text, anti_alias, self.colour)
    
    def draw(self, screen):
        screen.blit(self.surface, (self.entity.x, self.entity.y))
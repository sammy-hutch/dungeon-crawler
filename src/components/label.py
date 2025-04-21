import pygame
from data.config import FONT_FOLDER

fonts = {}

anti_alias = True

class Label:
    def __init__(self, font, text, size=32, colour=(255, 255, 255)):
        from core.engine import engine
        self.colour = colour
        if font in fonts:
            self.font = fonts[font]
        else:
            self.font = pygame.font.Font(FONT_FOLDER + "/" + font, size)
    
        self.set_text(text)
        engine.ui_drawables.append(self)
    
    def breakdown(self):
        from core.engine import engine
        engine.ui_drawables.remove(self)
    
    def get_bounds(self):
        return pygame.Rect(0, 0, self.surface.get_width(), self.surface.get_height())
    
    def set_text(self, text):
        self.text = text
        self.surface = self.font.render(self.text, anti_alias, self.colour)
        self.shadow_surface = self.font.render(self.text, anti_alias, (0,0,0))
    
    def draw(self, screen):
        screen.blit(self.shadow_surface, (self.entity.x+1, self.entity.y+1))
        screen.blit(self.surface, (self.entity.x, self.entity.y))
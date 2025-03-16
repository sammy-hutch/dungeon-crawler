import os
from dotenv import load_dotenv
import pygame

load_dotenv()

fonts = {}
labels = []

anti_alias = True
font_folder = os.getenv("FONT_FOLDER")

class Label:
    def __init__(self, font, text, size=32, colour=(255, 255, 255)):
        global labels
        self.colour = colour
        if font in fonts:
            self.font = fonts[font]
        else:
            self.font = pygame.font.Font(font_folder + "/" + font, size)
    
        self.set_text(text)
        labels.append(self)
    
    def set_text(self, text):
        self.text = text
        self.surface = self.font.render(self.text, anti_alias, self.colour)
    
    def draw(self, screen):
        screen.blit(self.surface, (self.entity.x, self.entity.y))
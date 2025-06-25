import pygame

from core.camera import camera
from data.config import EFFECT_IMAGE_FOLDER, FONT_FOLDER

effects = []

effect_image_folder = EFFECT_IMAGE_FOLDER
font_folder = FONT_FOLDER

hit_x_speed = 0
hit_y_speed = -1
hit_life = 60
hit_size = 30
hit_font = None
hit_font_file = FONT_FOLDER + "/" + "RedRose-Regular.ttf"

def create_hit_text(x, y, text, color=(255, 255, 255)):
    global hit_font
    if hit_font is None:
        hit_font = pygame.font.Font(hit_font_file, hit_size)
    image = hit_font.render(text, True, color)
    Effect(x, y, hit_x_speed, hit_y_speed, hit_life, image)

class Effect:
    def __init__(self, x, y, x_speed, y_speed, life, image):
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.life = life
        self.image = image # pygame.image.load(effect_image_folder + "/" + image) # TODO: other effects will be broken, review them
        global effects
        effects.append(self)
    
    def draw(self, screen):
        self.life -= 1
        self.x += self.x_speed
        self.y += self.y_speed
        if self.life <= 0:
            global effects
            effects.remove(self)
        screen.blit(self.image, (self.x - camera.x, self.y - camera.y))
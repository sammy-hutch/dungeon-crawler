import pygame

from core.camera import camera
from data.config import EFFECT_IMAGE_FOLDER

effects = []

effect_image_folder = EFFECT_IMAGE_FOLDER

class Effect:
    def __init__(self, x, y, x_speed, y_speed, life, image):
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.life = life
        self.image = pygame.image.load(effect_image_folder + "/" + image)
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
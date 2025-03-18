import os
from dotenv import load_dotenv
import pygame

from core.camera import camera
from core.engine import engine

load_dotenv()

loaded = {}

image_folder = os.getenv("SPRITE_IMAGE_FOLDER")

class Sprite:
    def __init__(self, image):
        if image in loaded:
            self.image = loaded[image]
        else:
            self.image = pygame.image.load(image_folder + "/" + image)
            loaded[image] = self.image
        engine.drawables.append(self)
    
    def delete(self):
        engine.drawables.remove(self)
    
    def draw(self, screen):
        screen.blit(self.image, (self.entity.x - camera.x, self.entity.y - camera.y))

